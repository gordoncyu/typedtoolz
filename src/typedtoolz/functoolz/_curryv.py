from toolz.functoolz import curry as _toolz_curry
from typing import Any

def curryv(_, f: Any): # pyright: ignore[reportAny, reportExplicitAny] # purely for pyright, further defined in stub files
    return _toolz_curry(f) # pyright: ignore[reportAny]

__all__ = [
        "curryv",
        ]
