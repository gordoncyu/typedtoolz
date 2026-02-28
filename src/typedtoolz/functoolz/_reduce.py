from typing import Callable, TypeVar, cast, get_args
from collections.abc import Iterable
from typing_extensions import overload, override
from typedtoolz.functoolz._curry import curry

A = TypeVar("A")
R = TypeVar("R")

_initial_missing = object()

# stolen from stdlib bcuz passing initial=foo would break if using the builtin
# for some reason the builtin behavior differs from the src behavior because dumb
# all so I can use pipe more ergonomically.
class _reduce_meta(type):
    @classmethod
    @overload
    def __call__(
            cls,
            function: Callable[[A, A], A],
            sequence: Iterable[A], 
            ) -> A: ...
    @classmethod
    @overload
    def __call__(
            cls,
            function: Callable[[R, A], R],
            sequence: Iterable[A], 
            initial: R = cast(R, _initial_missing),  # pyright: ignore[reportCallInDefaultInitializer]
            ) -> R: ...


    @staticmethod
    def _reduce(
            function: Callable[[A | R, A], R],
            initial: R,
            sequence: Iterable[A], 
            ) -> R:
        it = iter(sequence)

        if initial is _initial_missing:
            try:
                value = next(it)
            except StopIteration:
                raise TypeError("reduce() of empty sequence with no initial value") from None
        else:
            value = initial

        for element in it:
            value = function(value, element)

        return value  # pyright: ignore[reportReturnType]

    @classmethod
    @override
    def __call__(  # pyright: ignore[reportInconsistentOverload]
             cls,
            function: Callable[[A | R, A], R],
            sequence: Iterable[A], 
            initial: R = cast(R, _initial_missing),  # pyright: ignore[reportCallInDefaultInitializer]
            ) -> R:
        return cls._reduce(function, initial, sequence)

class reduce(metaclass=_reduce_meta):
    """
    reduce(function, iterable[, initial], /) -> value

    Apply a function of two arguments cumulatively to the items of an iterable, from left to right.

    This effectively reduces the iterable to a single value.  If initial is present,
    it is placed before the items of the iterable in the calculation, and serves as
    a default when the iterable is empty.

    For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5])
    calculates ((((1 + 2) + 3) + 4) + 5).

    Has curried versions as properties prefixed with c
    """
    c = curry(2, _reduce_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]
    ci = curry(_reduce_meta._reduce)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]

thing = reduce(
        lambda acc, v: acc + v,
        [1],
        2
        )

