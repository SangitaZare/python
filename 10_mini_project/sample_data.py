"""Sample expenses for `python main.py --demo`."""
from datetime import date

from tracker import ExpenseTracker

SAMPLE = [
    (date(2026, 10, 1), "bills", "Rent share", 8000),
    (date(2026, 10, 3), "food", "Groceries", 1850),
    (date(2026, 10, 5), "transport", "Metro card recharge", 500),
    (date(2026, 10, 7), "bills", "Electricity", 1240),
    (date(2026, 10, 10), "shopping", "Kurta", 1499),
    (date(2026, 10, 12), "food", "Dinner out", 920),
    (date(2026, 10, 15), "health", "Pharmacy", 360),
    (date(2026, 10, 18), "fun", "Movie tickets", 600),
    (date(2026, 10, 20), "transport", "Cab to airport", 780),
    (date(2026, 10, 22), "bills", "Mobile recharge", 299),
    (date(2026, 10, 24), "food", "Groceries", 1640),
    (date(2026, 10, 26), "shopping", "Python book", 802),
    (date(2026, 10, 28), "food", "Lunch with team", 450),
]


def demo_tracker() -> ExpenseTracker:
    tracker = ExpenseTracker(budget=25_000)
    for spent_on, category, description, amount in SAMPLE:
        tracker.add(amount, category, description, spent_on)
    return tracker
