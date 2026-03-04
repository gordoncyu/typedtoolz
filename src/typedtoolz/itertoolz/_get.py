# TODO: Review msc impl
from collections.abc import Mapping, Sequence
from typing import TypeVar, cast
from typing_extensions import override, overload
from cytoolz.itertoolz import get as _get
from typedtoolz.functoolz._curry import curry

T = TypeVar('T')
D = TypeVar('D')
K = TypeVar('K')
V = TypeVar('V')

_missing = object()


class _get_meta(type):
    @classmethod
    @overload
    def __call__(cls, ind: int, seq: Sequence[T]) -> T: ...
    @classmethod
    @overload
    def __call__(cls, ind: int, seq: Sequence[T], default: D) -> T | D: ...
    @classmethod
    @overload
    def __call__(cls, ind: list[int], seq: Sequence[T]) -> list[T]: ...
    @classmethod
    @overload
    def __call__(cls, ind: list[int], seq: Sequence[T], default: D) -> list[T | D]: ...
    @classmethod
    @overload
    def __call__(cls, ind: K, seq: Mapping[K, V]) -> V: ...
    @classmethod
    @overload
    def __call__(cls, ind: K, seq: Mapping[K, V], default: D) -> V | D: ...
    @classmethod
    @override
    def __call__(cls, ind: int | list[int] | K, seq: Sequence[T] | Mapping[K, V], default: D = cast(D, _missing)) -> T | list[T] | V | T | D:  # pyright: ignore[reportCallInDefaultInitializer, reportInconsistentOverload]
        if default is _missing:
            return _get(ind, seq)  # type: ignore[arg-type, return-value]
        return _get(ind, seq, default)  # type: ignore[arg-type, return-value]


class _get(metaclass=_get_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    get(ind, seq[, default]) -> element or list

    Get element(s) of a sequence or mapping.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _get_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


get = _get  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["get"]
