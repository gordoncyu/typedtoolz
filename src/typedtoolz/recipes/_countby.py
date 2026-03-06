from collections.abc import Callable, Iterable
from typing import TypeVar
from typing_extensions import override
from cytoolz.recipes import countby as cycountby  # pyright: ignore[reportUnknownVariableType]
from typedtoolz.functoolz._curry import curry

T = TypeVar('T')
K = TypeVar('K')


class _countby_meta(type):
    @staticmethod
    @override
    def __call__(key: Callable[[T], K], seq: Iterable[T]) -> dict[K, int]:
        return cycountby(key, seq)  # pyright: ignore[reportUnknownVariableType]


class _countby(metaclass=_countby_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    countby(key, seq) -> dict

    Count elements of a collection by a key function.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _countby_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


countby = _countby  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["countby"]
