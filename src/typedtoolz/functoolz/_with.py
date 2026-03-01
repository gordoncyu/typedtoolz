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

class with_(metaclass=_with_meta):
    c = curry(_with_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]

    @staticmethod
    def p(
            res: Callable[Ps, ContextManager[A]],
            body: Callable[[A], R],
            ) -> Callable[Ps, R]:
        def inner(*args: Ps.args, **kwargs: Ps.kwargs):
            with res(*args, **kwargs) as val:
                return body(val)
        
        return inner
    
    pc = curry(p)  # pyright: ignore[reportUnannotatedClassAttribute]

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

class with_op(metaclass=_with_op_meta):
    c = curry(_with_op_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]

    @staticmethod
    def p(
            body: Callable[[A], R],
            res: Callable[Ps, ContextManager[A]],
            ) -> Callable[Ps, R]:
        def inner(*args: Ps.args, **kwargs: Ps.kwargs):
            with res(*args, **kwargs) as val:
                return body(val)
        
        return inner
    
    pc = curry(p)  # pyright: ignore[reportUnannotatedClassAttribute]
