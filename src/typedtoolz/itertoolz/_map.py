from collections.abc import Iterable, Iterator
from typing import Callable, TypeVar
from typing_extensions import Any, overload, override
from typedtoolz.functoolz import curry, curryv
from builtins import map as rmap
import sys

_T1 = TypeVar("_T1")
_T2 = TypeVar("_T2")
_T3 = TypeVar("_T3")
_T4 = TypeVar("_T4")
_T5 = TypeVar("_T5")
_S = TypeVar("_S")
class _map_meta(type):
    if sys.version_info >= (3, 14): # 3.14 adds `strict` argument.
        @staticmethod
        @override
        def __call__(
                func: Callable[..., _S],
                iterable: Iterable[Any],  # pyright: ignore[reportExplicitAny]
                /,
                *iterables: Iterable[Any],  # pyright: ignore[reportExplicitAny]
                strict: bool = False,
                ) -> Iterator[_S]:
            return rmap(func, iterable, *iterables, strict=strict)  # pyright: ignore[reportCallIssue]
    else:
        @staticmethod
        @override
        def __call__(
                func: Callable[..., _S],
                iterable: Iterable[Any],  # pyright: ignore[reportExplicitAny]
                /,
                *iterables: Iterable[Any],  # pyright: ignore[reportExplicitAny]
                ) -> Iterator[_S]:
            return rmap(func, iterable, *iterables)

class map(metaclass=_map_meta):
    """
    Make an iterator that computes the function using arguments from
    each of the iterables.  Stops when the shortest iterable is exhausted.

    If strict is true and one of the arguments is exhausted before the others,
    raise a ValueError.

    Has a curried version as the property c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curryv(2, _map_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]

__all__ = [
        "map",
        ]
