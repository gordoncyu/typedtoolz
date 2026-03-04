# TODO: Review msc impl
from collections.abc import Callable, Mapping
from typing import TypeVar
from typing_extensions import override
from cytoolz.dicttoolz import merge as _merge, merge_with as _merge_with
from typedtoolz.functoolz._curry import curry

K = TypeVar('K')
V = TypeVar('V')
W = TypeVar('W')


class _merge_meta(type):
    @classmethod
    @override
    def __call__(cls, *dicts: Mapping[K, V]) -> dict[K, V]:
        return _merge(*dicts)


class _merge(metaclass=_merge_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    merge(*dicts) -> dict

    Merge a collection of dictionaries.
    """


merge = _merge  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _merge_with_meta(type):
    @classmethod
    @override
    def __call__(cls, func: Callable[[list[V]], W], *dicts: Mapping[K, V]) -> dict[K, W]:
        return _merge_with(func, *dicts)


class _merge_with(metaclass=_merge_with_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    merge_with(func, *dicts) -> dict

    Merge dictionaries and apply func to combine values for common keys.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(1, _merge_with_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


merge_with = _merge_with  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["merge", "merge_with"]
