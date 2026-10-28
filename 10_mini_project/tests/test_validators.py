import unittest
from datetime import date

from errors import ExpenseError, InvalidAmountError, InvalidCategoryError, InvalidDateError
from validators import parse_amount, parse_category, parse_date, parse_id

TODAY = date(2026, 10, 28)


class ParseAmountTests(unittest.TestCase):
    def test_accepts_plain_and_formatted_numbers(self):
        self.assertEqual(parse_amount("250"), 250.0)
        self.assertEqual(parse_amount(" 99.5 "), 99.5)
        self.assertEqual(parse_amount("1,250.50"), 1250.5)
        self.assertEqual(parse_amount("₹450"), 450.0)

    def test_rounds_to_two_decimals(self):
        self.assertEqual(parse_amount("10.456"), 10.46)

    def test_rejects_bad_amounts(self):
        for text in ("abc", "", "0", "-5", "nan", "inf", "99999999999"):
            with self.subTest(text=text):
                with self.assertRaises(InvalidAmountError):
                    parse_amount(text)


class ParseCategoryTests(unittest.TestCase):
    def test_accepts_name_in_any_case(self):
        self.assertEqual(parse_category("Food"), "food")
        self.assertEqual(parse_category("  BILLS "), "bills")

    def test_accepts_number_from_list(self):
        self.assertEqual(parse_category("1"), "food")
        self.assertEqual(parse_category("2"), "transport")

    def test_rejects_unknown(self):
        for text in ("snacks", "0", "8", ""):
            with self.subTest(text=text):
                with self.assertRaises(InvalidCategoryError):
                    parse_category(text)


class ParseDateTests(unittest.TestCase):
    def test_empty_means_today(self):
        self.assertEqual(parse_date("", TODAY), TODAY)

    def test_parses_dd_mm_yyyy(self):
        self.assertEqual(parse_date("01-10-2026", TODAY), date(2026, 10, 1))

    def test_rejects_invalid_and_future_dates(self):
        for text in ("31-02-2026", "2026-10-01", "yesterday", "29-10-2026"):
            with self.subTest(text=text):
                with self.assertRaises(InvalidDateError):
                    parse_date(text, TODAY)


class ParseIdTests(unittest.TestCase):
    def test_parses_digits(self):
        self.assertEqual(parse_id(" 7 "), 7)

    def test_rejects_non_digits(self):
        for text in ("abc", "-1", "1.5", ""):
            with self.subTest(text=text):
                with self.assertRaises(ExpenseError):
                    parse_id(text)


if __name__ == "__main__":
    unittest.main()
