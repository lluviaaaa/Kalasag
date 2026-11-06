
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]


def load_schema(path=None):
    path = Path(path) if path else ROOT / "data" / "schema" / "feature_schema.json"
    return json.loads(path.read_text(encoding="utf-8"))


def load_scaler(path=None):
    return joblib.load(path or ROOT / "models" / "scaler.pkl")


def load_label_encoder(path=None):
    return joblib.load(path or ROOT / "models" / "label_encoder.pkl")


def load_imputer(path=None):
    path = Path(path) if path else ROOT / "models" / "imputer.pkl"
    return joblib.load(path) if path.exists() else None


def prepare_live_features(raw, schema, scaler, imputer=None):
    names = [feature["name"] for feature in schema["features"]]

    missing = [name for name in names if name not in raw.columns]

    if missing:
        raise ValueError(f"Missing feature columns: {missing}")

    X = raw[names].astype("float64")
    X = X.replace([np.inf, -np.inf], np.nan)

    if imputer is not None:
        X = pd.DataFrame(
            imputer.transform(X),
            columns=names,
            index=X.index
        )

    if X.isna().any().any():
        raise ValueError(
            "Live features contain missing or infinite values; "
            "no fitted imputer is available."
        )

    return pd.DataFrame(
        scaler.transform(X),
        columns=names,
        index=X.index
    )
