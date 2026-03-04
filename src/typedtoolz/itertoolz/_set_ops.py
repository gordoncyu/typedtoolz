# TODO: Review msc impl
from collections.abc import Callable, Iterable, Iterator
from typing import TypeVar, cast
from typing_extensions import override
from cytoolz.itertoolz import unique as _unique, diff as _diff, join as _join
from typedtoolz.functoolz._curry import curry

T = TypeVar('T')
K = TypeVar('K')
L = TypeVar('L')
R = TypeVar('R')

_missing = object()


class _unique_meta(type):
    @classmethod
    @override
    def __call__(cls, seq: Iterable[T], key: Callable[[T], object] = cast(Callable[[T], object], _missing)) -> Iterator[T]:  # pyright: ignore[reportCallInDefaultInitializer]
        if key is _missing:
            return _unique(seq)
        return _unique(seq, key=key)  # type: ignore[arg-type]


class _unique(metaclass=_unique_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    unique(seq, key=identity) -> Iterator

    Return only unique elements of a sequence.
    """


unique = _unique  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _diff_meta(type):
    @classmethod
    @override
    def __call__(cls, *seqs: Iterable[T], key: Callable[[T], object] = cast(Callable[[T], object], _missing), default: T = cast(T, _missing)) -> Iterator[tuple[T, ...]]:  # pyright: ignore[reportCallInDefaultInitializer]
        kwargs: dict[str, object] = {}
        if key is not _missing:
            kwargs['key'] = key
        if default is not _missing:
            kwargs['default'] = default
        return _diff(*seqs, **kwargs)  # type: ignore[arg-type]


class _diff(metaclass=_diff_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    diff(*seqs, key=identity, default=no_default) -> Iterator[tuple]

    Return those items that differ between sequences.
    """


diff = _diff  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _join_meta(type):
    @classmethod
    @override
    def __call__(
        cls,
        leftkey: Callable[[L], K],
        leftseq: Iterable[L],
        rightkey: Callable[[R], K],
        rightseq: Iterable[R],
        left_default: L = cast(L, _missing),
        right_default: R = cast(R, _missing),
    ) -> Iterator[tuple[L, R]]:  # pyright: ignore[reportCallInDefaultInitializer]
        kwargs: dict[str, object] = {}
        if left_default is not _missing:
            kwargs['left_default'] = left_default
        if right_default is not _missing:
            kwargs['right_default'] = right_default
        return _join(leftkey, leftseq, rightkey, rightseq, **kwargs)  # type: ignore[arg-type]


class _join(metaclass=_join_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    join(leftkey, leftseq, rightkey, rightseq, left_default=, right_default=) -> Iterator[tuple]

    Join two sequences on a common attribute.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(4, _join_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


join = _join  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["unique", "diff", "join"]
