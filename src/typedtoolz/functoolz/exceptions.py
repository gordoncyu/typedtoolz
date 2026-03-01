from typing import Any, Callable, Literal, ParamSpec, TypeVar, get_args
from typing_extensions import override
from typedtoolz import identity
from typedtoolz.functoolz._curry import curry
from functools import wraps
import logging


logger = logging.getLogger(__name__)

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

class _tuple_error_meta(type):
    @staticmethod
    @override
    def __call__(
            exc: type[E] | tuple[type[E]],
            func: Callable[Ps, B],
            ) -> Callable[Ps, tuple[Literal[True], B] | tuple[Literal[False], E]]:
        @wraps(func)
        def inner(*args: Ps.args, **kwargs: Ps.kwargs):
            return (True, func(*args, **kwargs))
        def handler(e: E):
            return (False, e)
        return excepts(handler, exc, inner)

class tuple_error(metaclass=_union_error_meta):
    c = curry(_tuple_error_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]

class _remap_error_meta(type):
    @staticmethod
    @override
    def __call__(
            handler: Callable[[E], BaseException | tuple[str, BaseException]],
            exc: type[E] | tuple[type[E]],
            func: Callable[Ps, B],
            logger_method: Callable[[str], Any] = logger.error,  # pyright: ignore[reportExplicitAny]
            ) -> Callable[Ps, B]:
        @wraps(func)
        def wrapper(*args: Ps.args, **kwargs: Ps.kwargs) -> B:
            try:
                return func(*args, **kwargs)
            except exc as err:
                match handler(err):
                    case (log, remapped):
                        logger_method(log)
                    case remapped: ...
                raise remapped

        return wrapper

class remap_error(metaclass=_union_error_meta):
    c = curry(_remap_error_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]

__all__ = [
        "excepts",
        "union_error",
        "tuple_error",
        "remap_error",
        ]
