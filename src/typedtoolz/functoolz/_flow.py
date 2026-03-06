from cytoolz import compose_left
from typing import Any, Callable, TypeVar


T = TypeVar("T")
def flow(fn: Callable[[T], Any], *fns: Callable[[Any], Any]) -> Callable[[T], Any]:  # pyright: ignore[reportExplicitAny]
    """Compose functions to operate in series, left to right.

    Returns a function that applies each function in sequence so that
    ``flow(f, g, h)(x)`` is the same as ``h(g(f(x)))``.

    >>> inc = lambda i: i + 1
    >>> flow(inc, str)(3)
    '4'

    See Also:
        pipe
    """
    return compose_left(fn, *fns)  # pyright: ignore[reportCallIssue, reportUnknownVariableType]

__all__ = [
        "flow",
        ]
