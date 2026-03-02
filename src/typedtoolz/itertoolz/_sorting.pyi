from collections.abc import Callable, Iterable
from typing import TypeVar

T = TypeVar('T')

def merge_sorted(*seqs: Iterable[T], key: Callable[[T], object] = ...) -> Iterable[T]: ...
def topk(k: int, seq: Iterable[T], key: Callable[[T], object] = ...) -> list[T]: ...
