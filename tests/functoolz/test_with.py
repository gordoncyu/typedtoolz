import pytest
from contextlib import contextmanager
from typedtoolz.functoolz import with_, with_op


# ── helpers ───────────────────────────────────────────────────────────────────

@contextmanager
def managed(value):
    yield value

@contextmanager
def managed_labeled(label, *, prefix=""):
    yield f"{prefix}{label}"

log = []

@contextmanager
def tracked(value):
    log.append(f"enter:{value}")
    try:
        yield value
    finally:
        log.append(f"exit:{value}")


# ── with_ — direct ContextManager ─────────────────────────────────────────────

def test_with_direct_cm_passes_value():
    result = with_(managed(42), lambda x: x * 2)
    assert result == 84

def test_with_direct_cm_body_return_passed_through():
    assert with_(managed("hi"), str.upper) == "HI"

def test_with_direct_cm_exit_called():
    log.clear()
    with_(tracked("a"), lambda x: x)
    assert log == ["enter:a", "exit:a"]

def test_with_direct_cm_exit_called_on_exception():
    log.clear()
    def raise_val(x):
        raise ValueError
    with pytest.raises(ValueError):
        with_(tracked("b"), raise_val)
    assert "exit:b" in log


# ── with_ — zero-arg factory ──────────────────────────────────────────────────

def test_with_factory_passes_value():
    result = with_(lambda: managed(99), lambda x: x + 1)
    assert result == 100

def test_with_factory_called_each_time():
    count = []
    def factory():
        count.append(1)
        return managed("x")
    with_(factory, lambda x: x)
    with_(factory, lambda x: x)
    assert len(count) == 2


# ── with_.c ───────────────────────────────────────────────────────────────────

def test_with_c_partial_res_then_body():
    result = with_.c(managed(10))(lambda x: x + 5)
    assert result == 15

def test_with_c_fully_applied():
    assert with_.c(managed(3), lambda x: x * 3) == 9

def test_with_c_factory_partial():
    result = with_.c(lambda: managed("hello"))(str.upper)
    assert result == "HELLO"


# ── with_.p ───────────────────────────────────────────────────────────────────

def test_with_p_returns_callable():
    fn = with_.p(managed_labeled, lambda s: s.upper())
    assert callable(fn)

def test_with_p_passes_args_to_factory():
    fn = with_.p(managed_labeled, lambda s: s)
    assert fn("world") == "world"

def test_with_p_passes_kwargs_to_factory():
    fn = with_.p(managed_labeled, lambda s: s)
    assert fn("world", prefix="hello_") == "hello_world"

def test_with_p_called_multiple_times():
    fn = with_.p(managed_labeled, lambda s: s)
    assert fn("a") == "a"
    assert fn("b") == "b"


# ── with_.pc ──────────────────────────────────────────────────────────────────

def test_with_pc_partial_res_then_body():
    fn = with_.pc(managed_labeled)(lambda s: s.upper())
    assert fn("test") == "TEST"

def test_with_pc_fully_applied():
    fn = with_.pc(managed_labeled, lambda s: s)
    assert fn("x") == "x"


# ── with_op — direct ContextManager ──────────────────────────────────────────

def test_with_op_direct_cm_passes_value():
    result = with_op(lambda x: x * 2, managed(42))
    assert result == 84

def test_with_op_direct_cm_body_return_passed_through():
    assert with_op(str.upper, managed("hi")) == "HI"

def test_with_op_exit_called():
    log.clear()
    with_op(lambda x: x, tracked("c"))
    assert log == ["enter:c", "exit:c"]


# ── with_op — zero-arg factory ────────────────────────────────────────────────

def test_with_op_factory_passes_value():
    result = with_op(lambda x: x + 1, lambda: managed(99))
    assert result == 100


# ── with_op.c ────────────────────────────────────────────────────────────────

def test_with_op_c_partial_body_then_res():
    result = with_op.c(lambda x: x + 5)(managed(10))
    assert result == 15

def test_with_op_c_fully_applied():
    assert with_op.c(lambda x: x * 3, managed(3)) == 9

def test_with_op_c_body_curried_before_resource():
    get = with_op.c(str.upper)
    assert get(managed("hello")) == "HELLO"
    assert get(managed("world")) == "WORLD"


# ── with_op.p ────────────────────────────────────────────────────────────────

def test_with_op_p_returns_callable():
    fn = with_op.p(lambda s: s.upper(), managed_labeled)
    assert callable(fn)

def test_with_op_p_passes_args_to_factory():
    fn = with_op.p(lambda s: s, managed_labeled)
    assert fn("world") == "world"

def test_with_op_p_passes_kwargs_to_factory():
    fn = with_op.p(lambda s: s, managed_labeled)
    assert fn("world", prefix="hello_") == "hello_world"


# ── with_op.pc ───────────────────────────────────────────────────────────────

def test_with_op_pc_partial_body_then_res():
    fn = with_op.pc(lambda s: s.upper())(managed_labeled)
    assert fn("test") == "TEST"

def test_with_op_pc_fully_applied():
    fn = with_op.pc(lambda s: s, managed_labeled)
    assert fn("x") == "x"
