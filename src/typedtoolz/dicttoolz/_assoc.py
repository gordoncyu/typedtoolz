from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Any, TypeVar
from typing_extensions import override
from cytoolz.dicttoolz import assoc as cyassoc, dissoc as cydissoc, assoc_in as cyassoc_in, update_in as cyupdate_in, get_in as cyget_in  # pyright: ignore[reportUnknownVariableType]
from typedtoolz.functoolz._curry import curry
from typedtoolz.functoolz._curryv import curryv

K = TypeVar('K')
V = TypeVar('V')
D = TypeVar('D')

_missing = object()


class _assoc_meta(type):
    @staticmethod
    @override
    def __call__(d: Mapping[K, V], key: K, value: V) -> dict[K, V]:
        return cyassoc(d, key, value)  # pyright: ignore[reportUnknownVariableType]


class _assoc(metaclass=_assoc_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    assoc(d, key, value) -> dict

    Return a new dictionary with key associated to value.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(3, _assoc_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


assoc = _assoc  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _dissoc_meta(type):
    @staticmethod
    @override
    def __call__(d: Mapping[K, V], *keys: K) -> dict[K, V]:
        return cydissoc(d, *keys)  # pyright: ignore[reportUnknownVariableType]


class _dissoc(metaclass=_dissoc_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    dissoc(d, *keys) -> dict

    Return a new dictionary with the given keys removed.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curryv(2, _dissoc_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


dissoc = _dissoc  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _assoc_in_meta(type):
    @staticmethod
    @override
    def __call__(d: Mapping[object, Any], keys: Iterable[object], value: object) -> dict[object, Any]:  # pyright: ignore[reportExplicitAny]
        return cyassoc_in(d, keys, value)  # pyright: ignore[reportUnknownVariableType]


class _assoc_in(metaclass=_assoc_in_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    assoc_in(d, keys, value) -> dict

    Return a new dictionary with nested value set.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(3, _assoc_in_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


assoc_in = _assoc_in  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _update_in_meta(type):
    @staticmethod
    @override
    def __call__(d: Mapping[object, Any], keys: Iterable[object], func: Callable[..., object], default: object = _missing) -> dict[object, Any]:  # pyright: ignore[reportExplicitAny]
        if default is _missing:
            return cyupdate_in(d, keys, func)  # pyright: ignore[reportUnknownVariableType]
        return cyupdate_in(d, keys, func, default)  # pyright: ignore[reportUnknownVariableType]


class _update_in(metaclass=_update_in_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    update_in(d, keys, func[, default]) -> dict

    Update a nested value in a dictionary using a function.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(3, _update_in_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


update_in = _update_in  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs


class _get_in_meta(type):
    @staticmethod
    @override
    def __call__(keys: Iterable[object], coll: Mapping[object, Any] | Sequence[Any], default: D = None, no_default: bool = False) -> Any | D:  # pyright: ignore[reportExplicitAny]
        if default is _missing:
            return cyget_in(keys, coll, no_default=no_default)  # pyright: ignore[reportUnknownVariableType]
        return cyget_in(keys, coll, default, no_default=no_default)  # pyright: ignore[reportUnknownVariableType]

    @staticmethod
    def _call(keys: Iterable[object], coll: Mapping[object, Any] | Sequence[Any]) -> Any:  # pyright: ignore[reportExplicitAny, reportAny]
        return cyget_in(keys, coll, no_default=True)  # pyright: ignore[reportUnknownVariableType]

    @staticmethod
    def _call_default(default: D, keys: Iterable[object], coll: Mapping[object, Any] | Sequence[Any]) -> Any | D:  # pyright: ignore[reportExplicitAny]
        return cyget_in(keys, coll, default)  # pyright: ignore[reportUnknownVariableType]

class _get_in(metaclass=_get_in_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    get_in(keys, coll[, default, no_default]) -> value

    Return a nested value from a collection.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _get_in_meta._call)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage] # TODO: maybe make default c one not a foot gun (no default)
    cd = curry(3, _get_in_meta._call_default)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]


get_in = _get_in  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["assoc", "dissoc", "assoc_in", "update_in", "get_in"]
