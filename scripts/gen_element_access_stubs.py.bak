#!/usr/bin/env python3
"""
Generate overloads for nth, first, second, last, rest, peek, peekn.

nth(Literal[i], tuple[A1, ..., A{i+1}, *Ts]) -> A{i+1}
first(tuple[T, *Ts]) -> T
second(tuple[A1, T, *Ts]) -> T
last(tuple[*Ts, T]) -> T

Tuple arity max = first CLI arg (default 10).
"""
from __future__ import annotations
import sys

MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10

# ── header ────────────────────────────────────────────────────────────
print("from collections.abc import Iterable, Iterator")
print("from typing import Literal, TypeVar, TypeVarTuple, overload\n")

print("T = TypeVar('T')")
print("A1 = TypeVar('A1')")
print("A2 = TypeVar('A2')")
for i in range(3, MAX + 2):
    print(f"A{i} = TypeVar('A{i}')")
print("Ts = TypeVarTuple('Ts')\n")

# ── nth ───────────────────────────────────────────────────────────────
for idx in range(MAX):  # 0-indexed access
    # minimum tuple size is idx+1; remaining elements are *Ts
    type_params = ", ".join(f"A{j + 1}" for j in range(idx + 1))
    print("@overload")
    print(f"def nth(n: Literal[{idx}], seq: tuple[{type_params}, *Ts]) -> A{idx + 1}: ...")
print("@overload")
print("def nth(n: int, seq: Iterable[T]) -> T: ...\n")

# ── first ─────────────────────────────────────────────────────────────
print("@overload")
print("def first(seq: tuple[T, *Ts]) -> T: ...")
print("@overload")
print("def first(seq: Iterable[T]) -> T: ...\n")

# ── second ────────────────────────────────────────────────────────────
print("@overload")
print("def second(seq: tuple[A1, T, *Ts]) -> T: ...")
print("@overload")
print("def second(seq: Iterable[T]) -> T: ...\n")

# ── last ──────────────────────────────────────────────────────────────
print("@overload")
print("def last(seq: tuple[*Ts, T]) -> T: ...")
print("@overload")
print("def last(seq: Iterable[T]) -> T: ...\n")

# ── rest / peek / peekn ───────────────────────────────────────────────
print("def rest(seq: Iterable[T]) -> Iterator[T]: ...\n")
print("def peek(seq: Iterable[T]) -> tuple[T, Iterator[T]]: ...\n")
print("def peekn(n: int, seq: Iterable[T]) -> tuple[list[T], Iterator[T]]: ...")
