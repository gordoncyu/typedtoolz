from typing import List, Tuple, Any
from typedtoolz.functoolz.curry import curry

A = TypeVar('A')  # Generic type for the accumulator

def _takewhile_acc(
    func: Callable[[A, T], Tuple[bool, A]],
    initial_acc: A,
    iterable: Iterable[T],
) -> List[T]:
    result = []
    acc = initial_acc

    for item in iterable:
        predicate, acc = func(acc, item)
        if not predicate:
            break
        result.append(item)

    return result

takewhile_acc = curry(_takewhile_acc)
