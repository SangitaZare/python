# 03 · Collections (list, tuple, set, dict)

Run the examples:

```bash
python 03_collections/examples.py
```

## Quick comparison

| | `list` | `tuple` | `set` | `dict` |
|---|---|---|---|---|
| Syntax | `[1, 2, 3]` | `(1, 2, 3)` | `{1, 2, 3}` | `{"a": 1}` |
| Ordered? | Yes | Yes | **No** | Yes (insertion order, Python 3.7+) |
| Mutable? | Yes | **No** | Yes | Yes |
| Duplicates? | Allowed | Allowed | **Not allowed** | Keys must be unique |
| Access by | Index | Index | Not possible (only `in`) | Key |
| Use when | You need an ordered, changeable collection | You need fixed data or a dict key | You need unique items or fast lookup | You need to look up values by a name |

## 1. List

An ordered, changeable collection. It's the one you'll use most.

```python
fruits = ["apple", "banana"]
fruits.append("mango")        # add to the end
fruits.insert(0, "kiwi")      # add at a position
fruits.extend(["fig", "pear"])# add many items
fruits.remove("banana")       # remove by value (first match)
last = fruits.pop()           # remove and return the last item
fruits.pop(0)                 # remove by index
fruits.sort()                 # sort in place (returns None!)
sorted(fruits)                # returns a NEW sorted list
fruits.reverse()
fruits.index("mango"); fruits.count("fig"); len(fruits)
```

Slicing works exactly like it does for strings: `nums[1:3]`, `nums[::-1]`.

## 2. Tuple

An ordered collection that **can't be changed**. Use it for fixed data like coordinates, RGB colours or database rows.

```python
point = (10, 20)
single = (5,)          # a one-item tuple needs a comma! (5) is just an int
x, y = point           # unpacking
a, b = b, a            # swap two variables (this uses a tuple)
```

Because tuples are immutable, they are **hashable**, so they can be used as dict keys or set items. Lists cannot.

## 3. Set

An unordered collection of **unique** items. Lookup with `in` is very fast: O(1) on average.

```python
tags = {"python", "data"}
tags.add("ml")
tags.discard("java")        # no error if missing (remove() would raise KeyError)
empty = set()               # NOT {} (that's an empty dict!)

a = {1, 2, 3}; b = {2, 3, 4}
a | b    # union         {1, 2, 3, 4}
a & b    # intersection  {2, 3}
a - b    # difference    {1}
a ^ b    # symmetric difference {1, 4}
```

The classic use is removing duplicates: `list(set(items))`. Note that this loses the order. Use `list(dict.fromkeys(items))` if you need to keep the order.

## 4. Dictionary

Stores **key → value** pairs. Keys must be unique and immutable (str, int, tuple).

```python
student = {"name": "Sangita", "age": 25}
student["city"] = "Pune"            # add or update
student["name"]                     # KeyError if the key is missing
student.get("email")                # None if missing (no error)
student.get("email", "N/A")         # with a default
del student["age"]
student.pop("city")
student.update({"age": 26, "course": "Python"})

for key, value in student.items():  # loop over pairs
    print(key, value)
student.keys(); student.values()
"name" in student                   # checks KEYS
```

## 5. Copying: shallow vs deep

```python
a = [1, 2, 3]
b = a            # NOT a copy: both names point to the same list
c = a.copy()     # shallow copy (also a[:] or list(a))

import copy
nested = [[1, 2], [3, 4]]
shallow = nested.copy()        # the inner lists are still shared!
deep = copy.deepcopy(nested)   # everything is copied
```

## 6. Unpacking and useful built-ins

```python
first, *rest = [1, 2, 3, 4]       # first=1, rest=[2, 3, 4]
len(), min(), max(), sum(), sorted(), reversed(), enumerate(), zip()

names = ["A", "B"]; scores = [90, 80]
dict(zip(names, scores))         # {'A': 90, 'B': 80}
```

## 7. The `collections` module (good to know)

```python
from collections import Counter, defaultdict, namedtuple, deque
Counter("banana").most_common(1)   # [('a', 3)]
groups = defaultdict(list); groups["x"].append(1)   # no KeyError
Point = namedtuple("Point", "x y"); Point(1, 2).x
dq = deque([1, 2]); dq.appendleft(0)                # fast on both ends
```

## Common mistakes

- `nums = nums.sort()` sets `nums` to `None`. `sort()` changes the list in place and returns `None`.
- `b = a` doesn't copy a list. Changing `b` also changes `a`.
- `{}` is an empty **dict**, not a set. Use `set()` for an empty set.
- `(5)` is not a tuple. Write `(5,)`.
- Changing a list or dict while you loop over it. Loop over a copy instead: `for x in items[:]:`.
- `d["missing"]` raises a `KeyError`. Use `d.get("missing")` when the key might not exist.

---

## Interview questions

**1. What is the difference between a list and a tuple?**
A list is mutable and uses `[]`. A tuple is immutable and uses `()`. Tuples are slightly faster and use less memory, and they are hashable, so they can be dict keys. Use a tuple for data that shouldn't change.

**2. Why can't a list be a dictionary key?**
Dict keys must be **hashable**: their hash must never change. A list can change, so its hash could change and the dict would lose track of the key. Tuples (of immutable items) are hashable.

**3. How do you remove duplicates from a list?**
`list(set(items))` loses the order. `list(dict.fromkeys(items))` keeps the original order.

**4. What is the difference between `sort()` and `sorted()`?**
`list.sort()` sorts **in place** and returns `None`. It only works on lists. `sorted(iterable)` returns a **new** list and works on any iterable.

**5. What is the difference between `remove()`, `pop()` and `del`?**
`remove(value)` deletes the first matching value. `pop(i)` deletes by index and **returns** the item (the last one by default). `del lst[i]` deletes by index or slice and returns nothing.

**6. What is the difference between a shallow copy and a deep copy?**
A shallow copy creates a new outer container, but the inner objects are still shared. A deep copy (`copy.deepcopy`) recursively copies everything, so nested changes don't affect the original.

**7. What is the time complexity of `x in list` vs `x in set`?**
For a list it is O(n), because Python checks every item. For a set or dict it is O(1) on average, because Python uses a hash lookup. Use a set when you check membership many times.

**8. Are dictionaries ordered?**
Yes, since Python 3.7 they keep insertion order. That is guaranteed by the language.

**9. What is the difference between `dict["key"]` and `dict.get("key")`?**
`dict["key"]` raises a `KeyError` if the key is missing. `get` returns `None`, or a default you pass in.

**10. How do you merge two dictionaries?**
`{**d1, **d2}`, `d1 | d2` (Python 3.9+) or `d1.update(d2)`, which changes `d1` in place. If both have the same key, the value from `d2` wins.

---

## Practice

1. Given `nums = [5, 3, 8, 3, 1, 8, 9]`, print the unique values sorted, the max, the min and the sum.
2. Count how many times each word appears in a sentence using a dict, without `Counter`.
3. Given two lists of students in two courses, find the students who are in **both** courses and the students in **only one**.
4. Build a dict `{name: marks}` for 4 students and print the topper's name.
5. Predict the output, then run it: `a = [[0]] * 3; a[0].append(1); print(a)`
