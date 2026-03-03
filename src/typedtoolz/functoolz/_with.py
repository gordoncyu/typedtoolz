from io import TextIOBase, UnsupportedOperation
from typing import Callable, ContextManager, Literal, ParamSpec, TypeVar, cast
from typing_extensions import overload, override
from typedtoolz import identityv
from typedtoolz.functoolz._curry import curry
from typedtoolz.utils import is_context_manager, is_zero_required_callable


A = TypeVar("A")
R = TypeVar("R")
Ps = ParamSpec("Ps")

class _with_meta(type):
    @staticmethod
    @override
    def __call__(
            res: (
                ContextManager[A] 
                | Callable[[], ContextManager[A]]
                ),
            body: Callable[[A], R],
            ) -> R:
        if is_context_manager(res):
            with res as val:
                return body(val)
        with res() as val:
            return body(val)

class _with_(metaclass=_with_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/master/docs/typing_bs/metaclass_static_callables.md
    """Open a context manager and pass the managed value to body.

    with_(res, body) -> R

    res may be a ContextManager directly or a zero-argument callable that
    produces one. body receives the value yielded by __enter__.

    Has curried versions as the properties c and pc (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(_with_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]

    @staticmethod
    def p(
            res: Callable[Ps, ContextManager[A]],
            body: Callable[[A], R],
            ) -> Callable[Ps, R]:
        """Create a callable that opens res(*args) and passes the value to body.

        with_.p(res, body) -> Callable[Ps, R]

        res is a parametrized context manager factory; the returned callable
        accepts the same arguments and applies body inside the context.
        """
        def inner(*args: Ps.args, **kwargs: Ps.kwargs):
            with res(*args, **kwargs) as val:
                return body(val)
        
        return inner
    
    pc = curry(p)  # pyright: ignore[reportUnannotatedClassAttribute]

with_ = _with_  # why? See: https://github.com/gordoncyu/typedtoolz/blob/master/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

class _with_op_meta(type):
    @staticmethod
    @override
    def __call__(
            body: Callable[[A], R],
            res: (
                ContextManager[A] 
                | Callable[[], ContextManager[A]]
                ),
            ) -> R:
        if is_context_manager(res):
            with res as val:
                return body(val)
        with res() as val:
            return body(val)

class _with_op(metaclass=_with_op_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/master/docs/typing_bs/metaclass_static_callables.md
    """Open a context manager and pass the managed value to body (body-first argument order).

    with_op(body, res) -> R

    res may be a ContextManager directly or a zero-argument callable that
    produces one. body receives the value yielded by __enter__.

    Argument order is flipped relative to with_ — body comes first, res second
    — which makes it more natural to curry body before supplying the resource.

    Has curried versions as the properties c and pc (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(_with_op_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]

    @staticmethod
    def p(
            body: Callable[[A], R],
            res: Callable[Ps, ContextManager[A]],
            ) -> Callable[Ps, R]:
        """Create a callable that opens res(*args) and passes the managed value to body.

        with_op.p(body, res) -> Callable[Ps, R]

        res is a parametrized context manager factory; the returned callable
        accepts the same arguments and applies body inside the context.

        Argument order is flipped relative to with_.p — body comes first, res
        second.
        """
        def inner(*args: Ps.args, **kwargs: Ps.kwargs):
            with res(*args, **kwargs) as val:
                return body(val)
        
        return inner
    
    pc = curry(p)  # pyright: ignore[reportUnannotatedClassAttribute]

with_op = _with_op  # why? See: https://github.com/gordoncyu/typedtoolz/blob/master/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = [
        "with_",
        "with_op",
        ]
