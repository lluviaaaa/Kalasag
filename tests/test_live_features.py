import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

from src.live.convert import (
    COLUMN_MAP,
    apply_live_rules,
    to_scaled,
    tool_to_training_frame,
)
from src.preprocessing.artifacts import convert_live_features


def fake_tool_output():
    rng = np.random.default_rng(1)
    raw = pd.DataFrame(
        rng.uniform(1, 10, size=(3, len(COLUMN_MAP))),
        columns=list(COLUMN_MAP),
    )
    raw["src_ip"] = "10.10.10.3"
    return raw


def test_convert_live_features_uses_live_converter():
    raw = fake_tool_output()

    training_features = apply_live_rules(
        tool_to_training_frame(raw)
    )

    scaler = StandardScaler().fit(training_features)

    result, usable = convert_live_features(raw, scaler)
    expected, expected_usable = to_scaled(raw, scaler)

    assert list(result.columns) == list(scaler.feature_names_in_)
    assert usable.tolist() == expected_usable.tolist()
    np.testing.assert_allclose(result.to_numpy(), expected.to_numpy())
