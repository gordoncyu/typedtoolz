from typing import Callable, Type, overload, TypeVar


A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

@overload
def excepts( # pyright: ignore[reportNoOverloadImplementation]
    exc: Type[C] | tuple[Type[C], ...],
    func: Callable[[A], B],
) -> Callable[[A], B | None]: ...

@overload
def excepts(
    exc: Type[C] | tuple[Type[C], ...],
    func: Callable[[A], B],
    handler: Callable[[C], B],
) -> Callable[[A], B]: ...

from toolz.curried import excepts # pyright: ignore[reportAssignmentType]

