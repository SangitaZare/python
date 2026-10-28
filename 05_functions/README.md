# 05 · Functions

Run the examples:

```bash
python 05_functions/examples.py
```

A function is a **named, reusable block of code**. Functions keep code DRY (Don't Repeat Yourself), readable and testable.

## 1. Defining and calling

```python
def greet(name):
    """Return a greeting for name."""     # docstring: shown by help(greet)
    return f"Hello, {name}!"

message = greet("Sangita")
```

- `return` sends a value back and **ends** the function.
- A function with no `return` returns `None`.
- You can return several values at once. They come back as a tuple: `return total, average`, then `t, a = stats(nums)`.

## 2. Types of arguments

```python
def order(item, qty=1, *, express=False):
    ...

order("pen")                       # positional + default
order("pen", 3)                    # positional
order(item="pen", qty=3)           # keyword (order doesn't matter)
order("pen", express=True)         # express is keyword-only (it comes after *)
```

| Kind | Example | Notes |
|------|---------|-------|
| Positional | `f(1, 2)` | Matched by position |
| Keyword | `f(a=1, b=2)` | Matched by name, more readable |
| Default | `def f(a, b=10)` | Optional when calling |
| `*args` | `def f(*args)` | Collects extra positional args into a **tuple** |
| `**kwargs` | `def f(**kwargs)` | Collects extra keyword args into a **dict** |
| Keyword-only | `def f(a, *, b)` | `b` must be passed by name |
| Positional-only | `def f(a, /, b)` | `a` cannot be passed by name |

The order in a signature is: `def f(pos_only, /, normal, *args, kw_only, **kwargs)`

## 3. `*args` and `**kwargs`

```python
def total(*args):
    return sum(args)            # args is a tuple
total(1, 2, 3)                  # 6

def profile(**kwargs):
    for k, v in kwargs.items(): # kwargs is a dict
        print(k, v)
profile(name="Sangita", city="Pune")
```

`*` and `**` also **unpack** values when you call a function:

```python
nums = [1, 2, 3];  total(*nums)
info = {"name": "A", "city": "B"};  profile(**info)
```

## 4. The mutable default argument trap ⚠️

```python
def add_item(item, basket=[]):     # BAD
    basket.append(item)
    return basket

add_item("a")   # ['a']
add_item("b")   # ['a', 'b']   <- surprise!
```

Default values are created **once**, when the function is defined, not on every call. The same list is reused every time.

The fix is to use `None` as the default:

```python
def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket
```

## 5. Scope: the LEGB rule

When Python looks up a name, it searches these scopes in order:
**L**ocal → **E**nclosing (an outer function) → **G**lobal (the module) → **B**uilt-in (`len`, `print`...).

```python
x = "global"
def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)       # local
    inner()
```

- `global x` lets a function **change** a module-level variable. Avoid it; return values instead.
- `nonlocal x` lets an inner function change a variable of its enclosing function.

## 6. Lambda (anonymous functions)

A lambda is a one-line function without a name. Use it for short throwaway logic, usually as a `key=`.

```python
square = lambda x: x * x
students = [("Asha", 88), ("Ravi", 92)]
sorted(students, key=lambda s: s[1], reverse=True)
```

It works well with `map`, `filter` and `sorted`, although a comprehension is often clearer:

```python
list(map(lambda x: x * 2, nums))       # same as [x * 2 for x in nums]
list(filter(lambda x: x > 0, nums))    # same as [x for x in nums if x > 0]
```

## 7. Functions are first-class objects

You can assign a function to a variable, pass it to another function, return it from a function, or store it in a list or dict.

```python
def shout(t): return t.upper()
def apply(func, value): return func(value)
apply(shout, "hi")    # 'HI'

operations = {"+": lambda a, b: a + b, "-": lambda a, b: a - b}
operations["+"](2, 3) # 5
```

A function that takes or returns another function is called a **higher-order function**.

## 8. Closures

A closure is an inner function that **remembers variables from its enclosing scope**, even after the outer function has finished.

```python
def make_multiplier(n):
    def multiply(x):
        return x * n      # remembers n
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
double(5), triple(5)      # (10, 15)
```

Closures are the foundation of **decorators**, which we cover in topic 09.

## 9. Recursion

A function that calls itself. It always needs a **base case** to stop.

```python
def factorial(n):
    if n <= 1:          # base case
        return 1
    return n * factorial(n - 1)
```

Python's default recursion limit is about 1000 calls. For deep problems, a loop is usually better.

## 10. Type hints (a preview)

```python
def area(width: float, height: float) -> float:
    return width * height
```

Python does **not** enforce these hints. They are for readability, editors and tools like `mypy`.

## Common mistakes

- Using a mutable default argument (`[]`, `{}`). Use `None`.
- Forgetting `return`, so the function gives back `None`.
- `print` vs `return`: printing shows a value, but returning **gives it back** so the caller can use it.
- Writing `func` when you mean `func()`. The first is the function object; the second calls it.
- Changing a global variable without `global`, which raises an `UnboundLocalError`.

---

## Interview questions

**1. What are `*args` and `**kwargs`?**
`*args` collects extra positional arguments into a tuple. `**kwargs` collects extra keyword arguments into a dict. They let a function accept any number of arguments. The names are only a convention; the `*` and `**` are what matter.

**2. Explain the mutable default argument problem.**
Default values are evaluated **once**, when the function is defined. A mutable default like `[]` is shared across all calls, so changes build up between calls. Fix it with `def f(x=None): if x is None: x = []`.

**3. Does Python pass arguments by value or by reference?**
Neither exactly. It is **"pass by object reference"** (also called pass by assignment). The function gets a reference to the same object. If the object is mutable (a list), changing it inside the function affects the caller. Rebinding the name (`x = ...`) inside the function does not.

**4. What is the LEGB rule?**
The order in which Python looks up names: Local, Enclosing, Global, Built-in.

**5. What is the difference between `global` and `nonlocal`?**
`global` lets you assign to a module-level variable from inside a function. `nonlocal` lets a nested function assign to a variable in its enclosing function's scope.

**6. What is a lambda function? What are its limits?**
A small anonymous function written in one expression: `lambda args: expr`. It cannot contain statements (no `if` blocks, loops or assignments) and has no name in tracebacks. Use `def` for anything non-trivial.

**7. What is a closure?**
An inner function that captures variables from its enclosing function and keeps them alive after the outer function returns. For example, `make_multiplier(2)` returns a function that remembers `n=2`.

**8. What does "functions are first-class objects" mean?**
Functions can be treated like any other value: stored in variables, passed as arguments, returned from other functions and kept in data structures.

**9. What is the difference between `map`/`filter` and list comprehensions?**
They do the same job. `map` and `filter` return lazy iterators. Comprehensions are generally considered more Pythonic and readable, especially when you would otherwise need a lambda.

**10. What is a docstring?**
A string literal on the first line of a function, class or module that documents it. You can read it with `help(func)` or `func.__doc__`.

---

## Practice

1. Write `calculate(a, b, op="+")` that supports `+ - * /` and returns `None` for division by zero.
2. Write `average(*numbers)` that works with any number of arguments and returns 0 if none are given.
3. Write `build_profile(name, **details)` that returns a dict with the name plus all the extra details.
4. Sort a list of `(name, age)` tuples by age using `sorted` with a lambda.
5. Write `make_counter()` that returns a function. Each call to that function returns the next number (1, 2, 3...). Use a closure with `nonlocal`.
6. Write a recursive `fibonacci(n)`, then rewrite it with a loop. Which is faster for `n=30`?
