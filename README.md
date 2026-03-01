# typedtoolz

A typed functional utility library for Python 3.12+, extending [toolz](https://toolz.readthedocs.io) with precise type signatures and additional patterns.

## Contents

- [Installation](#installation)
- [Overview](#overview)
- [functoolz](#functoolz)
  - [`curry` / `curryv`](#curry--curryv)
  - [`pipe` / `flow`](#pipe--flow)
  - [`reduce`](#reduce)
  - [`excepts` / `union_error` / `tuple_error` / `remap_error`](#excepts--union_error--tuple_error--remap_error)
  - [`defer`](#defer)
  - [`with_` / `with_op`](#with_--with_op)
  - [`return_parameter`](#return_parameter)
- [itertoolz](#itertoolz)
  - [`map`](#map)
  - [`takewhile_acc`](#takewhile_acc)
- [Root utilities](#root-utilities)
- [Requirements](#requirements)

---

## Installation

```bash
pip install git+https://github.com/gordoncyu/typedtoolz.git
```

## Overview

```
typedtoolz
├── functoolz    - function composition, error handling, resource management
└── itertoolz    - typed iteration utilities
```

---

## functoolz

### `curry` / `curryv`

Enables partial application: call a function with fewer arguments than it needs and get back a callable that accepts the rest.

```python
from typedtoolz.functoolz import curry, curryv

@curry
def mul(x: int, y: int) -> int:
    return x * y
```

```python
>>> double = mul(2)
>>> double(10)
20
>>> mul(2, 10)
20
```

> **How signatures change:** currying erases argument *names* for all positions that become curryable--the types are preserved, but callers see positional-only slots rather than named parameters, and the docstring is lost. Without an explicit `n`, `curry` also treats any positional-but-optional parameters as required, since it cannot tell them apart from required ones at the type level. `curry(n, fn)` solves this by declaring exactly how many arguments must be satisfied before the function fires--optional positionals beyond position `n` are stripped from the required slots entirely. `curryv` works the same way but additionally preserves optional positionals and keyword-only args past position `n` in the visible signature. Note that because the type system cannot track whether a keyword argument has already been supplied in an earlier partial call, those args will remain visible in the signature even after being fulfilled. Because of these caveats, many of the functions typedtoolz aren't curried but have a `.c`-prefixed members that are curried so that others can still easily read function descriptions and parameter names.

```python
@curryv(2)
def greet(name: str, greeting: str, *, punct: str = "!") -> str:
    return f"{greeting}, {name}{punct}"
```

```python
>>> hello = greet(greeting="Hello")
>>> hello("World")
'Hello, World!'
>>> hello("World", punct=".")
'Hello, World.'
```

---

### `pipe` / `flow`

Without these, applying a sequence of transformations must be read right-to-left: `h(g(f(x)))`. `pipe` and `flow` let you write them left-to-right in the order they actually execute.

```python
from typedtoolz.functoolz import pipe, flow
```

```python
>>> pipe("  hello  ", str.strip, str.upper, lambda s: s + "!")
'HELLO!'
```

`flow(f, g, h)` returns a reusable composed function rather than applying immediately:

```python
shout = flow(str.strip, str.upper, lambda s: s + "!")
```

```python
>>> shout("  hello  ")
'HELLO!'
```

---

### `reduce`

Left fold over an iterable, compatible with `functools.reduce`.

```python
from typedtoolz.functoolz import reduce
```

```python
>>> reduce(lambda a, b: a + b, [1, 2, 3, 4, 5])
15
>>> reduce(lambda a, b: a + [b], [1, 2, 3], [])
[1, 2, 3]
>>> sum_all = reduce.c(lambda a, b: a + b)
>>> sum_all([1, 2, 3])
6
```

`reduce.c` is a curried variant without `initial` and `reduce.ci` is a curried variant with argument order `(func, initial, iterable)`

---

### `excepts` / `union_error` / `tuple_error` / `remap_error`

Wrap functions to handle exceptions in a functional style.

```python
from typedtoolz.functoolz import excepts, union_error, tuple_error, remap_error
```

**`excepts`** -- replace a caught exception with a handler's return value:

```python
safe_div = excepts(lambda e: 0, ZeroDivisionError, lambda x: 10 // x)
```

```python
>>> safe_div(0)
0
>>> safe_div(2)
5
```

**`union_error`** -- return the exception as a value instead of raising:

```python
safe_div = union_error(ZeroDivisionError, lambda x: 10 // x)
```

```python
>>> safe_div(0)
ZeroDivisionError('integer division or modulo by zero')
>>> safe_div(2)
5
```

**`tuple_error`** -- return `(True, value)` on success or `(False, exc)` on failure, for use with `match`:

```python
safe_div = tuple_error(ZeroDivisionError, lambda x: 10 // x)
```

```python
>>> match safe_div(2):
...     case (True, result): print(f"got {result}")
...     case (False, exc):   print(f"failed: {exc}")
got 5
>>> match safe_div(0):
...     case (True, result): print(f"got {result}")
...     case (False, exc):   print(f"failed: {exc}")
failed: integer division or modulo by zero
```

Pairs naturally with `with_` for resource-safe operations:

```python
safe_read = tuple_error(OSError, with_.c(open)(lambda f: f.read()))
```

```python
>>> match safe_read("file.txt"):
...     case (True, contents): print(contents[:40])
...     case (False, exc):     print(f"could not read: {exc}")
```

**`remap_error`** -- catch, remap, optionally log, and re-raise.

```python
import logging

def handle_request(request):
    ...

safe_handler = remap_error(
    lambda e: ("Internal error processing request", RuntimeError("500 Internal Server Error")),
    BaseException,
    handle_request,
    logger_method=logging.error,
)
```

```python
>>> safe_handler(bad_request)  # logs full details, raises generic RuntimeError to caller
RuntimeError('500 Internal Server Error')
```

---

### `defer`

Guarantees a cleanup function runs after a body, like a functional `try/finally`.

```python
from typedtoolz.functoolz import defer
```

```python
>>> defer(cleanup, do_work)  # cleanup() runs even if do_work() raises
```

**`defer.hof`** -- used as a decorator to guarantee cleanup runs after every call. The cleanup can receive the return of the body, but if the body raises, the cleanup receives `...` (Ellipsis) as the result:

```python
@defer.hof(lambda result: logger.info("finished, result: %s", result))
def process(data):
    ...
```

```python
>>> process(data)  # runs process(data), then logs result or logs ... on exception
```

**`defer.hof.defer_args`** -- two-stage: capture arguments for the cleanup first, then wrap the body:

```python
@defer.hof.defer_args(lambda result, label: logger.info("%s: %s", label, result))
def process(data):
    ...
```

```python
>>> tracked = process("my-job")
>>> tracked(data)  # runs process(data), then logs "my-job: <result>"
```

---

### `with_` / `with_op`

Apply a context manager functionally.

```python
from typedtoolz.functoolz import with_, with_op
```

`res` may be a `ContextManager` directly or a zero-argument factory:

```python
>>> with_(open("file.txt"), lambda f: f.read())
'...'
>>> with_(lambda: open("file.txt"), lambda f: f.read())
'...'
```

`with_op` flips the argument order--handy when currying the body first:

```python
read = with_op.c(lambda f: f.read())
```

```python
>>> read(open("file.txt"))
'...'
```

**`with_.p` / `with_op.p`** -- parametrised factory: the returned callable passes its arguments through to the resource factory:

```python
read_file = with_.p(open, lambda f: f.read())
```

```python
>>> read_file("file.txt", encoding="utf-8")
'...'
```

---

### `return_parameter`

The *return parameter* pattern: pass a mutable accumulator into a function, fill it, and get it back--without the caller managing it. Recursive calls transparently reuse the same accumulator.

```python
from typedtoolz.functoolz import return_parameter as rp
```

`first` / `last` selects whether the accumulator is the first or last parameter. Three decorator variants control what the caller receives:

#### `only(factory)` -- accumulator is the sole output

The function's own return value is discarded; the caller gets only the accumulator.

```python
@rp.last.only(list)
def flatten(items: list, acc: list) -> None:
    for item in items:
        if isinstance(item, list):
            flatten(item)   # recursive--reuses the same acc
        else:
            acc.append(item)
```

```python
>>> flatten([[1, [2, 3]], 4])
[1, 2, 3, 4]
```

#### `joined.in_tuple(factory)` -- returns `(acc, result)`

The caller gets a tuple of the accumulator and the function's scalar return value.

```python
@rp.last.joined.in_tuple(list)
def collect_counted(items: list, acc: list) -> int:
    acc.extend(items)
    return len(items)
```

```python
>>> collected, count = collect_counted([1, 2, 3])
>>> collected
[1, 2, 3]
>>> count
3
```

#### `joined.with_tuple(factory)` -- returns `(acc, *results)`

The function returns a tuple; the accumulator is prepended to it.

```python
@rp.last.joined.with_tuple(list)
def collect_stats(items: list, acc: list) -> tuple[int, int]:
    acc.extend(items)
    return (len(items), max(items))
```

```python
>>> collected, count, maximum = collect_stats([1, 2, 3])
>>> collected
[1, 2, 3]
>>> count, maximum
(3, 3)
```

---

## itertoolz

### `map`

Typed drop-in for the builtin `map`.

```python
from typedtoolz.itertoolz import map
```

```python
>>> list(map(str.upper, ["a", "b", "c"]))
['A', 'B', 'C']
>>> upper_all = map.c(str.upper)
>>> list(upper_all(["a", "b"]))
['A', 'B']
```

---

### `takewhile_acc`

Like `itertools.takewhile` but with an accumulator--the predicate can carry state across iterations.

```python
from typedtoolz.itertoolz import takewhile_acc

def under(limit):
    def func(acc, item):
        new = acc + item
        return (new < limit, new)   # (continue?, new_acc)
    return func
```

```python
>>> takewhile_acc(under(10), [1, 2, 3, 4, 5], 0)
[1, 2, 3]
>>> takewhile_acc(under(10), [1, 2, 3, 4, 5], 0, take_first_negative=True)
[1, 2, 3, 4]
```

The predicate can also return a `TypedDict` with a `"take"` key and any descriptive key name of your choice for the accumulator, which is useful when the accumulator has a clear domain meaning:

```python
>>> takewhile_acc(
...     lambda budget, price: {"take": budget >= price, "budget": budget - price},
...     [3, 2, 5, 1],
...     10,
... )
[3, 2, 5]
```

`takewhile_acc.c` curries `(func, iterable[, initial])`. `takewhile_acc.ci` curries with argument order `(func, initial, iterable)`, useful when building pipelines that supply the iterable last.

---

## Root utilities

```python
from typedtoolz import identity, identityv, return_none
```

```python
>>> identity(42)
42
>>> identityv(1, "a", 3)
(1, 'a', 3)
>>> return_none(1, 2, x=3) is None
True
```

---

## Requirements

- Python ≥ 3.12
- [toolz](https://github.com/pytoolz/toolz) ≥ 1.0.0
- [typing-extensions](https://pypi.org/project/typing-extensions/) == 4.10.0
