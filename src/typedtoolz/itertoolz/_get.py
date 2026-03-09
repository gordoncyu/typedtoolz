# TODO: scriptify
from collections.abc import Mapping, Sequence
from typing import TypeVar, cast
from typing_extensions import override, overload
from cytoolz.itertoolz import get as cyget  # pyright: ignore[reportUnknownVariableType]
from typedtoolz.functoolz._curry import curry
from typedtoolz.utils import no_default

T = TypeVar('T')
D = TypeVar('D')
K = TypeVar('K')
V = TypeVar('V')


class _get_meta(type):
    @staticmethod
    @overload
    def __call__(ind: int, seq: Sequence[T]) -> T: ...
    @staticmethod
    @overload
    def __call__(ind: int, seq: Sequence[T], default: D) -> T | D: ...
    @staticmethod
    @overload
    def __call__(ind: list[int], seq: Sequence[T]) -> list[T]: ...
    @staticmethod
    @overload
    def __call__(ind: list[int], seq: Sequence[T], default: D) -> list[T | D]: ...
    @staticmethod
    @overload
    def __call__(ind: K, seq: Mapping[K, V]) -> V: ...
    @staticmethod
    @overload
    def __call__(ind: K, seq: Mapping[K, V], default: D) -> V | D: ...
    @staticmethod
    @override
    def __call__(ind: int | list[int] | K, seq: Sequence[T] | Mapping[K, V], default: D = cast(D, no_default)) -> T | list[T] | V | T | D:  # pyright: ignore[reportCallInDefaultInitializer]
        if default is no_default:
            return cyget(ind, seq)  # pyright: ignore[reportUnknownVariableType]
        return cyget(ind, seq, default)  # pyright: ignore[reportUnknownVariableType]

    @staticmethod
    def _call_ind_default(default: D, ind: int, seq: Sequence[T]) -> T | D:
        return cyget(ind, seq, default)  # pyright: ignore[reportUnknownVariableType]

    @staticmethod
    def _call_inds(ind: list[int], seq: Sequence[T]) -> list[T]:
        return cyget(ind, seq)  # pyright: ignore[reportUnknownVariableType]
    @staticmethod
    def _call_inds_default(default: D, ind: list[int], seq: Sequence[T]) -> list[T | D]:
        return cyget(ind, seq, default)  # pyright: ignore[reportUnknownVariableType]

    @staticmethod
    def _call_mapping(ind: K, seq: Mapping[K, V]) -> V:
        return cyget(ind, seq)  # pyright: ignore[reportUnknownVariableType]
    @staticmethod
    def _call_mapping_default(default: D, ind: K, seq: Mapping[K, V]) -> V | D:
        return cyget(ind, seq, default)  # pyright: ignore[reportUnknownVariableType]


class _get(metaclass=_get_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    get(ind, seq[, default]) -> element or list

    Get element(s) of a sequence or mapping.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2)(_get_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]
    cd = curry(3)(_get_meta._call_ind_default)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]

    cs = curry(2)(_get_meta._call_inds)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]
    csd = curry(3)(_get_meta._call_inds_default)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]

    cm = curry(2)(_get_meta._call_mapping)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]
    cmd = curry(3)(_get_meta._call_mapping_default)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]


get = _get  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["get"]
