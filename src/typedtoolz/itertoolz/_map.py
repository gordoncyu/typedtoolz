from collections.abc import Iterable, Iterator
from typing import Callable, TypeVar, overload
from typing_extensions import Any, override
from typedtoolz.functoolz import curryv
from builtins import map as cymap
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
        @overload
        def __call__(
                func: Callable[[_T1], _S],
                iterable: Iterable[_T1],
                /,
                strict: bool = False,
                ) -> Iterable[_S]: ...
        @staticmethod
        @overload
        def __call__(
                func: Callable[[_T1, _T2], _S],
                iterable: Iterable[_T1],
                iter2: Iterable[_T2],
                /,
                strict: bool = False,
                ) -> Iterable[_S]: ...
        @staticmethod
        @overload
        def __call__(
                func: Callable[[_T1, _T2, _T3], _S],
                iterable: Iterable[_T1],
                iter2: Iterable[_T2],
                iter3: Iterable[_T3],
                /,
                strict: bool = False,
                ) -> Iterable[_S]: ...
        @staticmethod
        @overload
        def __call__(
                func: Callable[[_T1, _T2, _T3, _T4], _S],
                iterable: Iterable[_T1],
                iter2: Iterable[_T2],
                iter3: Iterable[_T3],
                iter4: Iterable[_T4],
                /,
                strict: bool = False,
                ) -> Iterable[_S]: ...
        @staticmethod
        @overload
        def __call__(
                func: Callable[[_T1, _T2, _T3, _T4, _T5], _S],
                iterable: Iterable[_T1],
                iter2: Iterable[_T2],
                iter3: Iterable[_T3],
                iter4: Iterable[_T4],
                iter5: Iterable[_T5],
                /,
                strict: bool = False,
                ) -> Iterable[_S]: ...
        @staticmethod  # pyright: ignore[reportUnreachable]
        @override
        def __call__(
                func: Callable[..., _S],
                iterable: Iterable[Any],  # pyright: ignore[reportExplicitAny, reportUnnecessaryTypeIgnoreComment]
                /,
                *iterables: Iterable[Any],  # pyright: ignore[reportExplicitAny, reportUnnecessaryTypeIgnoreComment]
                strict: bool = False,
                ) -> Iterator[_S]:
            return cymap(func, iterable, *iterables, strict=strict)
    else:
        @staticmethod
        @overload
        def __call__(
                func: Callable[[_T1], _S],
                iterable: Iterable[_T1],
                /,
                ) -> Iterable[_S]: ...
        @staticmethod
        @overload
        def __call__(
                func: Callable[[_T1, _T2], _S],
                iterable: Iterable[_T1],
                iter2: Iterable[_T2],
                /,
                ) -> Iterable[_S]: ...
        @staticmethod
        @overload
        def __call__(
                func: Callable[[_T1, _T2, _T3], _S],
                iterable: Iterable[_T1],
                iter2: Iterable[_T2],
                iter3: Iterable[_T3],
                /,
                ) -> Iterable[_S]: ...
        @staticmethod
        @overload
        def __call__(
                func: Callable[[_T1, _T2, _T3, _T4], _S],
                iterable: Iterable[_T1],
                iter2: Iterable[_T2],
                iter3: Iterable[_T3],
                iter4: Iterable[_T4],
                /,
                ) -> Iterable[_S]: ...
        @staticmethod
        @overload
        def __call__(
                func: Callable[[_T1, _T2, _T3, _T4, _T5], _S],
                iterable: Iterable[_T1],
                iter2: Iterable[_T2],
                iter3: Iterable[_T3],
                iter4: Iterable[_T4],
                iter5: Iterable[_T5],
                /,
                ) -> Iterable[_S]: ...
        @staticmethod
        @override
        def __call__(  # pyright: ignore[reportInconsistentOverload]
                func: Callable[..., _S],
                iterable: Iterable[Any],  # pyright: ignore[reportExplicitAny, reportUnnecessaryTypeIgnoreComment]
                /,
                *iterables: Iterable[Any],  # pyright: ignore[reportExplicitAny, reportUnnecessaryTypeIgnoreComment]
                ) -> Iterator[_S]:
            return cymap(func, iterable, *iterables)

class _map(metaclass=_map_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    Make an iterator that computes the function using arguments from
    each of the iterables.  Stops when the shortest iterable is exhausted.

    If strict is true and one of the arguments is exhausted before the others,
    raise a ValueError.

    Has a curried version as the property c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curryv(2)(_map_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]

map = _map  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = [
        "map",
        ]
