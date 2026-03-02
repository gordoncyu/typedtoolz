from typing import Any, Callable, ParamSpec, TypeVar, overload

P = ParamSpec('P')
R1 = TypeVar('R1')
R2 = TypeVar('R2')
R3 = TypeVar('R3')
R4 = TypeVar('R4')
R5 = TypeVar('R5')
R6 = TypeVar('R6')
R7 = TypeVar('R7')
R8 = TypeVar('R8')
R9 = TypeVar('R9')
R10 = TypeVar('R10')

@overload
def juxt(f1: Callable[P, R1], /) -> Callable[P, tuple[R1]]: ...

@overload
def juxt(f1: Callable[P, R1], f2: Callable[P, R2], /) -> Callable[P, tuple[R1, R2]]: ...

@overload
def juxt(f1: Callable[P, R1], f2: Callable[P, R2], f3: Callable[P, R3], /) -> Callable[P, tuple[R1, R2, R3]]: ...

@overload
def juxt(f1: Callable[P, R1], f2: Callable[P, R2], f3: Callable[P, R3], f4: Callable[P, R4], /) -> Callable[P, tuple[R1, R2, R3, R4]]: ...

@overload
def juxt(f1: Callable[P, R1], f2: Callable[P, R2], f3: Callable[P, R3], f4: Callable[P, R4], f5: Callable[P, R5], /) -> Callable[P, tuple[R1, R2, R3, R4, R5]]: ...

@overload
def juxt(f1: Callable[P, R1], f2: Callable[P, R2], f3: Callable[P, R3], f4: Callable[P, R4], f5: Callable[P, R5], f6: Callable[P, R6], /) -> Callable[P, tuple[R1, R2, R3, R4, R5, R6]]: ...

@overload
def juxt(f1: Callable[P, R1], f2: Callable[P, R2], f3: Callable[P, R3], f4: Callable[P, R4], f5: Callable[P, R5], f6: Callable[P, R6], f7: Callable[P, R7], /) -> Callable[P, tuple[R1, R2, R3, R4, R5, R6, R7]]: ...

@overload
def juxt(f1: Callable[P, R1], f2: Callable[P, R2], f3: Callable[P, R3], f4: Callable[P, R4], f5: Callable[P, R5], f6: Callable[P, R6], f7: Callable[P, R7], f8: Callable[P, R8], /) -> Callable[P, tuple[R1, R2, R3, R4, R5, R6, R7, R8]]: ...

@overload
def juxt(f1: Callable[P, R1], f2: Callable[P, R2], f3: Callable[P, R3], f4: Callable[P, R4], f5: Callable[P, R5], f6: Callable[P, R6], f7: Callable[P, R7], f8: Callable[P, R8], f9: Callable[P, R9], /) -> Callable[P, tuple[R1, R2, R3, R4, R5, R6, R7, R8, R9]]: ...

@overload
def juxt(f1: Callable[P, R1], f2: Callable[P, R2], f3: Callable[P, R3], f4: Callable[P, R4], f5: Callable[P, R5], f6: Callable[P, R6], f7: Callable[P, R7], f8: Callable[P, R8], f9: Callable[P, R9], f10: Callable[P, R10], /) -> Callable[P, tuple[R1, R2, R3, R4, R5, R6, R7, R8, R9, R10]]: ...

@overload
def juxt(*funcs: Callable[..., Any], /) -> Callable[..., tuple[Any, ...]]: ...
