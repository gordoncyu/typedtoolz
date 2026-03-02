from typing import Callable, overload, TypeVar

A = TypeVar('A', contravariant=True)
T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')
T5 = TypeVar('T5')
T6 = TypeVar('T6')
T7 = TypeVar('T7')
T8 = TypeVar('T8')
T9 = TypeVar('T9')
T10 = TypeVar('T10')
T11 = TypeVar('T11')
T12 = TypeVar('T12')
T13 = TypeVar('T13')
T14 = TypeVar('T14')
T15 = TypeVar('T15')
T16 = TypeVar('T16')
T17 = TypeVar('T17')
T18 = TypeVar('T18')
T19 = TypeVar('T19')
R = TypeVar('R', covariant=True)

@overload
def compose(f1: Callable[[A], R], /) -> Callable[[A], R]: ...

@overload
def compose(f2: Callable[[T1], R], f1: Callable[[A], T1], /) -> Callable[[A], R]: ...

@overload
def compose(f3: Callable[[T2], R], f2: Callable[[T1], T2], f1: Callable[[A], T1], /) -> Callable[[A], R]: ...

@overload
def compose(f4: Callable[[T3], R], f3: Callable[[T2], T3], f2: Callable[[T1], T2], f1: Callable[[A], T1], /) -> Callable[[A], R]: ...

@overload
def compose(f5: Callable[[T4], R], f4: Callable[[T3], T4], f3: Callable[[T2], T3], f2: Callable[[T1], T2], f1: Callable[[A], T1], /) -> Callable[[A], R]: ...

@overload
def compose(f6: Callable[[T5], R], f5: Callable[[T4], T5], f4: Callable[[T3], T4], f3: Callable[[T2], T3], f2: Callable[[T1], T2], f1: Callable[[A], T1], /) -> Callable[[A], R]: ...

@overload
def compose(f7: Callable[[T6], R], f6: Callable[[T5], T6], f5: Callable[[T4], T5], f4: Callable[[T3], T4], f3: Callable[[T2], T3], f2: Callable[[T1], T2], f1: Callable[[A], T1], /) -> Callable[[A], R]: ...

@overload
def compose(f8: Callable[[T7], R], f7: Callable[[T6], T7], f6: Callable[[T5], T6], f5: Callable[[T4], T5], f4: Callable[[T3], T4], f3: Callable[[T2], T3], f2: Callable[[T1], T2], f1: Callable[[A], T1], /) -> Callable[[A], R]: ...

@overload
def compose(f9: Callable[[T8], R], f8: Callable[[T7], T8], f7: Callable[[T6], T7], f6: Callable[[T5], T6], f5: Callable[[T4], T5], f4: Callable[[T3], T4], f3: Callable[[T2], T3], f2: Callable[[T1], T2], f1: Callable[[A], T1], /) -> Callable[[A], R]: ...

@overload
def compose(f10: Callable[[T9], R], f9: Callable[[T8], T9], f8: Callable[[T7], T8], f7: Callable[[T6], T7], f6: Callable[[T5], T6], f5: Callable[[T4], T5], f4: Callable[[T3], T4], f3: Callable[[T2], T3], f2: Callable[[T1], T2], f1: Callable[[A], T1], /) -> Callable[[A], R]: ...

@overload
def compose(f11: Callable[[T10], R], f10: Callable[[T9], T10], f9: Callable[[T8], T9], f8: Callable[[T7], T8], f7: Callable[[T6], T7], f6: Callable[[T5], T6], f5: Callable[[T4], T5], f4: Callable[[T3], T4], f3: Callable[[T2], T3], f2: Callable[[T1], T2], f1: Callable[[A], T1], /) -> Callable[[A], R]: ...

@overload
def compose(f12: Callable[[T11], R], f11: Callable[[T10], T11], f10: Callable[[T9], T10], f9: Callable[[T8], T9], f8: Callable[[T7], T8], f7: Callable[[T6], T7], f6: Callable[[T5], T6], f5: Callable[[T4], T5], f4: Callable[[T3], T4], f3: Callable[[T2], T3], f2: Callable[[T1], T2], f1: Callable[[A], T1], /) -> Callable[[A], R]: ...

@overload
def compose(f13: Callable[[T12], R], f12: Callable[[T11], T12], f11: Callable[[T10], T11], f10: Callable[[T9], T10], f9: Callable[[T8], T9], f8: Callable[[T7], T8], f7: Callable[[T6], T7], f6: Callable[[T5], T6], f5: Callable[[T4], T5], f4: Callable[[T3], T4], f3: Callable[[T2], T3], f2: Callable[[T1], T2], f1: Callable[[A], T1], /) -> Callable[[A], R]: ...

@overload
def compose(f14: Callable[[T13], R], f13: Callable[[T12], T13], f12: Callable[[T11], T12], f11: Callable[[T10], T11], f10: Callable[[T9], T10], f9: Callable[[T8], T9], f8: Callable[[T7], T8], f7: Callable[[T6], T7], f6: Callable[[T5], T6], f5: Callable[[T4], T5], f4: Callable[[T3], T4], f3: Callable[[T2], T3], f2: Callable[[T1], T2], f1: Callable[[A], T1], /) -> Callable[[A], R]: ...

@overload
def compose(f15: Callable[[T14], R], f14: Callable[[T13], T14], f13: Callable[[T12], T13], f12: Callable[[T11], T12], f11: Callable[[T10], T11], f10: Callable[[T9], T10], f9: Callable[[T8], T9], f8: Callable[[T7], T8], f7: Callable[[T6], T7], f6: Callable[[T5], T6], f5: Callable[[T4], T5], f4: Callable[[T3], T4], f3: Callable[[T2], T3], f2: Callable[[T1], T2], f1: Callable[[A], T1], /) -> Callable[[A], R]: ...

@overload
def compose(f16: Callable[[T15], R], f15: Callable[[T14], T15], f14: Callable[[T13], T14], f13: Callable[[T12], T13], f12: Callable[[T11], T12], f11: Callable[[T10], T11], f10: Callable[[T9], T10], f9: Callable[[T8], T9], f8: Callable[[T7], T8], f7: Callable[[T6], T7], f6: Callable[[T5], T6], f5: Callable[[T4], T5], f4: Callable[[T3], T4], f3: Callable[[T2], T3], f2: Callable[[T1], T2], f1: Callable[[A], T1], /) -> Callable[[A], R]: ...

@overload
def compose(f17: Callable[[T16], R], f16: Callable[[T15], T16], f15: Callable[[T14], T15], f14: Callable[[T13], T14], f13: Callable[[T12], T13], f12: Callable[[T11], T12], f11: Callable[[T10], T11], f10: Callable[[T9], T10], f9: Callable[[T8], T9], f8: Callable[[T7], T8], f7: Callable[[T6], T7], f6: Callable[[T5], T6], f5: Callable[[T4], T5], f4: Callable[[T3], T4], f3: Callable[[T2], T3], f2: Callable[[T1], T2], f1: Callable[[A], T1], /) -> Callable[[A], R]: ...

@overload
def compose(f18: Callable[[T17], R], f17: Callable[[T16], T17], f16: Callable[[T15], T16], f15: Callable[[T14], T15], f14: Callable[[T13], T14], f13: Callable[[T12], T13], f12: Callable[[T11], T12], f11: Callable[[T10], T11], f10: Callable[[T9], T10], f9: Callable[[T8], T9], f8: Callable[[T7], T8], f7: Callable[[T6], T7], f6: Callable[[T5], T6], f5: Callable[[T4], T5], f4: Callable[[T3], T4], f3: Callable[[T2], T3], f2: Callable[[T1], T2], f1: Callable[[A], T1], /) -> Callable[[A], R]: ...

@overload
def compose(f19: Callable[[T18], R], f18: Callable[[T17], T18], f17: Callable[[T16], T17], f16: Callable[[T15], T16], f15: Callable[[T14], T15], f14: Callable[[T13], T14], f13: Callable[[T12], T13], f12: Callable[[T11], T12], f11: Callable[[T10], T11], f10: Callable[[T9], T10], f9: Callable[[T8], T9], f8: Callable[[T7], T8], f7: Callable[[T6], T7], f6: Callable[[T5], T6], f5: Callable[[T4], T5], f4: Callable[[T3], T4], f3: Callable[[T2], T3], f2: Callable[[T1], T2], f1: Callable[[A], T1], /) -> Callable[[A], R]: ...

@overload
def compose(f20: Callable[[T19], R], f19: Callable[[T18], T19], f18: Callable[[T17], T18], f17: Callable[[T16], T17], f16: Callable[[T15], T16], f15: Callable[[T14], T15], f14: Callable[[T13], T14], f13: Callable[[T12], T13], f12: Callable[[T11], T12], f11: Callable[[T10], T11], f10: Callable[[T9], T10], f9: Callable[[T8], T9], f8: Callable[[T7], T8], f7: Callable[[T6], T7], f6: Callable[[T5], T6], f5: Callable[[T4], T5], f4: Callable[[T3], T4], f3: Callable[[T2], T3], f2: Callable[[T1], T2], f1: Callable[[A], T1], /) -> Callable[[A], R]: ...

