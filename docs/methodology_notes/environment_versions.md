# Kalasag — Python Environment Versions

## 1. Local Preprocessing Environment

**Operating System:** Windows
**Python Version:** 3.13.3
**Environment:** Project-local `.venv`

| Package | Version |
|---|---|
| pandas | 3.1.0 |
| numpy | 2.5.4 |
| scikit-learn | 1.9.1 |
| imbalanced-learn | 0.14.2 |
| XGBoost | 3.4.1 |
| LightGBM | 4.7.0 |
| joblib | 1.6.0 |
| PyArrow | 26.0.0 |

These versions were verified using `python -m pip show`.

## 2. Model Development Environment

The Model Development Lead reported the following environment:

| Package | Version |
|---|---|
| Python | 3.13.16 |
| scikit-learn | 1.6.1 |
| imbalanced-learn | 0.14.2 |
| XGBoost | 3.4.1 |
| joblib | 1.6.0 |

The final XGBoost model was trained using the prepared scaled Parquet datasets.

## 3. Scaler Compatibility

The saved `models/scaler.pkl` was created using scikit-learn 1.9.1.

Loading this artifact under scikit-learn 1.6.1 produced an `InconsistentVersionWarning`.

To investigate compatibility, the saved `models/scaler.json` was compared against `models/scaler.pkl` using 100 synthetic input records.

**Verification results:**
- Feature count: 46
- Scaler parameter comparison: Passed
- Maximum transformation difference: 0.0
- Numerical equivalence: Passed

The JSON contains the feature names, means, and scaling factors required to reproduce the StandardScaler transformation.

JSON-based scaling is recommended for dashboard integration, subject to end-to-end inference validation.

## 4. Reproducibility Notes

- Preserve the exact order of all 46 input features.
- Do not refit the scaler using validation, test, or live inference data.
- Apply the same preprocessing rules used during training.
- Keep the final model and its training environment documented.
- Validate predictions after dashboard integration.

## 5. Environment Verification

The local Python environment was verified successfully.

Google Colab and Kaggle also passed basic smoke tests covering Python execution, library imports, StandardScaler, SMOTE, and XGBoost training.

Cloud environments were not verified against the exact pinned local dependency versions.