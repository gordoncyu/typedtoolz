from __future__ import annotations

from types import EllipsisType
from typing import Any, Callable, ParamSpec, Protocol, TypeVar
from typing_extensions import override
from typedtoolz.functoolz._curry import curry

from typedtoolz.utils import is_zero_required_callable

A = TypeVar("A")
E = TypeVar("E")
R = TypeVar("R")

Ps = ParamSpec("Ps")
PBody = ParamSpec("PBody")
PEnd = ParamSpec("PEnd")

class _defer_meta(type):
    @staticmethod
    @override
    def __call__(
            end: Callable[[], object],
            body: Callable[[], R],
            ) -> R:
        try:
            return body()
        finally:
            end()

class _defer_hof_meta(type):
    @staticmethod
    @override
    def __call__(
        end: Callable[[], Any] | Callable[[R | EllipsisType], Any],  # pyright: ignore[reportExplicitAny]
        body: Callable[PBody, R],
        /,
    ) -> Callable[PBody, R]:
        def inner(*bargs: PBody.args, **bkwargs: PBody.kwargs) -> R:
            br = ...
            try:
                res = body(*bargs, **bkwargs)
                br = res
                return res
            finally:
                if is_zero_required_callable(end):
                    end()
                else:
                    end(br)  # pyright: ignore[reportCallIssue]
        return inner

BR = TypeVar("BR", contravariant=True)
class AcceptsBodyReturn(Protocol[BR, Ps]):
    def __call__(self, defer_body_return: BR | EllipsisType, /, *args: Ps.args, **kwargs: Ps.kwargs) -> Any: ... # pyright: ignore[reportExplicitAny, reportAny]

class _defer_hof_defer_args_meta(type):
    @staticmethod
    @override
    def __call__(
        end: AcceptsBodyReturn[R, PEnd],
        body: Callable[PBody, R],
        /,
    ) -> Callable[PEnd, Callable[PBody, R]]:
        def earg_acc(*eargs: PEnd.args, **ekwargs: PEnd.kwargs) -> Callable[PBody, R]:
            def barg_acc(*bargs: PBody.args, **bkwargs: PBody.kwargs) -> R:
                br = ...
                try:
                    res = body(*bargs, **bkwargs)
                    br = res
                    return res
                finally:
                    end(br, *eargs, **ekwargs)
            return barg_acc
        return earg_acc

class _defer(metaclass=_defer_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """Run body(), calling end() in a finally block regardless of outcome.

    defer(end, body) -> R

    end is a zero-argument callable. body is a zero-argument callable whose
    return value is passed through. Analogous to a try/finally block.

    Has a curried version as the property c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(_defer_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]
    class hof(metaclass=_defer_hof_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
        """Wrap body so that end is called after each invocation.

        defer.hof(end, body) -> Callable[PBody, R]

        end may be zero-argument, or accept a single argument: the body's
        return value (or ``...`` if the body raised an exception).

        Has a curried version as the property c (see :func:`typedtoolz.functoolz.curry`).
        """
        class defer_args(metaclass=_defer_hof_defer_args_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
            """Wrap body with a deferred end that also captures extra arguments.

            defer.hof.defer_args(end, body) -> Callable[PEnd, Callable[PBody, R]]

            Returns a two-stage callable: first call captures the arguments for
            end; second call wraps body and invokes end(body_result, *eargs,
            **ekwargs) in a finally block.

            Has a curried version as the property c (see :func:`typedtoolz.functoolz.curry`).
            """
            c = curry(_defer_hof_defer_args_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]

        c = curry(_defer_hof_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]

defer = _defer  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = [
        "defer",
        ]
