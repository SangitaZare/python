# 11 · NumPy: Fast Numbers in Python

Run the examples (inside the virtual environment):

```bash
.venv\Scripts\activate          # Windows; macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt  # once
python 11_numpy/examples.py
```

## What is NumPy, and why does data science need it?

**NumPy** (Numerical Python) gives Python a new data type: the **array** (`ndarray`), a grid of numbers that is **all one type** and stored **side by side in memory**.

That one design choice makes it:
- **Fast**: 10–100× faster than Python lists for maths, because the loops run in compiled C code.
- **Compact**: a million integers take about 8 MB as an array, versus about 36 MB as a list.
- **Expressive**: `prices * 1.18` multiplies every item. No loop needed.

Almost every data tool is built on NumPy: **Pandas** stores its columns as NumPy arrays, **Matplotlib** plots them, and **scikit-learn** trains models on them. Learn NumPy well and the rest gets much easier.

```python
import numpy as np        # "np" is the universal convention

prices = [100, 250, 80]
[p * 1.18 for p in prices]      # Python list: needs a loop

arr = np.array([100, 250, 80])
arr * 1.18                      # NumPy: one expression -> array([118. , 295. ,  94.4])
```

---

## 1. Creating arrays

```python
np.array([1, 2, 3])                 # from a list
np.array([[1, 2], [3, 4]])          # 2-D (a matrix: rows x columns)
np.zeros(5)                         # [0. 0. 0. 0. 0.]
np.ones((2, 3))                     # 2 rows, 3 columns of 1.0
np.full(3, 7)                       # [7 7 7]
np.arange(0, 10, 2)                 # [0 2 4 6 8]  like range(), stop excluded
np.linspace(0, 1, 5)                # [0. 0.25 0.5 0.75 1.]  5 evenly spaced, stop INCLUDED
np.eye(3)                           # 3x3 identity matrix

rng = np.random.default_rng(seed=42)  # the modern way to make random numbers
rng.integers(1, 7, size=5)            # 5 dice rolls
rng.normal(loc=50, scale=10, size=3)  # bell-curve numbers: mean 50, std 10
```

Always set a **seed** for random numbers in data science. The same seed gives the same numbers, so your results can be reproduced.

## 2. Array attributes

```python
a = np.array([[1, 2, 3], [4, 5, 6]])
a.shape     # (2, 3)   rows, columns
a.ndim      # 2        number of dimensions
a.size      # 6        total items
a.dtype     # int64    the type of every item
```

| Dimensions | Name | Example in data science |
|-----------|------|-------------------------|
| 0-D | Scalar | One temperature |
| 1-D | Vector | One column of a table |
| 2-D | Matrix | A whole table (rows = samples, columns = features) |
| 3-D | Tensor | A colour image (height × width × RGB) |

## 3. Data types (dtype)

Every item in an array has the **same type**. If you mix types, NumPy converts ("upcasts") everything to the most general one:

```python
np.array([1, 2, 3]).dtype        # int64
np.array([1, 2.5, 3]).dtype      # float64  -> [1.  2.5 3. ]
np.array([1, "a"]).dtype         # <U21     everything became text!
np.array([1.9, 2.7]).astype(int) # [1 2]    astype converts; float -> int CUTS the decimals
```

## 4. Indexing and slicing

1-D works just like a list. For 2-D, use `[row, column]`:

```python
m = np.array([[10, 20, 30],
              [40, 50, 60],
              [70, 80, 90]])
m[0, 2]      # 30            row 0, column 2
m[1]         # [40 50 60]    whole row 1
m[:, 1]      # [20 50 80]    whole column 1  (":" means "all rows")
m[:2, 1:]    # [[20 30] [50 60]]  first 2 rows, columns 1 onward
m[-1]        # [70 80 90]    last row
```

### ⚠️ Slices are views, not copies

This is the opposite of Python lists. A slice **shares memory** with the original:

```python
a = np.array([1, 2, 3, 4])
part = a[:2]
part[0] = 99
a            # [99  2  3  4]   the original changed!
safe = a[:2].copy()   # use .copy() when you need an independent array
```

NumPy does this on purpose, because copying large arrays would be slow and use memory.

## 5. Boolean masks and fancy indexing

This is the **most-used NumPy skill** in data science: filtering with conditions.

```python
marks = np.array([45, 82, 67, 91, 38])
marks > 60                    # [False  True  True  True False]   a "mask"
marks[marks > 60]             # [82 67 91]
marks[(marks > 60) & (marks < 90)]   # [82 67]   use & | ~ (not and/or/not), with brackets!
(marks >= 40).sum()           # 4   True counts as 1, so this counts the passes
np.where(marks >= 40, "pass", "fail")   # ['pass' 'pass' 'pass' 'pass' 'fail']

marks[[0, 3]]                 # [45 91]   "fancy indexing": pick by a list of positions
```

## 6. Vectorised operations and ufuncs

Operations apply **element by element**, with no loop:

```python
a = np.array([1, 2, 3])
b = np.array([10, 20, 30])
a + b        # [11 22 33]
a * b        # [10 40 90]
a ** 2       # [1 4 9]
b / a        # [10. 10. 10.]
```

**ufuncs** ("universal functions") are fast built-in functions that work the same way: `np.sqrt`, `np.exp`, `np.log`, `np.abs`, `np.round`, `np.maximum`.

**Vectorisation** means replacing Python loops with whole-array operations. It is the main way to make data code fast.

## 7. Broadcasting

Broadcasting lets NumPy combine arrays of **different shapes** by "stretching" the smaller one (without actually copying it).

```python
prices = np.array([[100, 200],
                   [300, 400]])     # shape (2, 2)
prices * 2                          # a scalar is stretched to every item
prices * np.array([1.0, 0.5])       # shape (2,) is stretched down the rows
# [[100. 100.]
#  [300. 200.]]
```

**The rule:** compare the shapes from the **right**. Two dimensions fit together if they are **equal** or one of them is **1**.

| Shape A | Shape B | Works? | Result |
|---------|---------|--------|--------|
| (3, 4) | (4,) | ✅ | (3, 4) |
| (3, 4) | (3, 1) | ✅ | (3, 4) |
| (3, 1) | (1, 4) | ✅ | (3, 4) |
| (3, 4) | (3,) | ❌ | Error: the last dimensions are 4 and 3 |

A classic use is **normalising data**: `(data - data.mean(axis=0)) / data.std(axis=0)` scales every column at once.

## 8. Aggregations and `axis`

```python
sales = np.array([[10, 20, 30],     # rows = shops
                  [40, 50, 60]])    # columns = days
sales.sum()            # 210   everything
sales.sum(axis=0)      # [50 70 90]   down the rows    -> one result per COLUMN
sales.sum(axis=1)      # [ 60 150]    across columns   -> one result per ROW
sales.mean(), sales.max(), sales.min(), sales.std()
sales.argmax()         # 5   position of the biggest value (in the flattened array)
np.median(sales), np.percentile(sales, 90)
np.cumsum([1, 2, 3])   # [1 3 6]   running total
```

**How to remember `axis`:** the axis you name is the one that **disappears**. `axis=0` collapses the rows, so you get one value per column.

## 9. Reshaping and combining

```python
a = np.arange(6)          # [0 1 2 3 4 5]
a.reshape(2, 3)           # [[0 1 2] [3 4 5]]
a.reshape(3, -1)          # -1 means "work it out": (3, 2)
a.reshape(2, 3).T         # transpose: swap rows and columns -> shape (3, 2)
m.flatten()               # back to 1-D (always a copy)
m.ravel()                 # back to 1-D (a view when possible, so faster)

np.concatenate([a, a])    # join along an existing axis
np.vstack([a, a])         # stack as rows    -> shape (2, 6)
np.hstack([a, a])         # stack side by side
a[:, np.newaxis]          # turn shape (6,) into a column, shape (6, 1)
```

The total size must stay the same: `np.arange(6).reshape(4, 2)` is an error.

## 10. Missing values: NaN

`np.nan` means "Not a Number" (a missing value). It spreads through calculations:

```python
data = np.array([10, np.nan, 30])
data.mean()          # nan   one missing value ruins the result
np.nanmean(data)     # 20.0  the nan-versions skip missing values
np.isnan(data)       # [False  True False]
data[~np.isnan(data)]   # [10. 30.]   keep only real values
np.nan == np.nan     # False!  so always test with np.isnan, never ==
```

## 11. Linear algebra (a preview for machine learning)

```python
A = np.array([[1, 2], [3, 4]])
x = np.array([5, 6])
A @ x                 # [17 39]  matrix multiplication (same as np.dot(A, x))
A * A                 # element-wise multiplication (NOT matrix multiplication)
np.linalg.inv(A)      # inverse
np.linalg.solve(A, x) # solves A·y = x
```

Machine-learning models are mostly matrix multiplications, so `@` will matter a lot later.

## Common mistakes

- Using `and`/`or` with arrays. Use `&`/`|` and wrap each condition in brackets: `(a > 1) & (a < 5)`.
- Forgetting that a slice is a **view**, so changing it changes the original. Use `.copy()`.
- Mixing up `axis=0` and `axis=1`.
- Testing for missing values with `== np.nan`, which is always False. Use `np.isnan()`.
- `np.array([1, 2]) + [3]` works through broadcasting, but `[1, 2] + [3]` is list joining: `[1, 2, 3]`.
- Writing Python loops over arrays. Look for a vectorised version first.
- Using the old `np.random.seed()`/`np.random.rand()`. Prefer `np.random.default_rng(seed)`.

---

## Interview questions

**1. Why is NumPy faster than Python lists?**
Arrays store items of **one type** in **one contiguous block of memory**, and operations run in compiled C loops. A Python list stores pointers to separate Python objects, each with its own type information, so every operation goes through the slow interpreter.

**2. What is vectorisation?**
Replacing explicit Python loops with operations on whole arrays (`a * 2` instead of looping). It is faster and shorter.

**3. What is broadcasting?**
NumPy's rule for combining arrays of different shapes. Compare shapes from the right; dimensions fit if they are equal or one of them is 1. The smaller array is virtually stretched, without copying.

**4. What is the difference between a view and a copy?**
A view shares memory with the original array (basic slices, `reshape`, `ravel`), so changes affect both. A copy is independent (`.copy()`, `flatten()`, boolean and fancy indexing).

**5. What does `axis=0` mean?**
Operate down the rows, giving one result per column. `axis=1` operates across the columns, giving one result per row.

**6. What is the difference between `flatten()` and `ravel()`?**
Both return a 1-D array. `flatten()` always copies. `ravel()` returns a view when possible, which is faster and uses less memory.

**7. What does `-1` mean in `reshape`?**
"Work out this dimension from the others." `arange(12).reshape(3, -1)` gives shape `(3, 4)`.

**8. Why is `np.nan == np.nan` False?**
By the IEEE floating-point standard, NaN is not equal to anything, including itself. Use `np.isnan()` to find NaNs.

**9. What is the difference between `*` and `@`?**
`*` multiplies element by element. `@` is matrix multiplication (the dot product).

**10. How do you make random results reproducible?**
Create a generator with a fixed seed: `rng = np.random.default_rng(42)`, and use `rng` for all random numbers.

**11. How would you replace all negative values in an array with 0?**
`np.where(a < 0, 0, a)` (returns a new array), `a[a < 0] = 0` (in place), or `np.maximum(a, 0)`.

**12. How do you normalise every column of a 2-D array?**
`(X - X.mean(axis=0)) / X.std(axis=0)`. Broadcasting applies each column's mean and standard deviation to that column.

---

## Practice

1. Create a 4×5 array of random integers from 1 to 100 (with a seed). Print its shape, the max of each row, and the mean of each column.
2. From `np.arange(1, 21)`, select the even numbers greater than 10 using a mask.
3. Given exam marks for 5 students in 3 subjects (a 5×3 array), find each student's total, the class average per subject, and the top student's index.
4. Use `np.where` to turn marks into grades: `"A"` for 75 and above, otherwise `"B"`.
5. Normalise the columns of the marks array so that each column has mean 0.
6. Time `sum()` on a 1-million-item Python list vs `np.sum` on an array, using `time.perf_counter()`.
7. Load the CSV exported from the Expense Tracker with `np.genfromtxt` and find the total and largest amount.
