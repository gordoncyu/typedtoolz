import pytest
from typedtoolz.itertoolz import takewhile_acc


# ── helpers ───────────────────────────────────────────────────────────────────

def under(limit):
    """Take while running sum stays under limit."""
    def func(acc, item):
        new = acc + item
        return (new < limit, new)
    return func

def under_dict(limit):
    """Same predicate using TakeAcc dict form."""
    def func(acc, item):
        new = acc + item
        return {"take": new < limit, "acc": new}
    return func

def always_take(acc, item):
    return (True, acc)

def never_take(acc, item):
    return (False, acc)


# ── basic tuple return ────────────────────────────────────────────────────────

def test_takes_while_predicate_holds():
    result = takewhile_acc(under(10), [1, 2, 3, 4, 5], 0)
    assert result == [1, 2, 3]

def test_stops_on_first_false():
    result = takewhile_acc(never_take, [1, 2, 3], 0)
    assert result == []

def test_takes_all_when_always_true():
    result = takewhile_acc(always_take, [1, 2, 3], 0)
    assert result == [1, 2, 3]

def test_empty_iterable_with_initial():
    result = takewhile_acc(under(10), [], 0)
    assert result == []

def test_single_item_passes():
    result = takewhile_acc(under(10), [5], 0)
    assert result == [5]

def test_single_item_fails():
    result = takewhile_acc(under(10), [15], 0)
    assert result == []

def test_accumulator_updates_correctly():
    # running sum: 3, 6, 9, 12 — stops at 12
    result = takewhile_acc(under(12), [3, 3, 3, 3], 0)
    assert result == [3, 3, 3]


# ── TakeAcc dict return ───────────────────────────────────────────────────────

def test_dict_form_takes_while_predicate_holds():
    result = takewhile_acc(under_dict(10), [1, 2, 3, 4, 5], 0)
    assert result == [1, 2, 3]

def test_dict_form_stops_correctly():
    result = takewhile_acc(under_dict(10), [5, 5, 5], 0)
    assert result == [5]

def test_dict_form_all_pass():
    result = takewhile_acc(under_dict(100), [1, 2, 3], 0)
    assert result == [1, 2, 3]


# ── take_first_negative ───────────────────────────────────────────────────────

def test_take_first_negative_includes_failing_item():
    result = takewhile_acc(under(10), [1, 2, 3, 4, 5], 0, take_first_negative=True)
    assert result == [1, 2, 3, 4]

def test_take_first_negative_false_excludes_failing_item():
    result = takewhile_acc(under(10), [1, 2, 3, 4, 5], 0, take_first_negative=False)
    assert result == [1, 2, 3]

def test_take_first_negative_on_first_item():
    result = takewhile_acc(never_take, [1, 2, 3], 0, take_first_negative=True)
    assert result == [1]

def test_take_first_negative_empty_iterable():
    result = takewhile_acc(never_take, [], 0, take_first_negative=True)
    assert result == []

def test_take_first_negative_dict_form():
    result = takewhile_acc(under_dict(10), [1, 2, 3, 4, 5], 0, take_first_negative=True)
    assert result == [1, 2, 3, 4]


# ── no initial ────────────────────────────────────────────────────────────────

def test_no_initial_empty_raises():
    with pytest.raises(TypeError):
        takewhile_acc(under(10), [])

def test_no_initial_uses_first_element_as_acc():
    # first element (3) becomes initial acc; remaining items tested against it
    def within_5_of_acc(acc, item):
        return (abs(item - acc) <= 5, item)
    result = takewhile_acc(within_5_of_acc, [3, 5, 7, 20])
    assert result == [5, 7]


# ── takewhile_acc.c ───────────────────────────────────────────────────────────

def test_c_partial_func_then_iterable():
    fn = takewhile_acc.c(under(10))
    assert fn([1, 2, 3, 4, 5], 0) == [1, 2, 3]

def test_c_fully_applied():
    assert takewhile_acc.c(under(10), [1, 2, 3, 4, 5], 0) == [1, 2, 3]

def test_c_with_take_first_negative():
    fn = takewhile_acc.c(under(10))
    assert fn([1, 2, 3, 4, 5], 0, take_first_negative=True) == [1, 2, 3, 4]


# ── takewhile_acc.ci ──────────────────────────────────────────────────────────

def test_ci_partial_step_by_step():
    step1 = takewhile_acc.ci(under(10))
    step2 = step1(0)
    assert step2([1, 2, 3, 4, 5]) == [1, 2, 3]

def test_ci_fully_applied():
    assert takewhile_acc.ci(under(10), 0, [1, 2, 3, 4, 5]) == [1, 2, 3]

def test_ci_with_take_first_negative():
    result = takewhile_acc.ci(under(10), 0, [1, 2, 3, 4, 5], True)
    assert result == [1, 2, 3, 4]
