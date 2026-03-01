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
    """Wrap func to catch exc and pass the exception to handler.

    excepts(handler, exc, func) -> Callable[Ps, B | D]

    When func raises an exception matching exc, handler is called with the
    exception and its return value is substituted for the normal return.

    Has a curried version as the property c (see :func:`typedtoolz.functoolz.curry`).
    """
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
    """Wrap func so that a caught exception is returned rather than raised.

    union_error(exc, func) -> Callable[Ps, B | E]

    On success returns the normal result; on a matching exception returns the
    exception instance as a value, making the error visible in the return type.

    Has a curried version as the property c (see :func:`typedtoolz.functoolz.curry`).
    """
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

class tuple_error(metaclass=_tuple_error_meta):
    """Wrap func to return a success/failure tuple instead of raising.

    tuple_error(exc, func) -> Callable[Ps, tuple[True, B] | tuple[False, E]]

    Returns ``(True, result)`` on success or ``(False, exception)`` on a
    matching exception, allowing the caller to branch on the first element.

    Has a curried version as the property c (see :func:`typedtoolz.functoolz.curry`).
    """
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

class remap_error(metaclass=_remap_error_meta):
    """Wrap func to catch exc, remap it via handler, and re-raise the remapped exception.

    remap_error(handler, exc, func[, logger_method]) -> Callable[Ps, B]

    handler receives the caught exception and must return either:
      - a new exception to raise directly, or
      - ``(message, exception)`` to log message before raising.

    Has a curried version as the property c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(_remap_error_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]

__all__ = [
        "excepts",
        "union_error",
        "tuple_error",
        "remap_error",
        ]
