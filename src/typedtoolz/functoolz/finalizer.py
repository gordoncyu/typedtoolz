from typing import overload, Callable, TypeVar
from toolz import curry


A = TypeVar('A')
B = TypeVar('B')

@overload
def finalizer(
    func: Callable[[A], B],
    finalizer: Callable[[A], None],
) -> Callable[[A], B]: ...
@overload
def finalizer(
    func: Callable[[A], B],
) -> Callable[[Callable[[A], None]], Callable[[A], B]]: ...

@curry
def finalizer(func: Callable[[A], B], finalizer: Callable[[A], None]) -> Callable[[A], B]:
    def wrapped(x: A) -> B:
        try:
            return func(x)
        finally:
            finalizer(x)
    return wrapped

