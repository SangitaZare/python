import csv
import tempfile
import unittest
from pathlib import Path

import storage
from errors import StorageError
from sample_data import demo_tracker


class StorageTests(unittest.TestCase):
    def setUp(self):
        # A temporary folder that is deleted after each test, so tests never
        # touch your real data/expenses.json.
        self.temp = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_save_then_load_gives_same_data(self):
        original = demo_tracker()
        original.budget = 30000
        path = self.folder / "expenses.json"
        storage.save(original, path)
        loaded = storage.load(path)
        self.assertEqual(list(loaded), list(original))
        self.assertEqual(loaded.budget, 30000)
        self.assertFalse(path.with_suffix(".tmp").exists())

    def test_missing_file_means_empty_tracker(self):
        tracker = storage.load(self.folder / "nothing-here.json")
        self.assertEqual(len(tracker), 0)

    def test_corrupt_file_raises_storage_error(self):
        path = self.folder / "broken.json"
        path.write_text("{ this is not json", encoding="utf-8")
        with self.assertRaises(StorageError):
            storage.load(path)

    def test_invalid_expense_in_file_raises_storage_error(self):
        path = self.folder / "bad.json"
        path.write_text(
            '{"expenses": [{"id": 1, "date": "2026-10-01", "category": "snacks",'
            ' "description": "x", "amount": 5}]}',
            encoding="utf-8",
        )
        with self.assertRaises(StorageError):
            storage.load(path)

    def test_export_csv(self):
        path = self.folder / "out.csv"
        count = storage.export_csv(list(demo_tracker()), path)
        self.assertEqual(count, 13)
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(list(rows[0]), storage.CSV_FIELDS)
        self.assertEqual(rows[0]["description"], "Rent share")
        self.assertEqual(rows[0]["date"], "2026-10-01")


if __name__ == "__main__":
    unittest.main()
