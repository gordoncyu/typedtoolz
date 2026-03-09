from collections.abc import Iterable, Iterator, Mapping, Sequence
from typing import TypeVar, cast
from typing_extensions import override, overload
from cytoolz.itertoolz import pluck as cypluck  # pyright: ignore[reportUnknownVariableType]
from typedtoolz.functoolz._curry import curry
from typedtoolz.utils import no_default

T = TypeVar('T')
D = TypeVar('D')
K = TypeVar('K')
V = TypeVar('V')


class _pluck_meta(type):
    @staticmethod
    @overload
    def __call__(ind: int, seqs: Iterable[Sequence[T]]) -> Iterator[T]: ...
    @staticmethod
    @overload
    def __call__(ind: int, seqs: Iterable[Sequence[T]], default: D) -> Iterator[T | D]: ...
    @staticmethod
    @overload
    def __call__(ind: K, seqs: Iterable[Mapping[K, V]]) -> Iterator[V]: ...
    @staticmethod
    @overload
    def __call__(ind: K, seqs: Iterable[Mapping[K, V]], default: D) -> Iterator[V | D]: ...
    @staticmethod
    @override
    def __call__(ind: int | K, seqs: Iterable[Sequence[T]] | Iterable[Mapping[K, V]], default: D = cast(D, no_default)) -> Iterator[T | V | D]:  # pyright: ignore[reportCallInDefaultInitializer]
        if default is no_default:
            return cypluck(ind, seqs)  # type: ignore[arg-type, return-value]  # pyright: ignore[reportUnknownVariableType]
        return cypluck(ind, seqs, default)  # type: ignore[arg-type, return-value]  # pyright: ignore[reportUnknownVariableType]

    @staticmethod
    def _call_default(default: D, ind: int, seqs: Iterable[Sequence[T]]) -> Iterator[T | D]:
        return cypluck(ind, seqs, default)  # pyright: ignore[reportUnknownVariableType]

    @staticmethod
    def _call_mapping(ind: K, seqs: Iterable[Mapping[K, V]]) -> Iterator[V]:
        return cypluck(ind, seqs)  # pyright: ignore[reportUnknownVariableType]
    @staticmethod
    def _call_mapping_default(default: D, ind: K, seqs: Iterable[Mapping[K, V]]) -> Iterator[V | D]:
        return cypluck(ind, seqs, default)  # pyright: ignore[reportUnknownVariableType]


class _pluck(metaclass=_pluck_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    pluck(ind, seqs[, default]) -> Iterator

    Pluck an element from each item in a sequence.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2)(_pluck_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]
    cd = curry(3)(_pluck_meta._call_default)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]

    cm = curry(2)(_pluck_meta._call_mapping)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]
    cmd = curry(3)(_pluck_meta._call_mapping_default)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]


pluck = _pluck  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["pluck"]
