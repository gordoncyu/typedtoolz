from collections.abc import Callable
from typing import TypeVar
from typing_extensions import override
from typedtoolz.functoolz._curry import curry

E = TypeVar('E', bound=BaseException)


class _raises_meta(type):
    @staticmethod
    @override
    def __call__(err: type[E], lamda: Callable[[], object]) -> bool:
        try:
            lamda()
            return False
        except err:
            return True


class _raises(metaclass=_raises_meta):  # See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md
    """
    raises(err, lamda) -> bool

    Check if a function raises an exception.

    Has a curried version as the property c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curry(2, _raises_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]


raises = _raises  # why? See: https://github.com/gordoncyu/typedtoolz/blob/main/docs/typing_bs/metaclass_static_callables.md#msc_hover_bs

__all__ = ["raises"]
