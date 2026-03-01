from typedtoolz.functoolz import flow


inc  = lambda x: x + 1
dbl  = lambda x: x * 2
neg  = lambda x: -x


def test_flow_single():
    assert flow(inc)(3) == 4

def test_flow_two():
    assert flow(inc, str)(3) == "4"

def test_flow_three():
    # inc(3)=4, dbl(4)=8, str(8)="8"
    assert flow(inc, dbl, str)(3) == "8"

def test_flow_order():
    # order matters: neg then dbl ≠ dbl then neg
    assert flow(neg, dbl)(3) == -6   # dbl(neg(3)) = dbl(-3) = -6
    assert flow(dbl, neg)(3) == -6   # neg(dbl(3)) = neg(6) = -6 — same here
    assert flow(inc, neg)(3) == -4   # neg(inc(3)) = neg(4) = -4
    assert flow(neg, inc)(3) == -2   # inc(neg(3)) = inc(-3) = -2

def test_flow_returns_callable():
    assert callable(flow(inc))

def test_flow_string_pipeline():
    pipeline = flow(str.strip, str.upper, lambda s: s + "!")
    assert pipeline("  hello  ") == "HELLO!"
