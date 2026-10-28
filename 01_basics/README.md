# 01 · Python Basics

Run the examples:

```bash
python 01_basics/examples.py
```

## 1. Variables

A variable is a **name that points to a value**. You don't declare a type. Python works it out from the value.

```python
name = "Sangita"
age = 25
age = "twenty-five"   # allowed: the same name now points to a str
```

This is called **dynamic typing**. Types are checked while the program runs.

Naming rules:
- Use letters, digits and `_`. A name cannot start with a digit.
- Names are case-sensitive: `age` and `Age` are different.
- The convention is `snake_case` for variables and functions, and `UPPER_CASE` for constants.

## 2. Core data types

| Type | Example | Meaning | Mutable? |
|------|---------|---------|----------|
| `int` | `42` | Whole number (no size limit) | No |
| `float` | `3.14` | Decimal number | No |
| `bool` | `True`, `False` | Yes or no | No |
| `str` | `"hello"` | Text | No |
| `NoneType` | `None` | "No value" | No |
| `list` | `[1, 2, 3]` | Ordered collection | **Yes** |
| `dict` | `{"a": 1}` | Key → value pairs | **Yes** |

Use `type(x)` to see a value's type and `isinstance(x, int)` to check it.

## 3. Operators

| Operator | Example | Result |
|----------|---------|--------|
| `+ - *` | `7 * 2` | `14` |
| `/` true division | `7 / 2` | `3.5` (always a float) |
| `//` floor division | `7 // 2` | `3` |
| `%` remainder | `7 % 2` | `1` |
| `**` power | `2 ** 3` | `8` |

Comparison operators: `== != < > <= >=`
Logical operators: `and or not`

## 4. `==` vs `is`

- `==` asks: **are the values equal?**
- `is` asks: **are these the same object in memory?**

```python
a = [1, 2]; b = [1, 2]
a == b   # True  (same values)
a is b   # False (two different lists)
```

Use `is` only to check for `None`, as in `if x is None:`.

## 5. Mutable vs immutable

- **Immutable** values (int, float, str, tuple) can't be changed. Any "change" creates a new object.
- **Mutable** values (list, dict, set) can change in place. If two names point to the same list, a change through one name shows up through the other.

## 6. Truthy and falsy

These values count as `False` in an `if`: `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `None`.
Every other value counts as `True`.

```python
items = []
if not items:
    print("List is empty")
```

## 7. Input and type conversion

`input()` **always returns a string**. Convert it before you do math:

```python
age = int(input("Your age: "))
```

Conversion functions: `int()`, `float()`, `str()`, `bool()`.

## Common mistakes

- `0.1 + 0.2 == 0.3` is `False` because of how decimal numbers are stored. Use `math.isclose()` to compare floats.
- `"5" + 5` raises a `TypeError`. Python won't mix types automatically; it is **strongly typed**.
- `bool("False")` is `True`, because any non-empty string is truthy.

---

## Interview questions

**1. Is Python compiled or interpreted?**
Both. Python first compiles the source code to *bytecode* (`.pyc` files), and then the Python Virtual Machine interprets that bytecode.

**2. What does "dynamically typed" mean? Is Python also strongly typed?**
Dynamically typed means types are checked at runtime, and a variable can point to any type. Python is also strongly typed: it won't convert types implicitly, so `"1" + 1` is an error.

**3. What is the difference between `==` and `is`?**
`==` compares values. `is` compares identity, meaning whether both names point to the same object (`id()`).

**4. What are mutable and immutable types? Give examples.**
Mutable types can change in place: list, dict, set. Immutable types cannot: int, float, str, tuple, bool.

**5. What is the difference between `/` and `//`?**
`/` always returns a float (`7/2 = 3.5`). `//` does floor division (`7//2 = 3`, and `-7//2 = -4`).

**6. What is `None`?**
A special singleton object that means "no value". A function without a `return` returns `None`.

**7. What are truthy and falsy values?**
Falsy values are `0`, `0.0`, `""`, `[]`, `{}`, `set()` and `None`. All other values are truthy.

**8. What does `x = "" or "guest"` give?**
`"guest"`. `or` returns the first truthy operand, or the last operand if none are truthy. It doesn't always return a bool.

---

## Practice

1. Ask the user for their name and birth year, then print their age.
2. Take two numbers and print their sum, difference, product, quotient, floor division and remainder.
3. Predict the output, then run it to check: `print(bool([]), bool([0]), bool(" "), 10 // 3, -10 // 3)`
