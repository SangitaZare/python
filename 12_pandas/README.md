# 12 · Pandas: Working with Tables of Data

**👉 Start with the notebook: [pandas_tutorial.ipynb](pandas_tutorial.ipynb).** GitHub shows it with all its outputs, so you can read it without installing anything.
It takes a messy online-shop dataset all the way to business answers. These notes explain the concepts behind it.

To run it yourself:

```bash
.venv\Scripts\activate             # Windows; macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook 12_pandas/pandas_tutorial.ipynb
```

Or open the `.ipynb` file in VS Code with the **Jupyter** extension and pick the `.venv` interpreter.

| File | What it is |
|------|------------|
| [pandas_tutorial.ipynb](pandas_tutorial.ipynb) | The hands-on tutorial (load → explore → clean → merge → analyse → save) |
| [data/orders.csv](data/orders.csv) | 305 shop orders, **deliberately messy** |
| [data/products.csv](data/products.csv) | 12 products with category and price |
| [data/sales_clean.csv](data/sales_clean.csv) | The cleaned result, which topic 13 starts from |
| [data/make_data.py](data/make_data.py) | The script that generated the data (fixed seed, so it's reproducible) |

---

## What is pandas?

**pandas** is Python's library for **tables**: think Excel, but with code. It's built on NumPy, so it's fast, and it adds what real data needs:
- **labels**: named columns and a row index, not just positions
- **mixed types**: text, numbers and dates in one table
- **missing data** handling
- reading and writing **CSV, Excel, JSON and SQL**
- **groupby**, **pivot tables** and **joins**

Data scientists often say that **80% of the job is getting and cleaning data**, and that's pandas' territory.

## 1. Series and DataFrame

```python
import pandas as pd

s = pd.Series([1999, 499], index=["Earbuds", "Charger"])   # one labelled column
df = pd.DataFrame({"product": ["Earbuds", "Charger"],         # a table
                   "price": [1999, 499]})
```

- A **Series** is a 1-D array with an **index** (labels).
- A **DataFrame** is a collection of Series that share one index. Each column is a Series.
- Every column has **one dtype**, like a NumPy array. Different columns can have different dtypes.

## 2. Load and explore: always look first

```python
df = pd.read_csv("data/orders.csv")      # also: read_excel, read_json, read_sql
df.head()          # first 5 rows (tail() for the last)
df.shape           # (rows, columns)
df.info()          # column types + non-null counts  ← start here
df.describe()      # count, mean, std, min, max... of numeric columns
df.isna().sum()    # missing values per column
df["city"].value_counts()   # how often each value appears
df.duplicated().sum()       # exact duplicate rows
df["customer"].nunique()    # number of distinct values
```

## 3. Selecting data

| You want | Code |
|----------|------|
| One column → Series | `df["city"]` |
| Several columns → DataFrame | `df[["city", "quantity"]]` |
| By **label** | `df.loc[0:5, ["city"]]` (the end label is **included**) |
| By **position** | `df.iloc[0:5, 0:2]` (the end is **excluded**) |
| Filter rows | `df[df["quantity"] > 1]` |
| Several conditions | `df[(df["a"] > 1) & (df["b"] == "x")]` |
| Readable filter | `df.query("a > 1 and b == 'x'")` |
| Value in a list | `df[df["city"].isin(["Pune", "Delhi"])]` |

## 4. Cleaning

| Problem | Fix |
|---------|-----|
| Duplicate rows | `df.drop_duplicates()` |
| Extra spaces or mixed case | `df["city"].str.strip().str.title()` |
| Different names for the same thing | `.replace({"Bangalore": "Bengaluru"})` |
| Dates stored as text | `pd.to_datetime(df["order_date"])` |
| Wrong type | `df["qty"].astype(int)` |
| Missing values | `fillna(value)`, `dropna()`, or leave them and say so |
| Impossible values | Find them with a mask, then set them to `NaN` or remove them |
| Bad column names | `df.rename(columns={"old": "new"})` |

**How to handle missing values is a decision, not a rule.** Ask:
- **How many are missing?** 2% can often be dropped or filled; 40% probably can't.
- **Can I make a sensible guess?** Use the median for numbers with outliers, the mode for categories, 0 only if 0 truly means "none".
- **Would guessing be misleading?** Then use a label like `"Unknown"`, or drop the rows **and report it**.

## 5. Adding columns

```python
df["revenue"] = df["quantity"] * df["price"]            # vectorised: fast and clear
df["month"] = df["order_date"].dt.to_period("M")        # .dt for dates
df["size"] = pd.cut(df["revenue"], bins=[0, 500, 2000, np.inf],
                    labels=["Small", "Medium", "Large"])  # numbers → buckets
df["big"] = np.where(df["revenue"] >= 3000, "Yes", "No")  # if/else for a column
df["city_code"] = df["city"].map({"Pune": "PNQ", "Delhi": "DEL"})
```

Avoid `df.apply(func, axis=1)` for simple maths. It runs a Python function **row by row**, which can be 100× slower than vectorised code. Use it only when no vectorised version exists.

## 6. groupby: split → apply → combine

The most important analysis tool. It's the same idea as SQL's `GROUP BY`.

```python
df.groupby("category")["revenue"].sum()                 # one number per group

df.groupby("category").agg(                              # several, with clear names
    orders=("order_id", "count"),
    revenue=("revenue", "sum"),
    avg_order=("revenue", "mean"),
)

df.groupby(["city", "category"])["revenue"].sum()       # group by two columns
```

## 7. Reshaping: pivot tables and crosstabs

```python
pd.pivot_table(df, values="revenue", index="city", columns="category",
               aggfunc="sum", fill_value=0, margins=True)   # just like Excel
pd.crosstab(df["category"], df["size"])                      # counts of combinations
```

## 8. Combining tables

```python
orders.merge(products, on="product_id", how="left")   # like SQL JOIN / Excel VLOOKUP
pd.concat([jan_df, feb_df])                           # stack tables with the same columns
```

| `how=` | Keeps |
|--------|-------|
| `"inner"` (default) | Only rows that match in **both** tables |
| `"left"` | **All** rows of the left table; NaN where there's no match |
| `"right"` | All rows of the right table |
| `"outer"` | Everything from both |

Add `indicator=True` to see which rows matched. It catches problems like the unknown product `P99` in our data.

## 9. Sorting and top-N

```python
df.sort_values("revenue", ascending=False)
df.sort_values(["city", "revenue"], ascending=[True, False])
df.nlargest(5, "revenue")
s.pct_change()          # growth from one row to the next
```

## 10. pandas 3: Copy-on-Write

pandas 3 (2026) uses **Copy-on-Write**: any DataFrame you get from another one behaves like a copy.

```python
df.loc[df["qty"] <= 0, "qty"] = np.nan    # ✅ the right way to change values
df["qty"][df["qty"] <= 0] = np.nan        # ❌ "chained assignment": does nothing in pandas 3
```

Rule: **change data in one step**, with `df.loc[rows, col] = ...` or `df[col] = ...`.

## Common mistakes

- `and`/`or` in filters. Use `&`/`|` and wrap each condition in brackets.
- Forgetting to assign the result: `df.drop_duplicates()` returns a **new** DataFrame. Use `df = df.drop_duplicates()`.
- `loc` vs `iloc`: `loc[0:5]` includes row label 5; `iloc[0:5]` doesn't include position 5.
- Assuming `read_csv` parses dates. It doesn't, unless you use `parse_dates=` or `pd.to_datetime`.
- A left join that adds NaN quietly turns integer columns into floats.
- Using an inner join without checking, which silently drops rows. Check the counts before and after a merge.
- Using `apply` with a lambda for simple column maths. Use vectorised operations.

---

## Interview questions

**1. What is the difference between a Series and a DataFrame?**
A Series is a single labelled 1-D column. A DataFrame is a 2-D table made of several Series that share an index.

**2. What is the difference between `loc` and `iloc`?**
`loc` selects by **labels** (index labels and column names), and slices include the end. `iloc` selects by integer **positions**, and slices exclude the end.

**3. How do you handle missing values?**
First measure them (`isna().sum()`), then decide based on the amount and the meaning: drop rows (`dropna`), fill with a statistic (mean, median or mode), fill with a label like "Unknown", or interpolate time series. Always document the choice, because it affects the results.

**4. What is the difference between `merge`, `join` and `concat`?**
`merge` combines tables on key columns, like SQL joins. `join` is a shortcut that merges on the index. `concat` stacks tables vertically (more rows) or horizontally (more columns) without matching keys.

**5. Explain inner, left and outer joins.**
Inner keeps only matching keys. Left keeps all rows of the left table and fills NaN where the right has no match. Outer keeps all keys from both tables.

**6. How does `groupby` work?**
Split–apply–combine: split the rows into groups by a key, apply an aggregation (sum, mean, count...) to each group, and combine the results into a new table.

**7. What is the difference between `apply`, `map` and vectorised operations?**
Vectorised operations work on whole columns in compiled code, so they're the fastest. `map` replaces each value in a Series using a dict or function. `apply` calls a Python function per row or column; it's flexible but slow, so use it only when needed.

**8. What is the difference between `pivot_table` and `groupby`?**
Both aggregate. `pivot_table` also reshapes the result into a 2-D grid (one key as rows, another as columns), like an Excel pivot table. `groupby` gives a long format.

**9. How do you find and remove duplicates?**
`df.duplicated()` marks duplicates and `df.drop_duplicates()` removes them. Use `subset=[...]` to compare only some columns and `keep="first"`/`"last"` to choose which one stays.

**10. Why did my integer column become float after a merge?**
A left or outer join inserted `NaN` for unmatched rows, and NaN is a float, so pandas upcast the column. Convert it back with `astype(int)` after handling the NaNs, or use the nullable `"Int64"` dtype.

**11. What is Copy-on-Write in pandas 3?**
Any DataFrame or Series derived from another behaves as a copy, so changing it never changes the original. Chained assignment (`df["a"][mask] = x`) no longer works; use `df.loc[mask, "a"] = x`.

**12. How would you find the top 3 products by revenue in each category?**
```python
(df.groupby(["category", "product"])["revenue"].sum()
   .groupby(level="category", group_keys=False).nlargest(3))
```

---

## Practice

Use `data/sales_clean.csv` (load it with `parse_dates=["order_date"]`):

1. Which weekday has the most orders? (Hint: the `weekday` column and `value_counts`.)
2. What is the average order value per city, sorted from highest to lowest?
3. Which product sold the most **items** (not revenue)?
4. For each month, what share of revenue came from Electronics?
5. Find customers who used **every** payment method at least once.
6. Add a `discounted_revenue` column with 10% off orders above ₹3,000.
7. **Challenge:** re-run `data/make_data.py` with a different seed, then re-run the notebook. Do the conclusions change?
