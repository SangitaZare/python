"""Train the bike demand model on ALL the data and save it.

    python 16_machine_learning/train.py

The notebook evaluates the model honestly (train on the past, test on the
future). Once we trust the method, the production model is retrained on
every row we have, because more data, and the most recent data, gives
better forecasts.
"""
from pathlib import Path

import joblib
import pandas as pd

from features import FEATURES, TARGET, build_model

HERE = Path(__file__).parent
DATA = HERE.parent / "15_eda_project" / "data" / "bike_hourly_clean.csv"
MODEL_FILE = HERE / "models" / "bike_demand.joblib"


def train_and_save() -> Path:
    df = pd.read_csv(DATA)
    humidity_median = df["humidity"].median()
    X = df[FEATURES].fillna({"humidity": humidity_median})
    model = build_model().fit(X, df[TARGET])

    MODEL_FILE.parent.mkdir(exist_ok=True)
    joblib.dump({"model": model, "features": FEATURES, "humidity_median": humidity_median}, MODEL_FILE)
    return MODEL_FILE


if __name__ == "__main__":
    path = train_and_save()
    print(f"Trained on all data and saved to {path.relative_to(HERE.parent)}")
