from collections.abc import Iterable, Iterator, Mapping, Sequence
from typing import TypeVar, overload

T = TypeVar('T')
D = TypeVar('D')
K = TypeVar('K')
V = TypeVar('V')

@overload
def pluck(ind: int, seqs: Iterable[Sequence[T]]) -> Iterator[T]: ...
@overload
def pluck(ind: int, seqs: Iterable[Sequence[T]], default: D) -> Iterator[T | D]: ...
@overload
def pluck(ind: K, seqs: Iterable[Mapping[K, V]]) -> Iterator[V]: ...
@overload
def pluck(ind: K, seqs: Iterable[Mapping[K, V]], default: D) -> Iterator[V | D]: ...
