import pytest
from typedtoolz.functoolz.exceptions import excepts, union_error, tuple_error, remap_error


# ── helpers ───────────────────────────────────────────────────────────────────

def good(x):
    return x * 2

def bad_value(x):
    raise ValueError("oops")

def bad_type(x):
    raise TypeError("nope")


# ── excepts ───────────────────────────────────────────────────────────────────

def test_excepts_success_returns_normally():
    fn = excepts(lambda e: -1, ValueError, good)
    assert fn(5) == 10

def test_excepts_caught_calls_handler():
    fn = excepts(lambda e: -1, ValueError, bad_value)
    assert fn(0) == -1

def test_excepts_handler_receives_exception():
    received = []
    fn = excepts(lambda e: received.append(e), ValueError, bad_value)
    fn(0)
    assert len(received) == 1
    assert isinstance(received[0], ValueError)

def test_excepts_uncaught_propagates():
    fn = excepts(lambda e: -1, TypeError, bad_value)
    with pytest.raises(ValueError):
        fn(0)

def test_excepts_tuple_of_exceptions():
    fn = excepts(lambda e: "caught", (ValueError, TypeError), bad_value)
    assert fn(0) == "caught"
    fn2 = excepts(lambda e: "caught", (ValueError, TypeError), bad_type)
    assert fn2(0) == "caught"

def test_excepts_passes_args_through():
    fn = excepts(lambda e: None, ValueError, lambda x, y: x + y)
    assert fn(3, 4) == 7


# ── excepts.c ─────────────────────────────────────────────────────────────────

def test_excepts_c_partial():
    handle = excepts.c(lambda e: -1)
    catch_val = handle(ValueError)
    fn = catch_val(bad_value)
    assert fn(0) == -1

def test_excepts_c_fully_applied():
    fn = excepts.c(lambda e: -1, ValueError, bad_value)
    assert fn(0) == -1

def test_excepts_c_success():
    fn = excepts.c(lambda e: -1, ValueError, good)
    assert fn(3) == 6


# ── union_error ───────────────────────────────────────────────────────────────

def test_union_error_success_returns_value():
    fn = union_error(ValueError, good)
    assert fn(4) == 8

def test_union_error_returns_exception_as_value():
    fn = union_error(ValueError, bad_value)
    result = fn(0)
    assert isinstance(result, ValueError)

def test_union_error_uncaught_propagates():
    fn = union_error(TypeError, bad_value)
    with pytest.raises(ValueError):
        fn(0)

def test_union_error_tuple_of_exceptions():
    fn = union_error((ValueError, TypeError), bad_value)
    assert isinstance(fn(0), ValueError)
    fn2 = union_error((ValueError, TypeError), bad_type)
    assert isinstance(fn2(0), TypeError)


# ── union_error.c ─────────────────────────────────────────────────────────────

def test_union_error_c_partial():
    fn = union_error.c(ValueError)(bad_value)
    assert isinstance(fn(0), ValueError)

def test_union_error_c_fully_applied():
    fn = union_error.c(ValueError, bad_value)
    assert isinstance(fn(0), ValueError)


# ── tuple_error ───────────────────────────────────────────────────────────────

def test_tuple_error_success_returns_true_tuple():
    fn = tuple_error(ValueError, good)
    ok, result = fn(5)
    assert ok is True
    assert result == 10

def test_tuple_error_failure_returns_false_tuple():
    fn = tuple_error(ValueError, bad_value)
    ok, result = fn(0)
    assert ok is False
    assert isinstance(result, ValueError)

def test_tuple_error_uncaught_propagates():
    fn = tuple_error(TypeError, bad_value)
    with pytest.raises(ValueError):
        fn(0)

def test_tuple_error_tuple_of_exceptions():
    fn = tuple_error((ValueError, TypeError), bad_value)
    ok, exc = fn(0)
    assert ok is False
    assert isinstance(exc, ValueError)


# ── tuple_error.c ─────────────────────────────────────────────────────────────

def test_tuple_error_c_partial():
    fn = tuple_error.c(ValueError)(good)
    ok, result = fn(3)
    assert ok is True
    assert result == 6

def test_tuple_error_c_failure():
    fn = tuple_error.c(ValueError)(bad_value)
    ok, exc = fn(0)
    assert ok is False
    assert isinstance(exc, ValueError)


# ── remap_error ───────────────────────────────────────────────────────────────

def test_remap_error_success_passes_through():
    fn = remap_error(lambda e: RuntimeError(), ValueError, good)
    assert fn(3) == 6

def test_remap_error_raises_remapped_exception():
    fn = remap_error(lambda e: RuntimeError("remapped"), ValueError, bad_value)
    with pytest.raises(RuntimeError, match="remapped"):
        fn(0)

def test_remap_error_original_not_raised():
    fn = remap_error(lambda e: RuntimeError(), ValueError, bad_value)
    with pytest.raises(RuntimeError):
        fn(0)

def test_remap_error_uncaught_propagates():
    fn = remap_error(lambda e: RuntimeError(), TypeError, bad_value)
    with pytest.raises(ValueError):
        fn(0)

def test_remap_error_tuple_handler_logs_message(caplog):
    import logging
    fn = remap_error(
        lambda e: ("something went wrong", RuntimeError("remapped")),
        ValueError,
        bad_value,
    )
    with caplog.at_level(logging.ERROR):
        with pytest.raises(RuntimeError):
            fn(0)
    assert "something went wrong" in caplog.text

def test_remap_error_custom_logger_method():
    log = []
    fn = remap_error(
        lambda e: ("msg", RuntimeError()),
        ValueError,
        bad_value,
        logger_method=log.append,
    )
    with pytest.raises(RuntimeError):
        fn(0)
    assert log == ["msg"]

def test_remap_error_tuple_of_exceptions():
    fn = remap_error(lambda e: RuntimeError(), (ValueError, TypeError), bad_value)
    with pytest.raises(RuntimeError):
        fn(0)


# ── remap_error.c ─────────────────────────────────────────────────────────────

def test_remap_error_c_partial():
    fn = remap_error.c(lambda e: RuntimeError("x"))(ValueError)(bad_value)
    with pytest.raises(RuntimeError, match="x"):
        fn(0)

def test_remap_error_c_fully_applied():
    fn = remap_error.c(lambda e: RuntimeError("y"), ValueError, bad_value)
    with pytest.raises(RuntimeError, match="y"):
        fn(0)

def test_remap_error_c_success():
    fn = remap_error.c(lambda e: RuntimeError(), ValueError, good)
    assert fn(4) == 8
