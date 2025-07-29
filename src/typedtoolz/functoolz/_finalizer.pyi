from __future__ import annotations

from typing import Callable, ParamSpec, TypeVar
from typedtoolz.functoolz.curry import curry

# ─── Generic type parameters ────────────────────────────────────────────
A = TypeVar("A")             # argument routed to `body`
E = TypeVar("E")             # argument routed to `end`
R = TypeVar("R")             # return type from `body`

PBody = ParamSpec("PBody")   # *args/**kwargs accepted by `body`
PEnd = ParamSpec("PEnd")     # *args/**kwargs accepted by `end`

# ─── Positional-argument version (single positional arg each) ───────────

def _finalizer(
    body: Callable[[A], R],
    end: Callable[[E], object],
    barg: A,
    earg: E,
    /,
) -> R: ...
finalizer = curry(_finalizer)

from typedtoolz.functoolz.pipe import pipe
from typedtoolz.functoolz.bring import bring
_finalizer_body_last = pipe(_finalizer, bring(1), bring(3))
finalizer_body_last = curry(_finalizer_body_last)

finalizer_args_first = pipe(_finalizer, bring(1), bring(3), bring(1), bring(2))

# ─── Fully variadic “kw” version (ParamSpec-powered) ────────────────────

def _finalizerkw(
    body: Callable[PBody, R],
    end: Callable[PEnd, object],
    /,
) -> Callable[PBody, Callable[PEnd, R]]: ...
finalizerkw = curry(_finalizerkw)

def finalizerkw_body_last(
    end: Callable[PEnd, object],
    /,
) -> Callable[
    PEnd,
    Callable[
        PBody,
        Callable[[Callable[PBody, R]], R],
    ],
]: ...
