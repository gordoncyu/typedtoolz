from typing import Callable, ParamSpec, TypeVar, get_args
from typing_extensions import override
from typedtoolz import identity
from typedtoolz.functoolz._curry import curry
from functools import wraps

A = TypeVar('A')
B = TypeVar('B')
D = TypeVar('D')
E = TypeVar('E')

Ps = ParamSpec("Ps")

class _excepts_meta(type):
    @staticmethod
    @override
    def __call__(
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

class excepts(metaclass=_excepts_meta):
    c = curry(_excepts_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


class _union_error_meta(type):
    @staticmethod
    @override
    def __call__(
            exc: type[E] | tuple[type[E]],
            func: Callable[Ps, B],
            ) -> Callable[Ps, B | E]:
        return excepts(identity, exc, func)

class union_error(metaclass=_union_error_meta):
    c = curry(_union_error_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]

