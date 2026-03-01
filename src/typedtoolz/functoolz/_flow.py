from typing import Any, Callable, TypeVar


T = TypeVar("T")
def flow(fn: Callable[[T], Any], *fns: Callable[[Any], Any]) -> Callable[[T], Any]:
    """Compose functions to operate in series, left to right.

    Returns a function that applies each function in sequence so that
    ``flow(f, g, h)(x)`` is the same as ``h(g(f(x)))``.

    >>> inc = lambda i: i + 1
    >>> flow(inc, str)(3)
    '4'

    See Also:
        pipe
    """
    def composed(x: T) -> Any:
        x = fn(x)
        for f in fns:
            x = f(x)
        return x
    return composed

__all__ = [
        "flow",
        ]
