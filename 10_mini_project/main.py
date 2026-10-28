"""Expense Tracker: a command-line app to track daily spending.

Run it from this folder:

    python main.py               # your own data  -> data/expenses.json
    python main.py --demo        # sample data     -> data/demo.json
    python main.py --budget 30000
    python main.py --help

This file is the only one that talks to the user (input/print). Everything
else is plain logic, which is why it can be unit tested.
"""
import argparse
import functools
import sys
from datetime import date
from pathlib import Path

import colors
import reports
import storage
from colors import paint
from errors import ExpenseError, StorageError
from models import CATEGORIES
from sample_data import demo_tracker
from tracker import ExpenseTracker
from validators import DATE_FORMAT, parse_amount, parse_category, parse_date, parse_id

CATEGORY_PROMPT = ", ".join(f"{n} {name}" for n, name in enumerate(CATEGORIES, start=1))


def autosave(method):
    """Decorator: save to disk after any action that returns True.   [Topic 09]

    Add and delete both change data. Instead of remembering to call save()
    in each of them, we decorate them once and it can't be forgotten.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        changed = method(self, *args, **kwargs)
        if changed:
            storage.save(self.tracker, self.path)
        return changed
    return wrapper


def display_path(path: Path) -> str:
    """Show 'data/expenses.json' for files in this project, full path otherwise."""
    try:
        return path.resolve().relative_to(Path(__file__).parent.resolve()).as_posix()
    except ValueError:
        return str(path)


def ask(prompt: str, parser):
    """Keep asking until `parser` accepts the answer.                [Topic 05]

    `parser` is any function that turns text into a value or raises an
    ExpenseError. Passing functions around like this is what "functions
    are first-class objects" means in practice.
    """
    while True:
        try:
            return parser(input(prompt))
        except ExpenseError as e:
            print(paint(f"  ✗ {e}", "red"))


class App:
    def __init__(self, tracker: ExpenseTracker, path: Path, today: date) -> None:
        self.tracker = tracker
        self.path = path
        self.today = today

    def run(self) -> None:
        try:
            while True:
                print()
                print(reports.menu(self.tracker, self.today))
                print()
                choice = input("Choose an option: ").strip().lower()
                print()
                match choice:                                        # [Topic 04]
                    case "1":
                        self.add_expense()
                    case "2":
                        self.view_all()
                    case "3":
                        self.filter_by_category()
                    case "4":
                        self.monthly_summary()
                    case "5":
                        self.delete_expense()
                    case "6":
                        self.export_csv()
                    case "0" | "q" | "quit" | "exit":
                        break
                    case _:
                        print(paint(f'  ✗ "{choice}" is not an option. Enter a number from the menu', "red"))
                input(paint("\nPress Enter to return to the menu...", "dim"))
        except (KeyboardInterrupt, EOFError):
            print()  # Ctrl+C or end of input: still save and say goodbye
        self.save_and_exit()

    # ---- menu actions ----------------------------------------------------

    @autosave
    def add_expense(self) -> bool:
        print(reports.heading("Add expense"))
        amount = ask("Amount (₹): ", parse_amount)
        category = ask(f"Category [{CATEGORY_PROMPT}]: ", parse_category)
        description = input("Description: ")
        spent_on = ask(
            f"Date [Enter = today, {self.today:{DATE_FORMAT}}]: ",
            lambda text: parse_date(text, self.today),
        )
        expense = self.tracker.add(amount, category, description, spent_on)
        print()
        print(paint(
            f'  ✓ Added #{expense.id}  {reports.money(expense.amount)}  '
            f'{expense.category}  "{expense.description}"', "green"))
        return True

    def view_all(self) -> None:
        print(reports.heading("All expenses"))
        print(reports.expense_table(list(self.tracker)))

    def filter_by_category(self) -> None:
        print(reports.heading("Filter by category"))
        category = ask(f"Category [{CATEGORY_PROMPT}]: ", parse_category)
        rows = list(self.tracker.filter(category=category))
        print()
        print(reports.expense_table(rows, show_category=False))
        if rows:
            share = reports.percent(self.tracker.total(rows), self.tracker.total(self.tracker))
            print(paint(f"{len(rows)} expenses · {share} of all spending", "dim"))

    def monthly_summary(self) -> None:
        month = reports.active_month(self.tracker, self.today)
        print(reports.summary(self.tracker, month, self.today))

    @autosave
    def delete_expense(self) -> bool:
        print(reports.heading("Delete expense"))
        if not len(self.tracker):
            print(paint("  There are no expenses to delete.", "dim"))
            return False
        # The parser both checks the text and looks up the ID, so a wrong ID
        # simply asks again (ExpenseNotFoundError is an ExpenseError).
        expense = ask("Expense ID to delete: ", lambda text: self.tracker.get(parse_id(text)))
        answer = input(
            f'Delete #{expense.id}  {reports.money(expense.amount)}  '
            f'{expense.category}  "{expense.description}"? (y/n): '
        ).strip().lower()
        if answer not in ("y", "yes"):
            print(paint("  Cancelled. Nothing was deleted.", "dim"))
            return False
        self.tracker.delete(expense.id)
        print(paint(f"  ✓ Deleted #{expense.id}", "green"))
        return True

    def export_csv(self) -> None:
        print(reports.heading("Export to CSV"))
        name = input("File name [expenses.csv]: ").strip() or "expenses.csv"
        path = storage.DATA_DIR / Path(name).with_suffix(".csv").name
        count = storage.export_csv(list(self.tracker), path)
        print(paint(f"  ✓ Exported {count} expenses to data/{path.name}", "green"))
        print(f'  Next: open it with pandas -> pd.read_csv("data/{path.name}")')

    def save_and_exit(self) -> None:
        storage.save(self.tracker, self.path)
        print(paint(f"✓ Saved {len(self.tracker)} expenses to {display_path(self.path)}", "green"))
        print("Goodbye! See you tomorrow.")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Track your daily expenses from the terminal.")
    parser.add_argument("--demo", action="store_true", help="try the app with sample data (data/demo.json)")
    parser.add_argument("--data", type=Path, help="use a different JSON data file")
    parser.add_argument("--budget", type=float, help="set your monthly budget, e.g. --budget 30000")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    # The ₹ and box characters need UTF-8, even when output is redirected.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    colors.enable_windows_ansi()

    path = args.data or (storage.DEMO_FILE if args.demo else storage.DEFAULT_FILE)
    try:
        tracker = storage.load(path)
    except StorageError as e:
        print(paint(f"✗ {e}", "red"))
        print("Fix the file or move it away, then run the app again.")
        return 1

    if args.demo and not len(tracker):
        tracker = demo_tracker()
        storage.save(tracker, path)

    if args.budget is not None:
        if args.budget <= 0:
            print(paint("✗ The budget must be more than 0", "red"))
            return 1
        tracker.budget = args.budget
        storage.save(tracker, path)

    App(tracker, path, date.today()).run()
    return 0


if __name__ == "__main__":                                           # [Topic 08]
    sys.exit(main())
