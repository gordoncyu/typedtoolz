from collections.abc import Callable, Iterable, Iterator
from typing import TypeVar

T = TypeVar('T')
K = TypeVar('K')
L = TypeVar('L')
R = TypeVar('R')

def unique(seq: Iterable[T], key: Callable[[T], object] = ...) -> Iterator[T]: ...
def diff(*seqs: Iterable[T], key: Callable[[T], object] = ..., default: T = ...) -> Iterator[tuple[T, ...]]: ...
def join(
    leftkey: Callable[[L], K],
    leftseq: Iterable[L],
    rightkey: Callable[[R], K],
    rightseq: Iterable[R],
    left_default: L = ...,
    right_default: R = ...,
) -> Iterator[tuple[L, R]]: ...
