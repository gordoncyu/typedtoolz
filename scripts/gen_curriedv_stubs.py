#!/usr/bin/env python3
"""
Generate CurriedV-family protocols (ParamSpec P) **and**
CurriedFixedV-family (no P, but variadic Ts).
Usage:
    python gen_curriedv_stubs.py 10 > _curryv.pyi
"""
from __future__ import annotations
import sys

MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10


def letters(n: int) -> list[str]:
    return [f"A{i+1}" for i in range(n)]


# ─── header ────────────────────────────────────────────────────────────
print("from typing import Callable, Concatenate, Literal, ParamSpec, Protocol, TypeVar, TypeVarTuple, Unpack, overload\n")

print("P = ParamSpec('P')")
print("Ts = TypeVarTuple('Ts')")        # for CurriedFixedV*
print("R = TypeVar('R', covariant=True)")
for tv in letters(MAX):
    print(f"{tv} = TypeVar('{tv}', contravariant=True)")
print()


# ─── helpers to emit protocol bodies ──────────────────────────────────
def emit_body(n: int, fixed_only: bool) -> None:
    args = letters(n)
    tail = ", *args: P.args, **kw: P.kwargs" if not fixed_only else ", *xs: Unpack[Ts]"
    call_suffix = tail if tail.strip() else ""
    # fully applied
    fp = ", ".join(f"{a}: {a}" for a in args)
    print("    @overload")
    print(f"    def __call__(self, {fp}{call_suffix}) -> R: ...")

    # partially applied
    for k in range(1, n):
        pre = ", ".join(f"{args[i]}: {args[i]}" for i in range(k))
        rest = ", ".join(args[k:])
        if fixed_only:
            ret = f"CurriedFixedV{n-k}[{rest}, *Ts, R]"
        else:
            ret = f"CurriedV{n-k}[{rest}, P, R]"
        print("    @overload")
        print(f"    def __call__(self, {pre}, /) -> {ret}: ...")

    # zero‐arg
    full_gen = ", ".join(
        args + ([] if fixed_only else ["P"]) + (["*Ts"] if fixed_only else []) + ["R"]
    )
    cls = "CurriedFixedV" if fixed_only else "CurriedV"
    print("    @overload")
    print(f"    def __call__(self) -> '{cls}{n}[{full_gen}]': ...\n")


# ─── emit protocols ──────────────────────────────────────────────────
for n in range(1, MAX + 1):
    # CurriedVn – keeps P
    g_full = ", ".join(letters(n) + ["P", "R"])
    print(f"class CurriedV{n}(Protocol[{g_full}]):")
    emit_body(n, fixed_only=False)

    # CurriedFixedVn – uses *Ts
    g_fixed = ", ".join(letters(n) + ["*Ts", "R"])
    print(f"class CurriedFixedV{n}(Protocol[{g_fixed}]):")
    emit_body(n, fixed_only=True)

# ─── curryv(...) overloads (unchanged) ────────────────────────────────
for n in range(MAX, 0, -1):
    ltrs = letters(n)
    prefix = ", ".join(ltrs)
    gen    = ", ".join(ltrs + ["P", "R"])
    print("@overload")
    print(
        f"def curryv(pn: Literal[{n}], f: Callable[Concatenate[{prefix}, P], R], /) -> CurriedV{n}[{gen}]: ...\n"
    )

print("@overload\ndef curryv(pn: int, f: Callable[..., R], /) -> Callable[..., R]: ...")

