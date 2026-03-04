# TODO: Review msc impl
from collections.abc import Callable, Iterable
from typing import TypeVar, cast
from typing_extensions import override
from cytoolz.itertoolz import merge_sorted as _merge_sorted, topk as _topk
from typedtoolz.functoolz._curry import curry

T = TypeVar('T')

_missing = object()


class _merge_sorted_meta(type):
    @classmethod
    @override
    def __call__(cls, *seqs: Iterable[T], key: Callable[[T], object] = cast(Callable[[T], object], _missing)) -> Iterable[T]:  # pyright: ignore[reportCallInDefaultInitializer]
        if key is _missing:
            return _merge_sorted(*seqs)
        return _merge_sorted(*seqs, key=key)  # type: ignore[arg-type]


class _merge_sorted(metaclass=_merge_sorted_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    merge_sorted(*seqs, key=None) -> Iterable

    Merge sorted sequences together.
    """


merge_sorted = _merge_sorted  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _topk_meta(type):
    @classmethod
    @override
    def __call__(cls, k: int, seq: Iterable[T], key: Callable[[T], object] = cast(Callable[[T], object], _missing)) -> list[T]:  # pyright: ignore[reportCallInDefaultInitializer]
        if key is _missing:
            return _topk(k, seq)
        return _topk(k, seq, key=key)  # type: ignore[arg-type]


class _topk(metaclass=_topk_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    topk(k, seq, key=None) -> list

    Find the k largest elements of a sequence.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _topk_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


topk = _topk  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["merge_sorted", "topk"]
