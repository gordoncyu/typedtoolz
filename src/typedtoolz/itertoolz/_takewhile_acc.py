from collections.abc import Callable, Iterable
from typing import TypeVar
from typedtoolz.functoolz import curry

A = TypeVar('A')
T = TypeVar('T')

def _takewhile_acc(
    func: Callable[[A, T], tuple[bool, A]],
    initial_acc: A,
    iterable: Iterable[T],
) -> list[T]:
    result = []
    acc = initial_acc

    for item in iterable:
        predicate, acc = func(acc, item)
        if not predicate:
            break
        result.append(item)

    return result

takewhile_acc = curry(_takewhile_acc)
