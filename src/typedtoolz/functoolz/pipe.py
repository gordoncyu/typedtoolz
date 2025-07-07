from typing import Callable, Type, TypeVar, cast, overload

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
E = TypeVar("E")
F = TypeVar("F")
G = TypeVar("G")
H = TypeVar("H")
I = TypeVar("I")
J = TypeVar("J")
K = TypeVar("K")

@overload
def pipe(val: A, f1: Callable[[A], B]) -> B: ... # typed pipe. something like str.lower().match() would instead be pipe(str, lower, match), except you can use any function in the pipe
@overload
def pipe(val: A, f1: Callable[[A], B], f2: Callable[[B], C]) -> C: ... # unfortunately the python type hinting system isn't built to do this
@overload
def pipe(val: A, f1: Callable[[A], B], f2: Callable[[B], C], f3: Callable[[C], D]) -> D: ... # I should really just codegen this
@overload
def pipe(val: A, f1: Callable[[A], B], f2: Callable[[B], C], f3: Callable[[C], D], f4: Callable[[D], E]) -> E: ...
@overload
def pipe(val: A, f1: Callable[[A], B], f2: Callable[[B], C], f3: Callable[[C], D], f4: Callable[[D], E], f5: Callable[[E], F]) -> F: ...
@overload
def pipe(val: A, f1: Callable[[A], B], f2: Callable[[B], C], f3: Callable[[C], D], f4: Callable[[D], E], f5: Callable[[E], F], f6: Callable[[F], G]) -> G: ...
@overload
def pipe(val: A, f1: Callable[[A], B], f2: Callable[[B], C], f3: Callable[[C], D], f4: Callable[[D], E], f5: Callable[[E], F], f6: Callable[[F], G], f7: Callable[[G], H]) -> H: ...
@overload
def pipe(val: A, f1: Callable[[A], B], f2: Callable[[B], C], f3: Callable[[C], D], f4: Callable[[D], E], f5: Callable[[E], F], f6: Callable[[F], G], f7: Callable[[G], H], f8: Callable[[H], I]) -> I: ...
@overload
def pipe(val: A, f1: Callable[[A], B], f2: Callable[[B], C], f3: Callable[[C], D], f4: Callable[[D], E], f5: Callable[[E], F], f6: Callable[[F], G], f7: Callable[[G], H], f8: Callable[[H], I], f9: Callable[[I], J]) -> J: ...
@overload
def pipe(val: A, f1: Callable[[A], B], f2: Callable[[B], C], f3: Callable[[C], D], f4: Callable[[D], E], f5: Callable[[E], F], f6: Callable[[F], G], f7: Callable[[G], H], f8: Callable[[H], I], f9: Callable[[I], J], f10: Callable[[J], K]) -> K: ...

def pipe(val, *funcs): # pyright: ignore[reportInconsistentOverload]
    for f in funcs:
        val = f(val)
    return val

