# 04 · Control Flow

Run the examples:

```bash
python 04_control_flow/examples.py
```

Python uses **indentation** (4 spaces), not `{ }`, to mark code blocks. A wrong indent is a syntax error or, worse, a logic bug.

## 1. if / elif / else

```python
marks = 72
if marks >= 90:
    grade = "A"
elif marks >= 60:
    grade = "B"
else:
    grade = "C"
```

- Chained comparisons work: `if 18 <= age < 60:`
- Conditional (ternary) expression: `status = "adult" if age >= 18 else "minor"`
- Membership checks: `if city in ("Pune", "Mumbai"):`

## 2. for loop

A `for` loop goes over **any iterable**: a list, string, dict, range or file.

```python
for i in range(5):          # 0, 1, 2, 3, 4
for i in range(2, 10, 2):   # 2, 4, 6, 8   (start, stop, step)
for i in range(5, 0, -1):   # 5, 4, 3, 2, 1
for i, name in enumerate(names):        # index + value
for name, score in zip(names, scores):  # two lists together
for key, value in my_dict.items():      # dict pairs
```

## 3. while loop

A `while` loop repeats **while a condition is True**. Use it when you don't know how many times to loop.

```python
count = 3
while count > 0:
    print(count)
    count -= 1        # forget this line and the loop never ends
```

## 4. break, continue, pass, else

| Keyword | What it does |
|---------|--------------|
| `break` | Exit the loop immediately |
| `continue` | Skip the rest of this iteration and go to the next one |
| `pass` | Do nothing (a placeholder where a statement is required) |
| `else` on a loop | Runs only if the loop finished **without** `break` |

```python
for n in [3, 7, 11]:
    if n % 2 == 0:
        print("Found an even number")
        break
else:
    print("No even number found")   # runs because there was no break
```

## 5. Comprehensions

A short, readable way to build a collection from a loop.

```python
squares = [x * x for x in range(5)]               # list
evens   = [x for x in range(10) if x % 2 == 0]    # with a filter
labels  = ["even" if x % 2 == 0 else "odd" for x in range(4)]  # if-else goes BEFORE the for
unique  = {len(w) for w in words}                 # set
lengths = {w: len(w) for w in words}              # dict
total   = sum(x * x for x in range(1_000_000))    # generator expression (no list in memory)
```

A comprehension is roughly equivalent to this loop:

```python
squares = []
for x in range(5):
    squares.append(x * x)
```

Keep comprehensions simple. If one needs more than one `for` plus one `if`, write a normal loop instead.

## 6. match statement (Python 3.10+)

This is "structural pattern matching", similar to `switch` in other languages but more powerful.

```python
match command.split():
    case ["go", direction]:
        print("Going", direction)
    case ["quit" | "exit"]:
        print("Bye")
    case _:
        print("Unknown command")   # _ matches anything (default)
```

It can also match by value (`case 404:`), match a dict's shape (`case {"status": 200}:`) and use guards (`case x if x > 0:`).

## 7. Walrus operator `:=` (Python 3.8+)

It assigns a value **and** uses it in the same expression:

```python
if (n := len(items)) > 3:
    print(f"Too many items: {n}")
```

## Common mistakes

- Using `=` instead of `==` in a condition. Python gives a syntax error, which is good.
- An infinite `while` loop because you forgot to update the variable.
- `range(1, 10)` stops at **9**, not 10.
- Changing a list while looping over it. Loop over a copy, or build a new list with a comprehension.
- In a comprehension, `if-else` goes **before** the `for`, and a filter `if` goes **after** it.

---

## Interview questions

**1. What is the difference between `break`, `continue` and `pass`?**
`break` exits the loop. `continue` skips to the next iteration. `pass` does nothing and only exists as a placeholder for an empty block.

**2. What does `else` on a `for` or `while` loop do?**
It runs when the loop ends normally, meaning **without hitting `break`**. It is useful for searches: "item not found".

**3. What is a list comprehension? Is it faster than a loop?**
It is a short syntax for building a list: `[expr for x in iterable if cond]`. It is usually a little faster than `append` in a loop, because it is optimised internally, and it is more readable for simple cases.

**4. What is the difference between a list comprehension and a generator expression?**
`[x for x in data]` builds the **whole list in memory**. `(x for x in data)` creates a **generator** that produces items one at a time, on demand. That is memory-efficient for large data.

**5. Does Python have a switch statement?**
Since Python 3.10 it has `match`/`case` (structural pattern matching). Before that, people used `if`/`elif` chains or a dict that maps keys to functions.

**6. What is the difference between `for` and `while`?**
Use `for` to go over an iterable or a known range. Use `while` to repeat until a condition changes, when you don't know the number of iterations in advance.

**7. What does `range()` return?**
A `range` object. It is a lazy, memory-efficient sequence, not a list. `range(10**9)` uses almost no memory.

**8. Print FizzBuzz from 1 to 15.**
```python
for i in range(1, 16):
    if i % 15 == 0: print("FizzBuzz")
    elif i % 3 == 0: print("Fizz")
    elif i % 5 == 0: print("Buzz")
    else: print(i)
```

---

## Practice

1. Print the multiplication table for a number the user enters.
2. Write FizzBuzz for numbers 1 to 30 without looking at the answer.
3. Use a list comprehension to get all the words longer than 4 letters from a sentence, in uppercase.
4. Write a number-guessing game: pick a secret number, keep asking with `while` until the guess is correct, and print "higher" or "lower" hints.
5. Check whether a number is prime using a `for ... else` loop.
6. Build a dict `{number: square}` for 1 to 10 with a dict comprehension.
