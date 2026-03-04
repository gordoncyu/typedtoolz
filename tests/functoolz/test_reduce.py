from typing import cast
import pytest
from typedtoolz.functoolz import reduce


# ── reduce() direct call ───────────────────────────────────────────────────────

def test_sum_no_initial():
    assert reduce(lambda a, b: a + b, [1, 2, 3, 4, 5]) == 15

def test_sum_with_initial():
    assert reduce(lambda a, b: a + b, [1, 2, 3], 10) == 16

def test_heterogeneous_initial():
    result = reduce(
            lambda acc, x: acc + [x * 2],
            [1, 2, 3],
            cast(list[int], []),
            )
    assert result == [2, 4, 6]

def test_single_element_no_initial():
    assert reduce(lambda a, b: a + b, [42]) == 42

def test_single_element_with_initial():
    assert reduce(lambda a, b: a + b, [1], 10) == 11

def test_empty_with_initial():
    assert reduce(lambda a, b: a + b, [], 99) == 99  # pyright: ignore[reportOperatorIssue, reportUnknownLambdaType]

def test_empty_no_initial_raises():
    with pytest.raises(TypeError, match="reduce\\(\\) of empty iterable with no initial value"):
        reduce(lambda a, b: a + b, cast(list[int], []))

def test_string_concat():
    assert reduce(lambda a, b: a + b, ["a", "b", "c"]) == "abc"

def test_generator_input():
    assert reduce(lambda a, b: a + b, (x for x in [1, 2, 3])) == 6


# ── reduce.c ──────────────────────────────────────────────────────────────────

def test_c_curried_function_then_sequence():
    add = reduce.c(lambda a, b: a + b)
    assert add([1, 2, 3]) == 6

def test_c_fully_applied():
    assert reduce.c(lambda a, b: a + b, [1, 2, 3]) == 6


# ── reduce.c with initial (new: __call__ staticmethod exposes initial param) ───

def test_c_with_initial_two_step():
    fn = reduce.c(lambda a, b: a + b)
    assert fn([1, 2, 3], 10) == 16

def test_c_with_initial_fully_applied():
    assert reduce.c(lambda a, b: a + b, [1, 2, 3], 10) == 16

def test_c_with_initial_empty_sequence():
    assert reduce.c(lambda a, b: a + b, [], 99) == 99  # pyright: ignore[reportOperatorIssue, reportUnknownLambdaType]

def test_c_with_heterogeneous_initial():
    fn = reduce.c(lambda acc, x: acc + [x * 2])
    assert fn([1, 2, 3], cast(list[int], [])) == [2, 4, 6]

