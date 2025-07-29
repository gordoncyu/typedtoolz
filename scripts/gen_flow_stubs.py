#!/usr/bin/env python3
"""
Generate overloads for:

    flow(f1, f2, ..., fn) -> Callable[[A], R]

Chain length max = first CLI arg (default 20).
"""

from __future__ import annotations
import sys

MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 20

# ── header ────────────────────────────────────────────────────────────
print("from typing import Callable, overload, TypeVar\n")

print("A = TypeVar('A', contravariant=True)")           # input type
for i in range(1, MAX):                                  # intermediates
    print(f"T{i} = TypeVar('T{i}')")
print("R = TypeVar('R', covariant=True)\n")              # output type

# ── overloads ─────────────────────────────────────────────────────────
for n in range(1, MAX + 1):
    parts = ["A"] + [f"T{i}" for i in range(1, n)] + ["R"]
    f_params = ", ".join(
        f"f{i}: Callable[[{parts[i-1]}], {parts[i]}]" for i in range(1, n + 1)
    )
    print("@overload")
    print(f"def flow({f_params}, /) -> Callable[[A], R]: ...\n")

# print("@overload\ndef flow(*funcs, **kw): ...")

