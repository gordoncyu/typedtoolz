from typing import Callable, Concatenate, ParamSpec, TypeVar

P = ParamSpec('P')
A = TypeVar('A')
B = TypeVar('B')
R = TypeVar('R')

def flip(func: Callable[Concatenate[A, B, P], R]) -> Callable[Concatenate[B, A, P], R]: ...
