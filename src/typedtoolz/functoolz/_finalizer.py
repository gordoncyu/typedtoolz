from __future__ import annotations

from typing import Callable, ParamSpec, TypeVar
from toolz.functoolz import curry

A = TypeVar("A")
E = TypeVar("E")
R = TypeVar("R")

PBody = ParamSpec("PBody")
PEnd = ParamSpec("PEnd")

def _finalizer(
    body: Callable[[A], R],
    end: Callable[[E], object],
    barg: A,
    earg: E,
    /,
) -> R:
    try:
        return body(barg)
    finally:
        end(earg)

finalizer = curry(_finalizer)

def _finalizer_body_last(
    end: Callable[[E], object],
    earg: E,
    barg: A,
    body: Callable[[A], R],
    /,
) -> R:
    return _finalizer(body, end, barg, earg)

finalizer_body_last = curry(_finalizer_body_last)

def _finalizerkw(
    body: Callable[PBody, R],
    end: Callable[PEnd, object],
    /,
) -> Callable[PBody, Callable[PEnd, R]]:
    def barg_acc(*bargs: PBody.args, **bkwargs: PBody.kwargs) -> Callable[PEnd, R]:
        def earg_acc(*eargs: PEnd.args, **ekwargs: PEnd.kwargs) -> R:
            try:
                return body(*bargs, **bkwargs)
            finally:
                end(*eargs, **ekwargs)
        return earg_acc
    return barg_acc

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
]:
    def earg_acc(*eargs: PEnd.args, **ekwargs: PEnd.kwargs) -> Callable[PBody, Callable[[Callable[PBody, R]], R]]:
        def barg_acc(*bargs: PBody.args, **bkwargs: PBody.kwargs) -> Callable[[Callable[PBody, R]], R]:
            def body_acc(body: Callable[PBody, R]) -> R:
                try:
                    return body(*bargs, **bkwargs)
                finally:
                    end(*eargs, **ekwargs)
            return body_acc
        return barg_acc
    return earg_acc
