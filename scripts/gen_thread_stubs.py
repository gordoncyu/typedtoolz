#!/usr/bin/env python3
"""
Generate overloads for thread_first and thread_last.

thread_first(val, form1, form2, ..., formN) -> R
  Each form is: Callable[[Ti], Ti1] | tuple[Callable[[Ti, *Tsi], Ti1], *Tsi]
  (val inserted as FIRST arg of the callable)

thread_last(val, form1, form2, ..., formN) -> R
  Each form is: Callable[[Ti], Ti1] | tuple[Callable[[*Tsi, Ti], Ti1], *Tsi]
  (val inserted as LAST arg of the callable)

Number of forms max = first CLI arg (default 10).
"""
from __future__ import annotations
import sys

MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10


def tv(i: int, n: int) -> str:
    """Return the TypeVar name for step i in a chain of n forms."""
    if i == 0:
        return "A"
    if i == n:
        return "R"
    return f"T{i}"


# ── header ────────────────────────────────────────────────────────────
print("from typing import Callable, TypeVar, TypeVarTuple, Unpack, overload\n")

print("A = TypeVar('A', contravariant=True)")
for i in range(1, MAX):
    print(f"T{i} = TypeVar('T{i}')")
print("R = TypeVar('R', covariant=True)")
for i in range(1, MAX + 1):
    print(f"Ts{i} = TypeVarTuple('Ts{i}')")
print()


def first_form(i: int, n: int, ts: str) -> str:
    """Form type for thread_first at step i (0-indexed input, n total forms)."""
    ti = tv(i, n)
    ti1 = tv(i + 1, n)
    return (
        f"Callable[[{ti}], {ti1}]"
        f" | tuple[Callable[[{ti}, *{ts}], {ti1}], *{ts}]"
    )


def last_form(i: int, n: int, ts: str) -> str:
    """Form type for thread_last at step i (val inserted last)."""
    ti = tv(i, n)
    ti1 = tv(i + 1, n)
    return (
        f"Callable[[{ti}], {ti1}]"
        f" | tuple[Callable[[*{ts}, {ti}], {ti1}], *{ts}]"
    )


# ── thread_first overloads ────────────────────────────────────────────
for n in range(1, MAX + 1):
    params = ["val: A"] + [
        f"form{i}: {first_form(i - 1, n, f'Ts{i}')}" for i in range(1, n + 1)
    ]
    print("@overload")
    print(f"def thread_first({', '.join(params)}) -> R: ...\n")

# ── thread_last overloads ─────────────────────────────────────────────
for n in range(1, MAX + 1):
    params = ["val: A"] + [
        f"form{i}: {last_form(i - 1, n, f'Ts{i}')}" for i in range(1, n + 1)
    ]
    print("@overload")
    print(f"def thread_last({', '.join(params)}) -> R: ...\n")
