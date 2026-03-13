#!/usr/bin/env python3
"""
gen_custom_curried_stubs.py
----------------------------------
Generate custom curried type stubs from a YAML specification.
Blocks are generated top-down (entry → k=n → … → k=1), then emitted in
Kahn's topological order so every definition precedes its uses, eliminating
forward-reference quotes except for unavoidable self-references.

Usage:
    python scripts/gen_custom_curried_stubs.py spec.yaml > output.pyi
    python scripts/gen_custom_curried_stubs.py --create-template <dir>
"""
from __future__ import annotations

import ast
import importlib.util
import inspect
import sys
import typing
from collections import deque
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# TypeVar enumeration (excludes TypeVarTuple / ParamSpec)
# ---------------------------------------------------------------------------

try:
    import typing_extensions as _typing_extensions
    _has_typing_extensions = True
except ImportError:
    _has_typing_extensions = False


def _is_plain_typevar(tp: object) -> bool:
    """True only for TypeVar, not TypeVarTuple or ParamSpec."""
    if not isinstance(tp, typing.TypeVar):
        return False
    for mod in [typing] + ([_typing_extensions] if _has_typing_extensions else []):
        for attr in ("TypeVarTuple", "ParamSpec"):
            cls = getattr(mod, attr, None)
            if cls is not None and isinstance(tp, cls):
                return False
    return True


def _enumerate_typevars(tp: object, seen: set[str] | None = None) -> list[str]:
    """Return ordered unique TypeVar names (plain only) found in a runtime annotation."""
    if seen is None:
        seen = set()
    result: list[str] = []
    if _is_plain_typevar(tp):
        name = tp.__name__  # type: ignore[union-attr]
        if name not in seen:
            seen.add(name)
            result.append(name)
        return result
    for arg in typing.get_args(tp):
        # Callable[[A, B], R] gives get_args → ([A, B], R); the param list is a plain list
        if isinstance(arg, (list, tuple)):
            for item in arg:
                result.extend(_enumerate_typevars(item, seen))
        else:
            result.extend(_enumerate_typevars(arg, seen))
    return result


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class ArgSlot:
    """One parameter of the original function."""
    name: str
    annotation_str: str    # source-level annotation string
    typevars: list[str]    # ordered TypeVar names appearing in annotation (plain only)
    is_pos_only: bool      # positional-only in the original function
    is_kw_only: bool       # keyword-only in the original function
    has_default: bool      # has a default value
    index: int             # position in full arg list (0-based)


@dataclass
class FuncInfo:
    """Introspected information about the source function."""
    name: str
    args: list[ArgSlot]
    return_annotation_str: str
    return_typevars: list[str]


@dataclass
class TypeImplication:
    """One rule in the type_implications list."""
    when_keywords: frozenset[int]      # indices into track_keywords; all must be in S
    when_positionals: frozenset[int]   # indices into required positional args; all must be provided
    not_keywords: frozenset[int]       # indices into track_keywords; none may be in S
    not_positionals: frozenset[int]    # indices into opt_pos args; none may be provided
    lc_keywords: frozenset[int]        # tracked keyword indices; all must be in the final call's T
    lc_req_pos: frozenset[int]         # required positional indices; all must be in the final call
    lc_opt_pos: frozenset[int]         # optional positional indices; all must be in the final call
    return_type: str | None            # None = no override for return type
    args: dict[str, str]               # arg name → annotation override (requires last_call)


@dataclass
class CurrySpec:
    """Everything needed to generate curried stubs."""
    func: FuncInfo
    preamble: str
    n: int                          # positional-only required (for currying)
    m: int                          # positional-only optional (for currying)
    track_keywords: list[str]       # keyword args that create combinatorial variants
    provided_names: list[str]       # display names for tracked keywords
    output_name: str | None         # override function name in generated output
    implications: list[TypeImplication]  # type implication rules, later = higher priority


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def powerset(items: list[int]) -> list[tuple[int, ...]]:
    result: list[tuple[int, ...]] = []
    for r in range(len(items) + 1):
        result.extend(combinations(items, r))
    return result


# ---------------------------------------------------------------------------
# Introspection / YAML loading
# ---------------------------------------------------------------------------

def _find_ast_func(tree: ast.Module, name_parts: list[str]) -> ast.FunctionDef:
    node: ast.AST = tree
    for part in name_parts[:-1]:
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.ClassDef) and child.name == part:
                node = child
                break
        else:
            raise ValueError(f"Could not find class '{part}' in AST")

    candidates: list[ast.FunctionDef] = []
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child.name == name_parts[-1]:
            candidates.append(child)  # type: ignore[arg-type]

    if not candidates:
        raise ValueError(f"Could not find function '{name_parts[-1]}'")

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

    track_set = set(track_keywords)

    decl_path = (yaml_file.parent / declaration_file).resolve()
    source = decl_path.read_text()
    tree = ast.parse(source)
    name_parts = declaration_name.split(".")

    preamble = _extract_preamble(source, tree, name_parts)
    func_node = _find_ast_func(tree, name_parts)

    module = _import_from_file(decl_path)
    runtime_obj = _resolve_obj(module, name_parts)

    try:
        hints = typing.get_type_hints(runtime_obj)
    except Exception:
        hints = {}

    sig = inspect.signature(runtime_obj)  # type: ignore[arg-type]

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
        tvars = _enumerate_typevars(hints.get(param.name))
        args.append(ArgSlot(
            name=param.name,
            annotation_str=ast_ann.get(param.name, "Any"),
            typevars=tvars,
            is_pos_only=param.kind == param.POSITIONAL_ONLY,
            is_kw_only=param.kind == param.KEYWORD_ONLY,
            has_default=param.default is not param.empty,
            index=idx,
        ))
        idx += 1

    ret_typevars = _enumerate_typevars(hints.get("return"))
    ret_str = _ann_str(func_node.returns)

    required_names = [a.name for a in args[:n]]
    required_name_set = set(required_names)
    opt_pos_names = [a.name for a in args[n : n + m]]
    opt_pos_name_set = set(opt_pos_names)

    def _parse_when_names(names: list[str], field: str) -> tuple[frozenset[int], frozenset[int]]:
        kw_indices: list[int] = []
        pos_indices: list[int] = []
        for name in names:
            if name == "/all_req_pos":
                pos_indices.extend(range(n))
            elif name == "/all_key_opt":
                kw_indices.extend(range(len(track_keywords)))
            elif name in track_set:
                kw_indices.append(track_keywords.index(name))
            elif name in required_name_set:
                pos_indices.append(required_names.index(name))
            else:
                raise ValueError(
                    f"type_implications '{field}' contains '{name}' which is not in "
                    f"track_keywords, required positional args, /all_req_pos, or /all_key_opt"
                )
        return frozenset(kw_indices), frozenset(pos_indices)

    def _parse_not_names(names: list[str]) -> tuple[frozenset[int], frozenset[int]]:
        kw_indices: list[int] = []
        pos_indices: list[int] = []
        for name in names:
            if name == "/all_opt_pos":
                pos_indices.extend(range(m))
            elif name == "/all_key_opt":
                kw_indices.extend(range(len(track_keywords)))
            elif name in track_set:
                kw_indices.append(track_keywords.index(name))
            elif name in opt_pos_name_set:
                pos_indices.append(opt_pos_names.index(name))
            else:
                raise ValueError(
                    f"type_implications 'not' contains '{name}' which is not in "
                    f"track_keywords, optional positional args, /all_opt_pos, or /all_key_opt"
                )
        return frozenset(kw_indices), frozenset(pos_indices)

    def _parse_last_call_names(names: list[str]) -> tuple[frozenset[int], frozenset[int], frozenset[int]]:
        kw_indices: list[int] = []
        req_pos_indices: list[int] = []
        opt_pos_indices: list[int] = []
        for name in names:
            if name == "/all_req_pos":
                req_pos_indices.extend(range(n))
            elif name == "/all_opt_pos":
                opt_pos_indices.extend(range(m))
            elif name == "/all_key_opt":
                kw_indices.extend(range(len(track_keywords)))
            elif name in track_set:
                kw_indices.append(track_keywords.index(name))
            elif name in required_name_set:
                req_pos_indices.append(required_names.index(name))
            elif name in opt_pos_name_set:
                opt_pos_indices.append(opt_pos_names.index(name))
            else:
                raise ValueError(
                    f"type_implications 'last_call' contains '{name}' which is not in "
                    f"track_keywords, required positional args, optional positional args, "
                    f"/all_req_pos, /all_opt_pos, or /all_key_opt"
                )
        return frozenset(kw_indices), frozenset(req_pos_indices), frozenset(opt_pos_indices)

    raw_implications: list[dict] = raw.get("type_implications", [])
    implications: list[TypeImplication] = []
    for rule in raw_implications:
        wk, wp = _parse_when_names(rule.get("when", []), "when")
        nk, np_ = _parse_not_names(rule.get("not", []))
        lck, lcrp, lcop = _parse_last_call_names(rule.get("last_call", []))
        rule_args: dict[str, str] = rule.get("args", {})
        has_last_call = bool(lck or lcrp or lcop)
        if rule_args and not has_last_call:
            raise ValueError(
                "type_implications 'args' requires 'last_call' to be non-empty"
            )
        all_arg_names = {a.name for a in args}
        for arg_name in rule_args:
            if arg_name not in all_arg_names:
                raise ValueError(
                    f"type_implications 'args' contains '{arg_name}' which is not "
                    f"a parameter of the function"
                )
        implications.append(TypeImplication(
            when_keywords=wk,
            when_positionals=wp,
            not_keywords=nk,
            not_positionals=np_,
            lc_keywords=lck,
            lc_req_pos=lcrp,
            lc_opt_pos=lcop,
            return_type=rule.get("return_type", None),
            args=rule_args,
        ))

    resolved_name = output_name if output_name else name_parts[-1]

    return CurrySpec(
        func=FuncInfo(
            name=resolved_name,
            args=args,
            return_annotation_str=ret_str,
            return_typevars=ret_typevars,
        ),
        preamble=preamble,
        n=n, m=m,
        track_keywords=track_keywords,
        provided_names=provided_names,
        output_name=resolved_name,
        implications=implications,
    )


# ---------------------------------------------------------------------------
# Code generation
# ---------------------------------------------------------------------------

# Block identifiers
# Protocol block: ('proto', k: int, S: frozenset[int])
# Entry block:    ('entry',)
BlockId = tuple

ENTRY_ID: BlockId = ('entry',)


def proto_id(k: int, S: frozenset[int]) -> BlockId:
    return ('proto', k, S)


def generate(spec: CurrySpec) -> str:
    func = spec.func
    n, m = spec.n, spec.m
    provided_names = spec.provided_names
    fname = spec.output_name or func.name

    # Classify args
    required = func.args[:n]
    opt_pos = func.args[n : n + m]
    rest = func.args[n + m :]
    tracked_by_name = {a.name: a for a in rest if a.name in set(spec.track_keywords)}
    tracked = [tracked_by_name[name] for name in spec.track_keywords]
    untracked = [a for a in rest if a.name not in set(spec.track_keywords)]

    o = len(tracked)
    tk_positions = list(range(o))
    tracked_ids = {id(a) for a in tracked}
    untracked_ids = {id(a) for a in untracked}

    # ------------------------------------------------------------------
    # Naming
    # ------------------------------------------------------------------

    def _to_pascal(name: str) -> str:
        return "".join(p.capitalize() for p in name.split("_")) if "_" in name else name[0].upper() + name[1:]

    fname_pascal = _to_pascal(fname)

    def _cls_name(S: frozenset[int], k: int) -> str:
        prefix = fname_pascal
        if S:
            prefix += "".join(provided_names[i] for i in sorted(S))
        return f"{prefix}Curried{k}"

    # ------------------------------------------------------------------
    # Protocol type params
    # ------------------------------------------------------------------

    def _proto_type_params(k: int, S: frozenset[int]) -> list[str]:
        consumed = list(required[0 : n - k]) + [tracked[i] for i in sorted(S)]
        seen: set[str] = set()
        result: list[str] = []
        for arg in consumed:
            for tv in arg.typevars:
                if tv not in seen:
                    seen.add(tv)
                    result.append(tv)
        return result

    # ------------------------------------------------------------------
    # Rendering helpers
    # ------------------------------------------------------------------

    def _ref_str(cls_name: str, type_params: list[str], quoted: bool) -> str:
        s = f"{cls_name}[{', '.join(type_params)}]" if type_params else cls_name
        return f"'{s}'" if quoted else s

    def _render_params(
        positional: list[ArgSlot],
        kw_provided: list[ArgSlot],
        include_untracked: bool,
        force_kw_tracked: bool,
        arg_overrides: dict[str, str] | None = None,
    ) -> str:
        parts: list[str] = []
        ovr = arg_overrides or {}

        has_pos_only = False
        last_pos_only_idx = -1
        for arg in positional:
            if arg.is_pos_only:
                has_pos_only = True
                last_pos_only_idx = len(parts)
            ann = ovr.get(arg.name, arg.annotation_str)
            parts.append(f"{arg.name}: {ann}")

        if has_pos_only:
            parts.insert(last_pos_only_idx + 1, "/")

        kw_args: list[ArgSlot] = list(kw_provided)
        if include_untracked:
            kw_args.extend(untracked)

        if kw_args:
            need_star = any(
                (force_kw_tracked and id(a) in tracked_ids)
                or a.is_kw_only
                or (id(a) in untracked_ids)
                for a in kw_args
            )
            if need_star:
                parts.append("*")
            for arg in kw_args:
                ann = ovr.get(arg.name, arg.annotation_str)
                parts.append(f"{arg.name}: {ann} = ...")

        return ", ".join(parts)

    # ------------------------------------------------------------------
    # Return type resolution with implication precedence
    # ------------------------------------------------------------------

    def _rule_dominated(impl: TypeImplication, others: list[TypeImplication]) -> bool:
        return any(
            impl.when_keywords < other.when_keywords and impl.when_positionals <= other.when_positionals
            or impl.when_keywords <= other.when_keywords and impl.when_positionals < other.when_positionals
            for other in others
        )

    def _resolve_implications(
        provided_pos: frozenset[int],
        S: frozenset[int],
        lc_req_pos: frozenset[int],
        lc_opt_pos: frozenset[int],
        lc_kw: frozenset[int],
    ) -> tuple[str, dict[str, str]]:
        matching = [
            (i, impl) for i, impl in enumerate(spec.implications)
            if not (impl.not_keywords & S) and not (impl.not_positionals & provided_pos)
            and impl.when_keywords <= S and impl.when_positionals <= provided_pos
            and impl.lc_keywords <= lc_kw
            and impl.lc_req_pos <= lc_req_pos
            and impl.lc_opt_pos <= lc_opt_pos
        ]
        if not matching:
            return func.return_annotation_str, {}
        matching_impls = [impl for _, impl in matching]
        maximal = [
            (i, impl) for i, impl in matching
            if not _rule_dominated(impl, [other for other in matching_impls if other is not impl])
        ]
        _, winner = max(maximal, key=lambda x: x[0])
        ret = winner.return_type or func.return_annotation_str
        return ret, winner.args

    # ------------------------------------------------------------------
    # Block collection
    #
    # We iterate top-down (entry first, then k=n..1) to reflect logical
    # dependency direction, but collect into named blocks so we can emit
    # them in topological order afterwards.
    # ------------------------------------------------------------------

    all_subsets = powerset(tk_positions)
    all_subsets.sort(key=lambda s: -len(s))  # largest subsets first within each level

    # block_id → (lines, deps)
    blocks: dict[BlockId, tuple[list[str], set[BlockId]]] = {}

    # ── Entry block (top of the conceptual hierarchy) ──────────────────

    elines: list[str] = []
    edeps: set[BlockId] = set()

    for p in range(n + m, -1, -1):
        for T_tuple in powerset(tk_positions):
            T = frozenset(T_tuple)

            pos = list(required[:p]) if p <= n else list(required) + list(opt_pos[:p - n])
            tracked_provided = [tracked[i] for i in sorted(T)]

            if p >= n:
                lc_req = frozenset(range(n))
                lc_opt = frozenset(range(p - n))
                ret, arg_ovr = _resolve_implications(frozenset(range(n)), T, lc_req, lc_opt, T)
                params = _render_params(pos, tracked_provided, include_untracked=True, force_kw_tracked=False, arg_overrides=arg_ovr)
                elines.append("@overload")
                elines.append(f"def {fname}({params}) -> {ret}: ..." if params else f"def {fname}() -> {ret}: ...")

            elif p > 0:
                tgt_k = n - p
                tgt_tp = _proto_type_params(tgt_k, T)
                tgt = proto_id(tgt_k, T)
                edeps.add(tgt)
                ref = _ref_str(_cls_name(T, tgt_k), tgt_tp, False)
                params = _render_params(pos, tracked_provided, include_untracked=True, force_kw_tracked=True)
                elines.append("@overload")
                elines.append(f"def {fname}({params}) -> {ref}: ...")

            else:
                tgt_k = n
                tgt_tp = _proto_type_params(tgt_k, T)
                tgt = proto_id(tgt_k, T)
                edeps.add(tgt)
                ref = _ref_str(_cls_name(T, tgt_k), tgt_tp, False)
                if not T:
                    params = _render_params([], [], include_untracked=True, force_kw_tracked=True)
                    elines.append("@overload")
                    elines.append(f"def {fname}({params}) -> {ref}: ..." if params else f"def {fname}() -> {ref}: ...")
                else:
                    params = _render_params([], tracked_provided, include_untracked=False, force_kw_tracked=True)
                    elines.append("@overload")
                    elines.append(f"def {fname}({params}) -> {ref}: ...")

    blocks[ENTRY_ID] = (elines, edeps)

    # ── Protocol blocks (top-down: k=n down to k=1) ────────────────────

    for k in range(n, 0, -1):
        for S_tuple in all_subsets:
            S = frozenset(S_tuple)
            bid = proto_id(k, S)
            blines: list[str] = []
            bdeps: set[BlockId] = set()

            type_params = _proto_type_params(k, S)
            cls = _cls_name(S, k)

            remaining_kw_indices = [i for i in tk_positions if i not in S]
            remaining_kw_subsets = powerset(remaining_kw_indices)
            remaining_req = required[n - k:]

            if type_params:
                blines.append(f"class {cls}(Protocol[{', '.join(type_params)}]):")
            else:
                blines.append(f"class {cls}(Protocol):")

            for p in range(k + m, -1, -1):
                for T_tuple in remaining_kw_subsets:
                    T = frozenset(T_tuple)
                    ST = S | T

                    pos = list(remaining_req[:p]) if p <= k else list(remaining_req) + list(opt_pos[:p - k])
                    tracked_provided = [tracked[i] for i in sorted(T)]

                    if p >= k:
                        # All required satisfied → return type
                        lc_req = frozenset(range(n - k, n))
                        lc_opt = frozenset(range(p - k))
                        ret, arg_ovr = _resolve_implications(frozenset(range(n)), ST, lc_req, lc_opt, T)
                        params = _render_params(pos, tracked_provided, include_untracked=True, force_kw_tracked=False, arg_overrides=arg_ovr)
                        blines.append("    @overload")
                        blines.append(f"    def __call__(self{',' if params else ''} {params}) -> {ret}: ..." if params else f"    def __call__(self) -> {ret}: ...")

                    elif p > 0:
                        # Partial application → lower Protocol
                        tgt_k = k - p
                        tgt_tp = _proto_type_params(tgt_k, ST)
                        tgt = proto_id(tgt_k, ST)
                        # self-reference only if same block
                        quoted = (tgt == bid)
                        if not quoted:
                            bdeps.add(tgt)
                        ref = _ref_str(_cls_name(ST, tgt_k), tgt_tp, quoted)
                        params = _render_params(pos, tracked_provided, include_untracked=True, force_kw_tracked=True)
                        blines.append("    @overload")
                        blines.append(f"    def __call__(self, {params}) -> {ref}: ...")

                    else:
                        # p == 0
                        if not T:
                            # Self-reference
                            ref = _ref_str(cls, type_params, True)
                            params = _render_params([], [], include_untracked=True, force_kw_tracked=True)
                            blines.append("    @overload")
                            blines.append(f"    def __call__(self, {params}) -> {ref}: ..." if params else f"    def __call__(self) -> {ref}: ...")
                        else:
                            # Only tracked kwargs → same k, larger S
                            tgt_tp = _proto_type_params(k, ST)
                            tgt = proto_id(k, ST)
                            quoted = (tgt == bid)
                            if not quoted:
                                bdeps.add(tgt)
                            ref = _ref_str(_cls_name(ST, k), tgt_tp, quoted)
                            params = _render_params([], tracked_provided, include_untracked=False, force_kw_tracked=True)
                            blines.append("    @overload")
                            blines.append(f"    def __call__(self, {params}) -> {ref}: ...")

            blines.append("")
            blocks[bid] = (blines, bdeps)

    # ------------------------------------------------------------------
    # Topological sort (Kahn's algorithm by indegree)
    #
    # Edges: dep → bid  (dep must be emitted before bid)
    # Nodes with indegree 0 have no pending dependencies → emit first.
    # This produces a bottom-up output order, ensuring every type is
    # defined before it is referenced, with no forward-reference quotes
    # needed except for genuine self-references.
    # ------------------------------------------------------------------

    in_degree: dict[BlockId, int] = {bid: 0 for bid in blocks}
    successors: dict[BlockId, list[BlockId]] = {bid: [] for bid in blocks}

    for bid, (_, deps) in blocks.items():
        for dep in deps:
            in_degree[bid] += 1
            successors[dep].append(bid)

    queue: deque[BlockId] = deque(bid for bid in blocks if in_degree[bid] == 0)
    topo_order: list[BlockId] = []
    while queue:
        bid = queue.popleft()
        topo_order.append(bid)
        for succ in successors[bid]:
            in_degree[succ] -= 1
            if in_degree[succ] == 0:
                queue.append(succ)

    if len(topo_order) != len(blocks):
        raise RuntimeError("Cycle detected in Protocol dependency graph")

    # ------------------------------------------------------------------
    # Emit in topological order
    # ------------------------------------------------------------------

    out: list[str] = [spec.preamble, "", "from typing import Protocol, overload", ""]
    for bid in topo_order:
        out.extend(blocks[bid][0])

    return "\n".join(out)


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
# type_implications:  # rules that change types based on which args are provided
#   - when: []           # matches when all listed names are provided (keywords or required positionals)
#     return_type: "A | None"
#   - when: [some_kwarg]
#     not: [some_opt_pos]  # excludes match if any listed name is provided (keywords or optional positionals)
#     return_type: "A"
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
