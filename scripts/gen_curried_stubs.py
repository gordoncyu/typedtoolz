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
    python gen_curried_stubs.py 10 > _curried.pyi
"""
from __future__ import annotations
import sys

MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10


def tv(i: int) -> str:
    return f"A{i}"


# ── header ────────────────────────────────────────────────────────────
print("from typing import Callable, Concatenate, ParamSpec, Protocol, TypeVar, overload\n")

print("P = ParamSpec('P')")
print("R = TypeVar('R', covariant=True)")
for i in range(1, MAX + 1):
    print(f"{tv(i)} = TypeVar('{tv(i)}', contravariant=True)")
print()


# ── emit protocols ────────────────────────────────────────────────────
def emit_curried(n: int, fixed_only: bool) -> None:
    # type-var lists
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


for arity in range(1, MAX + 1):
    emit_curried(arity, fixed_only=False)  # CurriedN
    emit_curried(arity, fixed_only=True)   # CurriedFixedN


# ── curry(...) overloads (point to CurriedN) ──────────────────────────
for n in range(MAX, 0, -1):
    params = ", ".join(tv(i) for i in range(1, n + 1))
    gener  = ", ".join([*params.split(", "), "P", "R"])
    print("@overload")
    print(
        f"def curry(fn: Callable[Concatenate[{params}, P], R], /) -> Curried{n}[{gener}]: ...\n"
    )

