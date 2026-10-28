"""Everything the notebook, the app and the tests share: data, features, model.

Keeping this in one module means the analysis and the app can never disagree
about how a feature is built or how the model is trained.
"""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

HERE = Path(__file__).parent
DATA_FILE = HERE / "data" / "bank-additional-full.csv"
MODEL_FILE = HERE / "models" / "campaign_model.joblib"

TEST_SHARE = 0.2  # the most recent 20% of calls are held back as "the future"

CATEGORICAL = ["job", "marital", "education", "default", "housing", "loan",
               "contact", "month", "day_of_week", "poutcome", "age_band"]
NUMERIC = ["previous", "contacted_before",
           "emp.var.rate", "cons.price.idx", "cons.conf.idx", "euribor3m", "nr.employed"]
FEATURES = CATEGORICAL + NUMERIC

# Known only AFTER the call, so using them would be leakage:
#   duration - call length; a 0-second call is always "no"
#   campaign - contacts in this campaign, *including the last one*
LEAKY = ["duration", "campaign"]

AGE_BINS = [0, 25, 35, 45, 55, 65, 120]
AGE_LABELS = ["≤25", "26–35", "36–45", "46–55", "56–65", "65+"]


def load_data(path: Path = DATA_FILE) -> pd.DataFrame:
    """Read the raw file (semicolon-separated), drop exact duplicates, add features."""
    df = pd.read_csv(path, sep=";").drop_duplicates().reset_index(drop=True)
    df["subscribed"] = (df["y"] == "yes").astype(int)
    return add_features(df)


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # pdays = 999 is a placeholder meaning "never contacted before", not a real
    # number of days. Left as a number, 999 would look like "a very long time ago".
    df["contacted_before"] = (df["pdays"] != 999).astype(int)
    # Young and older customers both say yes more often (a U-shape), which a
    # single linear "age" weight can't express. Bands let the model learn it.
    df["age_band"] = pd.cut(df["age"], AGE_BINS, labels=AGE_LABELS).astype(str)
    return df


def split_by_time(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """The file is ordered by date, so the last rows are the most recent calls."""
    cut = int(len(df) * (1 - TEST_SHARE))
    return df.iloc[:cut], df.iloc[cut:]


def build_model() -> Pipeline:
    """Logistic regression: it generalised best to the future (see the notebook)."""
    return make_pipeline(
        ColumnTransformer([
            ("categories", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
            ("numbers", StandardScaler(), NUMERIC),
        ]),
        LogisticRegression(max_iter=3000),
    )


def train_and_save(path: Path | None = None) -> Pipeline:
    """Train on the past (first 80%) so the app can show an honest backtest on the rest."""
    path = path or MODEL_FILE   # looked up at call time, so tests can redirect it
    train, _ = split_by_time(load_data())
    model = build_model().fit(train[FEATURES], train["subscribed"])
    path.parent.mkdir(exist_ok=True)
    joblib.dump(model, path)
    return model


def load_or_train(path: Path | None = None) -> Pipeline:
    path = path or MODEL_FILE
    # Only load model files you created yourself: pickle files can run code.
    return joblib.load(path) if path.exists() else train_and_save(path)


def gains_table(probabilities, outcomes, value_per_sale: float, cost_per_call: float) -> pd.DataFrame:
    """Call customers from most to least likely. What happens after each call?

    Returns one row per call: how many customers called so far, sales so far,
    what random calling would have achieved, and the profit.
    """
    order = np.argsort(-np.asarray(probabilities), kind="stable")
    hits = np.asarray(outcomes)[order]
    calls = np.arange(1, len(hits) + 1)
    sales = np.cumsum(hits)
    table = pd.DataFrame({
        "calls": calls,
        "share_called": calls / len(hits),
        "sales": sales,
        "random_sales": calls * hits.mean(),
        "probability": np.asarray(probabilities)[order],
    })
    table["profit"] = value_per_sale * table["sales"] - cost_per_call * table["calls"]
    table["random_profit"] = value_per_sale * table["random_sales"] - cost_per_call * table["calls"]
    return table
