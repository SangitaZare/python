"""08 - Modules, packages, __name__, sys.path, standard library, pip/venv info."""
import importlib.util
import sys

print("=== 1. __name__ of the file being run ===")
print("  __name__ =", __name__)

print("\n=== 2. Importing our own package (watch __init__.py run once) ===")
import shopkit                                  # runs shopkit/__init__.py
import shopkit                                  # cached: does NOT run again
from shopkit import add_tax, slugify            # exposed by __init__.py
from shopkit.pricing import GST_RATE, apply_discount  # straight from the module
from shopkit import pricing as pr               # module object with an alias

print("  add_tax(100)            =", add_tax(100))
print("  apply_discount(500, 20) =", apply_discount(500, 20))
print("  GST_RATE                =", GST_RATE)
print("  pr.add_tax(50, 0.05)    =", pr.add_tax(50, 0.05))
print("  slugify(...)            =", slugify("Blue Cotton T-Shirt!"))
print("  shopkit.__version__     =", shopkit.__version__)
print("  pricing module __name__ =", pr.__name__, "(not '__main__', because it was imported)")
print("  shopkit.__all__         =", shopkit.__all__)

print("\n=== 3. Module cache: sys.modules ===")
print("  'shopkit.pricing' in sys.modules:", "shopkit.pricing" in sys.modules)

print("\n=== 4. Where Python searches: sys.path (first 3) ===")
for path in sys.path[:3]:
    print("  ", path)

print("\n=== 5. Standard library tour ===")
import math
import random
import statistics
from collections import Counter
from datetime import date, datetime, timedelta

print("  math.sqrt(16), math.pi:", math.sqrt(16), round(math.pi, 4))
marks = [88, 92, 79, 95, 70]
print("  statistics mean/median:", statistics.mean(marks), statistics.median(marks))
random.seed(42)  # fixed seed so the output is repeatable
print("  random.choice:", random.choice(["red", "green", "blue"]), "| randint:", random.randint(1, 6))
today = date(2026, 10, 28)
print("  date + 30 days:", today + timedelta(days=30))
print("  formatted:", datetime(2026, 10, 28, 9, 30).strftime("%d %b %Y, %I:%M %p"))
print("  Counter:", Counter("hello world").most_common(2))

print("\n=== 6. Python & environment info ===")
print("  Python version :", sys.version.split()[0])
print("  Interpreter    :", sys.executable)
in_venv = sys.prefix != sys.base_prefix
print("  Inside a venv? :", in_venv)

print("\n=== 7. Is a third-party package installed? ===")
for name in ("numpy", "pandas", "requests"):
    found = importlib.util.find_spec(name) is not None
    hint = "installed" if found else "not installed -> pip install " + name
    print(f"  {name:9}: {hint}")

print("\n=== 8. Importing something that doesn't exist ===")
try:
    import not_a_real_module  # noqa: F401
except ModuleNotFoundError as e:
    print("  ModuleNotFoundError:", e)

print("\nTip: run `python 08_modules_and_venv/shopkit/pricing.py` to see the")
print("     if __name__ == '__main__' block run.")
