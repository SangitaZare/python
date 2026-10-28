"""Predict bike rentals for one hour from the command line.

    python 16_machine_learning/predict.py --hour 8 --day Tuesday --temp 22 --weather Clear
    python 16_machine_learning/predict.py --hour 14 --day Saturday --temp 26
    python 16_machine_learning/predict.py --help

The first run trains the model (a few seconds) if models/bike_demand.joblib
doesn't exist yet.

Security note: joblib/pickle files can run code when loaded. Only load model
files you created yourself or fully trust, never ones downloaded from strangers.
"""
import argparse
import sys

import joblib
import pandas as pd

from features import SEASONS, WEATHER, WEEKDAYS
from train import MODEL_FILE, train_and_save

SEASON_OF_MONTH = {12: "Winter", 1: "Winter", 2: "Winter", 3: "Spring", 4: "Spring", 5: "Spring",
                   6: "Summer", 7: "Summer", 8: "Summer", 9: "Fall", 10: "Fall", 11: "Fall"}


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Predict bike rentals for one hour in Washington DC.")
    parser.add_argument("--hour", type=int, required=True, choices=range(24), metavar="0-23")
    parser.add_argument("--day", required=True, choices=WEEKDAYS, help="day of the week")
    parser.add_argument("--temp", type=float, required=True, help="temperature in °C")
    parser.add_argument("--weather", default="Clear", choices=WEATHER)
    parser.add_argument("--month", type=int, default=6, choices=range(1, 13), metavar="1-12")
    parser.add_argument("--humidity", type=float, default=60.0, help="humidity in %%")
    parser.add_argument("--wind", type=float, default=12.0, help="wind speed")
    parser.add_argument("--holiday", action="store_true", help="the day is a public holiday")
    return parser.parse_args(argv)


def predict(args: argparse.Namespace) -> float:
    if not MODEL_FILE.exists():
        print("No saved model yet, training one first...", file=sys.stderr)
        train_and_save()
    saved = joblib.load(MODEL_FILE)

    workingday = int(args.day not in ("Saturday", "Sunday") and not args.holiday)
    row = pd.DataFrame([{
        "weekday": args.day, "season": SEASON_OF_MONTH[args.month], "weather": args.weather,
        "hour": args.hour, "month": args.month, "year": 2012, "workingday": workingday,
        "holiday": int(args.holiday), "temp_c": args.temp, "humidity": args.humidity, "windspeed": args.wind,
    }])
    assert row["season"].iloc[0] in SEASONS
    return max(0.0, float(saved["model"].predict(row[saved["features"]])[0]))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # so "°C" prints correctly on Windows too
    args = parse_args()
    rides = predict(args)
    kind = "holiday" if args.holiday else ("workday" if args.day not in ("Saturday", "Sunday") else "weekend")
    print(f"{args.day} ({kind}) {args.hour}:00, {args.temp:g}°C, {args.weather}: about {rides:.0f} rides")
