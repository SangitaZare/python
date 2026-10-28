import unittest
from datetime import date

import colors
import reports
from sample_data import demo_tracker
from tracker import ExpenseTracker

TODAY = date(2026, 10, 28)


class ReportTests(unittest.TestCase):
    def setUp(self):
        # Plain text is easier to check than text full of colour codes.
        colors.ENABLED = False
        self.tracker = demo_tracker()

    def test_helpers(self):
        self.assertEqual(reports.money(18940), "₹18,940.00")
        self.assertEqual(reports.whole(676.43), "₹676")
        self.assertEqual(reports.percent(1, 4), "25%")
        self.assertEqual(reports.percent(5, 0), "0%")
        self.assertEqual(reports.month_name("2026-10"), "October 2026")
        self.assertEqual(reports.shorten("Metro card recharge!!", 20), "Metro card recharge…")

    def test_days_counted(self):
        self.assertEqual(reports.days_counted("2026-10", TODAY), 28)  # current month: so far
        self.assertEqual(reports.days_counted("2026-09", TODAY), 30)  # past month: all days

    def test_budget_bar_never_overflows(self):
        self.assertEqual(reports.budget_bar(50, 100, width=10), "[█████░░░░░]")
        self.assertEqual(reports.budget_bar(500, 100, width=10), "[██████████]")

    def test_summary_matches_demo_numbers(self):
        text = reports.summary(self.tracker, "2026-10", TODAY)
        self.assertIn("OCTOBER 2026", text)
        self.assertIn("₹18,940.00", text)
        self.assertIn("76% used", text)
        self.assertIn("₹6,060 left", text)
        self.assertIn("Biggest expense: Rent share, ₹8,000", text)
        self.assertIn("Daily average: ₹676", text)
        self.assertIn("within budget", text)
        bills_line = next(line for line in text.splitlines() if line.strip().startswith("bills"))
        self.assertIn("50%", bills_line)

    def test_summary_over_budget(self):
        self.tracker.budget = 10000
        text = reports.summary(self.tracker, "2026-10", TODAY)
        self.assertIn("Over budget by ₹8,940", text)

    def test_summary_for_empty_month(self):
        text = reports.summary(ExpenseTracker(), "2026-10", TODAY)
        self.assertIn("No expenses in October 2026", text)

    def test_table_has_total_row(self):
        table = reports.expense_table(list(self.tracker))
        self.assertTrue(table.splitlines()[-1].endswith("Total  ₹18,940.00"))
        widths = {len(line) for line in table.splitlines()}
        self.assertEqual(len(widths), 1, "every row should be the same width")

    def test_menu_shows_active_month(self):
        text = reports.menu(self.tracker, TODAY)
        self.assertIn("October 2026", text)
        self.assertIn("13 expenses", text)


if __name__ == "__main__":
    unittest.main()
