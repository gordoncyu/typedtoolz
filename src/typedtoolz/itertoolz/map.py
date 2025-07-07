# Typed and curried map
from typing import overload, Callable, Iterable, cast, TypeVar
from toolz.curried import map as toolz_map


A = TypeVar("A")
B = TypeVar("B")

_map_iterable_not_passed = object()
@overload
def map(fn: Callable[[A], B]) -> Callable[[Iterable[A]], Iterable[B]]: ...
@overload
def map(fn: Callable[[A], B], xs: Iterable[A]) -> Iterable[B]: ...

def map(fn: Callable[[A], B], xs: Iterable[A] = cast(Iterable[A], _map_iterable_not_passed)): # pyright: ignore[reportInconsistentOverload]
    if xs is _map_iterable_not_passed:
        return lambda _xs: map(fn, _xs)
    return toolz_map(fn, xs)

