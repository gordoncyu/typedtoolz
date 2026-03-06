from collections.abc import Callable, Iterable, Iterator
from typing import TypeVar, cast
from typing_extensions import override
from cytoolz.itertoolz import unique as cyunique, diff as cydiff, join as cyjoin  # pyright: ignore[reportUnknownVariableType]
from typedtoolz.functoolz._curry import curry
from typedtoolz.functoolz._curryv import curryv
from typedtoolz.utils import no_default

T = TypeVar('T')
K = TypeVar('K')
L = TypeVar('L')
R = TypeVar('R')

_missing = object()  # used for optional key/predicate args (not the no_default API)


class _unique_meta(type):
    @staticmethod
    @override
    def __call__(seq: Iterable[T], key: Callable[[T], object] = cast(Callable[[T], object], _missing)) -> Iterator[T]:  # pyright: ignore[reportCallInDefaultInitializer]
        if key is _missing:
            return cyunique(seq)  # pyright: ignore[reportUnknownVariableType]
        return cyunique(seq, key=key)  # type: ignore[arg-type]  # pyright: ignore[reportUnknownVariableType]

    @staticmethod
    def _call_key(key: Callable[[T], object], seq: Iterable[T]) -> Iterator[T]:
        return cyunique(seq, key)  # type: ignore[arg-type]  # pyright: ignore[reportUnknownVariableType]


class _unique(metaclass=_unique_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    unique(seq, key=identity) -> Iterator

    Return only unique elements of a sequence.
    """
    c = curry(1, _unique_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]
    ck = curry(2, _unique_meta._call_key)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]

unique = _unique  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _diff_meta(type):
    @staticmethod
    @override
    def __call__(
            *seqs: Iterable[T],
            key: Callable[[T], object] = cast(Callable[[T], object], _missing),  # pyright: ignore[reportCallInDefaultInitializer]
            default: T = cast(T, no_default),  # pyright: ignore[reportCallInDefaultInitializer]
            ) -> Iterator[tuple[T, ...]]:
        kwargs: dict[str, object] = {}
        if key is not _missing:
            kwargs['key'] = key
        if default is not no_default:
            kwargs['default'] = default
        return cydiff(*seqs, **kwargs)  # pyright: ignore[reportUnknownVariableType]

    @staticmethod
    def _call(
            *seqs: Iterable[T],
            ) -> Iterator[tuple[T, ...]]:
        return cydiff(*seqs)  # pyright: ignore[reportUnknownVariableType]
    @staticmethod
    def _call_default(
            default: T,
            *seqs: Iterable[T],
            ) -> Iterator[tuple[T, ...]]:
        return cydiff(*seqs, default=default)  # pyright: ignore[reportUnknownVariableType]
    @staticmethod
    def _call_key(
            key: Callable[[T], object],
            *seqs: Iterable[T],
            ) -> Iterator[tuple[T, ...]]:
        return cydiff(*seqs, key=key)  # pyright: ignore[reportUnknownVariableType]
    @staticmethod
    def _call_default_key(
            default: T,
            key: Callable[[T], object],
            *seqs: Iterable[T],
            ) -> Iterator[tuple[T, ...]]:
        return cydiff(*seqs, default=default, key=key)  # pyright: ignore[reportUnknownVariableType]

class _diff(metaclass=_diff_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    diff(*seqs, key=identity, default=no_default) -> Iterator[tuple]

    Return those items that differ between sequences.
    """
    c = curryv(1, _diff_meta._call)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]
    cd = curryv(2, _diff_meta._call_default)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]
    ck = curryv(2, _diff_meta._call_key)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]
    cdk = curryv(3, _diff_meta._call_default_key)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]

diff = _diff  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _join_meta(type):
    @staticmethod
    @override
    def __call__(
        leftkey: Callable[[L], K],
        leftseq: Iterable[L],
        rightkey: Callable[[R], K],
        rightseq: Iterable[R],
        left_default: L = cast(L, no_default),  # pyright: ignore[reportCallInDefaultInitializer]
        right_default: R = cast(R, no_default),  # pyright: ignore[reportCallInDefaultInitializer]
    ) -> Iterator[tuple[L, R]]:
        kwargs: dict[str, object] = {}
        if left_default is not no_default:
            kwargs['left_default'] = left_default
        if right_default is not no_default:
            kwargs['right_default'] = right_default
        return cyjoin(leftkey, leftseq, rightkey, rightseq, **kwargs)  # pyright: ignore[reportUnknownVariableType]

    @staticmethod
    def _call_left_default(
        leftkey: Callable[[L], K],
        rightkey: Callable[[R], K],
        left_default: L,
        leftseq: Iterable[L],
        rightseq: Iterable[R],
    ) -> Iterator[tuple[L, R]]:
        return cyjoin(leftkey, leftseq, rightkey, rightseq, left_default)  # pyright: ignore[reportUnknownVariableType]
    @staticmethod
    def _call_right_default(
        leftkey: Callable[[L], K],
        rightkey: Callable[[R], K],
        right_default: R,
        leftseq: Iterable[L],
        rightseq: Iterable[R],
    ) -> Iterator[tuple[L, R]]:
        return cyjoin(leftkey, leftseq, rightkey, rightseq, right_default=right_default)  # pyright: ignore[reportUnknownVariableType]
    @staticmethod
    def _call_default(
        leftkey: Callable[[L], K],
        rightkey: Callable[[R], K],
        left_default: L,
        right_default: R,
        leftseq: Iterable[L],
        rightseq: Iterable[R],
    ) -> Iterator[tuple[L, R]]:
        return cyjoin(leftkey, leftseq, rightkey, rightseq, left_default, right_default)  # pyright: ignore[reportUnknownVariableType]

class _join(metaclass=_join_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    join(leftkey, leftseq, rightkey, rightseq, left_default=, right_default=) -> Iterator[tuple]

    Join two sequences on a common attribute.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(4, _join_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]
    cd = curry(6, _join_meta._call_default)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]
    cld = curry(5, _join_meta._call_left_default)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]
    crd = curry(5, _join_meta._call_right_default)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]


join = _join  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["unique", "diff", "join"]
