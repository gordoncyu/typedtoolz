from typedtoolz.functoolz import return_parameter as rp
from typing import TypeAlias, cast, Callable


# ── last ──────────────────────────────────────────────────────────────────────

@rp.last.only(lambda: cast(list[str], list()))
def last_only_fill(items: list[str], acc: list[str]) -> None:
    acc.extend(items)

@rp.last.joined.in_tuple(lambda: cast(list[str], list()))
def last_in_tuple_fill(items: list[str], acc: list[str]) -> int:
    acc.extend(items)
    return len(acc)

@rp.last.joined.with_tuple(lambda: cast(list[str], list()))
def last_with_tuple_fill(items: list[str], acc: list[str]) -> tuple[int, bool]:
    acc.extend(items)
    return (len(acc), len(acc) > 2)


def test_last_only():
    assert last_only_fill(["a", "b"]) == ["a", "b"]

def test_last_only_fresh_each_call():
    last_only_fill(["a"])
    assert last_only_fill(["b"]) == ["b"]

def test_last_joined_in_tuple():
    acc, count = last_in_tuple_fill(["x", "y", "z"])
    assert acc == ["x", "y", "z"]
    assert count == 3

def test_last_joined_with_tuple():
    acc, n, big = last_with_tuple_fill(["a", "b", "c"])
    assert acc == ["a", "b", "c"]
    assert n == 3
    assert big is True

def test_last_joined_with_tuple_small():
    acc, n, big = last_with_tuple_fill(["a"])
    assert acc == ["a"]
    assert n == 1
    assert big is False


# ── first ─────────────────────────────────────────────────────────────────────

@rp.first.only(lambda: cast(list[str], list()))
def first_only_fill(acc: list[str], items: list[str]) -> None:
    acc.extend(items)

@rp.first.joined.in_tuple(lambda: cast(list[str], list()))
def first_in_tuple_fill(acc: list[str], items: list[str]) -> int:
    acc.extend(items)
    return len(acc)

@rp.first.joined.with_tuple(lambda: cast(list[str], list()))
def first_with_tuple_fill(acc: list[str], items: list[str]) -> tuple[int, bool]:
    acc.extend(items)
    return (len(acc), len(acc) > 2)


def test_first_only():
    assert first_only_fill(["a", "b"]) == ["a", "b"]

def test_first_only_fresh_each_call():
    first_only_fill(["a"])
    assert first_only_fill(["b"]) == ["b"]

def test_first_joined_in_tuple():
    acc, count = first_in_tuple_fill(["x", "y", "z"])
    assert acc == ["x", "y", "z"]
    assert count == 3

def test_first_joined_with_tuple():
    acc, n, big = first_with_tuple_fill(["a", "b", "c"])
    assert acc == ["a", "b", "c"]
    assert n == 3
    assert big is True

def test_first_joined_with_tuple_small():
    acc, n, big = first_with_tuple_fill(["a"])
    assert acc == ["a"]
    assert n == 1
    assert big is False


# ── recursive ─────────────────────────────────────────────────────────────────

NestedIntList: TypeAlias = list["int | NestedIntList"]

@rp.last.only(lambda: cast(list[int], list()))
def last_flatten(items: NestedIntList, acc: list[int]) -> None:
    for item in items:
        if isinstance(item, list):
            last_flatten(item)
        else:
            acc.append(item)

@rp.last.joined.in_tuple(lambda: cast(list[int], list()))
def last_flatten_counted(items: NestedIntList, acc: list[int]) -> int:
    count = 0
    for item in items:
        if isinstance(item, list):
            acc, sub = last_flatten_counted(item)
            count += sub
        else:
            acc.append(item)
            count += 1
    return count

@rp.last.joined.with_tuple(lambda: cast(list[int], list()))
def last_flatten_stats(items: NestedIntList, acc: list[int]) -> tuple[int, int]:
    count = 0
    depth = 0
    for item in items:
        if isinstance(item, list):
            _, sub_count, sub_depth = last_flatten_stats(item)
            count += sub_count
            depth = max(depth, sub_depth + 1)
        else:
            acc.append(item)
            count += 1
    return (count, depth)

@rp.first.only(lambda: cast(list[int], list()))
def first_flatten(acc: list[int], items: NestedIntList) -> None:
    for item in items:
        if isinstance(item, list):
            first_flatten(item)
        else:
            acc.append(item)

@rp.first.joined.in_tuple(lambda: cast(list[int], list()))
def first_flatten_counted(acc: list[int], items: NestedIntList) -> int:
    count = 0
    for item in items:
        if isinstance(item, list):
            _, sub = first_flatten_counted(item)
            count += sub
        else:
            acc.append(item)
            count += 1
    return count

@rp.first.joined.with_tuple(lambda: cast(list[int], list()))
def first_flatten_stats(acc: list[int], items: NestedIntList) -> tuple[int, int]:
    count = 0
    depth = 0
    for item in items:
        if isinstance(item, list):
            _, sub_count, sub_depth = first_flatten_stats(item)
            count += sub_count
            depth = max(depth, sub_depth + 1)
        else:
            acc.append(item)
            count += 1
    return (count, depth)


def test_last_only_recursive():
    assert last_flatten([[1, [2, 3]], 4, [5, [6, 7]]]) == [1, 2, 3, 4, 5, 6, 7]

def test_last_only_recursive_fresh_each_call():
    last_flatten([1, 2])
    assert last_flatten([3, 4]) == [3, 4]

def test_last_joined_in_tuple_recursive():
    acc, count = last_flatten_counted([[1, [2, 3]], 4])
    assert acc == [1, 2, 3, 4]
    assert count == 4

def test_last_joined_with_tuple_recursive():
    acc, count, depth = last_flatten_stats([[1, [2, 3]], 4])
    assert acc == [1, 2, 3, 4]
    assert count == 4
    assert depth == 2

def test_first_only_recursive():
    assert first_flatten([[1, [2, 3]], 4, [5, [6, 7]]]) == [1, 2, 3, 4, 5, 6, 7]

def test_first_only_recursive_fresh_each_call():
    first_flatten([1, 2])
    assert first_flatten([3, 4]) == [3, 4]

def test_first_joined_in_tuple_recursive():
    acc, count = first_flatten_counted([[1, [2, 3]], 4])
    assert acc == [1, 2, 3, 4]
    assert count == 4

def test_first_joined_with_tuple_recursive():
    acc, count, depth = first_flatten_stats([[1, [2, 3]], 4])
    assert acc == [1, 2, 3, 4]
    assert count == 4
    assert depth == 2
