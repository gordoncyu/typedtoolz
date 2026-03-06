from typing import Callable, TypeVar
from typing_extensions import ParamSpec

R = TypeVar("R")
Ps = ParamSpec("Ps")

def apply(func: Callable[Ps, R], *args: Ps.args, **kwargs: Ps.kwargs) -> R: ...
