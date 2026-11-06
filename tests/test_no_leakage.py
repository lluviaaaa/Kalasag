
import numpy as np
import pandas as pd

from src.preprocessing.pipeline import (
    stratified_split,
    fit_scaler,
    apply_scaler,
    smote_train_only,
)


def make_dataset():
    rng = np.random.default_rng(42)

    X = pd.DataFrame(
        rng.normal(size=(200, 3)),
        columns=["feature_a", "feature_b", "feature_c"]
    )

    y = pd.Series([0] * 160 + [1] * 40)

    return X, y


def test_split_has_no_overlap():
    X, y = make_dataset()

    X_train, X_val, X_test, _, _, _ = stratified_split(X, y)

    assert set(X_train.index).isdisjoint(X_val.index)
    assert set(X_train.index).isdisjoint(X_test.index)
    assert set(X_val.index).isdisjoint(X_test.index)


def test_split_preserves_class_distribution():
    X, y = make_dataset()

    _, _, _, y_train, y_val, y_test = stratified_split(X, y)

    for subset in [y_train, y_val, y_test]:
        proportion = (subset == 1).mean()
        assert abs(proportion - 0.20) < 0.05


def test_scaler_uses_training_data_only():
    X_train = pd.DataFrame({"feature": [1.0, 2.0, 3.0]})
    X_test = pd.DataFrame({"feature": [100.0, 200.0]})

    scaler = fit_scaler(X_train)

    original_mean = scaler.mean_.copy()

    transformed = apply_scaler(scaler, X_test)

    assert np.array_equal(scaler.mean_, original_mean)
    assert transformed["feature"].mean() > 10


def test_smote_only_resamples_supplied_training_data():
    X, y = make_dataset()

    X_train, X_val, X_test, y_train, y_val, y_test = stratified_split(X, y)

    scaler = fit_scaler(X_train)

    X_train_s = apply_scaler(scaler, X_train)

    original_val_count = len(y_val)
    original_test_count = len(y_test)

    X_res, y_res = smote_train_only(
        X_train_s,
        y_train,
        floor=100,
        seed=42
    )

    assert len(X_res) > len(X_train_s)
    assert len(y_res) == len(X_res)
    assert len(y_val) == original_val_count
    assert len(y_test) == original_test_count
    assert (pd.Series(y_res) == 1).sum() == 100
