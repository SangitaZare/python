import unittest
from datetime import date

from errors import ExpenseNotFoundError
from sample_data import demo_tracker
from tracker import ExpenseTracker


class TrackerTests(unittest.TestCase):
    def setUp(self):
        # setUp runs before every test, so each test gets a fresh tracker.
        self.tracker = ExpenseTracker()
        self.tracker.add(500, "food", "Groceries", date(2026, 10, 3))
        self.tracker.add(200, "transport", "Bus", date(2026, 9, 30))
        self.tracker.add(300, "food", "Lunch", date(2026, 10, 1))

    def test_ids_increase(self):
        self.assertEqual([e.id for e in self.tracker._expenses], [1, 2, 3])
        self.assertEqual(self.tracker.next_id, 4)

    def test_iterates_in_date_order(self):
        self.assertEqual([e.description for e in self.tracker], ["Bus", "Lunch", "Groceries"])

    def test_delete(self):
        removed = self.tracker.delete(2)
        self.assertEqual(removed.description, "Bus")
        self.assertEqual(len(self.tracker), 2)
        with self.assertRaises(ExpenseNotFoundError):
            self.tracker.get(2)

    def test_delete_missing_id_raises(self):
        with self.assertRaises(ExpenseNotFoundError):
            self.tracker.delete(99)

    def test_filter_by_category_and_month(self):
        food = list(self.tracker.filter(category="food"))
        self.assertEqual(len(food), 2)
        october = list(self.tracker.filter(month="2026-10"))
        self.assertEqual({e.description for e in october}, {"Groceries", "Lunch"})
        both = list(self.tracker.filter(category="transport", month="2026-10"))
        self.assertEqual(both, [])

    def test_filter_is_lazy(self):
        # A generator: nothing is computed until we ask for items.
        result = self.tracker.filter(category="food")
        self.assertFalse(isinstance(result, list))
        self.assertEqual(next(result).description, "Lunch")

    def test_totals(self):
        self.assertEqual(ExpenseTracker.total(self.tracker), 1000)
        self.assertEqual(self.tracker.totals_by_category(), {"food": 800, "transport": 200})
        self.assertEqual(self.tracker.latest_month(), "2026-10")
        self.assertEqual(self.tracker.biggest().description, "Groceries")

    def test_empty_tracker(self):
        empty = ExpenseTracker()
        self.assertEqual(empty.next_id, 1)
        self.assertIsNone(empty.latest_month())
        self.assertIsNone(empty.biggest())
        self.assertEqual(empty.totals_by_category(), {})


class DemoDataTests(unittest.TestCase):
    def test_demo_numbers_match_the_readme(self):
        tracker = demo_tracker()
        self.assertEqual(len(tracker), 13)
        self.assertEqual(ExpenseTracker.total(tracker), 18940)
        totals = tracker.totals_by_category("2026-10")
        self.assertEqual(list(totals)[:2], ["bills", "food"])
        self.assertEqual(totals["bills"], 9539)


if __name__ == "__main__":
    unittest.main()
