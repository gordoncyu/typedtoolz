# TODO: Improve map typing
from collections.abc import Callable, Iterable
from typing import TypeVar, overload

T = TypeVar('T')
A = TypeVar('A')

@overload
def fold(
    binop: Callable[[T, T], T],
    seq: Iterable[T],
    *,
    map: Callable[..., object] = ...,
    chunksize: int = ...,
    combine: Callable[[T, T], T] | None = ...,
) -> T: ...
@overload
def fold(
    binop: Callable[[A, T], A],
    seq: Iterable[T],
    default: A,
    map: Callable[..., object] = ...,
    chunksize: int = ...,
    combine: Callable[[A, A], A] | None = ...,
) -> A: ...
