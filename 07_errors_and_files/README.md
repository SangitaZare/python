# 07 · Errors & Files

Run the examples:

```bash
python 07_errors_and_files/examples.py
```

The script writes its demo files into `07_errors_and_files/output/`. Git ignores that folder.

# Part A: Errors and exceptions

## 1. Syntax errors vs exceptions

- A **syntax error** means the code is invalid and won't run at all (for example, a missing `:`).
- An **exception** is an error that happens **while the code runs** (dividing by zero, a missing file, bad input). You can catch and handle exceptions.

## 2. Common built-in exceptions

| Exception | When |
|-----------|------|
| `ValueError` | The type is right but the value is wrong: `int("abc")` |
| `TypeError` | The type is wrong: `"5" + 5` |
| `KeyError` | A dict key is missing: `d["x"]` |
| `IndexError` | A list index is out of range: `lst[99]` |
| `ZeroDivisionError` | `10 / 0` |
| `FileNotFoundError` | Opening a file that doesn't exist |
| `AttributeError` | `None.upper()` |
| `NameError` | Using a variable that isn't defined |
| `ImportError` / `ModuleNotFoundError` | A module isn't found |

All of these inherit from `Exception`, which inherits from `BaseException`.

## 3. try / except / else / finally

```python
try:
    num = int(input("Number: "))
    result = 100 / num
except ValueError:
    print("Not a number")
except ZeroDivisionError:
    print("Cannot divide by zero")
except Exception as e:            # catch-all: keep it LAST
    print("Unexpected:", e)
else:
    print("Result:", result)      # runs only if there was NO exception
finally:
    print("Always runs")          # cleanup: close files, connections, etc.
```

- You can catch several exceptions in one line: `except (ValueError, TypeError):`
- Catch **specific** exceptions. A bare `except:` also catches `KeyboardInterrupt` (Ctrl+C) and hides real bugs.

## 4. Raising exceptions

```python
def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError("Amount must be positive")
    return balance - amount
```

- `raise` on its own, inside an `except` block, re-raises the current exception.
- `raise NewError("...") from e` chains exceptions, so the original cause is kept in the traceback.

## 5. Custom exceptions

```python
class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        super().__init__(f"Balance {balance} is less than {amount}")
        self.balance = balance
        self.amount = amount
```

Custom exceptions make errors **meaningful** for your application, and callers can catch exactly the case they care about.

## 6. EAFP vs LBYL

- **LBYL** ("Look Before You Leap"): `if key in d: value = d[key]`
- **EAFP** ("Easier to Ask Forgiveness than Permission"): `try: value = d[key] except KeyError: ...`

Python generally prefers **EAFP**. It is cleaner and avoids race conditions, for example a file being deleted between your check and your open.

# Part B: Working with files

## 7. Opening files with `with`

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("Hello\n")
# the file is closed automatically here, even if an error happened
```

| Mode | Meaning |
|------|---------|
| `"r"` | Read (the default). Error if the file is missing |
| `"w"` | Write. **Creates or overwrites** the file |
| `"a"` | Append to the end |
| `"x"` | Create a new file. Error if it already exists |
| `"b"` | Binary mode, added to another mode: `"rb"`, `"wb"` (images, PDFs) |
| `"+"` | Read and write: `"r+"` |

Always pass `encoding="utf-8"` for text files. On Windows, the default encoding is often not UTF-8.

## 8. Reading

```python
with open("notes.txt", encoding="utf-8") as f:
    content = f.read()          # the whole file as one string
    # f.readline()              # one line
    # f.readlines()             # a list of all lines

with open("big.log", encoding="utf-8") as f:
    for line in f:              # BEST for big files: reads one line at a time
        print(line.strip())
```

## 9. Context managers: how `with` works

`with` calls `__enter__` at the start and `__exit__` at the end. `__exit__` runs **even when an exception happens**. You can write your own context manager:

```python
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.perf_counter()
    yield                       # the body of the with block runs here
    print(f"took {time.perf_counter() - start:.4f}s")

with timer():
    sum(range(1_000_000))
```

## 10. pathlib: modern paths

```python
from pathlib import Path

folder = Path("data")
folder.mkdir(exist_ok=True)
file = folder / "notes.txt"         # the / operator joins paths on any OS
file.write_text("hi", encoding="utf-8")
file.read_text(encoding="utf-8")
file.exists(); file.suffix; file.stem; file.name
list(folder.glob("*.txt"))          # find files
```

## 11. JSON

JSON is the standard format for APIs and config files. It maps to Python dicts and lists.

```python
import json
data = {"name": "Sangita", "skills": ["Python", "SQL"]}

text = json.dumps(data, indent=2)            # Python -> JSON string
back = json.loads(text)                      # JSON string -> Python

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)             # Python -> file
with open("data.json", encoding="utf-8") as f:
    loaded = json.load(f)                    # file -> Python
```

A simple way to remember: `dumps` and `loads` work with **s**trings, while `dump` and `load` work with files.

## 12. CSV

```python
import csv
rows = [{"name": "Asha", "marks": 88}, {"name": "Ravi", "marks": 92}]

with open("marks.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "marks"])
    writer.writeheader()
    writer.writerows(rows)

with open("marks.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row["name"], int(row["marks"]))    # values are read back as STRINGS
```

In data science you'll mostly use `pandas.read_csv()`, but it's important to understand the basics first.

## Common mistakes

- Using a bare `except:` or `except Exception: pass`, which silently hides bugs.
- Opening a file without `with` and forgetting to close it.
- Using `"w"` when you meant `"a"`, which wipes the file.
- Forgetting `newline=""` when writing CSV files on Windows, which gives blank lines between rows.
- Forgetting that the csv module reads every value back as a **string**.
- Writing paths with backslashes (`"C:\new"`), where `\n` becomes a newline. Use `pathlib` or raw strings.

---

## Interview questions

**1. What is the difference between an error and an exception?**
A syntax error is detected before the code runs and can't be caught. An exception happens at runtime and can be handled with `try`/`except`.

**2. Explain `try`, `except`, `else` and `finally`.**
`try` holds the risky code. `except` handles specific errors. `else` runs only if no exception happened. `finally` always runs, and is used for cleanup.

**3. Why is a bare `except:` bad?**
It catches everything, including `KeyboardInterrupt` and `SystemExit`, and it hides real bugs. Catch specific exceptions instead, or `Exception` at most, and log the error.

**4. How do you create a custom exception?**
Subclass `Exception`: `class MyError(Exception): pass`. Add an `__init__` with extra attributes if you need them.

**5. What is the difference between `raise` and `raise ... from e`?**
`raise X from e` creates a new exception and links the original as its `__cause__`, so the traceback shows both. A bare `raise` re-raises the current exception unchanged.

**6. What is a context manager?**
An object that implements `__enter__` and `__exit__`, used with `with`. It guarantees setup and cleanup (closing files, releasing locks) even when an error happens. You can also write one with `@contextmanager` and `yield`.

**7. What is the difference between `read()`, `readline()` and `readlines()`?**
`read()` returns the whole file as one string. `readline()` returns one line. `readlines()` returns a list of all lines. For big files, loop over the file object instead.

**8. What is the difference between `json.dump` and `json.dumps`?**
`dumps` returns a JSON **string**. `dump` writes JSON to a **file**. The same goes for `loads` and `load`.

**9. What is EAFP?**
"Easier to Ask Forgiveness than Permission". You try the operation and handle the exception, instead of checking first. It is the Pythonic style.

**10. How would you read a 10 GB file?**
Don't call `read()`. Loop over the file line by line (`for line in f`), or read fixed-size chunks with `f.read(chunk_size)`. That way memory use stays small.

---

## Practice

1. Write `safe_divide(a, b)` that returns `None` and prints a message for division by zero or non-number input.
2. Write a program that keeps asking for an age until the user enters a valid positive integer.
3. Create an `InvalidAgeError` custom exception and raise it for ages outside 0–120.
4. Write a list of 5 tasks to `tasks.txt` (one per line), then read the file back and print the tasks numbered.
5. Save a dict of student marks to `marks.json`, load it back, and print the average.
6. Write the same marks to `marks.csv`, read it back with `csv.DictReader`, and print who scored above 80.
