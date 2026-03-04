from typing import Callable, TypeVar, cast, get_args
from collections.abc import Iterable
from typing_extensions import overload, override
from typedtoolz.functoolz._curryv import curryv
from functools import reduce as cyreduce

A = TypeVar("A")
R = TypeVar("R")

_initial_missing = object()

# stolen from stdlib bcuz passing initial=foo would break if using the builtin
# for some reason the builtin behavior differs from the src behavior because dumb
# all so I can use pipe more ergonomically.
class _reduce_meta(type):
    # Following __call__ overloads structured to be compatible with functools.reduce
    @staticmethod
    @overload
    def __call__(
            function: Callable[[A, A], A],
            sequence: Iterable[A], 
            ) -> A: ...
    @staticmethod
    @overload
    def __call__(
            function: Callable[[R, A], R],
            sequence: Iterable[A], 
            initial: R = cast(R, _initial_missing),  # pyright: ignore[reportCallInDefaultInitializer]
            ) -> R: ...

    @staticmethod
    @override
    def _reduce( # Because you can't pick a specific override to pass to a function this is a copy of the below
            function: Callable[[A | R, A], R],
            sequence: Iterable[A], 
            initial: R = cast(R, _initial_missing),  # pyright: ignore[reportCallInDefaultInitializer]
            ) -> R:
        if initial is _initial_missing:
            return cyreduce(function, sequence)  # pyright: ignore[reportReturnType, reportArgumentType]
        else:
            return cyreduce(function, sequence, initial)

    @staticmethod
    @override
    def __call__(  # pyright: ignore[reportInconsistentOverload]
            function: Callable[[A | R, A], R],
            sequence: Iterable[A], 
            initial: R = cast(R, _initial_missing),  # pyright: ignore[reportCallInDefaultInitializer]
            ) -> R:
        if initial is _initial_missing:
            return cyreduce(function, sequence)  # pyright: ignore[reportReturnType, reportArgumentType]
        else:
            return cyreduce(function, sequence, initial)

class _reduce(metaclass=_reduce_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    reduce(function, iterable[, initial], /) -> value

    Apply a function of two arguments cumulatively to the items of an iterable, from left to right.

    This effectively reduces the iterable to a single value.  If initial is present,
    it is placed before the items of the iterable in the calculation, and serves as
    a default when the iterable is empty.

    For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5])
    calculates ((((1 + 2) + 3) + 4) + 5).

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curryv(2, _reduce_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]

reduce = _reduce  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = [
        "reduce",
        ]
