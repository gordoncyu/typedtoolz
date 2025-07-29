from typing import Any, Callable, Mapping, ParamSpec, TypeVar, TypeVarTuple, TypedDict, Unpack

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
L = TypeVar("L")
M = TypeVar("M")
N = TypeVar("N")
O = TypeVar("O")
P = TypeVar("P")
Q = TypeVar("Q")
R = TypeVar("R")
S = TypeVar("S")
T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
W = TypeVar("W")
X = TypeVar("X")
Y = TypeVar("Y")
Z = TypeVar("Z")

Ts = TypeVarTuple("Ts")
Ps = ParamSpec("Ps")

def identity(x: A) -> A:
    return x

def identityv(*args: *Ts) -> tuple[*Ts]:
    return args

def return_none(*_: TypeVarTuple, **__: object) -> None:
    return None
