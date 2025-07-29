from typing import Callable, TypeVar, ParamSpec, Concatenate, overload, Literal

from toolz.functoolz import curry

def _bring(to_first, f):
    def wrapped(*args, **kwargs):
        if to_first >= len(args):
            raise IndexError(f"cannot _bring argument {to_first} to front: only {len(args)} arguments given")
        temp = args[0]
        args[0] = args[to_first]
        args[to_first] = temp
        return f(*args, **kwargs)
    return wrapped

bring = curry(_bring)
