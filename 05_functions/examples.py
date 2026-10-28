"""05 - Functions: arguments, *args/**kwargs, scope, lambda, closures, recursion."""

print("=== 1. Define, call, return ===")


def greet(name):
    """Return a greeting for name."""
    return f"Hello, {name}!"


def no_return():
    pass


def stats(nums):
    return sum(nums), sum(nums) / len(nums)  # returned as a tuple


print(greet("Sangita"))
print("no_return() ->", no_return())
total, avg = stats([10, 20, 30])
print("stats ->", total, avg)
print("docstring:", greet.__doc__)

print("\n=== 2. Argument types ===")


def order(item, qty=1, *, express=False):
    return f"{qty} x {item} ({'express' if express else 'normal'})"


print(order("pen"))
print(order("pen", 3))
print(order(qty=2, item="book"))
print(order("bag", express=True))
try:
    order("bag", 1, True)  # express is keyword-only
except TypeError as e:
    print("keyword-only error:", e)

print("\n=== 3. *args and **kwargs ===")


def total_of(*args):
    print("  args is a", type(args).__name__, args)
    return sum(args)


def profile(name, **kwargs):
    print("  kwargs is a", type(kwargs).__name__, kwargs)
    return {"name": name, **kwargs}


print("total:", total_of(1, 2, 3))
print("profile:", profile("Sangita", city="Pune", course="Python"))
nums = [4, 5, 6]
info = {"city": "Mumbai"}
print("unpack into call:", total_of(*nums), profile("Asha", **info))

print("\n=== 4. Mutable default trap ===")


def add_item_bad(item, basket=[]):
    basket.append(item)
    return basket


def add_item_good(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket


print("bad  call 1:", add_item_bad("a"))
print("bad  call 2:", add_item_bad("b"), "<- 'a' is still there!")
print("good call 1:", add_item_good("a"))
print("good call 2:", add_item_good("b"))

print("\n=== Pass by object reference ===")


def modify(lst):
    lst.append(99)        # mutates the caller's list


def rebind(lst):
    lst = [0]             # only changes the local name


data = [1, 2]
modify(data)
rebind(data)
print("after modify + rebind:", data)

print("\n=== 5. Scope (LEGB) ===")
x = "global"


def outer():
    x = "enclosing"

    def inner():
        x = "local"
        return x

    return inner(), x


print("inner/outer:", outer(), "| module:", x)

counter = 0


def increment():
    global counter
    counter += 1


increment()
increment()
print("global counter:", counter)

print("\n=== 6. Lambda, map, filter, sorted ===")
square = lambda n: n * n
print("square(4):", square(4))
students = [("Asha", 88), ("Ravi", 92), ("Meera", 79)]
print("sorted by marks:", sorted(students, key=lambda s: s[1], reverse=True))
values = [-2, -1, 0, 1, 2]
print("map x2:  ", list(map(lambda v: v * 2, values)))
print("filter>0:", list(filter(lambda v: v > 0, values)))
print("comprehension equivalent:", [v * 2 for v in values], [v for v in values if v > 0])

print("\n=== 7. First-class functions ===")


def shout(text):
    return text.upper()


def apply(func, value):
    return func(value)


print("apply(shout, 'hi'):", apply(shout, "hi"))
operations = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
}
for op, fn in operations.items():
    print(f"  6 {op} 3 = {fn(6, 3)}")

print("\n=== 8. Closures ===")


def make_multiplier(n):
    def multiply(value):
        return value * n  # n is remembered from the enclosing scope
    return multiply


double, triple = make_multiplier(2), make_multiplier(3)
print("double(5), triple(5):", double(5), triple(5))


def make_counter():
    count = 0

    def next_number():
        nonlocal count
        count += 1
        return count

    return next_number


c = make_counter()
print("counter:", c(), c(), c())

print("\n=== 9. Recursion ===")


def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)


print("factorial(5):", factorial(5))

print("\n=== 10. Type hints (not enforced) ===")


def area(width: float, height: float) -> float:
    return width * height


print("area(2, 3.5):", area(2, 3.5))
print("annotations:", area.__annotations__)
