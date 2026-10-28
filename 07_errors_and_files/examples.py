"""07 - Errors & files: exceptions, custom errors, with, pathlib, JSON, CSV."""
import csv
import json
import time
from contextlib import contextmanager
from pathlib import Path

# Write demo files next to this script, whatever folder you run it from.
OUTPUT = Path(__file__).parent / "output"
OUTPUT.mkdir(exist_ok=True)

print("=== 1. Common exceptions ===")
risky = [
    ("int('abc')", lambda: int("abc")),
    ("'5' + 5", lambda: "5" + 5),
    ("{}['x']", lambda: {}["x"]),
    ("[1][5]", lambda: [1][5]),
    ("10 / 0", lambda: 10 / 0),
    ("None.upper()", lambda: None.upper()),
    ("open('missing.txt')", lambda: open("missing.txt")),
]
for label, action in risky:
    try:
        action()
    except Exception as e:
        print(f"  {label:22} -> {type(e).__name__}: {e}")

print("\n=== 2. try / except / else / finally ===")


def divide(a, b):
    try:
        result = int(a) / int(b)
    except ValueError:
        print(f"  {a!r}/{b!r}: not a number")
    except ZeroDivisionError:
        print(f"  {a!r}/{b!r}: cannot divide by zero")
    else:
        print(f"  {a!r}/{b!r} = {result}")
    finally:
        print("    (finally always runs)")


divide("10", "2")
divide("10", "0")
divide("ten", "2")

print("\n=== 3. raise & custom exceptions ===")


class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        super().__init__(f"Balance {balance} is less than {amount}")
        self.balance = balance
        self.amount = amount


def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount


for amt in (200, -5, 5000):
    try:
        print("  new balance:", withdraw(1000, amt))
    except InsufficientFundsError as e:
        print(f"  custom error: {e} (short by {e.amount - e.balance})")
    except ValueError as e:
        print("  ValueError:", e)

print("\n=== 4. Exception chaining (raise ... from) ===")


class ConfigError(Exception):
    pass


def load_port(settings):
    try:
        return int(settings["port"])
    except (KeyError, ValueError) as e:
        raise ConfigError("Invalid port setting") from e


try:
    load_port({"port": "abc"})
except ConfigError as e:
    print(f"  {e} | caused by: {type(e.__cause__).__name__}: {e.__cause__}")

print("\n=== 5. EAFP vs LBYL ===")
stock = {"pen": 10}
# LBYL
if "book" in stock:
    print(stock["book"])
else:
    print("  LBYL: book not in stock")
# EAFP
try:
    print(stock["book"])
except KeyError:
    print("  EAFP: book not in stock")

print("\n=== 6. Text files with `with` ===")
notes = OUTPUT / "notes.txt"
with open(notes, "w", encoding="utf-8") as f:
    f.write("Learn Python\n")
    f.write("Practice daily\n")
with open(notes, "a", encoding="utf-8") as f:
    f.write("Start data science\n")
print("  closed after with?", f.closed)
with open(notes, encoding="utf-8") as f:
    for number, line in enumerate(f, start=1):
        print(f"  {number}. {line.strip()}")
with open(notes, encoding="utf-8") as f:
    print("  readlines():", f.readlines())

print("\n=== 7. pathlib ===")
print("  name:", notes.name, "| stem:", notes.stem, "| suffix:", notes.suffix)
print("  exists:", notes.exists(), "| size:", notes.stat().st_size, "bytes")
(OUTPUT / "quick.txt").write_text("written with pathlib", encoding="utf-8")
print("  read_text:", (OUTPUT / "quick.txt").read_text(encoding="utf-8"))
print("  glob *.txt:", sorted(p.name for p in OUTPUT.glob("*.txt")))

print("\n=== 8. Custom context manager ===")


@contextmanager
def timer(label):
    start = time.perf_counter()
    try:
        yield
    finally:
        print(f"  {label} took {time.perf_counter() - start:.4f}s")


with timer("sum of 1M numbers"):
    sum(range(1_000_000))

print("\n=== 9. JSON ===")
student = {"name": "Sangita", "age": 25, "skills": ["Python", "SQL"], "active": True}
text = json.dumps(student, indent=2)
print("  dumps ->", text.replace("\n", " "))
print("  loads ->", json.loads(text)["skills"])
json_file = OUTPUT / "student.json"
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(student, f, indent=2)
with open(json_file, encoding="utf-8") as f:
    loaded = json.load(f)
print("  round-trip equal:", loaded == student)

print("\n=== 10. CSV ===")
rows = [
    {"name": "Asha", "marks": 88},
    {"name": "Ravi", "marks": 92},
    {"name": "Meera", "marks": 74},
]
csv_file = OUTPUT / "marks.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "marks"])
    writer.writeheader()
    writer.writerows(rows)
print("  file content:", csv_file.read_text(encoding="utf-8").splitlines())
with open(csv_file, newline="", encoding="utf-8") as f:
    read_rows = list(csv.DictReader(f))
print("  first row:", read_rows[0], "<- marks is a str!")
above_80 = [r["name"] for r in read_rows if int(r["marks"]) > 80]
print("  scored above 80:", above_80)
average = sum(int(r["marks"]) for r in read_rows) / len(read_rows)
print(f"  average: {average:.2f}")
