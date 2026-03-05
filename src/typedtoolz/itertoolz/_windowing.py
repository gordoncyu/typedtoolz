from collections.abc import Iterable, Iterator
from typing import TypeVar, cast
from typing_extensions import override, overload
from cytoolz.itertoolz import sliding_window as cysliding_window, partition as cypartition, partition_all as cypartition_all  # pyright: ignore[reportUnknownVariableType]
from typedtoolz.functoolz._curry import curry

T = TypeVar('T')
D = TypeVar('D')

_missing = object()


class _sliding_window_meta(type):
    @staticmethod
    @override
    def __call__(n: int, seq: Iterable[T]) -> Iterator[tuple[T, ...]]:
        return cysliding_window(n, seq)  # pyright: ignore[reportUnknownVariableType]


class _sliding_window(metaclass=_sliding_window_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    sliding_window(n, seq) -> Iterator[tuple]

    A sequence of overlapping subsequences of length n.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _sliding_window_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


sliding_window = _sliding_window  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _partition_meta(type):
    @staticmethod
    @overload
    def __call__(n: int, seq: Iterable[T]) -> Iterator[tuple[T, ...]]: ...
    @staticmethod
    @overload
    def __call__(n: int, seq: Iterable[T], pad: D) -> Iterator[tuple[T | D, ...]]: ...
    @staticmethod
    @override
    def __call__(n: int, seq: Iterable[T], pad: D = cast(D, _missing)) -> Iterator[tuple[T | D, ...]]:  # pyright: ignore[reportCallInDefaultInitializer]
        if pad is _missing:
            return cypartition(n, seq)  # pyright: ignore[reportUnknownVariableType]
        return cypartition(n, seq, pad)  # type: ignore[arg-type]  # pyright: ignore[reportUnknownVariableType]
    @staticmethod
    def _call_pad(pad: D, n: int, seq: Iterable[T]) -> Iterator[tuple[T | D, ...]]:
        return cypartition(n, seq, pad)  # type: ignore[arg-type]  # pyright: ignore[reportUnknownVariableType]


class _partition(metaclass=_partition_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    partition(n, seq[, pad]) -> Iterator[tuple]

    Partition a sequence into tuples of length n.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _partition_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]
    cp = curry(3, _partition_meta._call_pad)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]


partition = _partition  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _partition_all_meta(type):
    @staticmethod
    @override
    def __call__(n: int, seq: Iterable[T]) -> Iterator[tuple[T, ...]]:
        return cypartition_all(n, seq)  # pyright: ignore[reportUnknownVariableType]


class _partition_all(metaclass=_partition_all_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    partition_all(n, seq) -> Iterator[tuple]

    Partition all elements of a sequence into tuples of at most length n.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _partition_all_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


partition_all = _partition_all  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["sliding_window", "partition", "partition_all"]
