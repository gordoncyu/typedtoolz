from typing import Callable, Concatenate, ParamSpec, TypeVar, overload
from typing_extensions import Any

P = ParamSpec('P')
R = TypeVar('R')
A1 = TypeVar('A1')
A2 = TypeVar('A2')
A3 = TypeVar('A3')
A4 = TypeVar('A4')
A5 = TypeVar('A5')
A6 = TypeVar('A6')
A7 = TypeVar('A7')
A8 = TypeVar('A8')
A9 = TypeVar('A9')
A10 = TypeVar('A10')

@overload
def partial(func: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, P], R], __a1: A1, __a2: A2, __a3: A3, __a4: A4, __a5: A5, __a6: A6, __a7: A7, __a8: A8, __a9: A9, __a10: A10, /, **kwargs: Any) -> Callable[P, R]: ...  # pyright: ignore[reportExplicitAny, reportAny]

@overload
def partial(func: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, P], R], __a1: A1, __a2: A2, __a3: A3, __a4: A4, __a5: A5, __a6: A6, __a7: A7, __a8: A8, __a9: A9, /, **kwargs: Any) -> Callable[P, R]: ...  # pyright: ignore[reportExplicitAny, reportAny]

@overload
def partial(func: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, P], R], __a1: A1, __a2: A2, __a3: A3, __a4: A4, __a5: A5, __a6: A6, __a7: A7, __a8: A8, /, **kwargs: Any) -> Callable[P, R]: ...  # pyright: ignore[reportExplicitAny, reportAny]

@overload
def partial(func: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, P], R], __a1: A1, __a2: A2, __a3: A3, __a4: A4, __a5: A5, __a6: A6, __a7: A7, /, **kwargs: Any) -> Callable[P, R]: ...  # pyright: ignore[reportExplicitAny, reportAny]

@overload
def partial(func: Callable[Concatenate[A1, A2, A3, A4, A5, A6, P], R], __a1: A1, __a2: A2, __a3: A3, __a4: A4, __a5: A5, __a6: A6, /, **kwargs: Any) -> Callable[P, R]: ...  # pyright: ignore[reportExplicitAny, reportAny]

@overload
def partial(func: Callable[Concatenate[A1, A2, A3, A4, A5, P], R], __a1: A1, __a2: A2, __a3: A3, __a4: A4, __a5: A5, /, **kwargs: Any) -> Callable[P, R]: ...  # pyright: ignore[reportExplicitAny, reportAny]

@overload
def partial(func: Callable[Concatenate[A1, A2, A3, A4, P], R], __a1: A1, __a2: A2, __a3: A3, __a4: A4, /, **kwargs: Any) -> Callable[P, R]: ...  # pyright: ignore[reportExplicitAny, reportAny]

@overload
def partial(func: Callable[Concatenate[A1, A2, A3, P], R], __a1: A1, __a2: A2, __a3: A3, /, **kwargs: Any) -> Callable[P, R]: ...  # pyright: ignore[reportExplicitAny, reportAny]

@overload
def partial(func: Callable[Concatenate[A1, A2, P], R], __a1: A1, __a2: A2, /, **kwargs: Any) -> Callable[P, R]: ...  # pyright: ignore[reportExplicitAny, reportAny]

@overload
def partial(func: Callable[Concatenate[A1, P], R], __a1: A1, /, **kwargs: Any) -> Callable[P, R]: ...  # pyright: ignore[reportExplicitAny, reportAny]

