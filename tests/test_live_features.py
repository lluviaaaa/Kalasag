
import numpy as np
import pandas as pd
import pytest

from sklearn.preprocessing import StandardScaler
from src.preprocessing.artifacts import prepare_live_features


def test_live_features_follow_schema_order():
    schema = {
        "features": [
            {"name": "feature_a"},
            {"name": "feature_b"},
        ]
    }

    train = pd.DataFrame({
        "feature_a": [1.0, 2.0, 3.0],
        "feature_b": [10.0, 20.0, 30.0],
    })

    scaler = StandardScaler().fit(train)

    raw = pd.DataFrame({
        "feature_b": [20.0],
        "feature_a": [2.0],
    })

    result = prepare_live_features(raw, schema, scaler)

    expected = scaler.transform(
        pd.DataFrame({
            "feature_a": [2.0],
            "feature_b": [20.0],
        })
    )

    assert list(result.columns) == ["feature_a", "feature_b"]
    np.testing.assert_allclose(result.to_numpy(), expected)


def test_live_features_reject_missing_columns():
    schema = {
        "features": [
            {"name": "feature_a"},
            {"name": "feature_b"},
        ]
    }

    train = pd.DataFrame({
        "feature_a": [1.0, 2.0],
        "feature_b": [3.0, 4.0],
    })

    scaler = StandardScaler().fit(train)

    raw = pd.DataFrame({"feature_a": [1.5]})

    with pytest.raises(ValueError, match="Missing feature columns"):
        prepare_live_features(raw, schema, scaler)
