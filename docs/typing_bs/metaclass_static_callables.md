As is detailed elsewhere, curry strips docstrings, removes some keyword-positional's names making them just positional, and makes reading typing more difficult. So for comprehensibility by others who are not necessarily knowledgeable about this package or fp, it is best to put the curried version as a member of a properly docstringed callable namespace. So we want statically callable namespaces

# How to: statically callable namespaces

It's obvious right?
```python
from typing import Callable, Iterable


class obvious:
    @staticmethod
    def __call__[A, B](f: Callable[[A, B], A], i: A, s: Iterable[B]) -> A: ...

def add(a: int, b: int):
    return a + b

obvious(add, 0, [1, 2, 3])
```

```
Diagnostics:
1. Expected 0 positional arguments [reportCallIssue]
```
ah. It assumes we're calling the init function, not the callable

## Metaclass static callables
Metaclasses are classes that make classes. Hence we can control the creation of a class such that there is no init, or, at least, it's been overridden by the call method. I don't actually know all the details because I have not used metaclasses otherwise, but I know it works. Here is an example:

```python
from typing import override

class _reduce_metaclass(type):
    @staticmethod
    @override
    def __call__[A, B](f: Callable[[A, B], A], i: A, s: Iterable[B]) -> A: ...

class reduce(metaclass=_reduce_metaclass):
    """
    cool function
    """

reduce(add, 0, [1, 2, 3])
```

We get no warnings for the above, and the return type is typed in accordance with the `__call__` method we defined.
<a id="msc_hover_bs"></a>However, if you hover over the `reduce(add, 0, [1, 2, 3])` on `reduce`:

```
class reduce()
──────────────────────────────────────────────────────────────
Initialize self.  See help(type(self)) for accurate signature.
```

Huh. 


```python
foldl = reduce
foldl(add, 0, [1, 2, 3])
```

```
(type) foldl = reduce
─────────────────────
cool function
```

Huh. That's odd. Does python just like `foldl` better? Unfortunately not. For whatever reason if you simply set a variable named something else to the class and use the variable instead, the problem is solved. Actually you can use the same name for the variable, but if you import it into another file it will be broken again. And this is only a problem when the class is being called, and if it's not a member of something else, e.g. `foo.reduce`.

Anyway, that's how you do statically callable namespaces.
