from typing import Callable, Generic, TypeVar, overload
from typing_extensions import Any, Self

T_co = TypeVar('T_co', covariant=True)
T = TypeVar('T')
S = TypeVar('S')

class InstanceProperty(property, Generic[S, T_co]):
    """Like @property, but returns ``classval`` when used as a class attribute."""
    classval: object
    def __init__(
        self,
        fget: Callable[[S], T_co] | None = ...,  # pyright: ignore[reportInvalidTypeVarUse]
        fset: Callable[[S, T_co], None] | None = ...,
        fdel: Callable[[S], None] | None = ...,
        doc: str | None = ...,
        classval: object = ...,
    ) -> None: ...
    @overload
    def __get__(self, instance: None, owner: type, /) -> Self: ...
    @overload
    def __get__(self, instance: object, owner: type | None = ...) -> T_co: ...

@overload
def instanceproperty(
    fget: Callable[[S], T],
    fset: Callable[[S, T], None] | None = ...,
    fdel: Callable[[S], None] | None = ...,
    doc: str | None = ...,
    classval: object = ...,
) -> InstanceProperty[T, S]: ...
@overload
def instanceproperty(
    fget: None = ...,
    fset: Callable[[Any], None] | None = ...,  # pyright: ignore[reportExplicitAny]
    fdel: Callable[[Any], None] | None = ...,  # pyright: ignore[reportExplicitAny]
    doc: str | None = ...,
    classval: object = ...,
) -> Callable[[Callable[[S], T]], InstanceProperty[T]]: ...
