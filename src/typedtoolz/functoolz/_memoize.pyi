# USES ANY
from typing import Callable, ParamSpec, TypeVar, overload

P = ParamSpec('P')
R = TypeVar('R')

@overload
def memoize(func: Callable[P, R]) -> Callable[P, R]: ...
@overload
def memoize(*, cache: dict[object, object] | None = ..., key: Callable[..., object] | None = ...) -> Callable[[Callable[P, R]], Callable[P, R]]: ...
