#!/usr/bin/env python3
"""
Generate overloads for unzip with fixed-length tuple inputs.

unzip(Iterable[tuple[A1, A2]]) -> tuple[Iterator[A1], Iterator[A2]]
...up to MAX-length tuples, then a general fallback.

Max tuple arity = first CLI arg (default 10).
"""
from __future__ import annotations
import sys

MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10

# ── header ────────────────────────────────────────────────────────────
print("from collections.abc import Iterable, Iterator")
print("from typing import TypeVar, overload\n")

for i in range(1, MAX + 1):
    print(f"A{i} = TypeVar('A{i}')")
print("T = TypeVar('T')\n")

# ── fixed-arity overloads ─────────────────────────────────────────────
for n in range(1, MAX + 1):
    type_vars = ", ".join(f"A{i}" for i in range(1, n + 1))
    in_tuple  = f"tuple[{type_vars}]"
    out_iters = ", ".join(f"Iterator[A{i}]" for i in range(1, n + 1))
    out_tuple = f"tuple[{out_iters}]"
    print("@overload")
    print(f"def unzip(seq: Iterable[{in_tuple}]) -> {out_tuple}: ...")

# ── general fallbacks ─────────────────────────────────────────────────
print("@overload")
print("def unzip(seq: Iterable[tuple[T, ...]]) -> tuple[Iterator[T], ...]: ...")
print("@overload")
print("def unzip(seq: Iterable[Iterable[T]]) -> tuple[Iterator[T], ...]: ...")
