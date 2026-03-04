# TODO: Review msc impl
# USES ANY
from collections.abc import Callable, Mapping, MutableMapping
from typing import Any, TypeVar, cast
from typing_extensions import override, overload
from cytoolz.dicttoolz import valfilter as _valfilter, keyfilter as _keyfilter, itemfilter as _itemfilter
from typedtoolz.functoolz._curry import curry

K = TypeVar('K')
V = TypeVar('V')
F = TypeVar('F', bound=MutableMapping[object, Any])  # pyright: ignore[reportExplicitAny]

_missing = object()


class _valfilter_meta(type):
    @classmethod
    @overload
    def __call__(cls, predicate: Callable[[V], object], d: Mapping[K, V]) -> dict[K, V]: ...
    @classmethod
    @overload
    def __call__(cls, predicate: Callable[[V], object], d: Mapping[K, V], factory: Callable[[], F]) -> F: ...
    @classmethod
    @override
    def __call__(cls, predicate: Callable[[V], object], d: Mapping[K, V], factory: Callable[[], F] = cast(Callable[[], F], _missing)) -> dict[K, V] | F:  # pyright: ignore[reportCallInDefaultInitializer, reportInconsistentOverload]
        if factory is _missing:
            return _valfilter(predicate, d)
        return _valfilter(predicate, d, factory)  # type: ignore[arg-type]


class _valfilter(metaclass=_valfilter_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    valfilter(predicate, d[, factory]) -> dict

    Filter items in dictionary by value.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _valfilter_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


valfilter = _valfilter  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _keyfilter_meta(type):
    @classmethod
    @overload
    def __call__(cls, predicate: Callable[[K], object], d: Mapping[K, V]) -> dict[K, V]: ...
    @classmethod
    @overload
    def __call__(cls, predicate: Callable[[K], object], d: Mapping[K, V], factory: Callable[[], F]) -> F: ...
    @classmethod
    @override
    def __call__(cls, predicate: Callable[[K], object], d: Mapping[K, V], factory: Callable[[], F] = cast(Callable[[], F], _missing)) -> dict[K, V] | F:  # pyright: ignore[reportCallInDefaultInitializer, reportInconsistentOverload]
        if factory is _missing:
            return _keyfilter(predicate, d)
        return _keyfilter(predicate, d, factory)  # type: ignore[arg-type]


class _keyfilter(metaclass=_keyfilter_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    keyfilter(predicate, d[, factory]) -> dict

    Filter items in dictionary by key.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _keyfilter_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


keyfilter = _keyfilter  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _itemfilter_meta(type):
    @classmethod
    @overload
    def __call__(cls, predicate: Callable[[tuple[K, V]], object], d: Mapping[K, V]) -> dict[K, V]: ...
    @classmethod
    @overload
    def __call__(cls, predicate: Callable[[tuple[K, V]], object], d: Mapping[K, V], factory: Callable[[], F]) -> F: ...
    @classmethod
    @override
    def __call__(cls, predicate: Callable[[tuple[K, V]], object], d: Mapping[K, V], factory: Callable[[], F] = cast(Callable[[], F], _missing)) -> dict[K, V] | F:  # pyright: ignore[reportCallInDefaultInitializer, reportInconsistentOverload]
        if factory is _missing:
            return _itemfilter(predicate, d)
        return _itemfilter(predicate, d, factory)  # type: ignore[arg-type]


class _itemfilter(metaclass=_itemfilter_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    itemfilter(predicate, d[, factory]) -> dict

    Filter items in dictionary by key-value pair.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _itemfilter_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


itemfilter = _itemfilter  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["valfilter", "keyfilter", "itemfilter"]
