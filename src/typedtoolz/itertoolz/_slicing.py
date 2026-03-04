# TODO: Review msc impl
from collections.abc import Iterable, Iterator
from typing import TypeVar
from typing_extensions import override
from cytoolz.itertoolz import take as _take, tail as _tail, drop as _drop, take_nth as _take_nth
from typedtoolz.functoolz._curry import curry

T = TypeVar('T')


class _take_meta(type):
    @staticmethod
    @override
    def __call__(n: int, seq: Iterable[T]) -> list[T]:
        return _take(n, seq)


class _take(metaclass=_take_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    take(n, seq) -> list

    The first n elements of a sequence.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _take_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


take = _take  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _tail_meta(type):
    @staticmethod
    @override
    def __call__(n: int, seq: Iterable[T]) -> list[T]:
        return _tail(n, seq)


class _tail(metaclass=_tail_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    tail(n, seq) -> list

    The last n elements of a sequence.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _tail_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


tail = _tail  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _drop_meta(type):
    @staticmethod
    @override
    def __call__(n: int, seq: Iterable[T]) -> Iterator[T]:
        return _drop(n, seq)


class _drop(metaclass=_drop_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    drop(n, seq) -> Iterator

    All elements of seq except the first n.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _drop_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


drop = _drop  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _take_nth_meta(type):
    @staticmethod
    @override
    def __call__(n: int, seq: Iterable[T]) -> Iterator[T]:
        return _take_nth(n, seq)


class _take_nth(metaclass=_take_nth_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    take_nth(n, seq) -> Iterator

    Every nth item in seq.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _take_nth_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


take_nth = _take_nth  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["take", "tail", "drop", "take_nth"]
