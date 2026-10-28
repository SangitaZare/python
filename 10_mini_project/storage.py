"""Saving, loading and exporting.                               [Topics 07, 08]"""
import csv
import json
import os
from pathlib import Path

from errors import ExpenseError, StorageError
from models import Expense
from tracker import DEFAULT_BUDGET, ExpenseTracker

# Paths are built from this file's location, so the app works no matter
# which folder you run it from.
DATA_DIR = Path(__file__).parent / "data"
DEFAULT_FILE = DATA_DIR / "expenses.json"
DEMO_FILE = DATA_DIR / "demo.json"
CSV_FIELDS = ["id", "date", "category", "description", "amount"]


def load(path: Path) -> ExpenseTracker:
    """Load a tracker from JSON. A missing file just means 'no data yet'."""
    if not path.exists():
        return ExpenseTracker()
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        expenses = [Expense.from_dict(item) for item in data["expenses"]]
        budget = float(data.get("budget", DEFAULT_BUDGET))
    except (json.JSONDecodeError, KeyError, TypeError, ValueError, ExpenseError) as e:
        # One clear error type for the caller, with the original kept as the cause.
        raise StorageError(f"Could not read {path.name}: {e}") from e
    return ExpenseTracker(expenses, budget)


def save(tracker: ExpenseTracker, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {"budget": tracker.budget, "expenses": [e.to_dict() for e in tracker]}

    # Write to a temporary file first, then swap it in with one rename.
    # If the program crashes halfway through writing, the old file is
    # still complete, so your data is never left half-written.
    temp = path.with_suffix(".tmp")
    with open(temp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(temp, path)


def export_csv(expenses: list[Expense], path: Path) -> int:
    """Write expenses to CSV (ready for pandas) and return how many rows."""
    path.parent.mkdir(parents=True, exist_ok=True)
    # newline="" stops the csv module from adding blank lines on Windows.
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(e.to_dict() for e in expenses)
    return len(expenses)
