# TODO: Review msc impl
from collections.abc import Callable, Iterable
from typing import TypeVar, cast
from typing_extensions import override, overload
from cytoolz.itertoolz import groupby as cygroupby, reduceby as cyreduceby, frequencies as cyfrequencies  # pyright: ignore[reportUnknownVariableType]
from cytoolz.recipes import countby as cycountby  # pyright: ignore[reportUnknownVariableType]
from typedtoolz.functoolz._curry import curry

T = TypeVar('T')
K = TypeVar('K')
A = TypeVar('A')

_missing = object()


class _groupby_meta(type):
    @staticmethod
    @override
    def __call__(key: Callable[[T], K], seq: Iterable[T]) -> dict[K, list[T]]:
        return cygroupby(key, seq)  # pyright: ignore[reportUnknownVariableType]


class _groupby(metaclass=_groupby_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    groupby(key, seq) -> dict

    Group a collection by a key function.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _groupby_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


groupby = _groupby  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _reduceby_meta(type):
    @staticmethod
    @overload
    def __call__(key: Callable[[T], K], binop: Callable[[T, T], T], seq: Iterable[T]) -> dict[K, T]: ...
    @staticmethod
    @overload
    def __call__(key: Callable[[T], K], binop: Callable[[A, T], A], seq: Iterable[T], init: Callable[[], A] | A = ...) -> dict[K, A]: ...
    @staticmethod
    @override
    def __call__(key: Callable[[T], K], binop: Callable[[A, T], A], seq: Iterable[T], init: Callable[[], A] | A = cast(Callable[[], A] | A, _missing)) -> dict[K, A]:  # pyright: ignore[reportCallInDefaultInitializer]
        if init is _missing:
            return cyreduceby(key, binop, seq)  # pyright: ignore[reportUnknownVariableType]
        return cyreduceby(key, binop, seq, init)  # pyright: ignore[reportUnknownVariableType]
    @staticmethod

    def _call_default(key: Callable[[T], K], init: Callable[[], A] | A, binop: Callable[[A, T], A], seq: Iterable[T]) -> dict[K, A]:
        return cyreduceby(key, binop, seq, init)  # pyright: ignore[reportUnknownVariableType]


class _reduceby(metaclass=_reduceby_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    reduceby(key, binop, seq[, init]) -> dict

    Perform a simultaneous groupby and reduction.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(3, _reduceby_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]
    ci = curry(4, _reduceby_meta._call_default)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]


reduceby = _reduceby  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _frequencies_meta(type):
    @staticmethod
    @override
    def __call__(seq: Iterable[T]) -> dict[T, int]:
        return cyfrequencies(seq)  # pyright: ignore[reportUnknownVariableType]


class _frequencies(metaclass=_frequencies_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    frequencies(seq) -> dict

    Find the number of occurrences of each element in a sequence.
    """


frequencies = _frequencies  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


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

__all__ = ["groupby", "reduceby", "frequencies", "countby"]
