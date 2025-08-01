from typing import Callable, Concatenate, ParamSpec, Protocol, TypeVar, overload

P = ParamSpec('P')
R = TypeVar('R', covariant=True)
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

class Curried1(Protocol[A1, P, R]):
    @overload
    def __call__(self, A1: A1, *args: P.args, **kw: P.kwargs) -> R: ...
    @overload
    def __call__(self) -> 'Curried1[A1, P, R]': ...

class CurriedFixed1(Protocol[A1, R]):
    @overload
    def __call__(self, A1: A1) -> R: ...
    @overload
    def __call__(self) -> 'CurriedFixed1[A1, R]': ...

class Curried2(Protocol[A1, A2, P, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, *args: P.args, **kw: P.kwargs) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> Curried1[A2, P, R]: ...
    @overload
    def __call__(self) -> 'Curried2[A1, A2, P, R]': ...

class CurriedFixed2(Protocol[A1, A2, R]):
    @overload
    def __call__(self, A1: A1, A2: A2) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> CurriedFixed1[A2, R]: ...
    @overload
    def __call__(self) -> 'CurriedFixed2[A1, A2, R]': ...

class Curried3(Protocol[A1, A2, A3, P, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, *args: P.args, **kw: P.kwargs) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> Curried2[A2, A3, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> Curried1[A3, P, R]: ...
    @overload
    def __call__(self) -> 'Curried3[A1, A2, A3, P, R]': ...

class CurriedFixed3(Protocol[A1, A2, A3, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> CurriedFixed2[A2, A3, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> CurriedFixed1[A3, R]: ...
    @overload
    def __call__(self) -> 'CurriedFixed3[A1, A2, A3, R]': ...

class Curried4(Protocol[A1, A2, A3, A4, P, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, *args: P.args, **kw: P.kwargs) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> Curried3[A2, A3, A4, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> Curried2[A3, A4, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> Curried1[A4, P, R]: ...
    @overload
    def __call__(self) -> 'Curried4[A1, A2, A3, A4, P, R]': ...

class CurriedFixed4(Protocol[A1, A2, A3, A4, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> CurriedFixed3[A2, A3, A4, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> CurriedFixed2[A3, A4, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> CurriedFixed1[A4, R]: ...
    @overload
    def __call__(self) -> 'CurriedFixed4[A1, A2, A3, A4, R]': ...

class Curried5(Protocol[A1, A2, A3, A4, A5, P, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, *args: P.args, **kw: P.kwargs) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> Curried4[A2, A3, A4, A5, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> Curried3[A3, A4, A5, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> Curried2[A4, A5, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, /) -> Curried1[A5, P, R]: ...
    @overload
    def __call__(self) -> 'Curried5[A1, A2, A3, A4, A5, P, R]': ...

class CurriedFixed5(Protocol[A1, A2, A3, A4, A5, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> CurriedFixed4[A2, A3, A4, A5, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> CurriedFixed3[A3, A4, A5, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> CurriedFixed2[A4, A5, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, /) -> CurriedFixed1[A5, R]: ...
    @overload
    def __call__(self) -> 'CurriedFixed5[A1, A2, A3, A4, A5, R]': ...

class Curried6(Protocol[A1, A2, A3, A4, A5, A6, P, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, *args: P.args, **kw: P.kwargs) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> Curried5[A2, A3, A4, A5, A6, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> Curried4[A3, A4, A5, A6, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> Curried3[A4, A5, A6, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, /) -> Curried2[A5, A6, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /) -> Curried1[A6, P, R]: ...
    @overload
    def __call__(self) -> 'Curried6[A1, A2, A3, A4, A5, A6, P, R]': ...

class CurriedFixed6(Protocol[A1, A2, A3, A4, A5, A6, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> CurriedFixed5[A2, A3, A4, A5, A6, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> CurriedFixed4[A3, A4, A5, A6, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> CurriedFixed3[A4, A5, A6, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, /) -> CurriedFixed2[A5, A6, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /) -> CurriedFixed1[A6, R]: ...
    @overload
    def __call__(self) -> 'CurriedFixed6[A1, A2, A3, A4, A5, A6, R]': ...

class Curried7(Protocol[A1, A2, A3, A4, A5, A6, A7, P, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, *args: P.args, **kw: P.kwargs) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> Curried6[A2, A3, A4, A5, A6, A7, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> Curried5[A3, A4, A5, A6, A7, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> Curried4[A4, A5, A6, A7, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, /) -> Curried3[A5, A6, A7, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /) -> Curried2[A6, A7, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, /) -> Curried1[A7, P, R]: ...
    @overload
    def __call__(self) -> 'Curried7[A1, A2, A3, A4, A5, A6, A7, P, R]': ...

class CurriedFixed7(Protocol[A1, A2, A3, A4, A5, A6, A7, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> CurriedFixed6[A2, A3, A4, A5, A6, A7, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> CurriedFixed5[A3, A4, A5, A6, A7, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> CurriedFixed4[A4, A5, A6, A7, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, /) -> CurriedFixed3[A5, A6, A7, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /) -> CurriedFixed2[A6, A7, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, /) -> CurriedFixed1[A7, R]: ...
    @overload
    def __call__(self) -> 'CurriedFixed7[A1, A2, A3, A4, A5, A6, A7, R]': ...

class Curried8(Protocol[A1, A2, A3, A4, A5, A6, A7, A8, P, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, A8: A8, *args: P.args, **kw: P.kwargs) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> Curried7[A2, A3, A4, A5, A6, A7, A8, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> Curried6[A3, A4, A5, A6, A7, A8, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> Curried5[A4, A5, A6, A7, A8, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, /) -> Curried4[A5, A6, A7, A8, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /) -> Curried3[A6, A7, A8, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, /) -> Curried2[A7, A8, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, /) -> Curried1[A8, P, R]: ...
    @overload
    def __call__(self) -> 'Curried8[A1, A2, A3, A4, A5, A6, A7, A8, P, R]': ...

class CurriedFixed8(Protocol[A1, A2, A3, A4, A5, A6, A7, A8, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, A8: A8) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> CurriedFixed7[A2, A3, A4, A5, A6, A7, A8, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> CurriedFixed6[A3, A4, A5, A6, A7, A8, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> CurriedFixed5[A4, A5, A6, A7, A8, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, /) -> CurriedFixed4[A5, A6, A7, A8, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /) -> CurriedFixed3[A6, A7, A8, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, /) -> CurriedFixed2[A7, A8, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, /) -> CurriedFixed1[A8, R]: ...
    @overload
    def __call__(self) -> 'CurriedFixed8[A1, A2, A3, A4, A5, A6, A7, A8, R]': ...

class Curried9(Protocol[A1, A2, A3, A4, A5, A6, A7, A8, A9, P, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, A8: A8, A9: A9, *args: P.args, **kw: P.kwargs) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> Curried8[A2, A3, A4, A5, A6, A7, A8, A9, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> Curried7[A3, A4, A5, A6, A7, A8, A9, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> Curried6[A4, A5, A6, A7, A8, A9, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, /) -> Curried5[A5, A6, A7, A8, A9, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /) -> Curried4[A6, A7, A8, A9, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, /) -> Curried3[A7, A8, A9, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, /) -> Curried2[A8, A9, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, A8: A8, /) -> Curried1[A9, P, R]: ...
    @overload
    def __call__(self) -> 'Curried9[A1, A2, A3, A4, A5, A6, A7, A8, A9, P, R]': ...

class CurriedFixed9(Protocol[A1, A2, A3, A4, A5, A6, A7, A8, A9, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, A8: A8, A9: A9) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> CurriedFixed8[A2, A3, A4, A5, A6, A7, A8, A9, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> CurriedFixed7[A3, A4, A5, A6, A7, A8, A9, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> CurriedFixed6[A4, A5, A6, A7, A8, A9, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, /) -> CurriedFixed5[A5, A6, A7, A8, A9, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /) -> CurriedFixed4[A6, A7, A8, A9, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, /) -> CurriedFixed3[A7, A8, A9, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, /) -> CurriedFixed2[A8, A9, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, A8: A8, /) -> CurriedFixed1[A9, R]: ...
    @overload
    def __call__(self) -> 'CurriedFixed9[A1, A2, A3, A4, A5, A6, A7, A8, A9, R]': ...

class Curried10(Protocol[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, P, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, A8: A8, A9: A9, A10: A10, *args: P.args, **kw: P.kwargs) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> Curried9[A2, A3, A4, A5, A6, A7, A8, A9, A10, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> Curried8[A3, A4, A5, A6, A7, A8, A9, A10, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> Curried7[A4, A5, A6, A7, A8, A9, A10, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, /) -> Curried6[A5, A6, A7, A8, A9, A10, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /) -> Curried5[A6, A7, A8, A9, A10, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, /) -> Curried4[A7, A8, A9, A10, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, /) -> Curried3[A8, A9, A10, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, A8: A8, /) -> Curried2[A9, A10, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, A8: A8, A9: A9, /) -> Curried1[A10, P, R]: ...
    @overload
    def __call__(self) -> 'Curried10[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, P, R]': ...

class CurriedFixed10(Protocol[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, A8: A8, A9: A9, A10: A10) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> CurriedFixed9[A2, A3, A4, A5, A6, A7, A8, A9, A10, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> CurriedFixed8[A3, A4, A5, A6, A7, A8, A9, A10, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> CurriedFixed7[A4, A5, A6, A7, A8, A9, A10, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, /) -> CurriedFixed6[A5, A6, A7, A8, A9, A10, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /) -> CurriedFixed5[A6, A7, A8, A9, A10, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, /) -> CurriedFixed4[A7, A8, A9, A10, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, /) -> CurriedFixed3[A8, A9, A10, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, A8: A8, /) -> CurriedFixed2[A9, A10, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, A8: A8, A9: A9, /) -> CurriedFixed1[A10, R]: ...
    @overload
    def __call__(self) -> 'CurriedFixed10[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, R]': ...

@overload
def curry(fn: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, P], R], /) -> Curried10[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, P, R]: ...

@overload
def curry(fn: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, P], R], /) -> Curried9[A1, A2, A3, A4, A5, A6, A7, A8, A9, P, R]: ...

@overload
def curry(fn: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, P], R], /) -> Curried8[A1, A2, A3, A4, A5, A6, A7, A8, P, R]: ...

@overload
def curry(fn: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, P], R], /) -> Curried7[A1, A2, A3, A4, A5, A6, A7, P, R]: ...

@overload
def curry(fn: Callable[Concatenate[A1, A2, A3, A4, A5, A6, P], R], /) -> Curried6[A1, A2, A3, A4, A5, A6, P, R]: ...

@overload
def curry(fn: Callable[Concatenate[A1, A2, A3, A4, A5, P], R], /) -> Curried5[A1, A2, A3, A4, A5, P, R]: ...

@overload
def curry(fn: Callable[Concatenate[A1, A2, A3, A4, P], R], /) -> Curried4[A1, A2, A3, A4, P, R]: ...

@overload
def curry(fn: Callable[Concatenate[A1, A2, A3, P], R], /) -> Curried3[A1, A2, A3, P, R]: ...

@overload
def curry(fn: Callable[Concatenate[A1, A2, P], R], /) -> Curried2[A1, A2, P, R]: ...

@overload
def curry(fn: Callable[Concatenate[A1, P], R], /) -> Curried1[A1, P, R]: ...

