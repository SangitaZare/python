# 02 · Strings

Run the examples:

```bash
python 02_strings/examples.py
```

## 1. Creating strings

```python
a = 'single quotes'
b = "double quotes"
c = """triple quotes
can span many lines"""
path = r"C:\new\folder"   # raw string: backslashes are kept as-is
```

Escape characters: `\n` is a new line, `\t` is a tab, `\\` is a backslash, `\"` is a quote.

## 2. Indexing and slicing

A string is an **ordered sequence of characters**, so each character has a position (index).

```
 P   y   t   h   o   n
 0   1   2   3   4   5     <- positive index
-6  -5  -4  -3  -2  -1     <- negative index
```

```python
s = "Python"
s[0]      # 'P'
s[-1]     # 'n'
s[1:4]    # 'yth'   start is included, stop is excluded
s[:3]     # 'Pyt'   from the beginning
s[3:]     # 'hon'   to the end
s[::2]    # 'Pto'   every 2nd character
s[::-1]   # 'nohtyP' reversed
```

Slicing never raises an error, even out of range (`s[2:100]` works). Indexing does: `s[100]` raises an `IndexError`.

## 3. Strings are immutable

You **cannot change** a character in place:

```python
s = "hello"
s[0] = "H"            # TypeError
s = "H" + s[1:]       # create a new string instead
```

Every string method **returns a new string**. The original never changes.

## 4. Most useful methods

| Method | Example | Result |
|--------|---------|--------|
| `upper()` / `lower()` | `"Hi".upper()` | `'HI'` |
| `title()` / `capitalize()` | `"hello world".title()` | `'Hello World'` |
| `strip()` | `"  hi  ".strip()` | `'hi'` |
| `replace(old, new)` | `"a-b".replace("-", "+")` | `'a+b'` |
| `split(sep)` | `"a,b,c".split(",")` | `['a', 'b', 'c']` |
| `sep.join(list)` | `"-".join(["a", "b"])` | `'a-b'` |
| `find(sub)` | `"hello".find("l")` | `2` (or `-1` if not found) |
| `count(sub)` | `"banana".count("a")` | `3` |
| `startswith` / `endswith` | `"file.py".endswith(".py")` | `True` |
| `isdigit` / `isalpha` / `isalnum` | `"123".isdigit()` | `True` |
| `in` operator | `"py" in "python"` | `True` |
| `len()` | `len("hello")` | `5` |

## 5. f-strings (formatting)

f-strings are the modern, fastest and most readable way to put values into text.

```python
name, price = "Pen", 12.5
f"{name} costs {price}"        # 'Pen costs 12.5'
f"{price:.2f}"                 # '12.50'     2 decimal places
f"{1234567:,}"                 # '1,234,567' thousands separator
f"{0.256:.1%}"                 # '25.6%'
f"{name:>10}"                  # right-align in 10 characters
f"{name=}"                     # "name='Pen'"  handy for debugging
f"{price * 2}"                 # any expression works
```

Older styles you may still see: `"{} costs {}".format(name, price)` and `"%s" % name`.

## 6. Looping over a string

```python
for ch in "abc":
    print(ch)

for i, ch in enumerate("abc"):
    print(i, ch)
```

## Common mistakes

- Calling `s.upper()` without saving the result. Strings are immutable, so you must write `s = s.upper()`.
- Building a string with `+=` in a big loop. That's slow. Collect the parts in a list and use `"".join(parts)`.
- Using `find()` and forgetting that it returns `-1`, not an error, when nothing is found.
- `"10" > "9"` is `False`. Strings compare **alphabetically**, character by character, not as numbers.

---

## Interview questions

**1. Why are strings immutable in Python?**
Immutability makes strings **hashable**, so they can be dict keys and set members. It also makes them safe to share between variables, and lets Python reuse (intern) them to save memory.

**2. How do you reverse a string?**
`s[::-1]`. Another way is `"".join(reversed(s))`.

**3. How do you check whether a string is a palindrome?**
```python
clean = s.lower().replace(" ", "")
clean == clean[::-1]
```

**4. What is the difference between `split()` and `split(" ")`?**
With no argument, `split()` splits on **any whitespace** (spaces, tabs, newlines) and ignores repeated spaces. `split(" ")` splits on **each single space**, so `"a  b".split(" ")` gives `['a', '', 'b']`.

**5. Why is `"".join(list)` preferred over `+=` in a loop?**
Each `+=` creates a new string and copies everything so far, which is O(n²) overall. `join` calculates the total size once and builds the result in one pass, which is O(n).

**6. What is the difference between `find()` and `index()`?**
Both return the position of a substring. If it isn't found, `find()` returns `-1` and `index()` raises a `ValueError`.

**7. How do you count the frequency of each character in a string?**
```python
from collections import Counter
Counter("banana")   # Counter({'a': 3, 'n': 2, 'b': 1})
```

**8. What is a raw string?**
A string prefixed with `r` where backslashes are not treated as escape characters. It's useful for Windows paths and regular expressions: `r"C:\new"`.

---

## Practice

1. Ask the user for a sentence. Print the number of words, the number of vowels, and the sentence in title case.
2. Write code that checks whether a word is a palindrome (`"Madam"` → `True`).
3. Given `email = "  Sangita.Zare@Gmail.COM "`, clean it to lowercase with no spaces, then print the username and the domain separately.
4. Print a receipt line with f-strings: the item name left-aligned in 15 characters and the price right-aligned with 2 decimals.
