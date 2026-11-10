import numpy as np
import pandas as pd
import pytest
from sklearn.preprocessing import StandardScaler

from src.live.convert import (COLUMN_MAP, FLAG_FEATURES, TIME_FEATURES,
                              apply_live_rules, to_scaled, tool_to_training_frame)


def fake_tool_output(n=3):
    rng = np.random.default_rng(1)
    raw = pd.DataFrame(rng.uniform(1, 10, size=(n, len(COLUMN_MAP))), columns=list(COLUMN_MAP))
    raw['src_ip'] = '10.10.10.3'            # extra column, like the real tool output
    return raw


def test_46_features_15_time_columns_3_flags():
    assert len(COLUMN_MAP) == 46 == len(set(COLUMN_MAP.values()))
    assert len(TIME_FEATURES) == 15 and len(FLAG_FEATURES) == 3
    assert set(TIME_FEATURES + FLAG_FEATURES) <= set(COLUMN_MAP.values())


def test_time_columns_x_1000000_and_rates_unchanged():
    x = tool_to_training_frame(fake_tool_output())
    y = apply_live_rules(x)
    assert np.allclose(y['Flow Duration'], x['Flow Duration'] * 1e6)
    assert np.allclose(y['Bwd IAT Min'], x['Bwd IAT Min'] * 1e6)
    assert np.allclose(y['Flow Packets/s'], x['Flow Packets/s'])


def test_flag_counts_become_0_or_1():
    x = tool_to_training_frame(fake_tool_output())
    x['FIN Flag Count'] = [0, 3, 876]
    assert apply_live_rules(x)['FIN Flag Count'].tolist() == [0.0, 1.0, 1.0]


def test_infinity_makes_the_row_unusable():
    raw = fake_tool_output()
    scaler = StandardScaler().fit(apply_live_rules(tool_to_training_frame(raw)))
    raw.loc[1, 'flow_byts_s'] = np.inf
    scaled, ok = to_scaled(raw, scaler)
    assert ok.tolist() == [True, False, True] and len(scaled) == 2


def test_missing_tool_column_raises():
    with pytest.raises(ValueError):
        tool_to_training_frame(fake_tool_output().drop(columns=['dst_port']))
