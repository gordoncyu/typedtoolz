from collections.abc import Iterable, Iterator
from typing import TypeVar

T = TypeVar('T')

def random_sample(prob: float, seq: Iterable[T], random_state: int | None = ...) -> Iterator[T]: ...
