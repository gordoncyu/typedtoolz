from collections.abc import Iterable, Iterator
from typing import TypeVar, overload

T = TypeVar('T')
D = TypeVar('D')

def sliding_window(n: int, seq: Iterable[T]) -> Iterator[tuple[T, ...]]: ...

@overload
def partition(n: int, seq: Iterable[T]) -> Iterator[tuple[T, ...]]: ...
@overload
def partition(n: int, seq: Iterable[T], pad: D) -> Iterator[tuple[T | D, ...]]: ...

def partition_all(n: int, seq: Iterable[T]) -> Iterator[tuple[T, ...]]: ...
