"""ExpenseTracker: the business logic.                   [Topics 03, 05, 06, 09]

There is no input() or print() in this file. It only works with data,
which is why it can be tested without typing anything, and why the same
class could later power a web app or a Jupyter notebook.
"""
from collections import defaultdict
from collections.abc import Iterable, Iterator
from datetime import date

from errors import ExpenseNotFoundError
from models import Expense

DEFAULT_BUDGET = 25_000.0


class ExpenseTracker:
    def __init__(self, expenses: Iterable[Expense] = (), budget: float = DEFAULT_BUDGET) -> None:
        # The leading underscore says "internal": other code should use the
        # methods below instead of changing this list directly.
        self._expenses: list[Expense] = list(expenses)
        self.budget = budget

    def __len__(self) -> int:
        return len(self._expenses)

    def __iter__(self) -> Iterator[Expense]:
        """`for e in tracker` always gives expenses in date order."""
        return iter(sorted(self._expenses, key=lambda e: (e.date, e.id)))

    def __repr__(self) -> str:
        return f"ExpenseTracker({len(self)} expenses, budget={self.budget})"

    @property
    def next_id(self) -> int:
        return max((e.id for e in self._expenses), default=0) + 1

    # ---- changing data -------------------------------------------------

    def add(self, amount: float, category: str, description: str, spent_on: date) -> Expense:
        expense = Expense(self.next_id, amount, category, description, spent_on)
        self._expenses.append(expense)
        return expense

    def get(self, expense_id: int) -> Expense:
        for expense in self._expenses:
            if expense.id == expense_id:
                return expense
        raise ExpenseNotFoundError(f"No expense with ID {expense_id}. Use option 2 to see all IDs")

    def delete(self, expense_id: int) -> Expense:
        expense = self.get(expense_id)  # raises if the ID doesn't exist
        self._expenses = [e for e in self._expenses if e.id != expense_id]
        return expense

    # ---- reading data --------------------------------------------------

    def filter(self, *, category: str | None = None, month: str | None = None) -> Iterator[Expense]:
        """A generator: yields matching expenses one at a time.

        The `*` makes category and month keyword-only, so a call reads
        clearly: tracker.filter(category="food").
        """
        for expense in self:
            if category is not None and expense.category != category:
                continue
            if month is not None and expense.month != month:
                continue
            yield expense

    @staticmethod
    def total(expenses: Iterable[Expense]) -> float:
        return round(sum(e.amount for e in expenses), 2)

    def totals_by_category(self, month: str | None = None) -> dict[str, float]:
        """{'bills': 9539.0, 'food': 4860.0, ...}, biggest first."""
        totals: defaultdict[str, float] = defaultdict(float)
        for expense in self.filter(month=month):
            totals[expense.category] += expense.amount
        return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))

    def biggest(self, month: str | None = None) -> Expense | None:
        return max(self.filter(month=month), key=lambda e: e.amount, default=None)

    def latest_month(self) -> str | None:
        return max((e.month for e in self._expenses), default=None)
