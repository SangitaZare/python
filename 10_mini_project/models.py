"""The Expense data model.                                   [Topics 06, 07]"""
from dataclasses import dataclass
from datetime import date

from errors import InvalidAmountError, InvalidCategoryError

# A tuple, not a list: the categories are fixed, and the order matters
# because the user can pick a category by its number (1 = food, ...).
CATEGORIES = ("food", "transport", "shopping", "bills", "health", "fun", "other")


@dataclass
class Expense:
    """One expense. @dataclass writes __init__, __repr__ and __eq__ for us."""

    id: int
    amount: float
    category: str
    description: str
    date: date

    def __post_init__(self) -> None:
        # Validating here means an invalid Expense can never exist, whether it
        # came from the keyboard, the JSON file, or a test.
        if self.amount <= 0:
            raise InvalidAmountError("Amount must be more than 0")
        if self.category not in CATEGORIES:
            raise InvalidCategoryError(f'"{self.category}" is not a category')
        self.amount = round(float(self.amount), 2)
        self.description = self.description.strip() or "(no description)"

    @property
    def month(self) -> str:
        """'2026-10' style key, used to group expenses by month."""
        return self.date.strftime("%Y-%m")

    def to_dict(self) -> dict:
        """Convert to plain types that JSON understands (no date objects)."""
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "category": self.category,
            "description": self.description,
            "amount": self.amount,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        """Alternative constructor: build an Expense from a JSON dict."""
        return cls(
            id=int(data["id"]),
            amount=float(data["amount"]),
            category=data["category"],
            description=data["description"],
            date=date.fromisoformat(data["date"]),
        )
