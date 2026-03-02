from typing import Callable, ParamSpec

P = ParamSpec('P')

def complement(func: Callable[P, object]) -> Callable[P, bool]: ...
