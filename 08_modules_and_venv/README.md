# 08 · Modules, Packages & Virtual Environments

Run the examples:

```bash
python 08_modules_and_venv/examples.py
```

This folder contains a small working package that the examples import:

```
08_modules_and_venv/
├── examples.py
├── requirements-example.txt
└── shopkit/                 <- a package (a folder with __init__.py)
    ├── __init__.py
    ├── pricing.py           <- a module
    └── text.py              <- a module
```

## 1. Module, package, library

| Term | What it is | Example |
|------|-----------|---------|
| **Module** | A single `.py` file | `pricing.py` |
| **Package** | A folder of modules with an `__init__.py` | `shopkit/` |
| **Library** | A collection of packages that you install | `pandas`, `requests` |
| **Standard library** | Comes built in with Python | `math`, `json`, `datetime`, `os` |

## 2. Ways to import

```python
import math                          # use as math.sqrt(16)
import numpy as np                   # alias (a convention in data science)
from math import sqrt, pi            # use directly: sqrt(16)
from shopkit.pricing import add_tax  # from a package's module
from shopkit import pricing          # import the module object
from math import *                   # AVOID: pollutes the namespace and hides where names come from
```

- **Absolute import**: `from shopkit.pricing import add_tax`. It's clear, so prefer it.
- **Relative import** (only inside a package): `from .pricing import add_tax`. The `.` means "this package".

A module's code runs **only once**, on its first import. After that, Python caches it in `sys.modules`.

## 3. `if __name__ == "__main__":`

Every module has a `__name__` variable:
- When you **run** the file directly, `__name__` is `"__main__"`.
- When it's **imported**, `__name__` is the module's name (for example `"shopkit.pricing"`).

```python
def add_tax(price): ...

if __name__ == "__main__":
    # This code runs only with `python pricing.py`, NOT on import.
    print(add_tax(100))
```

This lets a file work as a reusable module **and** as a runnable script, with quick tests or a demo.

## 4. `__init__.py`

- It marks a folder as a regular package.
- It runs when the package is first imported.
- It's often used to expose a clean API: `from .pricing import add_tax` inside `__init__.py` lets users write `from shopkit import add_tax`.
- `__all__ = [...]` controls what `from package import *` exports.

## 5. How Python finds modules: `sys.path`

When you write `import x`, Python searches these places in order:
1. The folder of the script being run
2. Folders listed in the `PYTHONPATH` environment variable
3. The standard library
4. `site-packages`, where pip installs libraries

⚠️ **Never name your file like a library you use.** A file called `random.py`, `pandas.py` or `json.py` **shadows** the real module and breaks your imports.

## 6. Useful standard library modules

| Module | Used for |
|--------|----------|
| `math`, `statistics`, `random` | Maths, mean/median, random numbers |
| `datetime` | Dates and times |
| `os`, `pathlib`, `shutil` | Files, folders, environment variables |
| `sys` | Interpreter info, `sys.argv`, `sys.path` |
| `json`, `csv` | Data formats |
| `collections`, `itertools`, `functools` | Advanced data structures and tools |
| `re` | Regular expressions |
| `logging` | Proper logging instead of `print` |
| `argparse` | Command-line arguments |

## 7. pip: installing packages

pip downloads packages from **PyPI** (the Python Package Index).

```bash
pip install requests              # latest version
pip install pandas==2.2.3         # exact version
pip install --upgrade pandas
pip uninstall requests
pip list                          # installed packages
pip show pandas                   # details for one package
pip freeze > requirements.txt     # save the exact versions
pip install -r requirements.txt   # install everything from the file
```

Tip: run pip as `python -m pip ...` so it always uses the same Python you run your code with.

## 8. Virtual environments (venv)

**The problem:** project A needs `pandas 1.5` and project B needs `pandas 2.2`. If you install both globally, they conflict.

**The solution:** each project gets its **own isolated environment** with its own packages.

```bash
# 1. Create (once per project)
python -m venv .venv

# 2. Activate (every time you open a new terminal)
.venv\Scripts\activate            # Windows (PowerShell / cmd)
source .venv/bin/activate         # macOS / Linux / Git Bash

# 3. Install packages: they go into .venv only
pip install numpy pandas

# 4. Save the dependencies
pip freeze > requirements.txt

# 5. Leave the environment
deactivate
```

- Add `.venv/` to `.gitignore`. **Never commit it.** Commit `requirements.txt` instead.
- Anyone else can rebuild the same environment with `pip install -r requirements.txt`.
- On Windows, if PowerShell blocks activation, run this once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
- Other tools you will hear about: **conda** (popular in data science), **uv** and **poetry** (modern, fast dependency managers).

## Common mistakes

- Naming your own file `pandas.py` or `random.py`, which shadows the real library.
- Installing packages without activating the venv, so they go to the global Python.
- Committing the `.venv` folder to Git.
- Circular imports: `a.py` imports `b.py` and `b.py` imports `a.py`. Fix it by moving the shared code into a third module.
- Using `from x import *`, which makes it unclear where names come from.

---

## Interview questions

**1. What is the difference between a module and a package?**
A module is a single `.py` file. A package is a directory of modules, usually with an `__init__.py`.

**2. What does `if __name__ == "__main__":` do?**
It runs code only when the file is executed directly, not when it's imported. This lets a file be both a reusable module and a script.

**3. What is `__init__.py` for?**
It marks a directory as a package and runs when the package is imported. It is often used to expose a clean public API or to set up the package.

**4. What is a virtual environment, and why use one?**
An isolated Python environment for each project, with its own installed packages. It prevents version conflicts between projects and makes setups reproducible.

**5. What is `requirements.txt`?**
A file that lists a project's dependencies, usually with pinned versions. You create it with `pip freeze > requirements.txt` and install from it with `pip install -r requirements.txt`.

**6. How does Python find a module when you import it?**
It checks `sys.modules` (the cache) first. Then it searches `sys.path` in order: the script's folder, `PYTHONPATH`, the standard library, then `site-packages`.

**7. What is the difference between `import module` and `from module import name`?**
`import module` binds the module name, and you access things as `module.name`. That is clear about where names come from. `from module import name` binds only that name directly, which is shorter but can cause naming clashes.

**8. What is the difference between absolute and relative imports?**
An absolute import uses the full path from the project root (`from shopkit.pricing import x`). A relative import uses dots for the current package (`from .pricing import x`) and only works inside packages.

**9. What happens if you import the same module twice?**
It runs only once. Later imports use the cached module from `sys.modules`.

**10. What is the difference between pip and conda?**
pip installs Python packages from PyPI. conda is a package **and** environment manager that can also install non-Python dependencies (such as C libraries). It is popular in data science.

---

## Practice

1. Create your own module `my_utils.py` with 2 functions and import it from another file.
2. Add an `if __name__ == "__main__":` block to `my_utils.py` that tests the functions. Check that it **doesn't** run on import.
3. Turn it into a package `utils/` with an `__init__.py` that exposes the functions directly.
4. In this repo folder, create a venv, activate it, `pip install requests`, and run `pip freeze > requirements.txt`.
5. Print `sys.path` and find where your installed packages live.
6. Create a file named `random.py` in a test folder, then try `import random; random.randint(1, 5)` there. Explain the error you get.
