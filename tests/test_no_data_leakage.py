
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal

from src.preprocessing.pipeline import smote_train_only


def test_resampling_only_touches_train():
    X_train = pd.DataFrame({
        "feature_a": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "feature_b": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    })
    y_train = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 1, 1])

    X_test = pd.DataFrame({
        "feature_a": [100, 200],
        "feature_b": [1000, 2000],
    }, index=[100, 101])
    y_test = pd.Series([0, 1], index=[100, 101])

    original_X_test = X_test.copy(deep=True)
    original_y_test = y_test.copy(deep=True)

    X_resampled, y_resampled = smote_train_only(
        X_train,
        y_train,
        floor=6,
        seed=42,
    )

    assert len(X_resampled) > len(X_train)
    assert len(y_resampled) == len(X_resampled)

    assert_frame_equal(X_test, original_X_test)
    assert_series_equal(y_test, original_y_test)

    assert X_test.index.tolist() == [100, 101]
    assert y_test.index.tolist() == [100, 101]
