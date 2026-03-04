# TODO: Review msc impl
from collections.abc import Iterable, Iterator
from typing import TypeVar, cast
from typing_extensions import override
from cytoolz.itertoolz import random_sample as _random_sample
from typedtoolz.functoolz._curry import curry

T = TypeVar('T')

_missing = object()


class _random_sample_meta(type):
    @staticmethod
    @override
    def __call__(prob: float, seq: Iterable[T], random_state: int | None = cast(int | None, _missing)) -> Iterator[T]:  # pyright: ignore[reportCallInDefaultInitializer]
        if random_state is _missing:
            return _random_sample(prob, seq)
        return _random_sample(prob, seq, random_state)  # type: ignore[arg-type]


class _random_sample(metaclass=_random_sample_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    random_sample(prob, seq, random_state=None) -> Iterator

    Return elements of seq based on a given probability.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _random_sample_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


random_sample = _random_sample  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["random_sample"]
