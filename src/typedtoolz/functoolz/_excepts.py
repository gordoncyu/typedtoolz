from typing import Callable, ParamSpec, TypeVar, TypeVarTuple
from typedtoolz import identity
from typedtoolz.functoolz.curry import curry
from toolz.functoolz import excepts as ex

A = TypeVar('A')
B = TypeVar('B')
D = TypeVar('D')
E = TypeVar('E')

Ps = ParamSpec("Ps")
from functools import wraps
def _union_error(exc, func):
    return _excepts(exc, identity, func)

union_error = curry(_union_error)

def _excepts(
    handler: Callable[[E], D],
    exc: type[E] | tuple[type[E]],
    func: Callable[Ps, B],
) -> Callable[Ps, B | D]:
    @wraps(func)
    def wrapper(*args: Ps.args, **kwargs: Ps.kwargs) -> B | D:
        try:
            return func(*args, **kwargs)
        except exc as err:
            return handler(err)

    return wrapper

excepts = curry(_excepts)

excepts_any = excepts(BaseException, identity)
_ = excepts_any(lambda: 1)()

