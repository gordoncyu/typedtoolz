from toolz.functoolz import curry
from typing import Any

def curryv(_, f: Any): # pyright: ignore[reportAny, reportExplicitAny] # purely for pyright, further defined in stub files
    return curry(f) # pyright: ignore[reportAny]
