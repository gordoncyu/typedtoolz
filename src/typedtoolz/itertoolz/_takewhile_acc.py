from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, Generic, ReadOnly, TypeVar, cast, reveal_type
from typing_extensions import TypedDict, overload, override
from typedtoolz.functoolz._curryv import curryv
from typedtoolz.functoolz._reduce import _initial_missing  # pyright: ignore[reportPrivateUsage]

A = TypeVar('A')
T = TypeVar('T')

class TakeAcc(Generic[A], TypedDict, extra_items=A):
    take: bool

class _takewhile_acc_meta(type):
    @classmethod
    @overload
    def __call__(
            cls,
            func: Callable[[A, T], tuple[bool, A] | TakeAcc[A]],
            iterable: Iterable[T],
            *,
            take_first_negative: bool = False,
            ) -> list[T]: ...
    @classmethod
    @overload
    def __call__(
            cls,
            func: Callable[[A, T], tuple[bool, A] | TakeAcc[A]],
            iterable: Iterable[T],
            initial: A = cast(A, _initial_missing),  # pyright: ignore[reportCallInDefaultInitializer]
            *,
            take_first_negative: bool = False,
            ) -> list[T]: ...

    @classmethod
    @override
    def __call__(
            cls,
            func: Callable[[A, T], tuple[bool, A] | TakeAcc[A]],
            iterable: Iterable[T],
            initial: A = cast(A, _initial_missing),  # pyright: ignore[reportCallInDefaultInitializer]
            *,
            take_first_negative: bool = False,
            ) -> list[T]:
        return cls._call(func, initial, iterable, take_first_negative)

    @staticmethod
    def _call(
        func: Callable[[A, T], tuple[bool, A] | TakeAcc[A]],
        initial: A,
        iterable: Iterable[T],
        take_first_negative: bool = False,
    ) -> list[T]:
        it = iter(iterable)

        if initial is _initial_missing:
            try:
                acc = next(it)
            except StopIteration:
                raise TypeError("reduce() of empty sequence with no initial value") from None
        else:
            acc = initial

        result: list[T] = []

        for item in it:
            match func(acc, item):
                case (predicate, acc): ...
                case {"take": predicate, **rest}: 
                    try:
                        acc = cast(A, next(iter(rest.values())))
                    except StopIteration:
                        raise ValueError(f"Provided accumulation function returned a dictionary with no extra key to treat as the accumulator")
                case bad_value: raise ValueError(f'Provided accumulation function must return either (bool, T) or {{"take": bool, [any string]: T}}, instead got: {bad_value}') # This never happens, pyright knows takeacc type has been covered yet it does not care, hence i need this case to be exhaustive according to it
            if not predicate:
                if take_first_negative: result.append(item)
                break
            result.append(item)

        return result

class takewhile_acc(metaclass=_takewhile_acc_meta):
    """Take items from iterable while an accumulator-based predicate holds.

    takewhile_acc(func, iterable[, initial], *, take_first_negative=False) -> list[T]

    func receives ``(accumulator, item)`` and must return either:
      - ``(bool, new_acc)``: a tuple of (continue?, new accumulator)
      - ``{"take": bool, key: new_acc}``: a TypedDict with the same semantics

    Iteration stops when func returns False. If take_first_negative is True,
    the first item that fails the predicate is included in the result.
    When no initial is provided, the first element of the iterable is used
    as the initial accumulator.

    Has curried versions as properties prefixed with c (see :func:`typedtoolz.functoolz.curry`).
    """
    c = curryv(2, _takewhile_acc_meta.__call__)  # pyright: ignore[reportUnannotatedClassAttribute]
    ci = curryv(3, _takewhile_acc_meta._call)  # pyright: ignore[reportUnannotatedClassAttribute, reportPrivateUsage]

__all__ = [
        "takewhile_acc",
        ]
