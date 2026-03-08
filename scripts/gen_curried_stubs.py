#!/usr/bin/env python3
"""
gen_curried_stubs.py
--------------------
Emit:

    CurriedN[A1, …, An, P, R]        • keeps ParamSpec tail
    CurriedFixedN[A1, …, An, R]      • no P, no Ts

Each __call__ overload returns either:
    • R  (when fully applied)
    • Curried(K) or CurriedFixed(K)   (when partially applied)
    • itself (when called with no args)

Usage:
    python gen_curried_stubs.py [MAX [PRE]] > _curried.pyi

    MAX  – max function arity tracked (default 10)
    PRE  – max positional args that can be pre-applied on the curry() call
           itself (default MAX // 2)
"""
from __future__ import annotations
import sys

MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10
PRE = int(sys.argv[2]) if len(sys.argv) > 2 else MAX // 2


def tv(i: int) -> str:
    return f"A{i}"


def ret_fixed_cls(remaining: int) -> str:
    return "Curried0" if remaining == 0 else f"CurriedFixed{remaining}"


def ret_fixed_gens(start: int, end: int) -> str:
    """Type params for CurriedFixed(end-start) or Curried0 return type."""
    parts = [tv(i) for i in range(start + 1, end + 1)]
    # Curried0 now takes P; CurriedFixedN does not
    if end == start:
        return "P, R"
    return ", ".join(parts + ["R"])


# ── header ────────────────────────────────────────────────────────────
print("from typing import Any, Callable, Concatenate, Literal, ParamSpec, Protocol, TypeVar, overload\n")

print("P = ParamSpec('P')")
print("R = TypeVar('R', covariant=True)")
for i in range(1, MAX + 1):
    print(f"{tv(i)} = TypeVar('{tv(i)}', contravariant=True)")
print()


# ── emit protocols ────────────────────────────────────────────────────
def emit_curried(n: int, fixed_only: bool) -> None:
    fixed = [tv(i) for i in range(1, n + 1)]
    gens  = fixed + ([] if fixed_only else ["P"]) + ["R"]
    cls   = f"Curried{'Fixed' if fixed_only else ''}{n}"
    print(f"class {cls}(Protocol[{', '.join(gens)}]):")

    # fully applied
    all_params = ", ".join(f"{a}: {a}" for a in fixed)
    tail = "" if fixed_only else ", *args: P.args, **kw: P.kwargs"
    print("    @overload")
    print(f"    def __call__(self, {all_params}{tail}) -> R: ...")

    # partially applied (1 … n-1)
    for k in range(1, n):
        prefix = ", ".join(f"{fixed[i]}: {fixed[i]}" for i in range(k))
        remaining = ", ".join(fixed[k:])
        ret_cls   = f"Curried{'Fixed' if fixed_only else ''}{n-k}"
        ret_gens  = remaining + ("" if fixed_only else ", P") + ", R"
        print("    @overload")
        print(f"    def __call__(self, {prefix}, /) -> {ret_cls}[{ret_gens}]: ...")

    # zero-arg
    print("    @overload")
    full_gens = ", ".join(gens)
    print(f"    def __call__(self) -> '{cls}[{full_gens}]': ...\n")


# Curried0 – no positional args remaining; P carries through kwargs
print("class Curried0(Protocol[P, R]):")
print("    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R: ...\n")

for arity in range(1, MAX + 1):
    emit_curried(arity, fixed_only=False)  # CurriedN
    emit_curried(arity, fixed_only=True)   # CurriedFixedN


# ── _CurryFixedNMaker protocols (returned by curry(n)) ────────────────
KW_IGNORE = "  # pyright: ignore[reportExplicitAny, reportAny]"

for n in range(1, MAX + 1):
    pre_n = min(PRE, n)
    fn_params = ", ".join(tv(i) for i in range(1, n + 1))
    fn_type = f"Callable[Concatenate[{fn_params}, P], R]"
    print(f"class _CurryFixed{n}Maker(Protocol):")
    # emit overloads from most pre-applied to least; use @overload only if >1 variant
    use_overload = pre_n > 0
    for k in range(pre_n, -1, -1):
        pre_args = ("".join(f", {tv(i)}: {tv(i)}" for i in range(1, k + 1))) if k > 0 else ""
        cls = ret_fixed_cls(n - k)
        gens = ret_fixed_gens(k, n)
        if use_overload:
            print("    @overload")
        print(f"    def __call__(self, fn: {fn_type}{pre_args}, /, **kwargs: Any) -> {cls}[{gens}]: ...{KW_IGNORE}")
    print()


# ── curry(fn) overloads (point to CurriedN, inferred arity) ───────────
# For each function arity N, emit k=min(PRE,N) down to k=0 pre-applied args.
for n in range(MAX, 0, -1):
    fn_params = ", ".join(tv(i) for i in range(1, n + 1))
    fn_type = f"Callable[Concatenate[{fn_params}, P], R]"
    pre_n = min(PRE, n)
    for k in range(pre_n, -1, -1):
        pre_args = ("".join(f", {tv(i)}: {tv(i)}" for i in range(1, k + 1))) if k > 0 else ""
        if k < n:
            remaining = [tv(i) for i in range(k + 1, n + 1)]
            ret = f"Curried{n - k}[{', '.join(remaining + ['P', 'R'])}]"
        else:
            ret = "Curried0[P, R]"
        print("@overload")
        print(f"def curry(fn: {fn_type}{pre_args}, /, **kwargs: Any) -> {ret}: ...{KW_IGNORE}\n")

# 0-arity function (no pre-application possible)
print("@overload")
print(f"def curry(fn: Callable[P, R], /, **kwargs: Any) -> Curried0[P, R]: ...{KW_IGNORE}\n")

# ── curry(pn) overloads (return maker that takes fn) ──────────────────
for n in range(MAX, 0, -1):
    print("@overload")
    print(f"def curry(pn: Literal[{n}], /) -> _CurryFixed{n}Maker: ...\n")
