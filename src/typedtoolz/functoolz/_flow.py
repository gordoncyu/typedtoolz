from typing import Any, Callable, TypeVar


T = TypeVar("T")
def flow(fn: Callable[[T], Any], *fns: Callable[[Any], Any]) -> Callable[[T], Any]:
    def composed(x: T) -> Any:
        for f in fns:
            x = f(x)
        return x
    return composed
