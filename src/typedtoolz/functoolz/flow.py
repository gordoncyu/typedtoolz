from typing import Any, Callable


def flow(*fns: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def composed(x: Any) -> Any:
        for f in fns:
            x = f(x)
        return x
    return composed
