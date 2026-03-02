#!/usr/bin/env python3
"""
Generate overloads for:

    compose(fn, ..., f2, f1) -> Callable[[A], R]

Arguments are RIGHT-to-LEFT: the last argument is applied first.
Chain length max = first CLI arg (default 20).
"""
from __future__ import annotations
import sys

MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 20

# ── header ────────────────────────────────────────────────────────────
print("from typing import Callable, overload, TypeVar\n")

print("A = TypeVar('A', contravariant=True)")
for i in range(1, MAX):
    print(f"T{i} = TypeVar('T{i}')")
print("R = TypeVar('R', covariant=True)\n")

# ── overloads ─────────────────────────────────────────────────────────
for n in range(1, MAX + 1):
    # parts[0]=A, parts[1]=T1, ..., parts[n-1]=T{n-1}, parts[n]=R
    parts = ["A"] + [f"T{i}" for i in range(1, n)] + ["R"]

    # compose arg position j (1-indexed, j=1 is first/outermost):
    #   maps parts[n-j] -> parts[n-j+1]
    #   name: f{n-j+1} (innermost function = f1 = last arg)
    f_params = ", ".join(
        f"f{n-j+1}: Callable[[{parts[n-j]}], {parts[n-j+1]}]" for j in range(1, n + 1)
    )
    print("@overload")
    print(f"def compose({f_params}, /) -> Callable[[A], R]: ...\n")
