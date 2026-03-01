from toolz.functoolz import curry as _toolz_curry
from typing import Any

def curryv(_, f: Any): # pyright: ignore[reportAny, reportExplicitAny] # purely for pyright, further defined in stub files
    """Curry a callable function, with n specifying the arity (required positional arguments).

    curryv(n, fn) -> curried fn

    Enables partial application of arguments: call the function with an
    incomplete set of arguments and receive a new callable that accepts the
    rest.

    >>> def mul(x, y):
    ...     return x * y
    >>> mul = curryv(2, mul)
    >>> double = mul(2)
    >>> double(10)
    20

    n tells the type checker how many positional arguments are required to
    trigger the call; parameters beyond position n are treated as optional
    positionals or keyword arguments and are passed through unchanged:

    >>> @curryv(2)
    ... def f(x, y, a=10):
    ...     return a * (x + y)
    >>> add = f(a=1)
    >>> add(2, 3)
    5

    n is consumed only by the type stubs (Pyright); at runtime this delegates
    directly to toolz.functoolz.curry(f).

    See also: :func:`typedtoolz.functoolz.curry`.
    """
    return _toolz_curry(f) # pyright: ignore[reportAny]

__all__ = [
        "curryv",
        ]
