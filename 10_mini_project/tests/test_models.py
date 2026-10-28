import unittest
from datetime import date

from errors import InvalidAmountError, InvalidCategoryError
from models import Expense


class ExpenseTests(unittest.TestCase):
    def make(self, **changes):
        fields = dict(id=1, amount=100, category="food", description="Tea", date=date(2026, 10, 5))
        fields.update(changes)
        return Expense(**fields)

    def test_invalid_expense_cannot_be_created(self):
        with self.assertRaises(InvalidAmountError):
            self.make(amount=0)
        with self.assertRaises(InvalidCategoryError):
            self.make(category="snacks")

    def test_cleans_description(self):
        self.assertEqual(self.make(description="  Tea  ").description, "Tea")
        self.assertEqual(self.make(description="   ").description, "(no description)")

    def test_month_key(self):
        self.assertEqual(self.make().month, "2026-10")

    def test_dict_round_trip(self):
        expense = self.make(amount=99.5)
        data = expense.to_dict()
        self.assertEqual(data["date"], "2026-10-05")  # JSON-friendly string
        self.assertEqual(Expense.from_dict(data), expense)  # __eq__ from @dataclass


if __name__ == "__main__":
    unittest.main()
