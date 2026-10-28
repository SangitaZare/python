"""09 - Advanced: iterators, generators, itertools, decorators, type hints."""
import functools
import itertools
import sys
import time
from typing import Callable, Iterator

print("=== 1. Iterables vs iterators ===")
nums = [1, 2, 3]
it = iter(nums)
print("  next(it):", next(it), next(it), next(it))
try:
    next(it)
except StopIteration:
    print("  StopIteration: the iterator is used up")
print("  the list can still be looped again:", [n for n in nums])


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


print("  custom iterator class:", list(Countdown(5)))

print("\n=== 2. Generators ===")


def countdown(start):
    print("    (generator body started)")
    while start > 0:
        yield start
        start -= 1


gen = countdown(3)
print("  calling countdown(3) gives:", type(gen).__name__, "(nothing ran yet)")
print("  next(gen):", next(gen))
print("  rest:", list(gen))
print("  reuse used-up generator:", list(gen), "<- empty!")

big_list = [x * x for x in range(1_000_000)]
big_gen = (x * x for x in range(1_000_000))
print(f"  memory: list = {sys.getsizeof(big_list):,} bytes | generator = {sys.getsizeof(big_gen)} bytes")
print("  sum via generator:", sum(x * x for x in range(1_000_000)))


def fibonacci():
    a, b = 0, 1
    while True:  # infinite, which is fine because it's lazy
        yield a
        a, b = b, a + b


print("  first 10 fibonacci:", list(itertools.islice(fibonacci(), 10)))


def read_lines():
    yield from ["INFO start", "ERROR disk full", "INFO ok", "ERROR timeout", "INFO done"]


errors = (line for line in read_lines() if line.startswith("ERROR"))
messages = (line.split(" ", 1)[1] for line in errors)
print("  generator pipeline:", list(messages))

print("\n=== 3. itertools & friends ===")
print("  count + islice:", list(itertools.islice(itertools.count(10, 5), 4)))
print("  cycle:", list(itertools.islice(itertools.cycle("AB"), 5)))
print("  chain:", list(itertools.chain([1, 2], (3, 4), "ab")))
print("  combinations:", list(itertools.combinations("ABC", 2)))
print("  permutations:", len(list(itertools.permutations("ABCD"))), "orderings of ABCD")
print("  accumulate:", list(itertools.accumulate([1, 2, 3, 4])))
sales = [("north", 10), ("north", 5), ("south", 7), ("south", 3)]
for region, group in itertools.groupby(sales, key=lambda s: s[0]):
    print(f"  groupby {region}: {sum(amount for _, amount in group)}")
print("  any/all:", any(n > 2 for n in nums), all(n > 0 for n in nums))

print("\n=== 4. Decorators ===")


def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  -> calling {func.__name__}{args}")
        result = func(*args, **kwargs)
        print(f"  <- {func.__name__} returned {result}")
        return result
    return wrapper


@log_calls
def add(a, b):
    """Add two numbers."""
    return a + b


add(2, 3)
print("  wraps kept the name/doc:", add.__name__, "|", add.__doc__)


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"  {func.__name__} took {time.perf_counter() - start:.4f}s")
        return result
    return wrapper


@timer
def slow_sum(n):
    return sum(range(n))


slow_sum(2_000_000)


def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


@repeat(times=3)
def cheer(name):
    print(f"  Go {name}!")


cheer("Sangita")


def retry(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"  attempt {attempt} failed: {e}")
            raise RuntimeError(f"{func.__name__} failed after {times} attempts")
        return wrapper
    return decorator


calls = {"count": 0}


@retry(times=3)
def flaky_api():
    calls["count"] += 1
    if calls["count"] < 3:
        raise ConnectionError("network glitch")
    return "data received"


print("  retry result:", flaky_api())

print("\n=== 5. lru_cache ===")


def fib_slow(n):
    return n if n < 2 else fib_slow(n - 1) + fib_slow(n - 2)


@functools.lru_cache(maxsize=None)
def fib_fast(n):
    return n if n < 2 else fib_fast(n - 1) + fib_fast(n - 2)


start = time.perf_counter()
fib_slow(27)
slow_time = time.perf_counter() - start
start = time.perf_counter()
fib_fast(27)
fast_time = time.perf_counter() - start
print(f"  fib(27): no cache {slow_time:.4f}s | lru_cache {fast_time:.6f}s")
print("  fib_fast(100) =", fib_fast(100))

print("\n=== 6. Type hints ===")


def average(scores: list[float]) -> float:
    return sum(scores) / len(scores) if scores else 0.0


def find_user(user_id: int) -> dict[str, str] | None:
    users = {1: {"name": "Sangita"}}
    return users.get(user_id)


def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)


def count_up(n: int) -> Iterator[int]:
    yield from range(1, n + 1)


print("  average:", average([88.0, 92.5]))
print("  find_user(1), (2):", find_user(1), find_user(2))
print("  apply:", apply(lambda x: x * 10, 4))
print("  count_up:", list(count_up(3)))
print("  hints are NOT enforced:", average([1, 2, 3]), "(ints passed, no error)")
print("  annotations:", find_user.__annotations__)

print("\n=== 7. Unpacking & multi-key sort ===")
first, *middle, last = [1, 2, 3, 4, 5]
print("  first/middle/last:", first, middle, last)
defaults, overrides = {"theme": "light", "lang": "en"}, {"theme": "dark"}
print("  merged dict:", {**defaults, **overrides})
people = [{"name": "Ravi", "age": 30}, {"name": "Asha", "age": 30}, {"name": "Meera", "age": 25}]
ordered = sorted(people, key=lambda p: (-p["age"], p["name"]))
print("  age desc, then name:", [p["name"] for p in ordered])
