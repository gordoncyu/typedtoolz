# USES ANY
from typing import Callable, ParamSpec, TypeVar, cast

from typedtoolz.functoolz._curryv import curryv

P = ParamSpec('P')
R = TypeVar('R')

# The most common usecase for memoize is in its curried form, and it would be obtrusive to use it like @memoize.c, hence no .c property
def _memoize_base(func: Callable[P, R], cache: dict[object, object] | None = ..., key: Callable[..., object] | None = ...) -> Callable[[Callable[P, R]], Callable[P, R]]: ...

memoize = curryv(1, _memoize_base)
""" Cache a function's result for speedy future evaluation

Considerations:
    Trades memory for speed.
    Only use on pure functions.

>>> def add(x, y):  return x + y
>>> add = memoize(add)

Or use as a decorator

>>> @memoize
... def add(x, y):
...     return x + y

Use the ``cache`` keyword to provide a dict-like object as an initial cache

>>> @memoize(cache={(1, 2): 3})
... def add(x, y):
...     return x + y

Note that the above works as a decorator because ``memoize`` is curried.

It is also possible to provide a ``key(args, kwargs)`` function that
calculates keys used for the cache, which receives an ``args`` tuple and
``kwargs`` dict as input, and must return a hashable value.  However,
the default key function should be sufficient most of the time.

>>> # Use key function that ignores extraneous keyword arguments
>>> @memoize(key=lambda args, kwargs: args)
... def add(x, y, verbose=False):
...     if verbose:
...         print('Calculating %s + %s' % (x, y))
...     return x + y
"""

