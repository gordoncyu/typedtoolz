from cytoolz.functoolz import curry as _toolz_curry  # pyright: ignore[reportUnknownVariableType]
from typing import Any

def curryv(n: Any, /):  # pyright: ignore[reportAny, reportExplicitAny]
    """Curry a callable function, with n specifying the arity (required positional arguments).

    curryv(n) -> maker: callable that accepts fn (and optional pre-applied args)
    curryv(n)(fn) -> curried fn
    curryv(n)(fn, a1, a2, **kw) -> curried fn with a1, a2, kw pre-applied

    Enables partial application of arguments: call the function with an
    incomplete set of arguments and receive a new callable that accepts the
    rest.

    >>> def mul(x, y):
    ...     return x * y
    >>> double = curryv(2)(mul, 2)
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
    if not isinstance(n, int):
        raise TypeError(f"curryv() first argument must be int, got {type(n).__name__!r}")

    def maker(fn: Any, /, *pre_args: Any, **pre_kwargs: Any) -> Any:  # pyright: ignore[reportAny, reportExplicitAny]
        return _toolz_curry(fn, *pre_args, **pre_kwargs)  # pyright: ignore[reportUnknownVariableType]
    return maker

__all__ = [
        "curryv",
        ]
