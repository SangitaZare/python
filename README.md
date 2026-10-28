# Python

A hands-on learning path: core Python first, then data science.

Each topic folder has:
- **`README.md`**: simple notes, common mistakes, **interview questions with answers**, and practice tasks
- **`examples.py`**: a runnable script for everything in the notes

```bash
python 01_basics/examples.py
```

Part 1 needs only Python 3.10 or newer. No libraries.

## Part 1: Python

| # | Topic | Status |
|---|-------|--------|
| 01 | [Basics](01_basics/): variables, types, operators, truthy/falsy, conversion | ✅ |
| 02 | [Strings](02_strings/): slicing, methods, f-strings, immutability | ✅ |
| 03 | [Collections](03_collections/): list, tuple, set, dict, copying | ✅ |
| 04 | [Control flow](04_control_flow/): if, loops, break/continue, comprehensions, match | ✅ |
| 05 | [Functions](05_functions/): args, `*args`/`**kwargs`, scope, lambda, closures | ✅ |
| 06 | [OOP](06_oop/): classes, 4 pillars, inheritance, dunder methods, dataclasses | ✅ |
| 07 | [Errors & files](07_errors_and_files/): exceptions, custom errors, `with`, pathlib, JSON, CSV | ✅ |
| 08 | [Modules & venv](08_modules_and_venv/): imports, packages, `__name__`, pip, virtual environments | ✅ |
| 09 | [Advanced](09_advanced/): iterators, generators, itertools, decorators, type hints | ✅ |
| 10 | [Mini project: Expense Tracker](10_mini_project/): a terminal app + Streamlit web app using topics 01–09, with 41 tests | ✅ |

## Part 2: Data Science

Part 2 uses libraries, so set up a virtual environment once (see [topic 08](08_modules_and_venv/)):

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows; macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

| # | Topic | Status |
|---|-------|--------|
| 11 | [NumPy](11_numpy/): arrays, vectorisation, broadcasting, axis, masks, NaN | ✅ |
| 12 | [Pandas](12_pandas/): cleaning messy data, groupby, merge, pivot tables (Jupyter notebook) | ✅ |
| 13 | [Visualisation](13_visualisation/): Matplotlib and Seaborn, 12 charts with design rules (notebook) | ✅ |
| 14 | [Statistics](14_statistics/): distributions, CLT, confidence intervals, hypothesis tests, A/B testing (notebook) | ✅ |
| 15 | EDA project on a real dataset | ⏳ |
| 16 | Machine learning with scikit-learn | ⏳ |
| 17 | Capstone: data → model → insights | ⏳ |

## How to study

1. Read the topic's `README.md`.
2. Run `examples.py` and compare the output with the code.
3. Change the code and break it on purpose to see the errors.
4. Answer the interview questions **out loud** before reading the answers.
5. Do the practice tasks.
