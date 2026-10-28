import unittest

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

import bank_model as bm


class FeatureTests(unittest.TestCase):
    def test_contacted_before_replaces_the_999_placeholder(self):
        df = bm.add_features(pd.DataFrame({"pdays": [999, 3, 0], "age": [30, 30, 30]}))
        self.assertEqual(df["contacted_before"].tolist(), [0, 1, 1])

    def test_age_bands_cover_the_edges(self):
        df = bm.add_features(pd.DataFrame({"pdays": [999] * 5, "age": [18, 25, 26, 65, 98]}))
        self.assertEqual(df["age_band"].tolist(), ["≤25", "≤25", "26–35", "56–65", "65+"])

    def test_leaky_columns_are_not_features(self):
        for column in bm.LEAKY:
            self.assertNotIn(column, bm.FEATURES)


class DataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = bm.load_data()

    def test_duplicates_removed_and_target_is_binary(self):
        self.assertEqual(self.df.duplicated(subset=[c for c in self.df.columns]).sum(), 0)
        self.assertEqual(set(self.df["subscribed"].unique()), {0, 1})

    def test_time_split_keeps_order_and_sizes(self):
        train, test = bm.split_by_time(self.df)
        self.assertEqual(len(train) + len(test), len(self.df))
        self.assertLess(train.index.max(), test.index.min())   # the test set is strictly "later"
        self.assertAlmostEqual(len(test) / len(self.df), bm.TEST_SHARE, places=2)

    def test_model_ranks_future_customers_better_than_chance(self):
        train, test = bm.split_by_time(self.df)
        model = bm.build_model().fit(train[bm.FEATURES], train["subscribed"])
        auc = roc_auc_score(test["subscribed"], model.predict_proba(test[bm.FEATURES])[:, 1])
        self.assertGreater(auc, 0.70)


class GainsTableTests(unittest.TestCase):
    def test_calls_best_customers_first(self):
        table = bm.gains_table([0.9, 0.1, 0.8, 0.2], [1, 0, 1, 0], value_per_sale=10, cost_per_call=1)
        self.assertEqual(table["sales"].tolist(), [1, 2, 2, 2])
        self.assertEqual(table["profit"].tolist(), [9, 18, 17, 16])
        self.assertEqual(table["random_sales"].tolist(), [0.5, 1.0, 1.5, 2.0])

    def test_best_profit_stops_before_unprofitable_calls(self):
        table = bm.gains_table([0.9, 0.1, 0.8, 0.2], [1, 0, 1, 0], value_per_sale=10, cost_per_call=1)
        self.assertEqual(int(table.loc[table["profit"].idxmax(), "calls"]), 2)

    def test_random_scores_give_no_lift_on_average(self):
        rng = np.random.default_rng(0)
        outcomes = rng.random(20_000) < 0.3
        table = bm.gains_table(rng.random(20_000), outcomes, 10, 1)
        half = table.iloc[9_999]
        self.assertAlmostEqual(half["sales"] / half["random_sales"], 1.0, delta=0.05)


if __name__ == "__main__":
    unittest.main()
