import pandas as pd

from src.preprocessing.pipeline import (
    fit_scaler,
    smote_train_only,
    stratified_split,
)


def test_resampling_only_touches_train():
    X_train = pd.DataFrame(
        {
            "feature_a": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "feature_b": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        }
    )
    y_train = pd.Series([0] * 8 + [1] * 2)

    X_resampled, y_resampled = smote_train_only(
        X_train, y_train, floor=6, seed=42
    )

    assert len(X_resampled) > len(X_train)
    assert len(y_resampled) == len(X_resampled)


def test_scaler_is_fitted_on_training_records_only():
    X_train = pd.DataFrame(
        {
            "feature_a": [1.0, 2.0, 3.0, 4.0],
            "feature_b": [10.0, 20.0, 30.0, 40.0],
        }
    )

    scaler = fit_scaler(X_train)

    assert scaler.n_samples_seen_ == len(X_train)
    assert list(scaler.feature_names_in_) == list(X_train.columns)
