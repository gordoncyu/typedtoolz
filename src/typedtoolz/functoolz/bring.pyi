from typing import Callable, Concatenate, Literal, ParamSpec, TypeVar, overload

A1 = TypeVar('A1', contravariant=True)
A2 = TypeVar('A2', contravariant=True)
A3 = TypeVar('A3', contravariant=True)
A4 = TypeVar('A4', contravariant=True)
A5 = TypeVar('A5', contravariant=True)
A6 = TypeVar('A6', contravariant=True)
A7 = TypeVar('A7', contravariant=True)
A8 = TypeVar('A8', contravariant=True)
A9 = TypeVar('A9', contravariant=True)
A10 = TypeVar('A10', contravariant=True)
A11 = TypeVar('A11', contravariant=True)
R = TypeVar('R', covariant=True)
P = ParamSpec('P')

@overload
def bring(n: Literal[0], func: Callable[Concatenate[A1, P], R], /) -> Callable[Concatenate[A1, P], R]: ...

@overload
def bring(n: Literal[0], /) -> Callable[[Callable[Concatenate[A1, P], R]], Callable[Concatenate[A1, P], R]]: ...

@overload
def bring(n: Literal[1], func: Callable[Concatenate[A1, A2, P], R], /) -> Callable[Concatenate[A2, A1, P], R]: ...

@overload
def bring(n: Literal[1], /) -> Callable[[Callable[Concatenate[A1, A2, P], R]], Callable[Concatenate[A2, A1, P], R]]: ...

@overload
def bring(n: Literal[2], func: Callable[Concatenate[A1, A2, A3, P], R], /) -> Callable[Concatenate[A3, A2, A1, P], R]: ...

@overload
def bring(n: Literal[2], /) -> Callable[[Callable[Concatenate[A1, A2, A3, P], R]], Callable[Concatenate[A3, A2, A1, P], R]]: ...

@overload
def bring(n: Literal[3], func: Callable[Concatenate[A1, A2, A3, A4, P], R], /) -> Callable[Concatenate[A4, A2, A3, A1, P], R]: ...

@overload
def bring(n: Literal[3], /) -> Callable[[Callable[Concatenate[A1, A2, A3, A4, P], R]], Callable[Concatenate[A4, A2, A3, A1, P], R]]: ...

@overload
def bring(n: Literal[4], func: Callable[Concatenate[A1, A2, A3, A4, A5, P], R], /) -> Callable[Concatenate[A5, A2, A3, A4, A1, P], R]: ...

@overload
def bring(n: Literal[4], /) -> Callable[[Callable[Concatenate[A1, A2, A3, A4, A5, P], R]], Callable[Concatenate[A5, A2, A3, A4, A1, P], R]]: ...

@overload
def bring(n: Literal[5], func: Callable[Concatenate[A1, A2, A3, A4, A5, A6, P], R], /) -> Callable[Concatenate[A6, A2, A3, A4, A5, A1, P], R]: ...

@overload
def bring(n: Literal[5], /) -> Callable[[Callable[Concatenate[A1, A2, A3, A4, A5, A6, P], R]], Callable[Concatenate[A6, A2, A3, A4, A5, A1, P], R]]: ...

@overload
def bring(n: Literal[6], func: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, P], R], /) -> Callable[Concatenate[A7, A2, A3, A4, A5, A6, A1, P], R]: ...

@overload
def bring(n: Literal[6], /) -> Callable[[Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, P], R]], Callable[Concatenate[A7, A2, A3, A4, A5, A6, A1, P], R]]: ...

@overload
def bring(n: Literal[7], func: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, P], R], /) -> Callable[Concatenate[A8, A2, A3, A4, A5, A6, A7, A1, P], R]: ...

@overload
def bring(n: Literal[7], /) -> Callable[[Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, P], R]], Callable[Concatenate[A8, A2, A3, A4, A5, A6, A7, A1, P], R]]: ...

@overload
def bring(n: Literal[8], func: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, P], R], /) -> Callable[Concatenate[A9, A2, A3, A4, A5, A6, A7, A8, A1, P], R]: ...

@overload
def bring(n: Literal[8], /) -> Callable[[Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, P], R]], Callable[Concatenate[A9, A2, A3, A4, A5, A6, A7, A8, A1, P], R]]: ...

@overload
def bring(n: Literal[9], func: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, P], R], /) -> Callable[Concatenate[A10, A2, A3, A4, A5, A6, A7, A8, A9, A1, P], R]: ...

@overload
def bring(n: Literal[9], /) -> Callable[[Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, P], R]], Callable[Concatenate[A10, A2, A3, A4, A5, A6, A7, A8, A9, A1, P], R]]: ...

@overload
def bring(n: Literal[10], func: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, P], R], /) -> Callable[Concatenate[A11, A2, A3, A4, A5, A6, A7, A8, A9, A10, A1, P], R]: ...

@overload
def bring(n: Literal[10], /) -> Callable[[Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11, P], R]], Callable[Concatenate[A11, A2, A3, A4, A5, A6, A7, A8, A9, A10, A1, P], R]]: ...

@overload
def bring(n: int, func: Callable[..., R], /) -> Callable[..., R]: ...

@overload
def bring(n: int, /) -> Callable[[Callable[..., R]], Callable[..., R]]: ...
