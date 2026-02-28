from typing import Any, TypeVar, TypeVarTuple, Callable, get_origin, get_type_hints, overload, staticmethod

PTs = TypeVarTuple("PTs")
RTs = TypeVarTuple("Ts")
RP = TypeVar("RP")
R = TypeVar("R")

class return_last_param:
    @staticmethod
    @overload
    def __call__(f: Callable[[*PTs, RP], None]) -> Callable[[*PTs], RP]: ...

    @staticmethod
    @overload
    def __call__(f: Callable[[*PTs, RP], tuple[*RTs]]) -> Callable[[*PTs], tuple[RP, *RTs]]: ...

    @staticmethod
    @overload
    def __call__(f: Callable[[*PTs, RP], R]) -> Callable[[*PTs], tuple[RP, R]]: ...

    @staticmethod
    def __call__(f: Callable[[*PTs, RP], R]) -> Callable[[*PTs], tuple[RP, R]]: ...

    @staticmethod
    def return_last_param_only(f: Callable[[*PTs, RP], Any]) -> Callable[[*PTs], RP]: ...

    @staticmethod
    @overload
    def return_last_param_joined(f: Callable[[*PTs, RP], tuple[*RTs]]) -> Callable[[*PTs], tuple[RP, *RTs]]: ...
    @staticmethod
    @overload
    def return_last_param_joined(f: Callable[[*PTs, RP], R]) -> Callable[[*PTs], tuple[RP, R]]: ...

    @staticmethod
    def return_last_param_joined(f: Callable[[*PTs, RP], R]) -> Callable[[*PTs], tuple[RP, R]]:
        hints = get_type_hints(f)
        if get_origin(hints.get("return")) is tuple:
            pass

    @staticmethod
    def return_last_param_joined_in_tuple(f: Callable[[*PTs, RP], R]) -> Callable[[*PTs], tuple[RP, R]]: ...

    @staticmethod
    def return_last_param_joined_with_tuple(f: Callable[[*PTs, RP], tuple[*RTs]]) -> Callable[[*PTs], tuple[RP, *RTs]]: ...
