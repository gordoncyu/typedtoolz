from cytoolz.functoolz import curry as _toolz_curry  # pyright: ignore[reportUnknownVariableType]
from typing import Any


def curry(pn_or_fn: Any, /, *args: Any, **kwargs: Any) -> Any:  # pyright: ignore[reportAny, reportExplicitAny]
    """Curry a callable function.

    curry(fn) -> curried fn
    curry(fn, a1, a2, **kw) -> curried fn with a1, a2, kw pre-applied
    curry(n) -> maker: callable that accepts fn (and optional pre-applied args)

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
    if callable(pn_or_fn):  # pyright: ignore[reportAny]
        return _toolz_curry(pn_or_fn, *args, **kwargs)  # pyright: ignore[reportUnknownVariableType]

    if not isinstance(pn_or_fn, int):
        raise TypeError(f"curry() first argument must be callable or int, got {type(pn_or_fn).__name__!r}")

    if len(args) + len(kwargs) != 0:
        raise ValueError("curry(int) cannot take any more arguments")
    # pn_or_fn is an arity hint int — return a maker
    def maker(fn: Any, /, *pre_args: Any, **pre_kwargs: Any) -> Any:  # pyright: ignore[reportAny, reportExplicitAny]
        return _toolz_curry(fn, *pre_args, **pre_kwargs)  # pyright: ignore[reportUnknownVariableType]
    return maker


__all__ = [
        "curry",
        ]
