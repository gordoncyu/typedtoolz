from collections.abc import Callable, Mapping
from typing import TypeVar
from typing_extensions import override
from cytoolz.dicttoolz import merge as cymerge, merge_with as cymerge_with  # pyright: ignore[reportUnknownVariableType]
from typedtoolz.functoolz._curryv import curryv

K = TypeVar('K')
V = TypeVar('V')
W = TypeVar('W')


class _merge_meta(type):
    @staticmethod
    @override
    def __call__(*dicts: Mapping[K, V]) -> dict[K, V]:
        return cymerge(*dicts)  # pyright: ignore[reportUnknownVariableType]


class _merge(metaclass=_merge_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    merge(*dicts) -> dict

    Merge a collection of dictionaries.
    """

# TODO: Consider making more useful for currying with a variant that requires at least 2 dicts
merge = _merge  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

class _merge_with_meta(type):
    @staticmethod
    @override
    def __call__(func: Callable[[list[V]], W], *dicts: Mapping[K, V]) -> dict[K, W]:
        return cymerge_with(func, *dicts)  # pyright: ignore[reportUnknownVariableType]


class _merge_with(metaclass=_merge_with_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    merge_with(func, *dicts) -> dict

    Merge dictionaries and apply func to combine values for common keys.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curryv(2, _merge_with_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


# TODO: Consider making more useful for currying with a variant that requires at least 2 dicts
merge_with = _merge_with  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["merge", "merge_with"]
