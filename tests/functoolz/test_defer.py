import pytest
from typedtoolz.functoolz import defer


# ── helpers ───────────────────────────────────────────────────────────────────

def _raise(exc: BaseException):
    raise exc


# ── defer ─────────────────────────────────────────────────────────────────────

def test_defer_returns_body_result():
    assert defer(lambda: None, lambda: 42) == 42

def test_defer_end_called_on_success():
    log = []
    defer(lambda: log.append("end"), lambda: log.append("body"))
    assert log == ["body", "end"]

def test_defer_end_called_on_exception():
    log = []
    with pytest.raises(ValueError):
        defer(lambda: log.append("end"), lambda: _raise(ValueError()))
    assert log == ["end"]

def test_defer_exception_propagates():
    with pytest.raises(ValueError):
        defer(lambda: None, lambda: _raise(ValueError()))


# ── defer.c ───────────────────────────────────────────────────────────────────

def test_defer_c_partial_then_call():
    log = []
    result = defer.c(lambda: log.append("end"))(lambda: 99)
    assert result == 99
    assert log == ["end"]

def test_defer_c_fully_applied():
    log = []
    result = defer.c(lambda: log.append("end"), lambda: 7)
    assert result == 7
    assert log == ["end"]

def test_defer_c_end_called_on_exception():
    log = []
    with pytest.raises(ValueError):
        defer.c(lambda: log.append("end"))(lambda: _raise(ValueError()))
    assert log == ["end"]


# ── defer.hof ─────────────────────────────────────────────────────────────────

def test_defer_hof_returns_callable():
    wrapped = defer.hof(lambda: None, lambda x: x)
    assert callable(wrapped)

def test_defer_hof_passes_args_through():
    wrapped = defer.hof(lambda: None, lambda x, y: x + y)
    assert wrapped(3, 4) == 7

def test_defer_hof_zero_arg_end_called_on_success():
    log = []
    wrapped = defer.hof(lambda: log.append("end"), lambda x: x * 2)
    assert wrapped(5) == 10
    assert log == ["end"]

def test_defer_hof_zero_arg_end_called_on_exception():
    log = []
    wrapped = defer.hof(lambda: log.append("end"), lambda x: _raise(ValueError()))
    with pytest.raises(ValueError):
        wrapped(1)
    assert log == ["end"]

def test_defer_hof_one_arg_end_receives_return_value():
    received = []
    wrapped = defer.hof(lambda r: received.append(r), lambda x: x * 2)
    wrapped(5)
    assert received == [10]

def test_defer_hof_one_arg_end_receives_ellipsis_on_exception():
    received = []
    wrapped = defer.hof(lambda r: received.append(r), lambda x: _raise(ValueError()))
    with pytest.raises(ValueError):
        wrapped(1)
    assert received == [...]

def test_defer_hof_called_multiple_times():
    log = []
    wrapped = defer.hof(lambda: log.append("end"), lambda x: x)
    wrapped(1)
    wrapped(2)
    assert log == ["end", "end"]


# ── defer.hof.c ───────────────────────────────────────────────────────────────

def test_defer_hof_c_partial_then_call():
    log = []
    wrapped = defer.hof.c(lambda: log.append("end"))(lambda x: x * 3)
    assert wrapped(4) == 12
    assert log == ["end"]

def test_defer_hof_c_fully_applied():
    log = []
    wrapped = defer.hof.c(lambda: log.append("end"), lambda x: x)
    assert wrapped(9) == 9
    assert log == ["end"]

def test_defer_hof_c_end_called_on_exception():
    log = []
    wrapped = defer.hof.c(lambda: log.append("end"))(lambda x: _raise(RuntimeError()))
    with pytest.raises(RuntimeError):
        wrapped(0)
    assert log == ["end"]


# ── defer.hof.defer_args ──────────────────────────────────────────────────────

def test_defer_hof_defer_args_basic():
    log = []
    def end(result, label):
        log.append((result, label))
    wrapped = defer.hof.defer_args(end, lambda x: x * 2)("op")
    assert wrapped(5) == 10
    assert log == [(10, "op")]

def test_defer_hof_defer_args_ellipsis_on_exception():
    log = []
    def end(result, label):
        log.append((result, label))
    wrapped = defer.hof.defer_args(end, lambda x: _raise(ValueError()))("op")
    with pytest.raises(ValueError):
        wrapped(1)
    assert log == [(..., "op")]

def test_defer_hof_defer_args_kwargs():
    log = []
    def end(result, *, label):
        log.append((result, label))
    wrapped = defer.hof.defer_args(end, lambda x: x)(label="test")
    assert wrapped(7) == 7
    assert log == [(7, "test")]

def test_defer_hof_defer_args_multiple_eargs():
    log = []
    def end(result, a, b):
        log.append((result, a, b))
    wrapped = defer.hof.defer_args(end, lambda x: x)("foo", "bar")
    wrapped(3)
    assert log == [(3, "foo", "bar")]


# ── defer.hof.defer_args.c ────────────────────────────────────────────────────

def test_defer_hof_defer_args_c_partial_then_call():
    log = []
    def end(result, label):
        log.append((result, label))
    wrapped = defer.hof.defer_args.c(end)(lambda x: x + 1)("op")(9)
    assert wrapped == 10
    assert log == [(10, "op")]

def test_defer_hof_defer_args_c_fully_applied():
    log = []
    def end(result, label):
        log.append((result, label))
    make = defer.hof.defer_args.c(end, lambda x: x)
    assert make("lbl")(5) == 5
    assert log == [(5, "lbl")]

def test_defer_hof_defer_args_c_ellipsis_on_exception():
    log = []
    def end(result, label):
        log.append((result, label))
    wrapped = defer.hof.defer_args.c(end)(lambda x: _raise(RuntimeError()))("op")
    with pytest.raises(RuntimeError):
        wrapped(0)
    assert log == [(..., "op")]
