import json
from pathlib import Path

import joblib

from src.live.convert import to_scaled

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


def convert_live_features(raw, scaler):
    """Convert CICFlowMeter output into scaled model features."""
    return to_scaled(raw, scaler)
