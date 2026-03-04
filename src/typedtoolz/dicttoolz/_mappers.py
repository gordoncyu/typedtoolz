# TODO: Review msc impl
# USES ANY
from collections.abc import Callable, Mapping, MutableMapping
from typing import Any, TypeVar, cast
from typing_extensions import override, overload
from cytoolz.dicttoolz import valmap as _valmap, keymap as _keymap, itemmap as _itemmap
from typedtoolz.functoolz._curry import curry

K = TypeVar('K')
V = TypeVar('V')
W = TypeVar('W')
J = TypeVar('J')
F = TypeVar('F', bound=MutableMapping[object, Any])  # pyright: ignore[reportExplicitAny]

_missing = object()


class _valmap_meta(type):
    @staticmethod
    @overload
    def __call__(func: Callable[[V], W], d: Mapping[K, V]) -> dict[K, W]: ...
    @staticmethod
    @overload
    def __call__(func: Callable[[V], W], d: Mapping[K, V], factory: Callable[[], F]) -> F: ...
    @staticmethod
    @override
    def __call__(func: Callable[[V], W], d: Mapping[K, V], factory: Callable[[], F] = cast(Callable[[], F], _missing)) -> dict[K, W] | F:  # pyright: ignore[reportCallInDefaultInitializer, reportInconsistentOverload]
        if factory is _missing:
            return _valmap(func, d)
        return _valmap(func, d, factory)  # type: ignore[arg-type]


class _valmap(metaclass=_valmap_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    valmap(func, d[, factory]) -> dict

    Apply func to each value in a dictionary.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _valmap_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


valmap = _valmap  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _keymap_meta(type):
    @staticmethod
    @overload
    def __call__(func: Callable[[K], J], d: Mapping[K, V]) -> dict[J, V]: ...
    @staticmethod
    @overload
    def __call__(func: Callable[[K], J], d: Mapping[K, V], factory: Callable[[], F]) -> F: ...
    @staticmethod
    @override
    def __call__(func: Callable[[K], J], d: Mapping[K, V], factory: Callable[[], F] = cast(Callable[[], F], _missing)) -> dict[J, V] | F:  # pyright: ignore[reportCallInDefaultInitializer, reportInconsistentOverload]
        if factory is _missing:
            return _keymap(func, d)
        return _keymap(func, d, factory)  # type: ignore[arg-type]


class _keymap(metaclass=_keymap_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    keymap(func, d[, factory]) -> dict

    Apply func to each key in a dictionary.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _keymap_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


keymap = _keymap  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _itemmap_meta(type):
    @staticmethod
    @overload
    def __call__(func: Callable[[tuple[K, V]], tuple[J, W]], d: Mapping[K, V]) -> dict[J, W]: ...
    @staticmethod
    @overload
    def __call__(func: Callable[[tuple[K, V]], tuple[J, W]], d: Mapping[K, V], factory: Callable[[], F]) -> F: ...
    @staticmethod
    @override
    def __call__(func: Callable[[tuple[K, V]], tuple[J, W]], d: Mapping[K, V], factory: Callable[[], F] = cast(Callable[[], F], _missing)) -> dict[J, W] | F:  # pyright: ignore[reportCallInDefaultInitializer, reportInconsistentOverload]
        if factory is _missing:
            return _itemmap(func, d)
        return _itemmap(func, d, factory)  # type: ignore[arg-type]


class _itemmap(metaclass=_itemmap_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    itemmap(func, d[, factory]) -> dict

    Apply func to each key-value pair in a dictionary.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _itemmap_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


itemmap = _itemmap  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["valmap", "keymap", "itemmap"]
