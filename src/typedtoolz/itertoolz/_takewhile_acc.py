from collections.abc import Callable, Iterable
from typing import TypeVar
from typedtoolz.functoolz import curryv

A = TypeVar('A')
T = TypeVar('T')

def _takewhile_acc(
    func: Callable[[A, T], tuple[bool, A]],
    initial_acc: A,
    iterable: Iterable[T],
    take_first_negative: bool = False,
) -> list[T]:
    result: list[T] = []
    acc = initial_acc

    for item in iterable:
        predicate, acc = func(acc, item)
        if not predicate:
            if take_first_negative: result.append(item)
            break
        result.append(item)

    return result

takewhile_acc = curryv(3, _takewhile_acc)
