# Data Splitting, Feature Scaling, and Class Imbalance Handling

## 1. Overview

This document describes the preprocessing procedures applied to the cleaned CICIDS2017 dataset for the Kalasag project. The procedures include label encoding, stratified dataset splitting, feature scaling, and partial class rebalancing using the Synthetic Minority Over-sampling Technique (SMOTE).

The preprocessing pipeline follows the sequence:

**Label Encoding → Stratified Splitting → Feature Scaling → SMOTE (Training Set Only)**

This order minimizes data leakage and preserves independent validation and testing datasets.

## 2. Dataset Information

- Source: Cleaned CICIDS2017 dataset
- Total records: 2,520,590
- Numerical input features: 52
- Target column: `Attack Type`
- Number of classes: 7
- Random seed: 42

The target labels were converted into numerical values using scikit-learn's `LabelEncoder`.

| Encoded Label | Traffic Category |
|---|---|
| 0 | Bots |
| 1 | Brute Force |
| 2 | DDoS |
| 3 | DoS |
| 4 | Normal Traffic |
| 5 | Port Scanning |
| 6 | Web Attacks |

The fitted encoder was saved as `models/label_encoder.pkl`.

## 3. Stratified Dataset Splitting

The dataset was divided using stratified random sampling with `random_state=42`, preserving approximately the same class proportions across all subsets.

| Dataset | Percentage | Records |
|---|---|---|
| Training | 70% | 1,764,413 |
| Validation | 15% | 378,088 |
| Testing | 15% | 378,089 |
| Total | 100% | 2,520,590 |

Assertions confirmed that the training, validation, and testing sets contain no overlapping original row indices.

The unscaled datasets were saved to `data/interim/` for reproducibility.

The test set was reserved for final evaluation and must not be used for model training, parameter tuning, or preprocessing decisions.

## 4. Missing-Value Handling

No median imputation was performed because the cleaned dataset contained no missing or infinite values.

Therefore, no imputer was required or saved.

## 5. Feature Scaling

Feature scaling was performed using scikit-learn's `StandardScaler`.

The scaler was fitted exclusively on the original training dataset using `fit_transform()`.

The validation and testing datasets were transformed using the same fitted scaler through `transform()`.

This approach prevents information from validation or testing records from influencing the training preprocessing parameters.

The fitted scaler was saved as:

`models/scaler.pkl`

The 52 input features were verified against `data/schema/feature_schema.json` to confirm consistent feature names and ordering.

## 6. Class Imbalance Handling Using SMOTE

The dataset exhibited substantial class imbalance, with Normal Traffic representing the majority of records.

Partial oversampling was performed using SMOTE with the following settings:

- Sampling floor: 10,000 records
- Random seed: 42
- Number of nearest neighbors (`k_neighbors`): 5
- Applied only to the scaled training dataset
- Validation and testing datasets were not resampled

### Training Class Distribution

| Class | Before SMOTE | After SMOTE |
|---|---:|---:|
| Bots | 1,364 | 10,000 |
| Brute Force | 6,405 | 10,000 |
| DDoS | 89,610 | 89,610 |
| DoS | 135,621 | 135,621 |
| Normal Traffic | 1,466,427 | 1,466,427 |
| Port Scanning | 63,486 | 63,486 |
| Web Attacks | 1,500 | 10,000 |
| **Total** | **1,764,413** | **1,785,144** |

SMOTE generated 20,731 additional synthetic training records.

The oversampling strategy intentionally avoided fully balancing all classes. A sampling floor of 10,000 was selected as an initial setting for comparison during model development.

## 7. Processed Dataset Outputs

The following datasets were saved in `data/processed/`:

| File | Records | Description |
|---|---:|---|
| `train_scaled.parquet` | 1,764,413 | Scaled original training records |
| `train_smote_floor10000.parquet` | 1,785,144 | Scaled training records with synthetic samples |
| `val_scaled.parquet` | 378,088 | Scaled validation records |
| `test_scaled.parquet` | 378,089 | Scaled testing records |

Each processed dataset contains 52 numerical input features and one numerically encoded target column named `label`.

## 8. Data Leakage Prevention

The following safeguards were implemented:

1. Dataset splitting was performed before feature scaling and SMOTE.
2. The scaler was fitted exclusively on training data.
3. Validation and testing data were transformed without refitting the scaler.
4. SMOTE was applied only to the training dataset.
5. The original row indices were checked to ensure no overlap between splits.
6. The test set was reserved for final model evaluation.

These safeguards reduce the risk of data leakage during preprocessing.

## 9. Limitations and Considerations

**Random splitting:** The dataset was split randomly rather than by capture day or attack session. Related network flows may therefore appear in multiple subsets, potentially producing optimistic evaluation results.

**Minority-class representation:** Bots and Web Attacks have relatively few original observations. Their validation and testing subsets contain approximately 300 records per class, which may lead to variability in class-specific evaluation metrics.

**Synthetic samples:** SMOTE generates artificial records through interpolation. These samples may contain feature combinations that do not perfectly represent real network traffic.

**Feature characteristics:** The original dataset contains highly correlated features, extreme values, and unusual negative measurements. These findings should be considered during model development.

**Sampling strategy:** The 10,000-record SMOTE floor is an initial configuration, not necessarily the optimal setting. Alternative sampling floors or class-weighting approaches may be evaluated using validation data.

## 10. Conclusion

The Kalasag preprocessing pipeline successfully prepared the cleaned CICIDS2017 dataset for machine learning development.

The dataset was stratified into training, validation, and testing subsets, standardized using training-only statistics, and partially rebalanced using SMOTE.

The resulting datasets provide a reproducible foundation for model training and evaluation while maintaining separation between training, validation, and testing data.