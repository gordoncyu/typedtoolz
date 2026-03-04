# TODO: Review msc impl
from collections.abc import Callable, Iterable, Iterator
from typing import TypeVar, cast
from typing_extensions import override, overload
from cytoolz.itertoolz import (
    remove as _remove, accumulate as _accumulate, cons as _cons,
    interpose as _interpose, interleave as _interleave, iterate as _iterate,
    concat as _concat, concatv as _concatv, mapcat as _mapcat,
)
from typedtoolz.functoolz._curry import curry

T = TypeVar('T')
A = TypeVar('A')
R = TypeVar('R')

_missing = object()


class _remove_meta(type):
    @classmethod
    @override
    def __call__(cls, predicate: Callable[[T], object], seq: Iterable[T]) -> Iterator[T]:
        return _remove(predicate, seq)


class _remove(metaclass=_remove_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    remove(predicate, seq) -> Iterator

    Return elements of seq for which predicate is False.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _remove_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


remove = _remove  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _accumulate_meta(type):
    @classmethod
    @overload
    def __call__(cls, binop: Callable[[T, T], T], seq: Iterable[T]) -> Iterator[T]: ...
    @classmethod
    @overload
    def __call__(cls, binop: Callable[[A, T], A], seq: Iterable[T], initial: A) -> Iterator[A]: ...
    @classmethod
    @override
    def __call__(cls, binop: Callable[[A, T], A], seq: Iterable[T], initial: A = cast(A, _missing)) -> Iterator[A]:  # pyright: ignore[reportCallInDefaultInitializer, reportInconsistentOverload]
        if initial is _missing:
            return _accumulate(binop, seq)  # type: ignore[arg-type, return-value]
        return _accumulate(binop, seq, initial)  # type: ignore[arg-type]


class _accumulate(metaclass=_accumulate_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    accumulate(binop, seq[, initial]) -> Iterator

    Repeatedly apply a binary function to a sequence, accumulating results.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _accumulate_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


accumulate = _accumulate  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _cons_meta(type):
    @classmethod
    @override
    def __call__(cls, el: T, seq: Iterable[T]) -> Iterator[T]:
        return _cons(el, seq)


class _cons(metaclass=_cons_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    cons(el, seq) -> Iterator

    Add el to the beginning of seq.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _cons_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


cons = _cons  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _interpose_meta(type):
    @classmethod
    @override
    def __call__(cls, el: T, seq: Iterable[T]) -> Iterator[T]:
        return _interpose(el, seq)


class _interpose(metaclass=_interpose_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    interpose(el, seq) -> Iterator

    Introduce el between each pair of elements in seq.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _interpose_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


interpose = _interpose  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _interleave_meta(type):
    @classmethod
    @override
    def __call__(cls, seqs: Iterable[Iterable[T]]) -> Iterable[T]:
        return _interleave(seqs)


class _interleave(metaclass=_interleave_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    interleave(seqs) -> Iterable

    Interleave multiple sequences into one.
    """


interleave = _interleave  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _iterate_meta(type):
    @classmethod
    @override
    def __call__(cls, func: Callable[[T], T], x: T) -> Iterator[T]:
        return _iterate(func, x)


class _iterate(metaclass=_iterate_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    iterate(func, x) -> Iterator

    Repeatedly apply func to x, yielding each result.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _iterate_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


iterate = _iterate  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _concat_meta(type):
    @classmethod
    @override
    def __call__(cls, seqs: Iterable[Iterable[T]]) -> Iterator[T]:
        return _concat(seqs)


class _concat(metaclass=_concat_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    concat(seqs) -> Iterator

    Concatenate zero or more iterables.
    """


concat = _concat  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _concatv_meta(type):
    @classmethod
    @override
    def __call__(cls, *seqs: Iterable[T]) -> Iterator[T]:
        return _concatv(*seqs)


class _concatv(metaclass=_concatv_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    concatv(*seqs) -> Iterator

    Variadic version of concat.
    """


concatv = _concatv  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _mapcat_meta(type):
    @classmethod
    @override
    def __call__(cls, func: Callable[[T], Iterable[R]], seqs: Iterable[T]) -> Iterator[R]:
        return _mapcat(func, seqs)


class _mapcat(metaclass=_mapcat_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    mapcat(func, seqs) -> Iterator

    Apply func to each element of seqs, then concatenate results.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _mapcat_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


mapcat = _mapcat  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = [
    "remove", "accumulate", "cons", "interpose", "interleave",
    "iterate", "concat", "concatv", "mapcat",
]
