from typing import TypeVar, TypeVarTuple

A = TypeVar("A")
Ts = TypeVarTuple("Ts")

def identity(x: A) -> A:
    """Return x unchanged."""
    return x

def identityv(*args: *Ts) -> tuple[*Ts]:
    """Return all positional arguments as a tuple, unchanged."""
    return args

def return_none(*_: TypeVarTuple, **__: object) -> None:  # pyright: ignore[reportUnusedParameter]
    """Accept any arguments and return None."""
    return None
