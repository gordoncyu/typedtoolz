from typing import ParamSpec, TypeVar, TypeVarTuple
from functools import partial
from builtins import filter, sorted
from importlib.metadata import version as _pkg_version

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
E = TypeVar("E")
F = TypeVar("F")
G = TypeVar("G")
H = TypeVar("H")
I = TypeVar("I")
J = TypeVar("J")
K = TypeVar("K")
L = TypeVar("L")
M = TypeVar("M")
N = TypeVar("N")
O = TypeVar("O")
P = TypeVar("P")
Q = TypeVar("Q")
R = TypeVar("R")
S = TypeVar("S")
T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")
W = TypeVar("W")
X = TypeVar("X")
Y = TypeVar("Y")
Z = TypeVar("Z")

Ts = TypeVarTuple("Ts")
Ps = ParamSpec("Ps")

from typedtoolz._top_level import identity, identityv, return_none

from typedtoolz import functoolz, itertoolz, dicttoolz, sandbox, recipes
from typedtoolz.recipes import countby, partitionby
from typedtoolz.functoolz import (
    excepts, reduce, pipe, curry, compose, compose_left,
    thread_first, thread_last, memoize, juxt, do, flip, complement, apply,
    star, unstar,
)
from typedtoolz.itertoolz import (
    map, first, second, nth, last, peek, peekn,
    take, tail, drop, take_nth, isiterable, isdistinct, count,
    get, pluck, sliding_window, partition, partition_all,
    groupby, reduceby, frequencies, unique, diff, join,
    remove, accumulate, cons, interpose, interleave, iterate, concat, concatv,
    mapcat, merge_sorted, topk, random_sample,
)
from typedtoolz.dicttoolz import (
    merge, merge_with, valmap, keymap, itemmap,
    valfilter, keyfilter, itemfilter, assoc, dissoc, assoc_in, update_in, get_in,
)

comp = compose

__version__ = _pkg_version("typedtoolz")
