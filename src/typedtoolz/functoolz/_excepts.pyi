from typing import Callable, ParamSpec, TypeVar, TypeVarTuple
from typedtoolz import identity
from typedtoolz.functoolz._curry import curry
from toolz.functoolz import excepts as ex
from typedtoolz.functoolz import wlth

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
