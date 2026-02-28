"""
return_parameter — decorators for the "return parameter" pattern.

A *return parameter* (rp) is a mutable accumulator passed into a function
that the function writes into, rather than returning a fresh value.  These
decorators hide the rp from callers: the factory creates it, the decorated
function fills it, and the wrapper returns it.

Recursive functions are supported transparently.  Because ``@decorator``
rebinds the function name, every recursive self-call goes through the
wrapper.  A ``threading.local`` slot carries the live rp across the call
stack so recursive calls reuse it instead of creating a fresh one.

Two top-level classes, ``first`` and ``last``, select which positional
parameter is the rp.  Each exposes three decorators:

``only(rp_factory)``
    The function's return value is ignored; the rp is the sole output.
    ``f(rp, *args) -> Any``  →  ``(*args) -> RP``

``joined.in_tuple(rp_factory)``
    The function returns a scalar alongside the rp.
    ``f(rp, *args) -> R``  →  ``(*args) -> tuple[RP, R]``

``joined.with_tuple(rp_factory)``
    The function returns a tuple that is spliced after the rp.
    ``f(rp, *args) -> tuple[*RTs]``  →  ``(*args) -> tuple[RP, *RTs]``

For ``last``, the rp is the *last* positional parameter; signatures are
``f(*args, rp)`` instead of ``f(rp, *args)``.

Examples::

    @last.only(list)
    def flatten(items: list, acc: list[int]) -> None:
        for item in items:
            if isinstance(item, list):
                flatten(item)   # recursive — reuses the same acc
            else:
                acc.append(item)

    flatten([[1, [2, 3]], 4])   # → [1, 2, 3, 4]


    @first.joined.in_tuple(dict)
    def index(acc: dict[str, int], pairs: list[tuple[str, int]]) -> int:
        for k, v in pairs:
            acc[k] = v
        return len(pairs)

    mapping, count = index([("a", 1), ("b", 2)])  # → {"a":1,"b":2}, 2
"""

import threading
from functools import wraps, reduce
from typing import Any, TypeVar, TypeVarTuple, Callable

PTs = TypeVarTuple("PTs")
RTs = TypeVarTuple("RTs")
RP = TypeVar("RP")
R = TypeVar("R")


class first:
    """Decorators where the *first* positional parameter is the return parameter."""

    @staticmethod
    def only(rp_factory: Callable[[], RP]):
        """Hide the rp; return it as the sole output.

        ``f(rp, *args) -> Any``  →  ``(*args) -> RP``
        """
        def inner(f: Callable[[RP, *PTs], Any]) -> Callable[[*PTs], RP]: # pyright: ignore[reportExplicitAny]
            _local = threading.local()
            @wraps(f)
            def innermost(*args):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
                if hasattr(_local, '_rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0'):
                    f(_local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0, *args)  # pyright: ignore[reportArgumentType, reportAny]
                    return _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0  # pyright: ignore[reportAny]
                _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0 = rp_factory()
                try:
                    f(_local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0, *args)  # pyright: ignore[reportArgumentType]
                finally:
                    rp = _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0
                    del _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0
                return rp
            return innermost  # pyright: ignore[reportUnknownVariableType]
        return inner

    class joined:
        """Decorators that include the rp alongside the function's own return value."""

        @staticmethod
        def in_tuple(rp_factory: Callable[[], RP]):
            """Return ``(rp, r)`` where ``r`` is the function's scalar return value.

            ``f(rp, *args) -> R``  →  ``(*args) -> tuple[RP, R]``
            """
            def inner(f: Callable[[RP, *PTs], R]) -> Callable[[*PTs], tuple[RP, R]]:
                _local = threading.local()
                @wraps(f)
                def innermost(*args):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
                    if hasattr(_local, '_rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0'):
                        r = f(_local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0, *args)  # pyright: ignore[reportArgumentType, reportAny]
                        return (_local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0, r)  # pyright: ignore[reportAny]
                    _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0 = rp_factory()
                    try:
                        r = f(_local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0, *args)  # pyright: ignore[reportArgumentType]
                    finally:
                        rp = _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0
                        del _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0
                    return (rp, r)
                return innermost  # pyright: ignore[reportUnknownVariableType]
            return inner

        @staticmethod
        def with_tuple(rp_factory: Callable[[], RP]):
            """Return ``(rp, *r)`` where ``r`` is the function's tuple return value.

            ``f(rp, *args) -> tuple[*RTs]``  →  ``(*args) -> tuple[RP, *RTs]``
            """
            def inner(f: Callable[[RP, *PTs], tuple[*RTs]]) -> Callable[[*PTs], tuple[RP, *RTs]]:
                _local = threading.local()
                @wraps(f)
                def innermost(*args):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
                    if hasattr(_local, '_rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0'):
                        r = f(_local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0, *args)  # pyright: ignore[reportArgumentType, reportAny]
                        return (_local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0, *r)  # pyright: ignore[reportAny]
                    _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0 = rp_factory()
                    try:
                        r = f(_local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0, *args)  # pyright: ignore[reportArgumentType]
                    finally:
                        rp = _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0
                        del _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0
                    return (rp, *r)
                return innermost  # pyright: ignore[reportUnknownVariableType]
            return inner


class last:
    """Decorators where the *last* positional parameter is the return parameter."""

    @staticmethod
    def only(rp_factory: Callable[[], RP]):
        """Hide the rp; return it as the sole output.

        ``f(*args, rp) -> Any``  →  ``(*args) -> RP``
        """
        def inner(f: Callable[[*PTs, RP], Any]) -> Callable[[*PTs], RP]: # pyright: ignore[reportExplicitAny]
            _local = threading.local()
            @wraps(f)
            def innermost(*args):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
                if hasattr(_local, '_rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0'):
                    f(*args, _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0)  # pyright: ignore[reportArgumentType, reportAny]
                    return _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0  # pyright: ignore[reportAny]
                _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0 = rp_factory()
                try:
                    f(*args, _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0)  # pyright: ignore[reportArgumentType]
                finally:
                    rp = _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0
                    del _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0
                return rp
            return innermost  # pyright: ignore[reportUnknownVariableType]
        return inner

    class joined:
        """Decorators that include the rp alongside the function's own return value."""

        @staticmethod
        def in_tuple(rp_factory: Callable[[], RP]):
            """Return ``(rp, r)`` where ``r`` is the function's scalar return value.

            ``f(*args, rp) -> R``  →  ``(*args) -> tuple[RP, R]``
            """
            def inner(f: Callable[[*PTs, RP], R]) -> Callable[[*PTs], tuple[RP, R]]:
                _local = threading.local()
                @wraps(f)
                def innermost(*args):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
                    if hasattr(_local, '_rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0'):
                        r = f(*args, _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0)  # pyright: ignore[reportArgumentType, reportAny]
                        return (_local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0, r)  # pyright: ignore[reportAny]
                    _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0 = rp_factory()
                    try:
                        r = f(*args, _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0)  # pyright: ignore[reportArgumentType]
                    finally:
                        rp = _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0
                        del _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0
                    return (rp, r)
                return innermost  # pyright: ignore[reportUnknownVariableType]
            return inner

        @staticmethod
        def with_tuple(rp_factory: Callable[[], RP]):
            """Return ``(rp, *r)`` where ``r`` is the function's tuple return value.

            ``f(*args, rp) -> tuple[*RTs]``  →  ``(*args) -> tuple[RP, *RTs]``
            """
            def inner(f: Callable[[*PTs, RP], tuple[*RTs]]) -> Callable[[*PTs], tuple[RP, *RTs]]:
                _local = threading.local()
                @wraps(f)
                def innermost(*args):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType]
                    if hasattr(_local, '_rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0'):
                        r = f(*args, _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0)  # pyright: ignore[reportArgumentType, reportAny]
                        return (_local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0, *r)  # pyright: ignore[reportAny]
                    _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0 = rp_factory()
                    try:
                        r = f(*args, _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0)  # pyright: ignore[reportArgumentType]
                    finally:
                        rp = _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0
                        del _local._rp_94fc446b_edce_4487_9dc0_fa9ab1974bf0
                    return (rp, *r)
                return innermost  # pyright: ignore[reportUnknownVariableType]
            return inner
