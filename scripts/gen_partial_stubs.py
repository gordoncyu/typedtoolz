#!/usr/bin/env python3
"""
gen_partial_stubs.py
--------------------
Generate overloads for functools.partial:

    partial(func, a1, ..., aN, **kwargs) -> Callable[P, R]

where func: Callable[Concatenate[A1, ..., AM, P], R]

Only the remaining positional args appear in the returned callable's signature.
Keyword args flow through unchanged via P.

Overloads are ordered by total positional args descending, so the most specific
match wins.

Usage:
    python gen_partial_stubs.py 10 > _partial.pyi
"""
from __future__ import annotations
import sys

MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10

# ── header ─────────────────────────────────────────────────────────────
print("from typing import Callable, Concatenate, ParamSpec, TypeVar, overload")
print("from typing_extensions import Any\n")

print("P = ParamSpec('P')")
print("R = TypeVar('R')")
for i in range(1, MAX + 1):
    print(f"A{i} = TypeVar('A{i}')")
print()

# ── overloads ───────────────────────────────────────────────────────────
for n in range(MAX, 0, -1):
    tvs       = [f"A{i}" for i in range(1, n + 1)]
    func_type = f"Callable[Concatenate[{', '.join(tvs + ['P'])}], R]"
    args      = ", ".join(f"__a{i}: A{i}" for i in range(1, n + 1))
    print("@overload")
    print(f"def partial(func: {func_type}, {args}, /, **kwargs: Any) -> Callable[P, R]: ...  # pyright: ignore[reportExplicitAny, reportAny]")
    print()

# ── 0 positional args (kwargs only) ────────────────────────────────────
print("@overload")
print("def partial(func: Callable[P, R], /, **kwargs: Any) -> Callable[P, R]: ...  # pyright: ignore[reportExplicitAny, reportAny]")
print()
