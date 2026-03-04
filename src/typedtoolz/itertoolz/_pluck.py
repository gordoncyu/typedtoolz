# TODO: Review msc impl
from collections.abc import Iterable, Iterator, Mapping, Sequence
from typing import TypeVar, cast
from typing_extensions import override, overload
from cytoolz.itertoolz import pluck as _pluck
from typedtoolz.functoolz._curry import curry

T = TypeVar('T')
D = TypeVar('D')
K = TypeVar('K')
V = TypeVar('V')

_missing = object()


class _pluck_meta(type):
    @classmethod
    @overload
    def __call__(cls, ind: int, seqs: Iterable[Sequence[T]]) -> Iterator[T]: ...
    @classmethod
    @overload
    def __call__(cls, ind: int, seqs: Iterable[Sequence[T]], default: D) -> Iterator[T | D]: ...
    @classmethod
    @overload
    def __call__(cls, ind: K, seqs: Iterable[Mapping[K, V]]) -> Iterator[V]: ...
    @classmethod
    @overload
    def __call__(cls, ind: K, seqs: Iterable[Mapping[K, V]], default: D) -> Iterator[V | D]: ...
    @classmethod
    @override
    def __call__(cls, ind: int | K, seqs: Iterable[Sequence[T]] | Iterable[Mapping[K, V]], default: D = cast(D, _missing)) -> Iterator[T | V | D]:  # pyright: ignore[reportCallInDefaultInitializer, reportInconsistentOverload]
        if default is _missing:
            return _pluck(ind, seqs)  # type: ignore[arg-type, return-value]
        return _pluck(ind, seqs, default)  # type: ignore[arg-type, return-value]


class _pluck(metaclass=_pluck_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    pluck(ind, seqs[, default]) -> Iterator

    Pluck an element from each item in a sequence.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _pluck_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


pluck = _pluck  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["pluck"]
