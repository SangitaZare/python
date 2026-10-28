"""11 - NumPy: arrays, dtypes, indexing, masks, vectorisation, broadcasting, axis, NaN."""
import sys
import time

import numpy as np

np.set_printoptions(precision=2, suppress=True)  # tidy decimal output

print("=== 0. Why NumPy: speed and memory ===")
n = 1_000_000
numbers_list = list(range(n))
numbers_array = np.arange(n)

start = time.perf_counter()
list_result = [x * 2 for x in numbers_list]
list_time = time.perf_counter() - start

start = time.perf_counter()
array_result = numbers_array * 2
array_time = time.perf_counter() - start

print(f"  double 1M numbers: list {list_time:.4f}s | numpy {array_time:.4f}s "
      f"-> about {list_time / array_time:.0f}x faster")
list_bytes = sys.getsizeof(numbers_list) + sum(sys.getsizeof(x) for x in numbers_list)
print(f"  memory: list ~{list_bytes / 1e6:.0f} MB | array {numbers_array.nbytes / 1e6:.0f} MB")

print("\n=== 1. Creating arrays ===")
print("  np.array:   ", np.array([1, 2, 3]))
print("  zeros:      ", np.zeros(5))
print("  full:       ", np.full(3, 7))
print("  arange:     ", np.arange(0, 10, 2))
print("  linspace:   ", np.linspace(0, 1, 5))
print("  ones (2,3):\n", np.ones((2, 3)))
rng = np.random.default_rng(seed=42)
print("  dice rolls: ", rng.integers(1, 7, size=5))
print("  normal:     ", rng.normal(loc=50, scale=10, size=3))

print("\n=== 2. Attributes ===")
a = np.array([[1, 2, 3], [4, 5, 6]])
print(f"  shape={a.shape} ndim={a.ndim} size={a.size} dtype={a.dtype}")

print("\n=== 3. dtypes and upcasting ===")
print("  [1, 2, 3]     ->", np.array([1, 2, 3]).dtype)
print("  [1, 2.5, 3]   ->", np.array([1, 2.5, 3]).dtype, np.array([1, 2.5, 3]))
print("  [1, 'a']      ->", np.array([1, "a"]).dtype, np.array([1, "a"]))
print("  [1.9, 2.7].astype(int) ->", np.array([1.9, 2.7]).astype(int), "(decimals cut, not rounded)")

print("\n=== 4. Indexing & slicing ===")
m = np.array([[10, 20, 30],
              [40, 50, 60],
              [70, 80, 90]])
print("  m[0, 2]  =", m[0, 2])
print("  m[1]     =", m[1])
print("  m[:, 1]  =", m[:, 1])
print("  m[:2, 1:] =\n", m[:2, 1:])

print("\n  Views vs copies:")
arr = np.array([1, 2, 3, 4])
part = arr[:2]
part[0] = 99
print("  after changing a slice, original =", arr, "<- changed!")
arr = np.array([1, 2, 3, 4])
safe = arr[:2].copy()
safe[0] = 99
print("  after changing a .copy(), original =", arr)
lst = [1, 2, 3, 4]
lst_part = lst[:2]
lst_part[0] = 99
print("  (a Python list slice is a copy:", lst, ")")

print("\n=== 5. Boolean masks & fancy indexing ===")
marks = np.array([45, 82, 67, 91, 38])
print("  marks > 60        ->", marks > 60)
print("  marks[marks > 60] ->", marks[marks > 60])
print("  60 < marks < 90   ->", marks[(marks > 60) & (marks < 90)])
print("  passed (>= 40)    ->", (marks >= 40).sum(), "students")
print("  np.where          ->", np.where(marks >= 40, "pass", "fail"))
print("  fancy [0, 3]      ->", marks[[0, 3]])
try:
    marks[marks > 60 and marks < 90]
except ValueError as e:
    print("  using 'and' ->", type(e).__name__, "(use & with brackets instead)")

print("\n=== 6. Vectorised operations & ufuncs ===")
x = np.array([1, 2, 3])
y = np.array([10, 20, 30])
print("  x + y =", x + y, "| x * y =", x * y, "| x ** 2 =", x ** 2, "| y / x =", y / x)
print("  sqrt  =", np.sqrt(np.array([1, 4, 9, 16])))
print("  round =", np.round(np.array([1.234, 5.678]), 1))
print("  maximum(arr, 0) =", np.maximum(np.array([-3, 5, -1, 2]), 0))
print("  list + list is joining:", [1, 2] + [3, 4], "| array + array is adding:", np.array([1, 2]) + np.array([3, 4]))

print("\n=== 7. Broadcasting ===")
prices = np.array([[100, 200],
                   [300, 400]])
print("  prices * 2 =\n", prices * 2)
print("  prices * [1.0, 0.5] (per column) =\n", prices * np.array([1.0, 0.5]))
print("  prices + [[1], [2]] (per row) =\n", prices + np.array([[1], [2]]))
try:
    np.ones((3, 4)) + np.ones(3)
except ValueError as e:
    print("  (3,4) + (3,) ->", "ValueError:", e)

print("\n=== 8. Aggregations & axis ===")
sales = np.array([[10, 20, 30],   # shop A, days 1-3
                  [40, 50, 60]])  # shop B
print("  sum()       =", sales.sum())
print("  sum(axis=0) =", sales.sum(axis=0), "<- per day (column)")
print("  sum(axis=1) =", sales.sum(axis=1), "<- per shop (row)")
print(f"  mean={sales.mean():.1f} max={sales.max()} std={sales.std():.2f} argmax={sales.argmax()}")
print("  median =", np.median(sales), "| 90th percentile =", np.percentile(sales, 90))
print("  cumsum =", np.cumsum([1, 2, 3, 4]))

print("\n=== 9. Reshape, transpose, stack ===")
r = np.arange(6)
print("  reshape(2, 3) =\n", r.reshape(2, 3))
print("  reshape(3, -1).shape =", r.reshape(3, -1).shape)
print("  .T shape =", r.reshape(2, 3).T.shape)
print("  vstack shape =", np.vstack([r, r]).shape, "| hstack shape =", np.hstack([r, r]).shape)
print("  newaxis shape =", r[:, np.newaxis].shape)
try:
    r.reshape(4, 2)
except ValueError as e:
    print("  reshape(4, 2) ->", "ValueError:", e)

print("\n=== 10. Missing values (NaN) ===")
data = np.array([10, np.nan, 30])
print("  mean    =", data.mean(), "| nanmean =", np.nanmean(data))
print("  isnan   =", np.isnan(data))
print("  cleaned =", data[~np.isnan(data)])
print("  np.nan == np.nan ->", np.nan == np.nan)

print("\n=== 11. Linear algebra preview ===")
A = np.array([[1, 2], [3, 4]])
v = np.array([5, 6])
print("  A @ v =", A @ v)
print("  A * A (element-wise) =\n", A * A)
print("  A @ A (matrix) =\n", A @ A)
print("  solve(A, v) =", np.linalg.solve(A, v))

print("\n=== 12. Real example: class marks (5 students x 3 subjects) ===")
rng = np.random.default_rng(seed=1)
scores = rng.integers(35, 100, size=(5, 3))
names = np.array(["Asha", "Ravi", "Meera", "Kabir", "Isha"])
subjects = ["Maths", "Science", "English"]
print("  scores =\n", scores)
totals = scores.sum(axis=1)
print("  total per student  :", dict(zip(names.tolist(), totals.tolist())))
print("  average per subject:", dict(zip(subjects, scores.mean(axis=0).round(1).tolist())))
print("  topper             :", names[totals.argmax()], "with", totals.max())
print("  failed any subject :", names[(scores < 40).any(axis=1)].tolist())
normalised = (scores - scores.mean(axis=0)) / scores.std(axis=0)
print("  normalised column means (all ~0):", normalised.mean(axis=0).round(6) + 0.0)  # + 0.0 turns -0. into 0.
grades = np.where(scores >= 75, "A", np.where(scores >= 50, "B", "C"))
print("  grades =\n", grades)
