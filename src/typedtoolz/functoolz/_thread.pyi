from typing import Callable, TypeVar, TypeVarTuple, Unpack, overload

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
R = TypeVar('R', covariant=True)
Ts1 = TypeVarTuple('Ts1')
Ts2 = TypeVarTuple('Ts2')
Ts3 = TypeVarTuple('Ts3')
Ts4 = TypeVarTuple('Ts4')
Ts5 = TypeVarTuple('Ts5')
Ts6 = TypeVarTuple('Ts6')
Ts7 = TypeVarTuple('Ts7')
Ts8 = TypeVarTuple('Ts8')
Ts9 = TypeVarTuple('Ts9')
Ts10 = TypeVarTuple('Ts10')

@overload
def thread_first(val: A, form1: Callable[[A], R] | tuple[Callable[[A, *Ts1], R], *Ts1]) -> R: ...

@overload
def thread_first(val: A, form1: Callable[[A], T1] | tuple[Callable[[A, *Ts1], T1], *Ts1], form2: Callable[[T1], R] | tuple[Callable[[T1, *Ts2], R], *Ts2]) -> R: ...

@overload
def thread_first(val: A, form1: Callable[[A], T1] | tuple[Callable[[A, *Ts1], T1], *Ts1], form2: Callable[[T1], T2] | tuple[Callable[[T1, *Ts2], T2], *Ts2], form3: Callable[[T2], R] | tuple[Callable[[T2, *Ts3], R], *Ts3]) -> R: ...

@overload
def thread_first(val: A, form1: Callable[[A], T1] | tuple[Callable[[A, *Ts1], T1], *Ts1], form2: Callable[[T1], T2] | tuple[Callable[[T1, *Ts2], T2], *Ts2], form3: Callable[[T2], T3] | tuple[Callable[[T2, *Ts3], T3], *Ts3], form4: Callable[[T3], R] | tuple[Callable[[T3, *Ts4], R], *Ts4]) -> R: ...

@overload
def thread_first(val: A, form1: Callable[[A], T1] | tuple[Callable[[A, *Ts1], T1], *Ts1], form2: Callable[[T1], T2] | tuple[Callable[[T1, *Ts2], T2], *Ts2], form3: Callable[[T2], T3] | tuple[Callable[[T2, *Ts3], T3], *Ts3], form4: Callable[[T3], T4] | tuple[Callable[[T3, *Ts4], T4], *Ts4], form5: Callable[[T4], R] | tuple[Callable[[T4, *Ts5], R], *Ts5]) -> R: ...

@overload
def thread_first(val: A, form1: Callable[[A], T1] | tuple[Callable[[A, *Ts1], T1], *Ts1], form2: Callable[[T1], T2] | tuple[Callable[[T1, *Ts2], T2], *Ts2], form3: Callable[[T2], T3] | tuple[Callable[[T2, *Ts3], T3], *Ts3], form4: Callable[[T3], T4] | tuple[Callable[[T3, *Ts4], T4], *Ts4], form5: Callable[[T4], T5] | tuple[Callable[[T4, *Ts5], T5], *Ts5], form6: Callable[[T5], R] | tuple[Callable[[T5, *Ts6], R], *Ts6]) -> R: ...

@overload
def thread_first(val: A, form1: Callable[[A], T1] | tuple[Callable[[A, *Ts1], T1], *Ts1], form2: Callable[[T1], T2] | tuple[Callable[[T1, *Ts2], T2], *Ts2], form3: Callable[[T2], T3] | tuple[Callable[[T2, *Ts3], T3], *Ts3], form4: Callable[[T3], T4] | tuple[Callable[[T3, *Ts4], T4], *Ts4], form5: Callable[[T4], T5] | tuple[Callable[[T4, *Ts5], T5], *Ts5], form6: Callable[[T5], T6] | tuple[Callable[[T5, *Ts6], T6], *Ts6], form7: Callable[[T6], R] | tuple[Callable[[T6, *Ts7], R], *Ts7]) -> R: ...

@overload
def thread_first(val: A, form1: Callable[[A], T1] | tuple[Callable[[A, *Ts1], T1], *Ts1], form2: Callable[[T1], T2] | tuple[Callable[[T1, *Ts2], T2], *Ts2], form3: Callable[[T2], T3] | tuple[Callable[[T2, *Ts3], T3], *Ts3], form4: Callable[[T3], T4] | tuple[Callable[[T3, *Ts4], T4], *Ts4], form5: Callable[[T4], T5] | tuple[Callable[[T4, *Ts5], T5], *Ts5], form6: Callable[[T5], T6] | tuple[Callable[[T5, *Ts6], T6], *Ts6], form7: Callable[[T6], T7] | tuple[Callable[[T6, *Ts7], T7], *Ts7], form8: Callable[[T7], R] | tuple[Callable[[T7, *Ts8], R], *Ts8]) -> R: ...

@overload
def thread_first(val: A, form1: Callable[[A], T1] | tuple[Callable[[A, *Ts1], T1], *Ts1], form2: Callable[[T1], T2] | tuple[Callable[[T1, *Ts2], T2], *Ts2], form3: Callable[[T2], T3] | tuple[Callable[[T2, *Ts3], T3], *Ts3], form4: Callable[[T3], T4] | tuple[Callable[[T3, *Ts4], T4], *Ts4], form5: Callable[[T4], T5] | tuple[Callable[[T4, *Ts5], T5], *Ts5], form6: Callable[[T5], T6] | tuple[Callable[[T5, *Ts6], T6], *Ts6], form7: Callable[[T6], T7] | tuple[Callable[[T6, *Ts7], T7], *Ts7], form8: Callable[[T7], T8] | tuple[Callable[[T7, *Ts8], T8], *Ts8], form9: Callable[[T8], R] | tuple[Callable[[T8, *Ts9], R], *Ts9]) -> R: ...

@overload
def thread_first(val: A, form1: Callable[[A], T1] | tuple[Callable[[A, *Ts1], T1], *Ts1], form2: Callable[[T1], T2] | tuple[Callable[[T1, *Ts2], T2], *Ts2], form3: Callable[[T2], T3] | tuple[Callable[[T2, *Ts3], T3], *Ts3], form4: Callable[[T3], T4] | tuple[Callable[[T3, *Ts4], T4], *Ts4], form5: Callable[[T4], T5] | tuple[Callable[[T4, *Ts5], T5], *Ts5], form6: Callable[[T5], T6] | tuple[Callable[[T5, *Ts6], T6], *Ts6], form7: Callable[[T6], T7] | tuple[Callable[[T6, *Ts7], T7], *Ts7], form8: Callable[[T7], T8] | tuple[Callable[[T7, *Ts8], T8], *Ts8], form9: Callable[[T8], T9] | tuple[Callable[[T8, *Ts9], T9], *Ts9], form10: Callable[[T9], R] | tuple[Callable[[T9, *Ts10], R], *Ts10]) -> R: ...

@overload
def thread_last(val: A, form1: Callable[[A], R] | tuple[Callable[[*Ts1, A], R], *Ts1]) -> R: ...

@overload
def thread_last(val: A, form1: Callable[[A], T1] | tuple[Callable[[*Ts1, A], T1], *Ts1], form2: Callable[[T1], R] | tuple[Callable[[*Ts2, T1], R], *Ts2]) -> R: ...

@overload
def thread_last(val: A, form1: Callable[[A], T1] | tuple[Callable[[*Ts1, A], T1], *Ts1], form2: Callable[[T1], T2] | tuple[Callable[[*Ts2, T1], T2], *Ts2], form3: Callable[[T2], R] | tuple[Callable[[*Ts3, T2], R], *Ts3]) -> R: ...

@overload
def thread_last(val: A, form1: Callable[[A], T1] | tuple[Callable[[*Ts1, A], T1], *Ts1], form2: Callable[[T1], T2] | tuple[Callable[[*Ts2, T1], T2], *Ts2], form3: Callable[[T2], T3] | tuple[Callable[[*Ts3, T2], T3], *Ts3], form4: Callable[[T3], R] | tuple[Callable[[*Ts4, T3], R], *Ts4]) -> R: ...

@overload
def thread_last(val: A, form1: Callable[[A], T1] | tuple[Callable[[*Ts1, A], T1], *Ts1], form2: Callable[[T1], T2] | tuple[Callable[[*Ts2, T1], T2], *Ts2], form3: Callable[[T2], T3] | tuple[Callable[[*Ts3, T2], T3], *Ts3], form4: Callable[[T3], T4] | tuple[Callable[[*Ts4, T3], T4], *Ts4], form5: Callable[[T4], R] | tuple[Callable[[*Ts5, T4], R], *Ts5]) -> R: ...

@overload
def thread_last(val: A, form1: Callable[[A], T1] | tuple[Callable[[*Ts1, A], T1], *Ts1], form2: Callable[[T1], T2] | tuple[Callable[[*Ts2, T1], T2], *Ts2], form3: Callable[[T2], T3] | tuple[Callable[[*Ts3, T2], T3], *Ts3], form4: Callable[[T3], T4] | tuple[Callable[[*Ts4, T3], T4], *Ts4], form5: Callable[[T4], T5] | tuple[Callable[[*Ts5, T4], T5], *Ts5], form6: Callable[[T5], R] | tuple[Callable[[*Ts6, T5], R], *Ts6]) -> R: ...

@overload
def thread_last(val: A, form1: Callable[[A], T1] | tuple[Callable[[*Ts1, A], T1], *Ts1], form2: Callable[[T1], T2] | tuple[Callable[[*Ts2, T1], T2], *Ts2], form3: Callable[[T2], T3] | tuple[Callable[[*Ts3, T2], T3], *Ts3], form4: Callable[[T3], T4] | tuple[Callable[[*Ts4, T3], T4], *Ts4], form5: Callable[[T4], T5] | tuple[Callable[[*Ts5, T4], T5], *Ts5], form6: Callable[[T5], T6] | tuple[Callable[[*Ts6, T5], T6], *Ts6], form7: Callable[[T6], R] | tuple[Callable[[*Ts7, T6], R], *Ts7]) -> R: ...

@overload
def thread_last(val: A, form1: Callable[[A], T1] | tuple[Callable[[*Ts1, A], T1], *Ts1], form2: Callable[[T1], T2] | tuple[Callable[[*Ts2, T1], T2], *Ts2], form3: Callable[[T2], T3] | tuple[Callable[[*Ts3, T2], T3], *Ts3], form4: Callable[[T3], T4] | tuple[Callable[[*Ts4, T3], T4], *Ts4], form5: Callable[[T4], T5] | tuple[Callable[[*Ts5, T4], T5], *Ts5], form6: Callable[[T5], T6] | tuple[Callable[[*Ts6, T5], T6], *Ts6], form7: Callable[[T6], T7] | tuple[Callable[[*Ts7, T6], T7], *Ts7], form8: Callable[[T7], R] | tuple[Callable[[*Ts8, T7], R], *Ts8]) -> R: ...

@overload
def thread_last(val: A, form1: Callable[[A], T1] | tuple[Callable[[*Ts1, A], T1], *Ts1], form2: Callable[[T1], T2] | tuple[Callable[[*Ts2, T1], T2], *Ts2], form3: Callable[[T2], T3] | tuple[Callable[[*Ts3, T2], T3], *Ts3], form4: Callable[[T3], T4] | tuple[Callable[[*Ts4, T3], T4], *Ts4], form5: Callable[[T4], T5] | tuple[Callable[[*Ts5, T4], T5], *Ts5], form6: Callable[[T5], T6] | tuple[Callable[[*Ts6, T5], T6], *Ts6], form7: Callable[[T6], T7] | tuple[Callable[[*Ts7, T6], T7], *Ts7], form8: Callable[[T7], T8] | tuple[Callable[[*Ts8, T7], T8], *Ts8], form9: Callable[[T8], R] | tuple[Callable[[*Ts9, T8], R], *Ts9]) -> R: ...

@overload
def thread_last(val: A, form1: Callable[[A], T1] | tuple[Callable[[*Ts1, A], T1], *Ts1], form2: Callable[[T1], T2] | tuple[Callable[[*Ts2, T1], T2], *Ts2], form3: Callable[[T2], T3] | tuple[Callable[[*Ts3, T2], T3], *Ts3], form4: Callable[[T3], T4] | tuple[Callable[[*Ts4, T3], T4], *Ts4], form5: Callable[[T4], T5] | tuple[Callable[[*Ts5, T4], T5], *Ts5], form6: Callable[[T5], T6] | tuple[Callable[[*Ts6, T5], T6], *Ts6], form7: Callable[[T6], T7] | tuple[Callable[[*Ts7, T6], T7], *Ts7], form8: Callable[[T7], T8] | tuple[Callable[[*Ts8, T7], T8], *Ts8], form9: Callable[[T8], T9] | tuple[Callable[[*Ts9, T8], T9], *Ts9], form10: Callable[[T9], R] | tuple[Callable[[*Ts10, T9], R], *Ts10]) -> R: ...

