from typing import Callable, Concatenate, ParamSpec, TypeVar, cast, overload
from typing_extensions import override
from cytoolz.functoolz import flip as cyflip

from typedtoolz.utils import no_default  # pyright: ignore[reportUnknownVariableType]

P = ParamSpec('P')
A = TypeVar('A')
B = TypeVar('B')
R = TypeVar('R')


class _flip_meta(type):
    @classmethod
    @overload
    def __call__(cls, func: Callable[Concatenate[B, A, P], R], a: A = ..., b: B = ...) -> Callable[Concatenate[B, A, P], R]: ...  # pyright: ignore[reportInconsistentOverload]
    @classmethod
    @override
    def __call__(cls, func: Callable[Concatenate[B, A, P], R], a: A = cast(A, no_default), b: B = cast(A, no_default)) -> Callable[Concatenate[B, A, P], R]:  # pyright: ignore[reportCallInDefaultInitializer]
        a_here = a is not no_default
        if b is not no_default and a_here:
            return cyflip(func, a, b)  # pyright: ignore[reportUnknownVariableType]
        if a_here:
            return cyflip(func, a)  # pyright: ignore[reportUnknownVariableType]
        return cyflip(func)  # pyright: ignore[reportUnknownVariableType]


class _flip(metaclass=_flip_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    flip(func) -> func with first two arguments swapped

    Swap the order of the first two positional arguments of a function.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """


flip = _flip  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

flip(int.__add__)

__all__ = ["flip"]
