from typing import Any, Callable, Concatenate, Literal, ParamSpec, Protocol, TypeVar, overload

P = ParamSpec('P')
R = TypeVar('R', covariant=True)
A1 = TypeVar('A1', contravariant=True)
A2 = TypeVar('A2', contravariant=True)
A3 = TypeVar('A3', contravariant=True)
A4 = TypeVar('A4', contravariant=True)
A5 = TypeVar('A5', contravariant=True)
A6 = TypeVar('A6', contravariant=True)
A7 = TypeVar('A7', contravariant=True)
A8 = TypeVar('A8', contravariant=True)
A9 = TypeVar('A9', contravariant=True)
A10 = TypeVar('A10', contravariant=True)

class CurriedV0(Protocol[P, R]):
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R: ...

class CurriedV1(Protocol[A1, P, R]):
    @overload
    def __call__(self, A1: A1, *args: P.args, **kw: P.kwargs) -> R: ...
    @overload
    def __call__(self) -> 'CurriedV1[A1, P, R]': ...
    @overload
    def __call__(self, **kw: Any) -> 'CurriedV1[A1, P, R]': ...  # pyright: ignore[reportAny, reportExplicitAny]

class CurriedV2(Protocol[A1, A2, P, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, *args: P.args, **kw: P.kwargs) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> CurriedV1[A2, P, R]: ...
    @overload
    def __call__(self) -> 'CurriedV2[A1, A2, P, R]': ...
    @overload
    def __call__(self, **kw: Any) -> 'CurriedV2[A1, A2, P, R]': ...  # pyright: ignore[reportAny, reportExplicitAny]

class CurriedV3(Protocol[A1, A2, A3, P, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, *args: P.args, **kw: P.kwargs) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> CurriedV2[A2, A3, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> CurriedV1[A3, P, R]: ...
    @overload
    def __call__(self) -> 'CurriedV3[A1, A2, A3, P, R]': ...
    @overload
    def __call__(self, **kw: Any) -> 'CurriedV3[A1, A2, A3, P, R]': ...  # pyright: ignore[reportAny, reportExplicitAny]

class CurriedV4(Protocol[A1, A2, A3, A4, P, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, *args: P.args, **kw: P.kwargs) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> CurriedV3[A2, A3, A4, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> CurriedV2[A3, A4, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> CurriedV1[A4, P, R]: ...
    @overload
    def __call__(self) -> 'CurriedV4[A1, A2, A3, A4, P, R]': ...
    @overload
    def __call__(self, **kw: Any) -> 'CurriedV4[A1, A2, A3, A4, P, R]': ...  # pyright: ignore[reportAny, reportExplicitAny]

class CurriedV5(Protocol[A1, A2, A3, A4, A5, P, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, *args: P.args, **kw: P.kwargs) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> CurriedV4[A2, A3, A4, A5, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> CurriedV3[A3, A4, A5, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> CurriedV2[A4, A5, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, /) -> CurriedV1[A5, P, R]: ...
    @overload
    def __call__(self) -> 'CurriedV5[A1, A2, A3, A4, A5, P, R]': ...
    @overload
    def __call__(self, **kw: Any) -> 'CurriedV5[A1, A2, A3, A4, A5, P, R]': ...  # pyright: ignore[reportAny, reportExplicitAny]

class CurriedV6(Protocol[A1, A2, A3, A4, A5, A6, P, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, *args: P.args, **kw: P.kwargs) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> CurriedV5[A2, A3, A4, A5, A6, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> CurriedV4[A3, A4, A5, A6, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> CurriedV3[A4, A5, A6, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, /) -> CurriedV2[A5, A6, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /) -> CurriedV1[A6, P, R]: ...
    @overload
    def __call__(self) -> 'CurriedV6[A1, A2, A3, A4, A5, A6, P, R]': ...
    @overload
    def __call__(self, **kw: Any) -> 'CurriedV6[A1, A2, A3, A4, A5, A6, P, R]': ...  # pyright: ignore[reportAny, reportExplicitAny]

class CurriedV7(Protocol[A1, A2, A3, A4, A5, A6, A7, P, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, *args: P.args, **kw: P.kwargs) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> CurriedV6[A2, A3, A4, A5, A6, A7, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> CurriedV5[A3, A4, A5, A6, A7, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> CurriedV4[A4, A5, A6, A7, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, /) -> CurriedV3[A5, A6, A7, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /) -> CurriedV2[A6, A7, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, /) -> CurriedV1[A7, P, R]: ...
    @overload
    def __call__(self) -> 'CurriedV7[A1, A2, A3, A4, A5, A6, A7, P, R]': ...
    @overload
    def __call__(self, **kw: Any) -> 'CurriedV7[A1, A2, A3, A4, A5, A6, A7, P, R]': ...  # pyright: ignore[reportAny, reportExplicitAny]

class CurriedV8(Protocol[A1, A2, A3, A4, A5, A6, A7, A8, P, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, A8: A8, *args: P.args, **kw: P.kwargs) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> CurriedV7[A2, A3, A4, A5, A6, A7, A8, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> CurriedV6[A3, A4, A5, A6, A7, A8, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> CurriedV5[A4, A5, A6, A7, A8, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, /) -> CurriedV4[A5, A6, A7, A8, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /) -> CurriedV3[A6, A7, A8, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, /) -> CurriedV2[A7, A8, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, /) -> CurriedV1[A8, P, R]: ...
    @overload
    def __call__(self) -> 'CurriedV8[A1, A2, A3, A4, A5, A6, A7, A8, P, R]': ...
    @overload
    def __call__(self, **kw: Any) -> 'CurriedV8[A1, A2, A3, A4, A5, A6, A7, A8, P, R]': ...  # pyright: ignore[reportAny, reportExplicitAny]

class CurriedV9(Protocol[A1, A2, A3, A4, A5, A6, A7, A8, A9, P, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, A8: A8, A9: A9, *args: P.args, **kw: P.kwargs) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> CurriedV8[A2, A3, A4, A5, A6, A7, A8, A9, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> CurriedV7[A3, A4, A5, A6, A7, A8, A9, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> CurriedV6[A4, A5, A6, A7, A8, A9, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, /) -> CurriedV5[A5, A6, A7, A8, A9, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /) -> CurriedV4[A6, A7, A8, A9, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, /) -> CurriedV3[A7, A8, A9, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, /) -> CurriedV2[A8, A9, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, A8: A8, /) -> CurriedV1[A9, P, R]: ...
    @overload
    def __call__(self) -> 'CurriedV9[A1, A2, A3, A4, A5, A6, A7, A8, A9, P, R]': ...
    @overload
    def __call__(self, **kw: Any) -> 'CurriedV9[A1, A2, A3, A4, A5, A6, A7, A8, A9, P, R]': ...  # pyright: ignore[reportAny, reportExplicitAny]

class CurriedV10(Protocol[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, P, R]):
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, A8: A8, A9: A9, A10: A10, *args: P.args, **kw: P.kwargs) -> R: ...
    @overload
    def __call__(self, A1: A1, /) -> CurriedV9[A2, A3, A4, A5, A6, A7, A8, A9, A10, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, /) -> CurriedV8[A3, A4, A5, A6, A7, A8, A9, A10, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, /) -> CurriedV7[A4, A5, A6, A7, A8, A9, A10, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, /) -> CurriedV6[A5, A6, A7, A8, A9, A10, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /) -> CurriedV5[A6, A7, A8, A9, A10, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, /) -> CurriedV4[A7, A8, A9, A10, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, /) -> CurriedV3[A8, A9, A10, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, A8: A8, /) -> CurriedV2[A9, A10, P, R]: ...
    @overload
    def __call__(self, A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, A6: A6, A7: A7, A8: A8, A9: A9, /) -> CurriedV1[A10, P, R]: ...
    @overload
    def __call__(self) -> 'CurriedV10[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, P, R]': ...
    @overload
    def __call__(self, **kw: Any) -> 'CurriedV10[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, P, R]': ...  # pyright: ignore[reportAny, reportExplicitAny]

class _CurryV1Maker(Protocol):
    @overload
    def __call__(self, f: Callable[Concatenate[A1, P], R], A1: A1, /, **kwargs: Any) -> CurriedV0[P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, P], R], /, **kwargs: Any) -> CurriedV1[A1, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]

class _CurryV2Maker(Protocol):
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, P], R], A1: A1, A2: A2, /, **kwargs: Any) -> CurriedV0[P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, P], R], A1: A1, /, **kwargs: Any) -> CurriedV1[A2, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, P], R], /, **kwargs: Any) -> CurriedV2[A1, A2, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]

class _CurryV3Maker(Protocol):
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, P], R], A1: A1, A2: A2, A3: A3, /, **kwargs: Any) -> CurriedV0[P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, P], R], A1: A1, A2: A2, /, **kwargs: Any) -> CurriedV1[A3, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, P], R], A1: A1, /, **kwargs: Any) -> CurriedV2[A2, A3, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, P], R], /, **kwargs: Any) -> CurriedV3[A1, A2, A3, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]

class _CurryV4Maker(Protocol):
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, P], R], A1: A1, A2: A2, A3: A3, A4: A4, /, **kwargs: Any) -> CurriedV0[P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, P], R], A1: A1, A2: A2, A3: A3, /, **kwargs: Any) -> CurriedV1[A4, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, P], R], A1: A1, A2: A2, /, **kwargs: Any) -> CurriedV2[A3, A4, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, P], R], A1: A1, /, **kwargs: Any) -> CurriedV3[A2, A3, A4, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, P], R], /, **kwargs: Any) -> CurriedV4[A1, A2, A3, A4, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]

class _CurryV5Maker(Protocol):
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, P], R], A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /, **kwargs: Any) -> CurriedV0[P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, P], R], A1: A1, A2: A2, A3: A3, A4: A4, /, **kwargs: Any) -> CurriedV1[A5, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, P], R], A1: A1, A2: A2, A3: A3, /, **kwargs: Any) -> CurriedV2[A4, A5, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, P], R], A1: A1, A2: A2, /, **kwargs: Any) -> CurriedV3[A3, A4, A5, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, P], R], A1: A1, /, **kwargs: Any) -> CurriedV4[A2, A3, A4, A5, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, P], R], /, **kwargs: Any) -> CurriedV5[A1, A2, A3, A4, A5, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]

class _CurryV6Maker(Protocol):
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, P], R], A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /, **kwargs: Any) -> CurriedV1[A6, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, P], R], A1: A1, A2: A2, A3: A3, A4: A4, /, **kwargs: Any) -> CurriedV2[A5, A6, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, P], R], A1: A1, A2: A2, A3: A3, /, **kwargs: Any) -> CurriedV3[A4, A5, A6, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, P], R], A1: A1, A2: A2, /, **kwargs: Any) -> CurriedV4[A3, A4, A5, A6, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, P], R], A1: A1, /, **kwargs: Any) -> CurriedV5[A2, A3, A4, A5, A6, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, P], R], /, **kwargs: Any) -> CurriedV6[A1, A2, A3, A4, A5, A6, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]

class _CurryV7Maker(Protocol):
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, P], R], A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /, **kwargs: Any) -> CurriedV2[A6, A7, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, P], R], A1: A1, A2: A2, A3: A3, A4: A4, /, **kwargs: Any) -> CurriedV3[A5, A6, A7, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, P], R], A1: A1, A2: A2, A3: A3, /, **kwargs: Any) -> CurriedV4[A4, A5, A6, A7, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, P], R], A1: A1, A2: A2, /, **kwargs: Any) -> CurriedV5[A3, A4, A5, A6, A7, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, P], R], A1: A1, /, **kwargs: Any) -> CurriedV6[A2, A3, A4, A5, A6, A7, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, P], R], /, **kwargs: Any) -> CurriedV7[A1, A2, A3, A4, A5, A6, A7, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]

class _CurryV8Maker(Protocol):
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, P], R], A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /, **kwargs: Any) -> CurriedV3[A6, A7, A8, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, P], R], A1: A1, A2: A2, A3: A3, A4: A4, /, **kwargs: Any) -> CurriedV4[A5, A6, A7, A8, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, P], R], A1: A1, A2: A2, A3: A3, /, **kwargs: Any) -> CurriedV5[A4, A5, A6, A7, A8, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, P], R], A1: A1, A2: A2, /, **kwargs: Any) -> CurriedV6[A3, A4, A5, A6, A7, A8, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, P], R], A1: A1, /, **kwargs: Any) -> CurriedV7[A2, A3, A4, A5, A6, A7, A8, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, P], R], /, **kwargs: Any) -> CurriedV8[A1, A2, A3, A4, A5, A6, A7, A8, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]

class _CurryV9Maker(Protocol):
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, P], R], A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /, **kwargs: Any) -> CurriedV4[A6, A7, A8, A9, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, P], R], A1: A1, A2: A2, A3: A3, A4: A4, /, **kwargs: Any) -> CurriedV5[A5, A6, A7, A8, A9, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, P], R], A1: A1, A2: A2, A3: A3, /, **kwargs: Any) -> CurriedV6[A4, A5, A6, A7, A8, A9, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, P], R], A1: A1, A2: A2, /, **kwargs: Any) -> CurriedV7[A3, A4, A5, A6, A7, A8, A9, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, P], R], A1: A1, /, **kwargs: Any) -> CurriedV8[A2, A3, A4, A5, A6, A7, A8, A9, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, P], R], /, **kwargs: Any) -> CurriedV9[A1, A2, A3, A4, A5, A6, A7, A8, A9, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]

class _CurryV10Maker(Protocol):
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, P], R], A1: A1, A2: A2, A3: A3, A4: A4, A5: A5, /, **kwargs: Any) -> CurriedV5[A6, A7, A8, A9, A10, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, P], R], A1: A1, A2: A2, A3: A3, A4: A4, /, **kwargs: Any) -> CurriedV6[A5, A6, A7, A8, A9, A10, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, P], R], A1: A1, A2: A2, A3: A3, /, **kwargs: Any) -> CurriedV7[A4, A5, A6, A7, A8, A9, A10, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, P], R], A1: A1, A2: A2, /, **kwargs: Any) -> CurriedV8[A3, A4, A5, A6, A7, A8, A9, A10, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, P], R], A1: A1, /, **kwargs: Any) -> CurriedV9[A2, A3, A4, A5, A6, A7, A8, A9, A10, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]
    @overload
    def __call__(self, f: Callable[Concatenate[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, P], R], /, **kwargs: Any) -> CurriedV10[A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, P, R]: ...  # pyright: ignore[reportAny, reportExplicitAny]

@overload
def curryv(pn: Literal[10], /) -> _CurryV10Maker: ...

@overload
def curryv(pn: Literal[9], /) -> _CurryV9Maker: ...

@overload
def curryv(pn: Literal[8], /) -> _CurryV8Maker: ...

@overload
def curryv(pn: Literal[7], /) -> _CurryV7Maker: ...

@overload
def curryv(pn: Literal[6], /) -> _CurryV6Maker: ...

@overload
def curryv(pn: Literal[5], /) -> _CurryV5Maker: ...

@overload
def curryv(pn: Literal[4], /) -> _CurryV4Maker: ...

@overload
def curryv(pn: Literal[3], /) -> _CurryV3Maker: ...

@overload
def curryv(pn: Literal[2], /) -> _CurryV2Maker: ...

@overload
def curryv(pn: Literal[1], /) -> _CurryV1Maker: ...

