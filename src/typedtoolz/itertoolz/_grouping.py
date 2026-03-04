# TODO: Review msc impl
from collections.abc import Callable, Iterable
from typing import TypeVar, cast
from typing_extensions import override, overload
from cytoolz.itertoolz import groupby as _groupby, reduceby as _reduceby, frequencies as _frequencies
from cytoolz.recipes import countby as _countby
from typedtoolz.functoolz._curry import curry

T = TypeVar('T')
K = TypeVar('K')
A = TypeVar('A')

_missing = object()


class _groupby_meta(type):
    @classmethod
    @override
    def __call__(cls, key: Callable[[T], K], seq: Iterable[T]) -> dict[K, list[T]]:
        return _groupby(key, seq)


class _groupby(metaclass=_groupby_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    groupby(key, seq) -> dict

    Group a collection by a key function.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _groupby_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


groupby = _groupby  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _reduceby_meta(type):
    @classmethod
    @overload
    def __call__(cls, key: Callable[[T], K], binop: Callable[[T, T], T], seq: Iterable[T]) -> dict[K, T]: ...
    @classmethod
    @overload
    def __call__(cls, key: Callable[[T], K], binop: Callable[[A, T], A], seq: Iterable[T], init: Callable[[], A] | A = ...) -> dict[K, A]: ...
    @classmethod
    @override
    def __call__(cls, key: Callable[[T], K], binop: Callable[[A, T], A], seq: Iterable[T], init: Callable[[], A] | A = cast(Callable[[], A] | A, _missing)) -> dict[K, A]:  # pyright: ignore[reportCallInDefaultInitializer, reportInconsistentOverload]
        if init is _missing:
            return _reduceby(key, binop, seq)  # type: ignore[return-value, arg-type]
        return _reduceby(key, binop, seq, init)  # type: ignore[arg-type]


class _reduceby(metaclass=_reduceby_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    reduceby(key, binop, seq[, init]) -> dict

    Perform a simultaneous groupby and reduction.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(3, _reduceby_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


reduceby = _reduceby  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _frequencies_meta(type):
    @classmethod
    @override
    def __call__(cls, seq: Iterable[T]) -> dict[T, int]:
        return _frequencies(seq)


class _frequencies(metaclass=_frequencies_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    frequencies(seq) -> dict

    Find the number of occurrences of each element in a sequence.
    """


frequencies = _frequencies  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _countby_meta(type):
    @classmethod
    @override
    def __call__(cls, key: Callable[[T], K], seq: Iterable[T]) -> dict[K, int]:
        return _countby(key, seq)


class _countby(metaclass=_countby_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    countby(key, seq) -> dict

    Count elements of a collection by a key function.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _countby_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


countby = _countby  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["groupby", "reduceby", "frequencies", "countby"]
