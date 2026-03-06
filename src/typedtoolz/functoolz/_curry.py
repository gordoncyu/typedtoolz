from cytoolz.functoolz import curry as _toolz_curry  # pyright: ignore[reportUnknownVariableType]
from typing import Any


def curry(pn_or_fn: Any, fn: Any = None, /) -> Any:  # pyright: ignore[reportAny, reportExplicitAny]
    """Curry a callable function.

    curry(fn) -> curried fn
    curry(n, fn) -> curried fn with arity (required positional arguments) hint n

    Enables partial application of arguments: call the function with an
    incomplete set of arguments and receive a new callable that accepts the
    rest.

    >>> def mul(x, y):
    ...     return x * y
    >>> mul = curry(mul)
    >>> double = mul(2)
    >>> double(10)
    20

    For keyword argument support beyond the required positionals, use
    :func:`typedtoolz.functoolz.curryv`.

    Delegates to toolz.functoolz.curry.
    """
    if fn is None:
        if callable(pn_or_fn):  # pyright: ignore[reportAny]
            return _toolz_curry(pn_or_fn)  # pyright: ignore[reportUnknownVariableType]
        return lambda f: _toolz_curry(f)  # pyright: ignore[reportUnknownVariableType, reportUnknownLambdaType]
    return _toolz_curry(fn)  # pyright: ignore[reportUnknownVariableType]


__all__ = [
        "curry",
        ]
