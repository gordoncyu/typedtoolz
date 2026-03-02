# USES ANY
from collections.abc import Callable, Mapping, MutableMapping
from typing import Any, TypeVar, overload

K = TypeVar('K')
V = TypeVar('V')
W = TypeVar('W')
J = TypeVar('J')
F = TypeVar('F', bound=MutableMapping[object, Any])  # pyright: ignore[reportExplicitAny]

@overload
def valmap(func: Callable[[V], W], d: Mapping[K, V]) -> dict[K, W]: ...
@overload
def valmap(func: Callable[[V], W], d: Mapping[K, V], factory: Callable[[], F]) -> F: ...

@overload
def keymap(func: Callable[[K], J], d: Mapping[K, V]) -> dict[J, V]: ...
@overload
def keymap(func: Callable[[K], J], d: Mapping[K, V], factory: Callable[[], F]) -> F: ...

@overload
def itemmap(func: Callable[[tuple[K, V]], tuple[J, W]], d: Mapping[K, V]) -> dict[J, W]: ...
@overload
def itemmap(func: Callable[[tuple[K, V]], tuple[J, W]], d: Mapping[K, V], factory: Callable[[], F]) -> F: ...
