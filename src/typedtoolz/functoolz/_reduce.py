from typing import Callable, TypeVar, Iterable
from typedtoolz.functoolz.curry import curry

A = TypeVar("A")
R = TypeVar("R")

_initial_missing = object() # instead of a propper bottom value, a unique object
# is used because people use the bottom value "None" too much to mean other things
# this is straight from the stdlib bro, man python makes you do some wild stuff

# stolen from stdlib bcuz passing initial=foo would break if using the builtin
# for some reason the builtin behavior differs from the src behavior because dumb
# all so I can use pipe more ergonomically. Gosh if I had to wrap everything in 
# lambdas everywhere that would be pain.
def _reduce(
    function: Callable[[A, A], A],
    sequence: Iterable[A],
) -> A:
    it = iter(sequence)
    try:
        value = next(it)
    except StopIteration:
        raise TypeError("reduce() of empty iterable with no initial value") from None
    return _reduced(function, value, it)

def _reduced(function: Callable[[R, A], R], initial: R, sequence: Iterable[A]) -> R:
    it = iter(sequence)

    value = initial
    for element in it:
        value = function(value, element)

    return value

reduce = curry(_reduce)
reduced = curry(_reduced)
