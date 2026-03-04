# TODO: Review msc impl
from collections.abc import Iterable, Iterator
from typing import Literal, TypeVar, TypeVarTuple
from typing_extensions import override, overload
from cytoolz.itertoolz import first as _first, second as _second, nth as _nth, last as _last, rest as _rest, peek as _peek, peekn as _peekn
from typedtoolz.functoolz._curry import curry

T = TypeVar('T')
A1 = TypeVar('A1')
A2 = TypeVar('A2')
A3 = TypeVar('A3')
A4 = TypeVar('A4')
A5 = TypeVar('A5')
A6 = TypeVar('A6')
A7 = TypeVar('A7')
A8 = TypeVar('A8')
A9 = TypeVar('A9')
A10 = TypeVar('A10')
Ts = TypeVarTuple('Ts')


class _nth_meta(type):
    @classmethod
    @overload
    def __call__(cls, n: Literal[0], seq: tuple[A1, *Ts]) -> A1: ...
    @classmethod
    @overload
    def __call__(cls, n: Literal[1], seq: tuple[A1, A2, *Ts]) -> A2: ...
    @classmethod
    @overload
    def __call__(cls, n: Literal[2], seq: tuple[A1, A2, A3, *Ts]) -> A3: ...
    @classmethod
    @overload
    def __call__(cls, n: Literal[3], seq: tuple[A1, A2, A3, A4, *Ts]) -> A4: ...
    @classmethod
    @overload
    def __call__(cls, n: Literal[4], seq: tuple[A1, A2, A3, A4, A5, *Ts]) -> A5: ...
    @classmethod
    @overload
    def __call__(cls, n: Literal[5], seq: tuple[A1, A2, A3, A4, A5, A6, *Ts]) -> A6: ...
    @classmethod
    @overload
    def __call__(cls, n: Literal[6], seq: tuple[A1, A2, A3, A4, A5, A6, A7, *Ts]) -> A7: ...
    @classmethod
    @overload
    def __call__(cls, n: Literal[7], seq: tuple[A1, A2, A3, A4, A5, A6, A7, A8, *Ts]) -> A8: ...
    @classmethod
    @overload
    def __call__(cls, n: Literal[8], seq: tuple[A1, A2, A3, A4, A5, A6, A7, A8, A9, *Ts]) -> A9: ...
    @classmethod
    @overload
    def __call__(cls, n: Literal[9], seq: tuple[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, *Ts]) -> A10: ...
    @classmethod
    @overload
    def __call__(cls, n: int, seq: Iterable[T]) -> T: ...
    @classmethod
    @override
    def __call__(cls, n: int, seq: Iterable[T]) -> T:  # pyright: ignore[reportInconsistentOverload]
        return _nth(n, seq)  # type: ignore[return-value]


class _nth(metaclass=_nth_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    nth(n, seq) -> element

    The nth element of a sequence.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _nth_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


nth = _nth  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _first_meta(type):
    @classmethod
    @overload
    def __call__(cls, seq: tuple[T, *Ts]) -> T: ...
    @classmethod
    @overload
    def __call__(cls, seq: Iterable[T]) -> T: ...
    @classmethod
    @override
    def __call__(cls, seq: Iterable[T]) -> T:  # pyright: ignore[reportInconsistentOverload]
        return _first(seq)


class _first(metaclass=_first_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    first(seq) -> element

    The first element of a sequence.
    """


first = _first  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _second_meta(type):
    @classmethod
    @overload
    def __call__(cls, seq: tuple[A1, T, *Ts]) -> T: ...
    @classmethod
    @overload
    def __call__(cls, seq: Iterable[T]) -> T: ...
    @classmethod
    @override
    def __call__(cls, seq: Iterable[T]) -> T:  # pyright: ignore[reportInconsistentOverload]
        return _second(seq)


class _second(metaclass=_second_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    second(seq) -> element

    The second element of a sequence.
    """


second = _second  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _last_meta(type):
    @classmethod
    @overload
    def __call__(cls, seq: tuple[*Ts, T]) -> T: ...
    @classmethod
    @overload
    def __call__(cls, seq: Iterable[T]) -> T: ...
    @classmethod
    @override
    def __call__(cls, seq: Iterable[T]) -> T:  # pyright: ignore[reportInconsistentOverload]
        return _last(seq)


class _last(metaclass=_last_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    last(seq) -> element

    The last element of a sequence.
    """


last = _last  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _rest_meta(type):
    @classmethod
    @override
    def __call__(cls, seq: Iterable[T]) -> Iterator[T]:
        return _rest(seq)


class _rest(metaclass=_rest_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    rest(seq) -> Iterator

    All elements of seq except the first.
    """


rest = _rest  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _peek_meta(type):
    @classmethod
    @override
    def __call__(cls, seq: Iterable[T]) -> tuple[T, Iterator[T]]:
        return _peek(seq)


class _peek(metaclass=_peek_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    peek(seq) -> (first, seq)

    Retrieve the first element of a sequence while retaining the original.
    """


peek = _peek  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _peekn_meta(type):
    @classmethod
    @override
    def __call__(cls, n: int, seq: Iterable[T]) -> tuple[list[T], Iterator[T]]:
        return _peekn(n, seq)


class _peekn(metaclass=_peekn_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    peekn(n, seq) -> (first_n, seq)

    Retrieve the first n elements of a sequence while retaining the original.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _peekn_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


peekn = _peekn  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["first", "second", "nth", "last", "rest", "peek", "peekn"]
