omap = map
from typedtoolz.itertoolz import map

def test_map_doubles():
    def double(x: int) -> int:
        return x * 2
    doublem = map.c(double)
    res = doublem([1, 2, 3])
    res = list(res)
    assert res == [2, 4, 6]

def test_map_upper():
    _ = map.c(str.upper)
    _ = _(["a", "b"])
    assert list(_) == ["A", "B"]
