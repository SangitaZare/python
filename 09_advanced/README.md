# 09 · Advanced Python

Run the examples:

```bash
python 09_advanced/examples.py
```

These are the topics that separate a beginner from a confident Python developer, and interviewers love them.

## 1. Iterables vs iterators

- An **iterable** is anything you can loop over: a list, string, dict, file or range. It has an `__iter__` method.
- An **iterator** is an object that produces values **one at a time** and remembers where it is. It has a `__next__` method.

```python
nums = [1, 2, 3]          # iterable
it = iter(nums)           # get an iterator from it
next(it)                  # 1
next(it)                  # 2
next(it)                  # 3
next(it)                  # StopIteration: the iterator is used up
```

A `for` loop does exactly this behind the scenes: it calls `iter()`, then `next()` repeatedly, and stops when it hits `StopIteration`.

An iterator can only be used **once**. A list can be looped over as many times as you like.

### A custom iterator class

```python
class Countdown:
    def __init__(self, start):
        self.current = start
    def __iter__(self):
        return self
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1
```

## 2. Generators

A generator is the **easy way to write an iterator**. It is a function that uses `yield` instead of `return`.

```python
def countdown(start):
    while start > 0:
        yield start        # pause here, hand out the value, and resume on the next call
        start -= 1

for n in countdown(3):
    print(n)               # 3, 2, 1
```

- Calling `countdown(3)` **does not run the code**. It returns a generator object.
- Each `next()` runs the code until the next `yield`, then **pauses** with all local variables saved.
- Generators are **lazy**: they produce values only when asked, so memory use stays tiny.

```python
nums_list = [x * x for x in range(10_000_000)]  # ~80+ MB in memory
nums_gen  = (x * x for x in range(10_000_000))  # ~200 bytes!
```

Generators can also be **infinite**, and you can **chain** them into pipelines:

```python
lines   = (line for line in open("big.log"))
errors  = (l for l in lines if "ERROR" in l)
first_5 = itertools.islice(errors, 5)
```

`yield from other_generator` hands out every value from another generator.

## 3. Useful iteration tools: `itertools`

```python
from itertools import count, cycle, islice, chain, combinations, permutations, groupby, accumulate
list(islice(count(10), 3))              # [10, 11, 12]
list(chain([1, 2], [3]))                # [1, 2, 3]
list(combinations("ABC", 2))            # [('A','B'), ('A','C'), ('B','C')]
list(accumulate([1, 2, 3, 4]))          # [1, 3, 6, 10] running total
```

Also useful: `any()`, `all()`, `zip()`, `enumerate()`, `sorted()`, `reversed()`, `min()`/`max()` with `key=`.

## 4. Decorators

A decorator is a function that **wraps another function** to add behaviour *without changing its code*. Examples are logging, timing, caching, authentication and retrying.

It is built from what we learned in topic 05: functions are objects, and closures remember variables.

```python
import functools

def log_calls(func):
    @functools.wraps(func)                  # keeps func's name and docstring
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}{args}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_calls                                  # same as: add = log_calls(add)
def add(a, b):
    return a + b
```

**`@decorator` is just syntax sugar for `func = decorator(func)`.**

### Decorators with arguments (3 levels)

```python
def repeat(times):                 # 1. takes the decorator's arguments
    def decorator(func):           # 2. takes the function
        @functools.wraps(func)
        def wrapper(*args, **kwargs):   # 3. replaces the function
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def hello(): print("hi")
```

### Built-in decorators you already know or will use

`@property`, `@classmethod`, `@staticmethod`, `@dataclass`, `@functools.lru_cache` (caches results), `@contextmanager`.

```python
@functools.lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
fib(100)   # instant, because each result is cached
```

## 5. Type hints

Type hints document what types a function expects and returns. Python **does not enforce** them at runtime. Editors (VS Code) and tools like `mypy` use them to catch bugs early.

```python
def average(scores: list[float]) -> float: ...
def find_user(user_id: int) -> dict[str, str] | None: ...     # | None means "may return None"
def greet(name: str, times: int = 1) -> None: ...

from typing import Callable, Iterator, TypedDict, Literal, Any
def apply(func: Callable[[int], int], value: int) -> int: ...
def counter(n: int) -> Iterator[int]: yield from range(n)
Mode = Literal["r", "w"]
```

Modern syntax (Python 3.10+): use `list[int]`, `dict[str, int]` and `X | None` instead of `List`, `Dict` and `Optional` from `typing`.

## 6. Other handy advanced features

```python
# Unpacking in all its forms
a, *middle, b = [1, 2, 3, 4, 5]
merged = {**defaults, **overrides}
combined = [*list1, *list2]

# Sorting by multiple keys
sorted(people, key=lambda p: (-p["age"], p["name"]))

# Ternary + walrus inside a comprehension
results = [y for x in data if (y := transform(x)) is not None]
```

## Bonus: GIL, threads and processes (concepts only)

- The **GIL** (Global Interpreter Lock) lets only one thread run Python bytecode at a time in standard CPython.
- So **threads** help with **I/O-bound** work (network, files, waiting), but not with CPU-heavy work.
- For **CPU-bound** work (heavy calculations), use **multiprocessing**. Each process has its own GIL.
- `asyncio` handles many I/O tasks in a single thread using `async`/`await`.
- Python 3.13+ offers an optional experimental "free-threaded" build without the GIL.

## Common mistakes

- Trying to reuse a used-up generator or iterator. The second loop gives nothing.
- Forgetting `@functools.wraps`, so the decorated function loses its name and docstring.
- Forgetting to `return result` inside a decorator's wrapper, so the function suddenly returns `None`.
- Expecting type hints to stop wrong types at runtime. They don't.
- Calling `len()` on a generator. Generators have no length; convert with `list()` first, if the data is small.

---

## Interview questions

**1. What is the difference between an iterable and an iterator?**
An iterable can be looped over: it has `__iter__`, which returns an iterator. An iterator produces values with `__next__`, keeps track of its state, and raises `StopIteration` at the end. Every iterator is iterable, but not every iterable is an iterator (a list, for example).

**2. What is a generator, and why use one?**
A function that uses `yield` to produce values lazily, one at a time, pausing between them. It is memory-efficient for large or infinite sequences, and it is a simple way to write an iterator.

**3. What is the difference between `yield` and `return`?**
`return` ends the function and sends back one value. `yield` sends back a value and **pauses** the function, keeping its state, so it can resume and produce more values.

**4. What is the difference between a generator expression and a list comprehension?**
`(x for x in data)` is lazy and uses almost no memory, but it can only be used once. `[x for x in data]` builds the whole list in memory, and it can be reused and indexed.

**5. What is a decorator?**
A function that takes a function and returns a new function that adds behaviour around it. `@dec` above `def f` means `f = dec(f)`. Typical uses are logging, timing, caching, authentication checks and retries.

**6. Why use `functools.wraps`?**
It copies the original function's `__name__`, `__doc__` and other metadata onto the wrapper. Without it, debugging, logging and documentation all show `wrapper` instead of the real function name.

**7. How do you write a decorator that takes arguments?**
Add an extra outer function: `def repeat(n): def decorator(func): def wrapper(...): ...`. `@repeat(3)` first calls `repeat(3)`, which returns the real decorator.

**8. What does `lru_cache` do?**
It memoises a function: it caches results by their arguments, so repeated calls return instantly. It turns recursive Fibonacci from exponential time into linear time.

**9. Are type hints enforced in Python?**
No. They are ignored at runtime. They help with readability and IDE autocomplete, and static checkers like `mypy` and libraries like Pydantic or FastAPI make use of them.

**10. What is the GIL?**
The Global Interpreter Lock in CPython allows only one thread to execute Python bytecode at a time. Threads still help with I/O-bound tasks. For CPU-bound tasks, use multiprocessing.

**11. How would you process a 50 GB log file and count the error lines?**
Use a generator pipeline that reads one line at a time: `sum(1 for line in open(path) if "ERROR" in line)`. The memory use stays constant whatever the file size.

---

## Practice

1. Write a generator `even_numbers(limit)` that yields even numbers up to `limit`.
2. Write an infinite generator `fibonacci()` and print the first 10 values using `itertools.islice`.
3. Write a `@timer` decorator that prints how long a function took to run.
4. Write a `@retry(times=3)` decorator that retries a function if it raises an exception.
5. Add type hints to 3 functions from earlier topics.
6. Compare the memory size of `[x for x in range(1_000_000)]` and `(x for x in range(1_000_000))` using `sys.getsizeof`.
