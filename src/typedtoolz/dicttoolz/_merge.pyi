from collections.abc import Callable, Mapping
from typing import TypeVar

K = TypeVar('K')
V = TypeVar('V')
W = TypeVar('W')

def merge(*dicts: Mapping[K, V]) -> dict[K, V]: ...
def merge_with(func: Callable[[list[V]], W], *dicts: Mapping[K, V]) -> dict[K, W]: ...
