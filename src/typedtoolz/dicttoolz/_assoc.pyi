# USES ANY
from collections.abc import Callable, Iterable, Mapping, Sequence
from typing import Any, TypeVar, overload

K = TypeVar('K')
V = TypeVar('V')
D = TypeVar('D')

def assoc(d: Mapping[K, V], key: K, value: V) -> dict[K, V]: ...
def dissoc(d: Mapping[K, V], *keys: K) -> dict[K, V]: ...
def assoc_in(d: Mapping[object, Any], keys: Iterable[object], value: object) -> dict[object, Any]: ...  # pyright: ignore[reportExplicitAny]
def update_in(d: Mapping[object, Any], keys: Iterable[object], func: Callable[..., object], default: object = ...) -> dict[object, Any]: ...  # pyright: ignore[reportExplicitAny]

@overload
def get_in(keys: Iterable[object], coll: Mapping[object, Any] | Sequence[Any], *, no_default: bool = ...) -> Any: ...  # pyright: ignore[reportExplicitAny]
@overload
def get_in(keys: Iterable[object], coll: Mapping[object, Any] | Sequence[Any], default: D, no_default: bool = ...) -> Any | D: ...  # pyright: ignore[reportExplicitAny]
