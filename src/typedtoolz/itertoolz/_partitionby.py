# TODO: Review msc impl
from collections.abc import Callable, Iterable, Iterator
from typing import TypeVar
from typing_extensions import override
from cytoolz.recipes import partitionby as _partitionby
from typedtoolz.functoolz._curry import curry

T = TypeVar('T')


class _partitionby_meta(type):
    @staticmethod
    @override
    def __call__(func: Callable[[T], object], seq: Iterable[T]) -> Iterator[tuple[T, ...]]:
        return _partitionby(func, seq)


class _partitionby(metaclass=_partitionby_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    partitionby(func, seq) -> Iterator[tuple]

    Partition a sequence according to a function.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _partitionby_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


partitionby = _partitionby  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["partitionby"]
