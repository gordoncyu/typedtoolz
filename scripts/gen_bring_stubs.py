#!/usr/bin/env python3
"""
gen_bring_stubs.py  –  overloads for a combinator that
brings the n-th positional argument (0-based) to the front.

Produces BOTH:
    bring(n, func)
    bring(n)(func)

Run:
    python gen_bring_stubs.py 6  > bring.pyi
"""
from __future__ import annotations
import sys

MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10

# ─── header ───────────────────────────────────────────────────────────
print("from typing import Callable, Concatenate, Literal, ParamSpec, TypeVar, overload\n")

for i in range(1, MAX + 2):                   # need MAX+1 explicit slots
    print(f"A{i} = TypeVar('A{i}', contravariant=True)")
print("R = TypeVar('R', covariant=True)")
print("P = ParamSpec('P')\n")

# ─── helper -----------------------------------------------------------
def after_list(n: int) -> str:
    """Return 'A{n+1}, A2 … A{n}, A1'  (identity for n == 0)."""
    if n == 0:
        return "A1"
    middle = ", ".join(f"A{i}" for i in range(2, n + 1))  # A2..An  (may be '')
    parts = [f"A{n+1}"] + ([middle] if middle else []) + ["A1"]
    return ", ".join(part for part in parts if part)

# ─── overloads --------------------------------------------------------
for n in range(0, MAX + 1):
    arity  = n + 1
    before = ", ".join(f"A{i}" for i in range(1, arity + 1))
    after  = after_list(n)

    fn_in   = f"Callable[Concatenate[{before}, P], R]"
    fn_out  = f"Callable[Concatenate[{after}, P], R]"

    # direct
    print("@overload")
    print(f"def bring(n: Literal[{n}], func: {fn_in}, /) -> {fn_out}: ...\n")

    # curried
    print("@overload")
    print(f"def bring(n: Literal[{n}], /) -> Callable[[{fn_in}], {fn_out}]: ...\n")

# ─── fallback ---------------------------------------------------------
print(
    "@overload\n"
    "def bring(n: int, func: Callable[..., R], /) -> Callable[..., R]: ...\n\n"
    "@overload\n"
    "def bring(n: int, /) -> Callable[[Callable[..., R]], Callable[..., R]]: ..."
)

