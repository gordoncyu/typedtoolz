from collections.abc import Callable, Mapping, MutableMapping
from typing import Any, TypeVar, cast
from typing_extensions import override, overload
from cytoolz.dicttoolz import valfilter as cyvalfilter, keyfilter as cykeyfilter, itemfilter as cyitemfilter  # pyright: ignore[reportUnknownVariableType]
from typedtoolz.functoolz._curry import curry

K = TypeVar('K')
V = TypeVar('V')
F = TypeVar('F', bound=MutableMapping[object, Any])  # pyright: ignore[reportExplicitAny]

_missing = object()


class _valfilter_meta(type):
    @staticmethod
    @overload
    def __call__(predicate: Callable[[V], object], d: Mapping[K, V]) -> dict[K, V]: ...
    @staticmethod
    @overload
    def __call__(predicate: Callable[[V], object], d: Mapping[K, V], factory: Callable[[], F]) -> F: ...
    @staticmethod
    @override
    def __call__(predicate: Callable[[V], object], d: Mapping[K, V], factory: Callable[[], F] = cast(Callable[[], F], _missing)) -> dict[K, V] | F:  # pyright: ignore[reportCallInDefaultInitializer]
        if factory is _missing:
            return cyvalfilter(predicate, d)  # pyright: ignore[reportUnknownVariableType]
        return cyvalfilter(predicate, d, factory)  # type: ignore[arg-type]  # pyright: ignore[reportUnknownVariableType]

    @staticmethod
    def _call_factory(factory: Callable[[], F], predicate: Callable[[V], object], d: Mapping[object, V]) -> F:
        return cyvalfilter(predicate, d, factory)  # pyright: ignore[reportUnknownVariableType]

class _valfilter(metaclass=_valfilter_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    valfilter(predicate, d[, factory]) -> dict

    Filter items in dictionary by value.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _valfilter_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]
    cd = curry(3, _valfilter_meta._call_factory)  # pyright: ignore[reportPrivateUsage, reportUnannotatedClassAttribute]


valfilter = _valfilter  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _keyfilter_meta(type):
    @staticmethod
    @overload
    def __call__(predicate: Callable[[K], object], d: Mapping[K, V]) -> dict[K, V]: ...
    @staticmethod
    @overload
    def __call__(predicate: Callable[[K], object], d: Mapping[K, V], factory: Callable[[], F]) -> F: ...
    @staticmethod
    @override
    def __call__(predicate: Callable[[K], object], d: Mapping[K, V], factory: Callable[[], F] = cast(Callable[[], F], _missing)) -> dict[K, V] | F:  # pyright: ignore[reportCallInDefaultInitializer]
        if factory is _missing:
            return cykeyfilter(predicate, d)  # pyright: ignore[reportUnknownVariableType]
        return cykeyfilter(predicate, d, factory)  # type: ignore[arg-type]  # pyright: ignore[reportUnknownVariableType]

    @staticmethod
    def _call_factory(factory: Callable[[], F], predicate: Callable[[K], object], d: Mapping[K, object]) -> F:
        return cykeyfilter(predicate, d, factory)  # pyright: ignore[reportUnknownVariableType]


class _keyfilter(metaclass=_keyfilter_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    keyfilter(predicate, d[, factory]) -> dict

    Filter items in dictionary by key.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _keyfilter_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]
    c = curry(3, _keyfilter_meta._call_factory)  # pyright: ignore[reportPrivateUsage]


keyfilter = _keyfilter  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _itemfilter_meta(type):
    @staticmethod
    @overload
    def __call__(predicate: Callable[[tuple[K, V]], object], d: Mapping[K, V]) -> dict[K, V]: ...
    @staticmethod
    @overload
    def __call__(predicate: Callable[[tuple[K, V]], object], d: Mapping[K, V], factory: Callable[[], F]) -> F: ...
    @staticmethod
    @override
    def __call__(predicate: Callable[[tuple[K, V]], object], d: Mapping[K, V], factory: Callable[[], F] = cast(Callable[[], F], _missing)) -> dict[K, V] | F:  # pyright: ignore[reportCallInDefaultInitializer]
        if factory is _missing:
            return cyitemfilter(predicate, d)  # pyright: ignore[reportUnknownVariableType]
        return cyitemfilter(predicate, d, factory)  # type: ignore[arg-type]  # pyright: ignore[reportUnknownVariableType]

    @staticmethod
    def _call_factory(factory: Callable[[], F], predicate: Callable[[tuple[K, V]], object], d: Mapping[K, V]) -> F:
        return cyitemfilter(predicate, d, factory)  # pyright: ignore[reportUnknownVariableType]


class _itemfilter(metaclass=_itemfilter_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    itemfilter(predicate, d[, factory]) -> dict

    Filter items in dictionary by key-value pair.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _itemfilter_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]
    c = curry(3, _itemfilter_meta._call_factory)  # pyright: ignore[reportPrivateUsage]


itemfilter = _itemfilter  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["valfilter", "keyfilter", "itemfilter"]
