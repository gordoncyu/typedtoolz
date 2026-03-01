from itertools import takewhile
from typing import Any, Callable, ParamSpec, Protocol, TypeIs, ContextManager, TypeVar, TypeVarTuple, get_args
import inspect
from inspect import Parameter
from typing_extensions import TypeGuard


Ps = ParamSpec("Ps")
R = TypeVar("R")

def is_context_manager(obj: Any) -> TypeIs[ContextManager[Any]]:  # pyright: ignore[reportExplicitAny, reportAny]
    t = type(obj)  # pyright: ignore[reportAny, reportUnknownVariableType]
    return (
        getattr(t, "__enter__", None) is not None  # pyright: ignore[reportUnknownArgumentType]
        and getattr(t, "__exit__", None) is not None  # pyright: ignore[reportUnknownArgumentType]
    )

def required_positional_arity(fn: Callable[Ps, Any]) -> int:  # pyright: ignore[reportExplicitAny]
    return len(tuple(takewhile(
        lambda p: (
            p.kind in (
                Parameter.POSITIONAL_ONLY,
                Parameter.POSITIONAL_OR_KEYWORD,
                )
            and p.default is Parameter.empty  # pyright: ignore[reportAny]
            ),
        inspect.signature(fn).parameters.values(),
        )))

def is_zero_required_callable(fn: Callable[..., R]) -> TypeGuard[Callable[[], R]]:
    return not any(
            (
                p.kind in (
                    Parameter.POSITIONAL_ONLY,
                    Parameter.POSITIONAL_OR_KEYWORD,
                    )
                and p.default is Parameter.empty   # pyright: ignore[reportAny]
                ) for p in inspect.signature(fn).parameters.values()
            )

