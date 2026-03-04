# TODO: Review msc impl
from collections.abc import Callable, Iterable
from typing import TypeVar, cast
from typing_extensions import override, overload
from toolz.sandbox.parallel import fold as _fold
from typedtoolz.functoolz._curry import curry

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
            return _fold(binop, seq, **kwargs)  # type: ignore[arg-type, return-value]
        return _fold(binop, seq, default, **kwargs)  # type: ignore[arg-type]


class _fold(metaclass=_fold_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    fold(binop, seq[, default], map=map, chunksize=8, combine=None) -> value

    Reduce without order using a binary operator (supports parallel execution).

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _fold_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


fold = _fold  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["fold"]
