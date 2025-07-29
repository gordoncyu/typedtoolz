#!/usr/bin/env python3
"""
Generate overloads for:

    pipe(value, f1, f2, ..., fn) -> R

where
    f1 : Callable[[A],  T1]
    f2 : Callable[[T1], T2]
    ...
    fn : Callable[[Tn-1], R]

The first CLI arg sets the maximum chain length (default 20).
"""

from __future__ import annotations
import sys

MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 20

# ── header ────────────────────────────────────────────────────────────
print("from typing import Callable, overload, TypeVar\n")

print("A = TypeVar('A', contravariant=True)")          # initial value
for i in range(1, MAX):                                 # intermediates
    print(f"T{i} = TypeVar('T{i}')")
print("R = TypeVar('R', covariant=True)\n")             # final result

# ── overloads ─────────────────────────────────────────────────────────
for n in range(1, MAX + 1):
    parts   = ["A"] + [f"T{i}" for i in range(1, n)] + ["R"]
    f_params = ", ".join(
        f"f{i}: Callable[[{parts[i-1]}], {parts[i]}]" for i in range(1, n + 1)
    )
    sig = ", ".join(["value: A", f_params])
    print("@overload")
    print(f"def pipe({sig}, /) -> R: ...\n")

# print("@overload\ndef pipe(*args, **kw): ...")

