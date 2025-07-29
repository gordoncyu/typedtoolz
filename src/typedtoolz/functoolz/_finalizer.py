from typing import Callable, ParamSpec, TypeVar

from toolz.functoolz import curry


def _finalizer(body, end, barg, earg):
    try:
        return body(barg)
    finally:
        end(earg)

finalizer = curry(_finalizer)

def _finalizer_body_last(end, earg, barg, body):
    return _finalizer(body, end, barg, earg)

finalizer_body_last = curry(_finalizer_body_last)

def _finalizer_args_first(barg, earg, body, end):
    return _finalizer(body, end, barg, earg)

finalizer_args_first = curry(_finalizer_args_first)

def _finalizerkw(body, end):
    def barg_acc(*bargs, **bkwargs):
        def earg_acc(*eargs, ekwargs):
            try:
                return body(*bargs, **bkwargs)
            finally:
                end(*eargs, **ekwargs)

    return barg_acc

finalizerkw = curry(_finalizerkw)

def finalizerkw_body_last(end):
    def earg_acc(*eargs, ekwargs):
        def barg_acc(*bargs, **bkwargs):
            def body_acc(body): 
                try:
                    return body(*bargs, **bkwargs)
                finally:
                    end(*eargs, **ekwargs)

    return earg_acc
