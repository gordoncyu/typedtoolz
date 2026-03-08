#!/usr/bin/env python3
"""
gen_custom_curried_stubs.py
---------------------------
Generate custom curried type stubs from a YAML specification.

Usage:
    python scripts/gen_custom_curried_stubs.py spec.yaml > output.pyi
"""
from __future__ import annotations

import ast
import importlib.util
import inspect
import sys
import typing
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# TypeVar detection
# ---------------------------------------------------------------------------

def _contains_typevar(tp: object) -> bool:
    """Recursively check if a type annotation contains TypeVar/TypeVarTuple/ParamSpec."""
    if isinstance(tp, typing.TypeVar):
        return True
    for mod in (typing, *([] if not _has_typing_extensions else [_typing_extensions])):
        for attr in ("TypeVarTuple", "ParamSpec"):
            cls = getattr(mod, attr, None)
            if cls is not None and isinstance(tp, cls):
                return True
    return any(_contains_typevar(a) for a in typing.get_args(tp))


try:
    import typing_extensions as _typing_extensions
    _has_typing_extensions = True
except ImportError:
    _has_typing_extensions = False


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class ArgSlot:
    """One parameter of the original function."""
    name: str
    annotation_str: str       # source-level annotation string
    has_typevars: bool         # annotation tree contains TypeVar/TypeVarTuple/ParamSpec
    is_pos_only: bool          # positional-only in the ORIGINAL function
    is_kw_only: bool           # keyword-only in the ORIGINAL function
    has_default: bool          # has a default value
    index: int                 # position in the full arg list (0-based)


@dataclass
class FuncInfo:
    """Introspected information about the source function."""
    name: str
    args: list[ArgSlot]
    return_annotation_str: str
    return_has_typevars: bool


@dataclass
class CurrySpec:
    """Everything needed to generate curried stubs."""
    func: FuncInfo
    preamble: str
    n: int                        # positional-only required (for currying)
    m: int                        # positional-only optional (for currying)
    track_keywords: list[str]     # keyword args that create combinatorial variants
    provided_names: list[str]     # display names for tracked keywords (len == len(track_keywords))
    output_name: str | None       # override function name in generated output


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def powerset(items: list[int]) -> list[tuple[int, ...]]:
    result: list[tuple[int, ...]] = []
    for r in range(len(items) + 1):
        result.extend(combinations(items, r))
    return result


# Slot identity: ("arg", index) or ("return", -1)
SlotId = tuple[str, int]


def _slot_id(slot: ArgSlot | None) -> SlotId:
    if slot is None:
        return ("return", -1)
    return ("arg", slot.index)


# ---------------------------------------------------------------------------
# Introspection / YAML loading
# ---------------------------------------------------------------------------

def _find_ast_func(tree: ast.Module, name_parts: list[str]) -> ast.FunctionDef:
    """Find a function AST node by dotted name (e.g. ['MyClass', 'method'])."""
    node: ast.AST = tree
    for part in name_parts[:-1]:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.ClassDef) and child.name == part:
                node = child
                break
        else:
            raise ValueError(f"Could not find class '{part}' in AST")

    func_name = name_parts[-1]
    candidates: list[ast.FunctionDef] = []
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child.name == func_name:
            candidates.append(child)  # type: ignore[arg-type]

    if not candidates:
        raise ValueError(f"Could not find function '{func_name}'")

    # Prefer the non-@overload definition
    for c in candidates:
        is_overload = any(
            (isinstance(d, ast.Name) and d.id == "overload")
            or (isinstance(d, ast.Attribute) and d.attr == "overload")
            for d in c.decorator_list
        )
        if not is_overload:
            return c
    return candidates[0]


def _extract_preamble(source: str, tree: ast.Module, name_parts: list[str]) -> str:
    top_name = name_parts[0]
    lines = source.split("\n")
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name == top_name:
            start = node.decorator_list[0].lineno if node.decorator_list else node.lineno
            preamble_lines = lines[: start - 1]
            while preamble_lines and not preamble_lines[-1].strip():
                preamble_lines.pop()
            return "\n".join(preamble_lines)
    raise ValueError(f"Could not find top-level name '{top_name}'")


def _ann_str(node: ast.expr | None) -> str:
    return ast.unparse(node) if node is not None else "Any"


def _import_from_file(file_path: Path) -> object:
    spec = importlib.util.spec_from_file_location("_decl_module", str(file_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot create import spec for {file_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _resolve_obj(module: object, name_parts: list[str]) -> object:
    obj = module
    for part in name_parts:
        obj = getattr(obj, part)
    return obj


def load_spec(yaml_path: str) -> CurrySpec:
    yaml_file = Path(yaml_path)
    with open(yaml_file) as f:
        raw = yaml.safe_load(f)

    declaration_file: str = raw["declaration_file"]
    declaration_name: str = raw["declaration_name"]
    n: int = raw["n"]
    m: int = raw["m"]
    track_keywords: list[str] = raw.get("track_keywords", [])
    provided_names: list[str] = raw.get("provided_names", [])
    output_name: str | None = raw.get("output_name", None)

    decl_path = (yaml_file.parent / declaration_file).resolve()
    source = decl_path.read_text()
    tree = ast.parse(source)
    name_parts = declaration_name.split(".")

    preamble = _extract_preamble(source, tree, name_parts)
    func_node = _find_ast_func(tree, name_parts)

    # Runtime import for TypeVar detection
    module = _import_from_file(decl_path)
    runtime_obj = _resolve_obj(module, name_parts)

    try:
        hints = typing.get_type_hints(runtime_obj)
    except Exception:
        hints = {}

    # Use inspect.signature for param kinds / defaults
    sig = inspect.signature(runtime_obj)  # type: ignore[arg-type]

    # Build AST annotation map (param name -> source string)
    ast_args = func_node.args
    ast_ann: dict[str, str] = {}
    for arg_node in (*ast_args.posonlyargs, *ast_args.args, *ast_args.kwonlyargs):
        ast_ann[arg_node.arg] = _ann_str(arg_node.annotation)

    args: list[ArgSlot] = []
    idx = 0
    for param in sig.parameters.values():
        if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
            continue
        if param.name == "self":
            continue
        args.append(ArgSlot(
            name=param.name,
            annotation_str=ast_ann.get(param.name, "Any"),
            has_typevars=_contains_typevar(hints.get(param.name)) if param.name in hints else False,
            is_pos_only=param.kind == param.POSITIONAL_ONLY,
            is_kw_only=param.kind == param.KEYWORD_ONLY,
            has_default=param.default is not param.empty,
            index=idx,
        ))
        idx += 1

    ret_str = _ann_str(func_node.returns)
    ret_has_tv = _contains_typevar(hints.get("return")) if "return" in hints else False

    resolved_name = output_name if output_name else name_parts[-1]

    return CurrySpec(
        func=FuncInfo(name=resolved_name, args=args,
                      return_annotation_str=ret_str, return_has_typevars=ret_has_tv),
        preamble=preamble,
        n=n, m=m,
        track_keywords=track_keywords,
        provided_names=provided_names,
        output_name=resolved_name,
    )


# ---------------------------------------------------------------------------
# Code generation
# ---------------------------------------------------------------------------

@dataclass
class _ProtoInfo:
    """Computed info about a Protocol variant."""
    class_name: str
    # Ordered typevar-containing slots (ArgSlot or None=return)
    tv_slots: list[ArgSlot | None]
    # Matching type param names (_T0, _T1, ..., _R)
    type_params: list[str]
    # All args present (including concrete-typed ones)
    all_args: list[ArgSlot]


def generate(spec: CurrySpec) -> str:
    func = spec.func
    n, m = spec.n, spec.m
    track_kw_names = set(spec.track_keywords)
    provided_names = spec.provided_names
    fname = spec.output_name or func.name

    # Classify args
    required = func.args[:n]
    opt_pos = func.args[n : n + m]
    rest = func.args[n + m :]
    tracked = [a for a in rest if a.name in track_kw_names]
    untracked = [a for a in rest if a.name not in track_kw_names]

    # Map tracked arg name -> its position in the tracked list
    tracked_name_to_idx = {a.name: i for i, a in enumerate(tracked)}
    # Map tracked list index -> provided_name
    # provided_names[i] corresponds to spec.track_keywords[i] which corresponds to tracked[i]
    # (assuming tracked order matches spec.track_keywords order)
    # Let's reorder tracked to match spec.track_keywords order
    tracked_by_name = {a.name: a for a in tracked}
    tracked = [tracked_by_name[name] for name in spec.track_keywords]
    tracked_name_to_idx = {a.name: i for i, a in enumerate(tracked)}

    o = len(tracked)
    tk_positions = list(range(o))

    # ------------------------------------------------------------------
    # Helpers for Protocol slot computation
    # ------------------------------------------------------------------

    def _tv_slots(args_present: list[ArgSlot]) -> list[ArgSlot | None]:
        """Typevar-containing slots: args with typevars + return."""
        slots: list[ArgSlot | None] = [a for a in args_present if a.has_typevars]
        if func.return_has_typevars:
            slots.append(None)
        return slots

    def _type_params(tv_slots: list[ArgSlot | None]) -> list[str]:
        params: list[str] = []
        ti = 0
        for slot in tv_slots:
            if slot is None:
                params.append("_R")
            else:
                params.append(f"_T{ti}")
                ti += 1
        return params

    def _all_args_for(k: int, S: frozenset[int]) -> list[ArgSlot]:
        """All args present in a Protocol(k, S) — required + opt_pos + untracked + remaining tracked."""
        args: list[ArgSlot] = []
        args.extend(required[n - k:])
        args.extend(opt_pos)
        args.extend(untracked)
        for i, ta in enumerate(tracked):
            if i not in S:
                args.extend([ta])
        return args

    def _proto_info(k: int, S: frozenset[int]) -> _ProtoInfo:
        all_args = _all_args_for(k, S)
        tv_slots = _tv_slots(all_args)
        tp = _type_params(tv_slots)
        return _ProtoInfo(
            class_name=_cls_name(S, k),
            tv_slots=tv_slots,
            type_params=tp,
            all_args=all_args,
        )

    def _to_pascal(name: str) -> str:
        # Handle snake_case and already-PascalCase
        return "".join(part.capitalize() for part in name.split("_")) if "_" in name else name[0].upper() + name[1:]

    fname_pascal = _to_pascal(fname)

    def _cls_name(S: frozenset[int], k: int) -> str:
        prefix = fname_pascal
        if S:
            prefix += "".join(provided_names[i] for i in sorted(S))
        return f"{prefix}Curried{k}"

    def _type_args_from_proto(src: _ProtoInfo, tgt: _ProtoInfo) -> list[str]:
        """Map src type params to tgt type params by slot identity."""
        src_map = {_slot_id(s): p for s, p in zip(src.tv_slots, src.type_params)}
        return [src_map[_slot_id(s)] for s in tgt.tv_slots]

    def _type_args_from_entry(tgt: _ProtoInfo) -> list[str]:
        """Map original annotation strings to tgt type params."""
        result: list[str] = []
        for slot in tgt.tv_slots:
            if slot is None:
                result.append(func.return_annotation_str)
            else:
                result.append(slot.annotation_str)
        return result

    def _ref_str(cls_name: str, type_args: list[str], quoted: bool) -> str:
        if type_args:
            s = f"{cls_name}[{', '.join(type_args)}]"
        else:
            s = cls_name
        return f"'{s}'" if quoted else s

    # ------------------------------------------------------------------
    # Forward-reference quoting logic
    # ------------------------------------------------------------------
    # Generation order: k=1..n, within each k: largest S first.
    all_subsets = powerset(tk_positions)
    all_subsets.sort(key=lambda s: -len(s))

    def _needs_quotes(cur_k: int, cur_S: frozenset[int],
                      tgt_k: int, tgt_S: frozenset[int]) -> bool:
        if tgt_k > cur_k:
            return True
        if tgt_k == cur_k:
            if tgt_S == cur_S:
                return True  # self
            if len(tgt_S) < len(cur_S):
                return True  # defined after us at same level
        return False

    # ------------------------------------------------------------------
    # Build a type-map for an overload inside a Protocol
    # ------------------------------------------------------------------

    def _proto_type_map(info: _ProtoInfo) -> dict[int, str]:
        """arg.index -> type string to use inside a Protocol overload."""
        m: dict[int, str] = {}
        for slot, tp in zip(info.tv_slots, info.type_params):
            if slot is not None:
                m[slot.index] = tp
        return m

    # ------------------------------------------------------------------
    # Render a parameter list
    # ------------------------------------------------------------------

    def _render_params(
        positional: list[ArgSlot],
        kw_provided: list[ArgSlot],   # tracked kwargs being provided
        include_untracked: bool,
        force_kw_tracked: bool,       # force tracked kwargs to be kw-only (Protocol-returning)
        type_map: dict[int, str],     # arg.index -> type string (for Protocol context)
        use_original: bool,           # True for entry-point overloads
    ) -> str:
        parts: list[str] = []

        def _type_for(arg: ArgSlot) -> str:
            if use_original:
                return arg.annotation_str
            return type_map.get(arg.index, arg.annotation_str)

        # --- Positional args ---
        has_pos_only = False
        last_pos_only_idx = -1
        for arg in positional:
            if arg.is_pos_only:
                has_pos_only = True
                last_pos_only_idx = len(parts)
            parts.append(f"{arg.name}: {_type_for(arg)}")

        if has_pos_only:
            parts.insert(last_pos_only_idx + 1, "/")

        # --- Keyword args (tracked provided + untracked) ---
        kw_args_to_add: list[tuple[ArgSlot, bool]] = []  # (arg, with_default)

        for arg in kw_provided:
            kw_args_to_add.append((arg, True))

        if include_untracked:
            for arg in untracked:
                kw_args_to_add.append((arg, True))

        if kw_args_to_add:
            # Determine if we need a * separator
            # Need * if: any arg is forced keyword-only, or is originally keyword-only,
            # AND there isn't already a * context from positional args.
            need_star = False
            for arg, _ in kw_args_to_add:
                if force_kw_tracked and arg in tracked:
                    need_star = True
                elif arg.is_kw_only:
                    need_star = True
                elif arg in untracked:
                    # Untracked are always keyword-only in curried context
                    need_star = True

            if need_star:
                parts.append("*")

            for arg, with_default in kw_args_to_add:
                t = _type_for(arg)
                if with_default:
                    parts.append(f"{arg.name}: {t} = ...")
                else:
                    parts.append(f"{arg.name}: {t}")

        return ", ".join(parts)

    # ------------------------------------------------------------------
    # Emit
    # ------------------------------------------------------------------

    lines: list[str] = []
    pr = lines.append

    # Preamble
    pr(spec.preamble)
    pr("")

    # Determine max _T index needed across all Protocols
    max_t = 0
    for k in range(1, n + 1):
        for S_tuple in all_subsets:
            S = frozenset(S_tuple)
            info = _proto_info(k, S)
            count = sum(1 for s in info.tv_slots if s is not None)
            if count > max_t:
                max_t = count
    # Also check entry-point
    entry_info = _proto_info(n, frozenset())
    entry_count = sum(1 for s in entry_info.tv_slots if s is not None)
    if entry_count > max_t:
        max_t = entry_count

    # Emit TypeVar declarations
    pr("from typing import Protocol, TypeVar, overload")
    pr("")
    for i in range(max_t):
        pr(f"_T{i} = TypeVar('_T{i}', contravariant=True)")
    if func.return_has_typevars:
        pr("_R = TypeVar('_R', covariant=True)")
    pr("")

    # ------------------------------------------------------------------
    # Protocol classes
    # ------------------------------------------------------------------

    for k in range(1, n + 1):
        for S_tuple in all_subsets:
            S = frozenset(S_tuple)
            info = _proto_info(k, S)
            tm = _proto_type_map(info)
            ret_type_str = "_R" if func.return_has_typevars else func.return_annotation_str

            remaining_kw_indices = [i for i in tk_positions if i not in S]
            remaining_kw_subsets = powerset(remaining_kw_indices)

            # Class header
            if info.type_params:
                pr(f"class {info.class_name}(Protocol[{', '.join(info.type_params)}]):")
            else:
                pr(f"class {info.class_name}(Protocol):")

            remaining_req = required[n - k:]

            for p in range(k + m, -1, -1):
                for T_tuple in remaining_kw_subsets:
                    T = frozenset(T_tuple)
                    ST = S | T

                    # Positional args for this overload
                    if p <= k:
                        pos = list(remaining_req[:p])
                    else:
                        pos = list(remaining_req) + list(opt_pos[: p - k])

                    tracked_provided = [tracked[i] for i in sorted(T)]

                    if p >= k:
                        # All required met -> R
                        params = _render_params(
                            pos, tracked_provided,
                            include_untracked=True,
                            force_kw_tracked=False,
                            type_map=tm,
                            use_original=False,
                        )
                        pr("    @overload")
                        if params:
                            pr(f"    def __call__(self, {params}) -> {ret_type_str}: ...")
                        else:
                            pr(f"    def __call__(self) -> {ret_type_str}: ...")

                    elif p > 0:
                        # Partial -> Curried(k-p) with subset ST
                        tgt_k = k - p
                        tgt_info = _proto_info(tgt_k, ST)
                        quoted = _needs_quotes(k, S, tgt_k, ST)
                        targs = _type_args_from_proto(info, tgt_info)
                        ref = _ref_str(tgt_info.class_name, targs, quoted)

                        params = _render_params(
                            pos, tracked_provided,
                            include_untracked=True,
                            force_kw_tracked=True,
                            type_map=tm,
                            use_original=False,
                        )
                        pr("    @overload")
                        pr(f"    def __call__(self, {params}) -> {ref}: ...")

                    else:
                        # p == 0
                        if not T:
                            # Self-reference (untracked kwargs subsume the empty case)
                            ref = _ref_str(info.class_name, info.type_params, True)
                            params = _render_params(
                                [], [],
                                include_untracked=True,
                                force_kw_tracked=True,
                                type_map=tm,
                                use_original=False,
                            )
                            pr("    @overload")
                            if params:
                                pr(f"    def __call__(self, {params}) -> {ref}: ...")
                            else:
                                pr(f"    def __call__(self) -> {ref}: ...")
                        else:
                            tgt_info = _proto_info(k, ST)
                            quoted = _needs_quotes(k, S, k, ST)
                            targs = _type_args_from_proto(info, tgt_info)
                            ref = _ref_str(tgt_info.class_name, targs, quoted)

                            params = _render_params(
                                [], tracked_provided,
                                include_untracked=False,
                                force_kw_tracked=True,
                                type_map=tm,
                                use_original=False,
                            )
                            pr("    @overload")
                            pr(f"    def __call__(self, {params}) -> {ref}: ...")

            pr("")

    # ------------------------------------------------------------------
    # Entry-point overloads
    # ------------------------------------------------------------------

    remaining_kw_subsets = powerset(tk_positions)

    for p in range(n + m, -1, -1):
        for T_tuple in remaining_kw_subsets:
            T = frozenset(T_tuple)

            if p <= n:
                pos = list(required[:p])
            else:
                pos = list(required) + list(opt_pos[: p - n])

            tracked_provided = [tracked[i] for i in sorted(T)]

            if p >= n:
                # All required met -> R
                params = _render_params(
                    pos, tracked_provided,
                    include_untracked=True,
                    force_kw_tracked=False,
                    type_map={},  # not used when use_original=True
                    use_original=True,
                )
                pr("@overload")
                if params:
                    pr(f"def {fname}({params}) -> {func.return_annotation_str}: ...")
                else:
                    pr(f"def {fname}() -> {func.return_annotation_str}: ...")

            elif p > 0:
                tgt_k = n - p
                tgt_info = _proto_info(tgt_k, T)
                targs = _type_args_from_entry(tgt_info)
                ref = _ref_str(tgt_info.class_name, targs, False)

                params = _render_params(
                    pos, tracked_provided,
                    include_untracked=True,
                    force_kw_tracked=True,
                    type_map={},
                    use_original=True,
                )
                pr("@overload")
                pr(f"def {fname}({params}) -> {ref}: ...")

            else:
                if not T:
                    tgt_info = _proto_info(n, frozenset())
                    targs = _type_args_from_entry(tgt_info)
                    ref = _ref_str(tgt_info.class_name, targs, False)
                    params = _render_params(
                        [], [],
                        include_untracked=True,
                        force_kw_tracked=True,
                        type_map={},
                        use_original=True,
                    )
                    pr("@overload")
                    if params:
                        pr(f"def {fname}({params}) -> {ref}: ...")
                    else:
                        pr(f"def {fname}() -> {ref}: ...")
                else:
                    tgt_info = _proto_info(n, T)
                    targs = _type_args_from_entry(tgt_info)
                    ref = _ref_str(tgt_info.class_name, targs, False)

                    params = _render_params(
                        [], tracked_provided,
                        include_untracked=False,
                        force_kw_tracked=True,
                        type_map={},
                        use_original=True,
                    )
                    pr("@overload")
                    pr(f"def {fname}({params}) -> {ref}: ...")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Template creation
# ---------------------------------------------------------------------------

_TEMPLATE_PY = """\
from typing import TypeVar

A = TypeVar('A')
B = TypeVar('B')

def example(a: A, b: B) -> B:
    ...
"""

_TEMPLATE_YAML = """\
declaration_file: declaration.py
declaration_name: example
# output_name: example  # optional override for generated function/class name
n: 2   # positional-only required args (for currying)
m: 0   # positional-only optional args (for currying)
# track_keywords:   # keyword args that create combinatorial Protocol variants
#   - some_kwarg
# provided_names:   # display names for tracked keywords (one per track_keywords entry)
#   - SomeKwarg
"""


def create_template(dir_path: str) -> None:
    d = Path(dir_path)
    d.mkdir(parents=True, exist_ok=True)
    (d / "declaration.py").write_text(_TEMPLATE_PY)
    (d / "spec.yaml").write_text(_TEMPLATE_YAML)
    print(f"Created template in {d}/")
    print(f"  {d}/declaration.py")
    print(f"  {d}/spec.yaml")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if "--create-template" in sys.argv:
        idx = sys.argv.index("--create-template")
        if idx + 1 >= len(sys.argv):
            print("Usage: python gen_custom_curried_stubs.py --create-template <dir>", file=sys.stderr)
            sys.exit(1)
        create_template(sys.argv[idx + 1])
        return

    if len(sys.argv) < 2:
        print("Usage: python gen_custom_curried_stubs.py <spec.yaml>", file=sys.stderr)
        print("       python gen_custom_curried_stubs.py --create-template <dir>", file=sys.stderr)
        sys.exit(1)
    spec = load_spec(sys.argv[1])
    print(generate(spec))


if __name__ == "__main__":
    main()
