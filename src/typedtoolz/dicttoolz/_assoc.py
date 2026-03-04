# TODO: Review msc impl
# USES ANY
from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Any, TypeVar, cast
from typing_extensions import override, overload
from cytoolz.dicttoolz import assoc as _assoc, dissoc as _dissoc, assoc_in as _assoc_in, update_in as _update_in, get_in as _get_in
from typedtoolz.functoolz._curry import curry

K = TypeVar('K')
V = TypeVar('V')
D = TypeVar('D')

_missing = object()


class _assoc_meta(type):
    @classmethod
    @override
    def __call__(cls, d: Mapping[K, V], key: K, value: V) -> dict[K, V]:
        return _assoc(d, key, value)


class _assoc(metaclass=_assoc_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    assoc(d, key, value) -> dict

    Return a new dictionary with key associated to value.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(3, _assoc_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


assoc = _assoc  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _dissoc_meta(type):
    @classmethod
    @override
    def __call__(cls, d: Mapping[K, V], *keys: K) -> dict[K, V]:
        return _dissoc(d, *keys)


class _dissoc(metaclass=_dissoc_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    dissoc(d, *keys) -> dict

    Return a new dictionary with the given keys removed.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(1, _dissoc_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


dissoc = _dissoc  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _assoc_in_meta(type):
    @classmethod
    @override
    def __call__(cls, d: Mapping[object, Any], keys: Iterable[object], value: object) -> dict[object, Any]:  # pyright: ignore[reportExplicitAny]
        return _assoc_in(d, keys, value)


class _assoc_in(metaclass=_assoc_in_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    assoc_in(d, keys, value) -> dict

    Return a new dictionary with nested value set.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(3, _assoc_in_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


assoc_in = _assoc_in  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _update_in_meta(type):
    @classmethod
    @override
    def __call__(cls, d: Mapping[object, Any], keys: Iterable[object], func: Callable[..., object], default: object = cast(object, _missing)) -> dict[object, Any]:  # pyright: ignore[reportExplicitAny, reportCallInDefaultInitializer]
        if default is _missing:
            return _update_in(d, keys, func)
        return _update_in(d, keys, func, default)


class _update_in(metaclass=_update_in_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    update_in(d, keys, func[, default]) -> dict

    Update a nested value in a dictionary using a function.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(3, _update_in_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


update_in = _update_in  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _get_in_meta(type):
    @classmethod
    @overload
    def __call__(cls, keys: Iterable[object], coll: Mapping[object, Any] | Sequence[Any], *, no_default: bool = ...) -> Any: ...  # pyright: ignore[reportExplicitAny]
    @classmethod
    @overload
    def __call__(cls, keys: Iterable[object], coll: Mapping[object, Any] | Sequence[Any], default: D, no_default: bool = ...) -> Any | D: ...  # pyright: ignore[reportExplicitAny]
    @classmethod
    @override
    def __call__(cls, keys: Iterable[object], coll: Mapping[object, Any] | Sequence[Any], default: D = cast(D, _missing), no_default: bool = False) -> Any | D:  # pyright: ignore[reportExplicitAny, reportCallInDefaultInitializer, reportInconsistentOverload]
        if default is _missing:
            return _get_in(keys, coll, no_default=no_default)
        return _get_in(keys, coll, default, no_default=no_default)  # type: ignore[arg-type]


class _get_in(metaclass=_get_in_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    get_in(keys, coll[, default, no_default]) -> value

    Return a nested value from a collection.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _get_in_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


get_in = _get_in  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["assoc", "dissoc", "assoc_in", "update_in", "get_in"]
