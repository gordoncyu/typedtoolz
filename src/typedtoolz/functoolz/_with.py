from io import TextIOBase, UnsupportedOperation
from typing import Annotated, Callable, ContextManager, TypeVar, cast
from typedtoolz import identityv
from typedtoolz.functoolz.bring import bring
from typedtoolz.functoolz.curry import Curried3, curry
from typedtoolz.functoolz.curryv import curryv

def _wlth[A, R](res: ContextManager[A], body: Callable[[A], R]) -> R:
    with res as val:
        return body(val)

wlth = curry(_wlth)

with_op = curry(bring(1, _wlth))

thing = wlth(open("asdfa"), lambda f: f.read())
thing = wlth(open("asdfa"))(lambda f: f.read())

from typing import Union
from typedtoolz.functoolz import excepts, union_error
A1 = TypeVar("A1")
A2 = TypeVar("A2")
A3 = TypeVar("A3")

file_errors = (
    FileNotFoundError,
    PermissionError,
    IsADirectoryError,
    NotADirectoryError,
    FileExistsError,
    ValueError,
    TypeError,
    UnsupportedOperation,
    LookupError,
)
open_errors = (
    ValueError,
    TypeError,
    UnsupportedOperation,
    BlockingIOError,
    InterruptedError,
    TimeoutError,
    IsADirectoryError,
    NotADirectoryError,
    PermissionError,
    FileNotFoundError,
    ConnectionResetError,
    ConnectionAbortedError,
    BrokenPipeError,
)

saferead = union_error(
        open_errors, 
        with_op(
            cast(
                Callable[[TextIOBase], str],
                lambda f: f.read()
                )
            )
        )
res = saferead(open("asdf"))
safereadfile = union_error(file_errors, lambda path: saferead(path))
res = safereadfile("asdf")
