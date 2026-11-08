# Kalasag — Data Preprocessing Handoff

**Prepared by:** Jaymie Aquino  
**Role:** Data & Preprocessing Lead  
**Recipient:** Pou — Model Training Lead  
**Date:** November 8, 2026  
**Pull Request:** https://github.com/lluviaaaa/Kalasag/pull/13

## 1. Dataset Availability

The regenerated datasets have been uploaded to Google Drive under:

`My Drive/kalasag/processed/`

| File | Rows | Columns |
|---|---:|---:|
| train_scaled.parquet | 1,762,376 | 47 |
| val_scaled.parquet | 377,652 | 47 |
| test_scaled.parquet | 377,653 | 47 |
| train_smote_floor10000.parquet | 1,783,111 | 47 |
| split_test_unscaled.parquet | 377,653 | 47 |

Additional uploaded artifacts:
- `scaler.pkl`
- `scaler.json`

Other required project artifacts:
- `models/label_encoder.pkl`
- `data/schema/feature_schema.json`

**Google Drive folder link:** (https://drive.google.com/drive/folders/1C_VmC5wgoaFSE1BbTOFeOiVTONUX9Ppl?usp=sharing)

Only regenerated files were uploaded. Old local backups were excluded.

## Preprocessing Environment

The following versions were used to generate the preprocessing artifacts:

- Python: 3.13.3
- scikit-learn: 1.9.1
- imbalanced-learn: 0.14.2
- joblib: 1.6.0

Use compatible versions when loading the saved scaler and label encoder.

## Live-Layer Preprocessing Rules

The live traffic monitoring system must apply these rules before scaling:

1. **Time Conversion**
   - Multiply Flow Duration and the 14 IAT features by 1,000,000.
   - This converts seconds into microseconds to match the training dataset.

2. **TCP Flag Conversion**
   - For FIN, PSH, and ACK Flag Count, convert any value greater than 0 to 1.
   - Keep zero values as 0.

3. **TCP Window Values**
   - Do not modify Init_Win_bytes_forward or Init_Win_bytes_backward.
   - A value of -1 is valid when no TCP packet was observed.

4. **Approximate Features**
   - UDP header lengths and min_seg_size_forward may differ from training values.
   - The live tool uses an approximate header length of 20, while training data may contain 20 or 32.

5. **Feature Consistency**
   - Use the exact 46 features in feature_schema.json.
   - Preserve their order before applying the saved scaler.

## 2. Dataset Cleaning Summary

| Processing stage | Records |
|---|---:|
| Original dataset | 2,520,751 |
| Duplicates removed | 161 |
| Records after deduplication | 2,520,590 |
| Invalid negative-value records removed | 2,909 |
| **Final cleaned records** | **2,517,681** |

Two TCP window features were excluded from negative-value filtering because they legitimately contain `-1` sentinel values:

- `Init_Win_bytes_forward`
- `Init_Win_bytes_backward`

### Per-Class Cleaning Results

| Attack Class | Before | Removed | After |
|---|---:|---:|---:|
| Bots | 1,948 | 0 | 1,948 |
| Brute Force | 9,150 | 6 | 9,144 |
| DDoS | 128,014 | 19 | 127,995 |
| DoS | 193,745 | 163 | 193,582 |
| Normal Traffic | 2,094,896 | 2,721 | 2,092,175 |
| Port Scanning | 90,694 | 0 | 90,694 |
| Web Attacks | 2,143 | 0 | 2,143 |
| **Total** | **2,520,590** | **2,909** | **2,517,681** |

All seven attack classes were preserved.

## 3. Feature Engineering

The final dataset contains 46 input features and one encoded target column (`label`).

The following six unsupported features were excluded:

- Active Mean
- Active Max
- Active Min
- Idle Mean
- Idle Max
- Idle Min

`Destination Port` remains included.

Feature ordering must match `data/schema/feature_schema.json`.

## 4. Data Splitting and Scaling

A stratified 70/15/15 train/validation/test split was applied before resampling.

| Dataset | Records |
|---|---:|
| Training | 1,762,376 |
| Validation | 377,652 |
| Testing | 377,653 |
| **Total** | **2,517,681** |

StandardScaler was fitted using training data only.

The same fitted scaler was applied to the training, validation, and test datasets.

## 5. SMOTE Results

SMOTE was applied exclusively to the training dataset, with a minimum target of 10,000 records per minority class.

**Final SMOTE dataset shape:** 1,783,111 rows × 47 columns.

| Label | Attack Class | After SMOTE |
|---|---|---:|
| 0 | Bots | 10,000 |
| 1 | Brute Force | 10,000 |
| 2 | DDoS | 89,596 |
| 3 | DoS | 135,507 |
| 4 | Normal Traffic | 1,464,522 |
| 5 | Port Scanning | 63,486 |
| 6 | Web Attacks | 10,000 |
| | **Total** | **1,783,111** |

The validation and test datasets were not resampled.

## Dataset Verification Script

Run the following code from the Kalasag project root with the processed files in their expected folders.

```python
import joblib
import pandas as pd

scaler = joblib.load("models/scaler.pkl")
train = pd.read_parquet("data/processed/train_scaled.parquet")

print("Dataset shape:", train.shape)
print("Class distribution:")
print(train["label"].value_counts().sort_index())

print(
    "Largest absolute feature mean:",
    train.drop(columns="label").mean().abs().max()
)

assert train.shape == (1762376, 47)
assert len(scaler.feature_names_in_) == 46

print("Verification passed!")
```

Expected results:
- Dataset shape: (1762376, 47)
- Seven attack classes
- Largest absolute feature mean approximately 0
- Verification passed!

The scaler must be loaded using a compatible scikit-learn version.

## 6. Validation Results

**Automated tests:** 10 passed, 2 skipped, 0 failed.

The train-only SMOTE leakage test executes and passes.

The remaining skipped tests concern:
- Live feature mapper/schema integration.
- Live pipeline/saved scaler integration.

Additional verification:
- All processed datasets contain 46 features and one label column.
- All seven attack classes are present.
- `scaler.pkl` and `scaler.json` have matching feature order, mean, and scale parameters.
- `split_test_unscaled.parquet` and `test_scaled.parquet` have matching row indices and label order.
- Transforming the unscaled test features using the saved scaler reproduces the scaled test values.

## 7. Label Encoding

| Encoded Label | Attack Type |
|---|---|
| 0 | Bots |
| 1 | Brute Force |
| 2 | DDoS |
| 3 | DoS |
| 4 | Normal Traffic |
| 5 | Port Scanning |
| 6 | Web Attacks |

Mapping verified against `models/label_encoder.pkl`.

## 8. Model Training Instructions for Pou

1. Use `train_smote_floor10000.parquet` for model training.
2. Use `val_scaled.parquet` for model comparison and hyperparameter selection.
3. Reserve `test_scaled.parquet` for final evaluation after model selection.
4. Preserve the exact 46-feature schema and feature order.
5. Use the verified label mapping when interpreting model predictions.
6. Keep the same fitted scaler for future live inference.

### Important Considerations

- The dataset remains imbalanced despite the SMOTE minority-class floor.
- Live-layer conversions must match training preprocessing, including applicable time-unit and flag-count conversions.
- The held-out test dataset must not be used for model selection.
- Do not mix artifacts from earlier preprocessing runs with the regenerated files.

**Handoff status:** Regenerated files uploaded to Google Drive. Recipient access and successful loading pending confirmation.