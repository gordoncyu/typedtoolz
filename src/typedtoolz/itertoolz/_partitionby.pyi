from collections.abc import Callable, Iterable, Iterator
from typing import TypeVar

T = TypeVar('T')

def partitionby(func: Callable[[T], object], seq: Iterable[T]) -> Iterator[tuple[T, ...]]: ...
