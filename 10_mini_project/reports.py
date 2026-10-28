"""Turn tracker data into text for the terminal.                [Topics 02, 03]

Every function returns a string and never prints. The caller decides where
the text goes (the screen, a file, a test), which keeps this easy to test.

Note on alignment: pad the text first, then colour it. The colour codes are
invisible but still count as characters, so padding coloured text breaks
the columns.
"""
import calendar
from datetime import date, datetime

from colors import category_color, paint
from models import Expense
from tracker import ExpenseTracker

WIDTH = 62
BAR_WIDTH = 26

MENU_OPTIONS = [
    ("1", "Add expense"),
    ("2", "View all expenses"),
    ("3", "Filter by category"),
    ("4", "Monthly summary"),
    ("5", "Delete expense"),
    ("6", "Export to CSV"),
    ("0", "Save and exit"),
]


# ---- small helpers --------------------------------------------------------

def money(amount: float) -> str:
    return f"₹{amount:,.2f}"


def whole(amount: float) -> str:
    return f"₹{amount:,.0f}"


def percent(part: float, total: float) -> str:
    return f"{part / total * 100:.0f}%" if total else "0%"


def month_name(month: str) -> str:
    """'2026-10' -> 'October 2026'"""
    return datetime.strptime(month, "%Y-%m").strftime("%B %Y")


def active_month(tracker: ExpenseTracker, today: date) -> str:
    """The month to show: the newest month with data, or the current month."""
    return tracker.latest_month() or today.strftime("%Y-%m")


def days_counted(month: str, today: date) -> int:
    """Days so far for the current month, or the whole month for past months."""
    year, number = map(int, month.split("-"))
    if (year, number) == (today.year, today.month):
        return today.day
    return calendar.monthrange(year, number)[1]


def shorten(text: str, width: int) -> str:
    return text if len(text) <= width else text[: width - 1] + "…"


def heading(title: str) -> str:
    return paint(f"── {title} " + "─" * max(0, WIDTH - len(title) - 4), "cyan", "bold")


def budget_bar(spent: float, budget: float, width: int = 20) -> str:
    used = spent / budget if budget else 0
    filled = min(width, round(used * width))
    color = "green" if used <= 0.8 else "yellow" if used <= 1 else "red"
    return "[" + paint("█" * filled, color) + paint("░" * (width - filled), "dim") + "]"


# ---- screens --------------------------------------------------------------

def menu(tracker: ExpenseTracker, today: date) -> str:
    month = active_month(tracker, today)
    rows = list(tracker.filter(month=month))
    spent = tracker.total(rows)
    inner = 44
    lines = [
        paint("╭" + "─" * inner + "╮", "cyan"),
        paint("│" + "EXPENSE TRACKER".center(inner) + "│", "cyan", "bold"),
        paint("╰" + "─" * inner + "╯", "cyan"),
        f"  {month_name(month)} · " + paint(f"{len(rows)} expenses", "dim"),
        f"  Spent {money(spent)} of {money(tracker.budget)}",
        f"  {budget_bar(spent, tracker.budget)}  {percent(spent, tracker.budget)} of budget",
        "",
    ]
    lines += [f"  {paint(key, 'yellow', 'bold')}  {label}" for key, label in MENU_OPTIONS]
    return "\n".join(lines)


def expense_table(expenses: list[Expense], show_category: bool = True) -> str:
    if not expenses:
        return paint("  No expenses to show. Choose 1 to add one.", "dim")

    category_header = f"{'Category':<10}  " if show_category else ""
    header = f"{'ID':>3}  {'Date':<10}  {category_header}{'Description':<20}  {'Amount':>12}"
    rule = "─" * len(header)

    rows = []
    for e in expenses:
        category = paint(f"{e.category:<10}", category_color(e.category)) + "  " if show_category else ""
        rows.append(
            f"{e.id:>3}  {e.date:%d-%m-%Y}  {category}"
            f"{shorten(e.description, 20):<20}  {money(e.amount):>12}"
        )

    total_text = f"Total  {money(ExpenseTracker.total(expenses))}"
    return "\n".join([
        paint(header, "dim"),
        paint(rule, "dim"),
        *rows,
        paint(rule, "dim"),
        paint(f"{total_text:>{len(header)}}", "bold"),
    ])


def summary(tracker: ExpenseTracker, month: str, today: date) -> str:
    rows = list(tracker.filter(month=month))
    if not rows:
        return paint(f"  No expenses in {month_name(month)} yet.", "dim")

    total = tracker.total(rows)
    budget = tracker.budget
    totals = tracker.totals_by_category(month)
    top = max(totals.values())
    biggest = tracker.biggest(month)

    if total <= budget:
        left = paint(f"{whole(budget - total)} left", "green")
        verdict = paint("  ✓ You are within budget this month", "green")
    else:
        left = paint(f"{whole(total - budget)} over", "red")
        verdict = paint(f"  ✗ Over budget by {whole(total - budget)}", "red")

    lines = [
        paint(f"  {month_name(month).upper()}", "cyan", "bold"),
        "",
        f"  Spent    {paint(money(total), 'bold')}",
        paint(f"  Budget   {money(budget)}", "dim"),
        f"  {budget_bar(total, budget)}  {percent(total, budget)} used · {left}",
        "",
        paint("  Where the money went", "cyan", "bold"),
        "",
    ]
    for category, amount in totals.items():
        size = max(1, round(amount / top * BAR_WIDTH))
        bar = paint("█" * size, category_color(category))
        gap = " " * (BAR_WIDTH + 1 - size)
        lines.append(f"  {category:<11}{bar}{gap}{percent(amount, total):>4}  {whole(amount)}")

    star = paint("★", "yellow")
    lines += [
        "",
        f"  {star} Biggest expense: {biggest.description}, {whole(biggest.amount)}",
        f"  {star} Daily average: {whole(total / days_counted(month, today))}",
        verdict,
    ]
    return "\n".join(lines)
