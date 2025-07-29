from typing import Callable, Concatenate, ParamSpec, TypeVar, TypeVarTuple, Union
from typedtoolz import identity
from typedtoolz.functoolz.bring import bring
from typedtoolz.functoolz.curry import Curried3, curry
from toolz.functoolz import excepts as ex
from typedtoolz.functoolz import wlth

from typedtoolz.functoolz.pipe import pipe

A = TypeVar('A')
B = TypeVar('B')
D = TypeVar('D')
E = TypeVar('E')

Ts = TypeVarTuple('Ts')

Ps = ParamSpec("Ps")

def _excepts(
    handler: Callable[[E], D],
    exc: type[E] | tuple[type[E], ...],  # ✅ accepts one or many
    func: Callable[Ps, B],
) -> Callable[Ps, B | D]: ...

excepts = curry(_excepts)

union_error = excepts(identity)
safe_read = union_error(type[MemoryError], lambda path: wlth(open(path), lambda f: f.read))
thing = safe_read("asdfas")
