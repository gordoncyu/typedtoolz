from typing import Callable, TypeVar, TypeVarTuple

Ts = TypeVarTuple("Ts")
R = TypeVar("R")

def star(f: Callable[[*Ts], R]) -> Callable[[tuple[*Ts]], R]:
    def starred(args: tuple[*Ts]):
        return f(*args)
    return starred

def unstar(f: Callable[[tuple[*Ts]], R]) -> Callable[[*Ts], R]:
    def unstarred(*args: *Ts):
        return f(args)
    return unstarred
