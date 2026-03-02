# USES ANY
from collections.abc import Callable, Mapping, MutableMapping
from typing import Any, TypeVar, overload

K = TypeVar('K')
V = TypeVar('V')
F = TypeVar('F', bound=MutableMapping[object, Any])  # pyright: ignore[reportExplicitAny]

@overload
def valfilter(predicate: Callable[[V], object], d: Mapping[K, V]) -> dict[K, V]: ...
@overload
def valfilter(predicate: Callable[[V], object], d: Mapping[K, V], factory: Callable[[], F]) -> F: ...

@overload
def keyfilter(predicate: Callable[[K], object], d: Mapping[K, V]) -> dict[K, V]: ...
@overload
def keyfilter(predicate: Callable[[K], object], d: Mapping[K, V], factory: Callable[[], F]) -> F: ...

@overload
def itemfilter(predicate: Callable[[tuple[K, V]], object], d: Mapping[K, V]) -> dict[K, V]: ...
@overload
def itemfilter(predicate: Callable[[tuple[K, V]], object], d: Mapping[K, V], factory: Callable[[], F]) -> F: ...
