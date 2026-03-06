from collections.abc import Callable, Iterable
from typing import TypeVar, cast
from typing_extensions import override, overload
from toolz.sandbox.parallel import fold as tz_fold  # pyright: ignore[reportUnknownVariableType]
from typedtoolz.functoolz._curryv import curryv

T = TypeVar('T')
A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

_missing = object()


class _fold_meta(type):
    @staticmethod
    @overload
    def __call__(
        binop: Callable[[T, T], T],
        seq: Iterable[T],
        *,
        map: Callable[[Callable[[B], C], Iterable[B]], Iterable[C]] = ...,
        chunksize: int = ...,
        combine: Callable[[T, T], T] | None = ...,
    ) -> T: ...
    @staticmethod
    @overload
    def __call__(
        binop: Callable[[A, T], A],
        seq: Iterable[T],
        default: A,
        map: Callable[[Callable[[B], C], Iterable[B]], Iterable[C]] = ...,
        chunksize: int = ...,
        combine: Callable[[A, A], A] | None = ...,
    ) -> A: ...
    @staticmethod
    @override
    def __call__(binop: Callable[[A, T], A], seq: Iterable[T], default: A = cast(A, _missing), **kwargs: object) -> A:  # pyright: ignore[reportCallInDefaultInitializer, reportInconsistentOverload]
        if default is _missing:
            return tz_fold(binop, seq, **kwargs)  # pyright: ignore[reportUnknownVariableType, reportArgumentType]
        return tz_fold(binop, seq, default, **kwargs)  # pyright: ignore[reportArgumentType, reportUnknownVariableType]

    @staticmethod
    def _call(
        binop: Callable[[T, T], T],
        seq: Iterable[T],
        map: Callable[[Callable[[B], C], Iterable[B]], Iterable[C]] = map,
        chunksize: int = 128
    ) -> T:
        return tz_fold(binop, seq, map=map, chunksize=chunksize)  # pyright: ignore[reportReturnType, reportUnknownVariableType, reportArgumentType]
    @staticmethod
    def _call_default(
        binop: Callable[[A, T], A],
        default: A,
        seq: Iterable[T],
        map: Callable[[Callable[[B], C], Iterable[B]], Iterable[C]] = map,
        chunksize: int = 128,
    ) -> A:
        return tz_fold(binop, seq, default, map, chunksize, None)  # pyright: ignore[reportReturnType, reportUnknownVariableType, reportArgumentType]
    @staticmethod
    def _call_combine(
        binop: Callable[[T, T], T],
        combine: Callable[[T, T], T] | None,
        seq: Iterable[T],
        map: Callable[[Callable[[B], C], Iterable[B]], Iterable[C]] = map,
        chunksize: int = 128,
    ) -> T:
        return tz_fold(binop, seq, map=map, chunksize=chunksize, combine=combine)  # pyright: ignore[reportReturnType, reportUnknownVariableType, reportArgumentType]
    @staticmethod
    def _call_combine_default(
        binop: Callable[[A, T], A],
        combine: Callable[[A, A], A] | None,
        default: A,
        seq: Iterable[T],
        map: Callable[[Callable[[B], C], Iterable[B]], Iterable[C]] = map,
        chunksize: int = 128,
    ) -> A:
        return tz_fold(binop, seq, default, map, chunksize, combine)  # pyright: ignore[reportReturnType, reportUnknownVariableType, reportArgumentType]


class _fold(metaclass=_fold_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    fold(binop, seq[, default], map=map, chunksize=8, combine=None) -> value

    Reduce without order using a binary operator (supports parallel execution).

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curryv(2, _fold_meta._call)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]
    cd = curryv(3, _fold_meta._call_default)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]
    cc = curryv(3, _fold_meta._call_combine)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]
    ccd = curryv(4, _fold_meta._call_combine_default)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]


fold = _fold  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["fold"]
