from toolz.functoolz import curry as _toolz_curry
from typing import Any


def curry(pn_or_fn: Any, fn: Any = None, /) -> Any:  # pyright: ignore[reportAny, reportExplicitAny]
    if fn is None:
        return _toolz_curry(pn_or_fn)  # pyright: ignore[reportAny]
    return _toolz_curry(fn)  # pyright: ignore[reportAny]


__all__ = ["curry"]
