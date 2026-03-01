from io import StringIO
from typing import TypeVar
import pytest
from typedtoolz.functoolz import curry
from contextlib import redirect_stdout

A1 = TypeVar("A1")
A2 = TypeVar("A2")
A3 = TypeVar("A3")
A4 = TypeVar("A4")

# simple helpers
def id1(x: A1) -> A1: return x
def id2(x: A1, y: A2) -> tuple[A1, A2]: return (x, y)
def id3(x: A1, y: A2, z: A3) -> tuple[A1, A2, A3]: return (x, y, z)
def id4(w: A4, x: A1, y: A2, z: A3) -> tuple[A4, A1, A2, A3]: return (w, x, y, z)
def id3p(x: A1, y: A2, z: A3, *, p: str = "def") -> tuple[A1, A2, A3]: 
    print(p)
    return (x, y, z)

def test_curry_arity1():
    assert curry(id1)("foo") == "foo"

@pytest.mark.parametrize("call", [
    lambda: curry(id2)("foo", 3),
    lambda: curry(id2)("foo")(3),
])
def test_curry_arity2(call):  # pyright: ignore[reportUnknownParameterType]
    assert call() == ("foo", 3)

@pytest.mark.parametrize("call", [
    lambda: curry(id3)("a", "b", "c"),
    lambda: curry(id3)("a")("b", "c"),
    lambda: curry(id3)("a", "b")("c"),
])
def test_curry_arity3(call):  # pyright: ignore[reportUnknownParameterType]
    assert call() == ("a", "b", "c")

@pytest.mark.parametrize("call", [
    lambda: curry(id4)("w", "x", "y", "z"),
    lambda: curry(id4)("w")("x", "y", "z"),
    lambda: curry(id4)("w", "x")("y", "z"),
    lambda: curry(id4)("w", "x", "y")("z"),
])
def test_curry_arity4(call):  # pyright: ignore[reportUnknownParameterType]
    assert call() == ("w", "x", "y", "z")

def test_curry_kw_default():
    s = StringIO()
    with redirect_stdout(s):
        assert curry(id3p)("foo", 3, True, p="yay") == ("foo", 3, True)
    assert s.getvalue().strip() == "yay"

