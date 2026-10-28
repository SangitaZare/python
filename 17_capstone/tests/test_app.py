"""Click through the Streamlit app without a browser, using AppTest."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import bank_model as bm

HAS_STREAMLIT = importlib.util.find_spec("streamlit") is not None
APP = str(Path(__file__).parent.parent / "app.py")


@unittest.skipUnless(HAS_STREAMLIT, "streamlit is not installed")
class AppTests(unittest.TestCase):
    def setUp(self):
        from streamlit.testing.v1 import AppTest

        # Train into a temporary folder so the tests never touch models/.
        self.temp = tempfile.TemporaryDirectory()
        self.patch = mock.patch.object(bm, "MODEL_FILE", Path(self.temp.name) / "model.joblib")
        self.patch.start()
        self.app = AppTest.from_file(APP, default_timeout=120).run()

    def tearDown(self):
        self.patch.stop()
        self.temp.cleanup()

    def test_loads_with_a_recommendation(self):
        self.assertFalse(self.app.exception)
        self.assertEqual(self.app.title[0].value, "Who should we call?")
        self.assertIn("Recommended: call the top", self.app.sidebar.success[0].value)
        self.assertEqual(len(self.app.metric), 4)

    def test_calling_everyone_matches_the_whole_list(self):
        self.app.sidebar.slider[0].set_value(100).run()
        self.assertFalse(self.app.exception)
        self.assertEqual(self.app.metric[0].value, f"{len(bm.split_by_time(bm.load_data())[1]):,}")

    def test_higher_call_cost_recommends_fewer_calls(self):
        cheap = self.app.sidebar.slider[0].value
        self.app.sidebar.number_input[0].set_value(20.0).run()
        self.assertLess(self.app.sidebar.slider[0].value, cheap)

    def test_previous_campaign_answer_changes_the_score_sensibly(self):
        def score(previous_campaign_option: int) -> float:
            # Find widgets by key, not position: columns change the order of elements.
            self.app.selectbox(key="poutcome").select_index(previous_campaign_option)   # 0 = not contacted, 2 = said yes
            self.app.tabs[2].button[0].click().run()
            self.assertFalse(self.app.exception)
            return float(self.app.tabs[2].metric[0].value.rstrip("%"))

        new_customer, said_no, said_yes = score(0), score(1), score(2)
        # The same order as in the data: said yes (65%) > never contacted (9%) ≈ said no (14%), and
        # a past "no" should not look better than a new customer (this caught an app bug once).
        self.assertGreater(said_yes, new_customer)
        self.assertGreater(new_customer, said_no)
        self.assertIn("of the call list", self.app.tabs[2].markdown[-1].value)


if __name__ == "__main__":
    unittest.main()
