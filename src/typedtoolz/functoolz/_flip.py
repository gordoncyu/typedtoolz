from typing import Callable, Concatenate, ParamSpec, TypeVar
from typing_extensions import override
from cytoolz.functoolz import flip as cyflip  # pyright: ignore[reportUnknownVariableType]

P = ParamSpec('P')
A = TypeVar('A')
B = TypeVar('B')
R = TypeVar('R')


class _flip_meta(type):
    @classmethod
    @override
    def __call__(cls, func: Callable[Concatenate[A, B, P], R]) -> Callable[Concatenate[B, A, P], R]:
        return cyflip(func)  # pyright: ignore[reportUnknownVariableType]


class _flip(metaclass=_flip_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    flip(func) -> func with first two arguments swapped

    Swap the order of the first two positional arguments of a function.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """


flip = _flip  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["flip"]
