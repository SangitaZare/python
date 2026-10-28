"""Tests for the Streamlit app, using Streamlit's built-in AppTest.

AppTest runs web_app.py without a browser and lets us click buttons and
fill inputs from code. These tests are skipped if Streamlit isn't installed,
so the rest of the suite still runs with plain Python.
"""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import storage

HAS_STREAMLIT = importlib.util.find_spec("streamlit") is not None
APP = str(Path(__file__).parent.parent / "web_app.py")


@unittest.skipUnless(HAS_STREAMLIT, "streamlit is not installed")
class WebAppTests(unittest.TestCase):
    def setUp(self):
        from streamlit.testing.v1 import AppTest

        # Point both data files at a temporary folder so tests never touch real data.
        self.temp = tempfile.TemporaryDirectory()
        folder = Path(self.temp.name)
        self.patches = [
            mock.patch.object(storage, "DEMO_FILE", folder / "demo.json"),
            mock.patch.object(storage, "DEFAULT_FILE", folder / "expenses.json"),
        ]
        for p in self.patches:
            p.start()
        self.app = AppTest.from_file(APP, default_timeout=30).run()

    def tearDown(self):
        for p in self.patches:
            p.stop()
        self.temp.cleanup()

    def test_demo_loads_without_errors(self):
        self.assertFalse(self.app.exception)
        self.assertEqual(self.app.title[0].value, "October 2026")
        spent = self.app.metric[0]
        self.assertEqual(spent.value, "₹18,940")

    def test_add_expense_saves_it(self):
        self.app.sidebar.number_input[1].set_value(250)
        self.app.sidebar.text_input[0].set_value("Chai")
        self.app.sidebar.button[0].click().run()
        self.assertFalse(self.app.exception)
        self.assertIn("Added #14", self.app.success[0].value)
        self.assertEqual(len(storage.load(storage.DEMO_FILE)), 14)

    def test_zero_amount_shows_error(self):
        self.app.sidebar.button[0].click().run()  # amount is still 0
        self.assertIn("more than 0", self.app.error[0].value)
        self.assertEqual(len(storage.load(storage.DEMO_FILE)), 13)

    def test_my_expenses_starts_empty(self):
        self.app.sidebar.radio[0].set_value("My expenses").run()
        self.assertIn("No expenses yet", self.app.info[0].value)


if __name__ == "__main__":
    unittest.main()
