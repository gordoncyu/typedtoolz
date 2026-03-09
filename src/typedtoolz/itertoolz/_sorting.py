from collections.abc import Callable, Iterable
from typing import TypeVar, cast
from typing_extensions import override
from cytoolz.itertoolz import merge_sorted as cymerge_sorted, topk as cytopk  # pyright: ignore[reportUnknownVariableType]
from typedtoolz.functoolz._curry import curry

T = TypeVar('T')

_missing = object()


class _merge_sorted_meta(type):
    @staticmethod
    @override
    def __call__(*seqs: Iterable[T], key: Callable[[T], object] = cast(Callable[[T], object], _missing)) -> Iterable[T]:  # pyright: ignore[reportCallInDefaultInitializer]
        if key is _missing:
            return cymerge_sorted(*seqs)  # pyright: ignore[reportUnknownVariableType]
        return cymerge_sorted(*seqs, key=key)  # pyright: ignore[reportUnknownVariableType]


class _merge_sorted(metaclass=_merge_sorted_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    merge_sorted(*seqs, key=None) -> Iterable

    Merge sorted sequences together.
    """


merge_sorted = _merge_sorted  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _topk_meta(type):
    @staticmethod
    @override
    def __call__(k: int, seq: Iterable[T], key: Callable[[T], object] = cast(Callable[[T], object], _missing)) -> list[T]:  # pyright: ignore[reportCallInDefaultInitializer]
        if key is _missing:
            return cytopk(k, seq)  # pyright: ignore[reportUnknownVariableType]
        return cytopk(k, seq, key)  # pyright: ignore[reportUnknownVariableType]

    @staticmethod
    def _call_key(key: Callable[[T], object], k: int, seq: Iterable[T]) -> list[T]:
        return cytopk(k, seq, key)  # pyright: ignore[reportUnknownVariableType]


class _topk(metaclass=_topk_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    topk(k, seq, key=None) -> list

    Find the k largest elements of a sequence.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2)(_topk_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]
    ck = curry(3)(_topk_meta._call_key)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]


topk = _topk  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["merge_sorted", "topk"]
