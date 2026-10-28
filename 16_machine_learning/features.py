"""Feature definitions shared by the notebook and predict.py.

Why a module? The saved model contains the preprocessing steps, and
loading it needs the same functions it was built with. Keeping them in one
importable file means training and prediction can never drift apart.
"""
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import FunctionTransformer, OrdinalEncoder

CATEGORICAL = ["weekday", "season", "weather"]
NUMERIC = ["hour", "month", "year", "workingday", "holiday", "temp_c", "humidity", "windspeed"]
FEATURES = CATEGORICAL + NUMERIC
TARGET = "rides"

# The values the model was trained on, for checking user input.
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
SEASONS = ["Winter", "Spring", "Summer", "Fall"]
WEATHER = ["Clear", "Mist / cloudy", "Light rain / snow", "Heavy rain / snow"]


def as_numbers(X):
    """Make every numeric column a float.

    The CSV stores workingday and holiday as True/False. Mixed with numbers,
    they turn the whole feature table into a generic 'object' array, and the
    model then fails on new rows that use plain 0/1. Converting inside the
    pipeline means training and prediction always see the same types.
    """
    return X.astype(float)


def tree_preprocessing() -> ColumnTransformer:
    """Categories -> number codes; numbers -> floats (trees need no scaling)."""
    return ColumnTransformer([
        ("categories", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=np.nan), CATEGORICAL),
        ("numbers", FunctionTransformer(as_numbers, feature_names_out="one-to-one"), NUMERIC),
    ])


def is_category_mask(extra_numeric: int = 0) -> list[bool]:
    """Tells gradient boosting which columns (after preprocessing) are categories."""
    return [True] * len(CATEGORICAL) + [False] * (len(NUMERIC) + extra_numeric)


def build_model() -> Pipeline:
    """The chosen model: preprocessing + gradient boosting, ready to fit."""
    return make_pipeline(
        tree_preprocessing(),
        HistGradientBoostingRegressor(categorical_features=is_category_mask(), max_iter=400,
                                      learning_rate=0.08, random_state=0),
    )
