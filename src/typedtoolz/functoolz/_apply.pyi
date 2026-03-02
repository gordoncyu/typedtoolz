from collections.abc import Iterable, Mapping
from typing import Callable, TypeVar, overload

R = TypeVar('R')

@overload
def apply(func: Callable[[], R]) -> R: ...
@overload
def apply(func: Callable[..., R], args: Iterable[object]) -> R: ...
@overload
def apply(func: Callable[..., R], args: Iterable[object], kwargs: Mapping[str, object]) -> R: ...
