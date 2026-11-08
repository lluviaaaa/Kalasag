
from collections import Counter

import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

SEED = 42


def stratified_split(X, y, seed=SEED):
    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=0.30,
        stratify=y,
        random_state=seed
    )

    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.50,
        stratify=y_temp,
        random_state=seed
    )

    return X_train, X_val, X_test, y_train, y_val, y_test


def fit_scaler(X_train):
    return StandardScaler().fit(X_train)


def apply_scaler(scaler, X):
    return pd.DataFrame(
        scaler.transform(X),
        columns=X.columns,
        index=X.index
    )


def smote_train_only(X_train_scaled, y_train, floor=10000, seed=SEED):
    counts = Counter(y_train)

    strategy = {
        cls: floor
        for cls, n in counts.items()
        if n < floor
    }

    if not strategy:
        return X_train_scaled, y_train

    k = min(5, min(counts[c] for c in strategy) - 1)

    smote = SMOTE(
        sampling_strategy=strategy,
        k_neighbors=k,
        random_state=seed
    )

    return smote.fit_resample(X_train_scaled, y_train)


def remove_invalid_negative_rows(df):
    allowed_negative_columns = {
        "Init_Win_bytes_backward",
        "Init_Win_bytes_forward",
    }

    numeric = df.select_dtypes(include="number")
    check_columns = [
        col for col in numeric.columns
        if col not in allowed_negative_columns
    ]

    invalid_mask = (numeric[check_columns] < 0).any(axis=1)

    cleaned = df.loc[~invalid_mask].copy()

    return cleaned, int(invalid_mask.sum())
