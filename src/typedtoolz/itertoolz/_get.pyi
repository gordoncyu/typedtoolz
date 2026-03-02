from collections.abc import Mapping, Sequence
from typing import TypeVar, overload

T = TypeVar('T')
D = TypeVar('D')
K = TypeVar('K')
V = TypeVar('V')

@overload
def get(ind: int, seq: Sequence[T]) -> T: ...
@overload
def get(ind: int, seq: Sequence[T], default: D) -> T | D: ...
@overload
def get(ind: list[int], seq: Sequence[T]) -> list[T]: ...
@overload
def get(ind: list[int], seq: Sequence[T], default: D) -> list[T | D]: ...
@overload
def get(ind: K, seq: Mapping[K, V]) -> V: ...
@overload
def get(ind: K, seq: Mapping[K, V], default: D) -> V | D: ...
