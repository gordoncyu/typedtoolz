#!/usr/bin/env python3
"""
Generate overloads for:

    juxt(f1, f2, ..., fn) -> Callable[P, tuple[R1, R2, ..., Rn]]

All functions share a common ParamSpec P (same input signature).
Arity max = first CLI arg (default 10).
"""
from __future__ import annotations
import sys

MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10

# ── header ────────────────────────────────────────────────────────────
print("from typing import Any, Callable, ParamSpec, TypeVar, overload\n")

print("P = ParamSpec('P')")
for i in range(1, MAX + 1):
    print(f"R{i} = TypeVar('R{i}')")
print()

# ── overloads ─────────────────────────────────────────────────────────
for n in range(1, MAX + 1):
    func_params = ", ".join(f"f{i}: Callable[P, R{i}]" for i in range(1, n + 1))
    ret_inner = ", ".join(f"R{i}" for i in range(1, n + 1))
    print("@overload")
    print(f"def juxt({func_params}, /) -> Callable[P, tuple[{ret_inner}]]: ...\n")

# ── fallback ───────────────────────────────────────────────────────────
print("@overload")
print("def juxt(*funcs: Callable[..., Any], /) -> Callable[..., tuple[Any, ...]]: ...")
