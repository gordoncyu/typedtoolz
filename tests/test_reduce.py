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
    with pytest.raises(TypeError, match="reduce\\(\\) of empty sequence with no initial value"):
        reduce(lambda a, b: a + b, cast(list[int], []))

def test_string_concat():
    assert reduce(lambda a, b: a + b, ["a", "b", "c"]) == "abc"

def test_generator_input():
    assert reduce(lambda a, b: a + b, (x for x in [1, 2, 3])) == 6


# ── reduce.c (curry(2, reduce)) — curries function + sequence ─────────────────

def test_c_curried_function_then_sequence():
    add = reduce.c(lambda a, b: a + b)
    assert add([1, 2, 3]) == 6

def test_c_fully_applied():
    assert reduce.c(lambda a, b: a + b, [1, 2, 3]) == 6


# ── reduce.ci (curry(reduce._reduce)) — curries function + sequence + initial ──

def test_ci_fully_applied():
    assert reduce.ci(lambda a, b: a + b, 0, [1, 2, 3]) == 6

def test_ci_curried_step_by_step():
    step1 = reduce.ci(lambda a, b: a + b)
    step2 = step1(0)
    assert step2([1, 2, 3]) == 6

def test_ci_with_heterogeneous_initial():
    result = reduce.ci(lambda acc, x: acc + [x], cast(list[int], []), [1, 2, 3])
    assert result == [1, 2, 3]
