from typing import Callable, TypeVar

T = TypeVar('T')

def do(func: Callable[[T], object], x: T) -> T: ...
