#!/usr/bin/env python3
"""
Generate CurriedV-family protocols (ParamSpec P) **and**
CurriedFixedV-family (no P, but variadic Ts).

Usage:
    python gen_curriedv_stubs.py [MAX [PRE]] > _curryv.pyi

    MAX  – max function arity tracked (default 10)
    PRE  – max positional args that can be pre-applied on the curryv() maker
           call itself (default MAX // 2)
"""
from __future__ import annotations
import sys

MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10
PRE = int(sys.argv[2]) if len(sys.argv) > 2 else MAX // 2

KW_IGNORE = "  # pyright: ignore[reportAny, reportExplicitAny]"


def letters(n: int) -> list[str]:
    return [f"A{i+1}" for i in range(n)]


# ─── header ────────────────────────────────────────────────────────────
print("from typing import Any, Callable, Concatenate, Literal, ParamSpec, Protocol, TypeVar, overload\n")

print("P = ParamSpec('P')")
print("R = TypeVar('R', covariant=True)")
for tv in letters(MAX):
    print(f"{tv} = TypeVar('{tv}', contravariant=True)")
print()


# ─── helpers to emit protocol bodies ──────────────────────────────────
def emit_body(n: int) -> None:
    args = letters(n)
    fp = ", ".join(f"{a}: {a}" for a in args)
    full_gen = ", ".join(args + ["P", "R"])
    # fully applied
    print("    @overload")
    print(f"    def __call__(self, {fp}, *args: P.args, **kw: P.kwargs) -> R: ...")
    # partially applied
    for k in range(1, n):
        pre = ", ".join(f"{args[i]}: {args[i]}" for i in range(k))
        rest = ", ".join(args[k:])
        print("    @overload")
        print(f"    def __call__(self, {pre}, /) -> CurriedV{n-k}[{rest}, P, R]: ...")
    # zero-arg
    print("    @overload")
    print(f"    def __call__(self) -> 'CurriedV{n}[{full_gen}]': ...")
    # kwargs-only → return self
    print("    @overload")
    print(f"    def __call__(self, **kw: Any) -> 'CurriedV{n}[{full_gen}]': ...{KW_IGNORE}")
    print()


# ─── CurriedV0 (used as return type when all args are pre-applied) ─────
print("class CurriedV0(Protocol[P, R]):")
print("    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R: ...\n")

# ─── emit protocols ──────────────────────────────────────────────────
for n in range(1, MAX + 1):
    g_full = ", ".join(letters(n) + ["P", "R"])
    print(f"class CurriedV{n}(Protocol[{g_full}]):")
    emit_body(n)

# ─── _CurryVNMaker protocols (returned by curryv(n)) ─────────────────
for n in range(1, MAX + 1):
    ltrs     = letters(n)
    prefix   = ", ".join(ltrs)
    fn_type  = f"Callable[Concatenate[{prefix}, P], R]"
    gen      = ", ".join(ltrs + ["P", "R"])
    pre_n    = min(PRE, n)
    print(f"class _CurryV{n}Maker(Protocol):")
    use_overload = pre_n > 0
    for k in range(pre_n, -1, -1):
        pre_args = ("".join(f", {ltrs[i]}: {ltrs[i]}" for i in range(k))) if k > 0 else ""
        remaining = ltrs[k:]
        if remaining:
            ret = f"CurriedV{len(remaining)}[{', '.join(remaining + ['P', 'R'])}]"
        else:
            ret = "CurriedV0[P, R]"
        if use_overload:
            print("    @overload")
        print(f"    def __call__(self, f: {fn_type}{pre_args}, /, **kwargs: Any) -> {ret}: ...{KW_IGNORE}")
    print()

# ─── curryv(n) overloads (return maker that takes f) ──────────────────
for n in range(MAX, 0, -1):
    print("@overload")
    print(f"def curryv(pn: Literal[{n}], /) -> _CurryV{n}Maker: ...\n")
