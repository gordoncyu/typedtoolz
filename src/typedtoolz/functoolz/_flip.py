# TODO: Review msc impl
from typing import Callable, Concatenate, ParamSpec, TypeVar
from typing_extensions import override
from typedtoolz.functoolz._curry import curry
from cytoolz.functoolz import flip as _flip

P = ParamSpec('P')
A = TypeVar('A')
B = TypeVar('B')
R = TypeVar('R')


class _flip_meta(type):
    @classmethod
    @override
    def __call__(cls, func: Callable[Concatenate[A, B, P], R]) -> Callable[Concatenate[B, A, P], R]:
        return _flip(func)


class _flip(metaclass=_flip_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    flip(func) -> func with first two arguments swapped

    Swap the order of the first two positional arguments of a function.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(1, _flip_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


flip = _flip  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["flip"]
