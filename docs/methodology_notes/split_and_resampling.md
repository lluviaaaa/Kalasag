# Data Splitting, Feature Scaling, and Class Imbalance Handling

## 1. Overview

This document describes the preprocessing procedures applied to the cleaned CICIDS2017 dataset for the Kalasag project. The procedures include feature selection, label encoding, stratified dataset splitting, feature scaling, and partial class rebalancing using the Synthetic Minority Over-sampling Technique (SMOTE).

The preprocessing pipeline follows this sequence:

**Feature Selection → Label Encoding → Stratified Splitting → Feature Scaling → SMOTE (Training Set Only)**

The pipeline was designed to maintain consistency between offline model training and live network traffic detection while minimizing data leakage.

## 2. Dataset Information

- Source: Cleaned CICIDS2017 dataset
- Total records: 2,520,590
- Original numerical input features: 52
- Final selected numerical input features: 46
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

## 3. Feature Selection and Schema Compatibility

Following the team's CICFlowMeter feature compatibility review, six unreliable Active/Idle features were excluded from the modeling pipeline.

These features consistently returned zero in the team's live Python CICFlowMeter implementation and were therefore excluded to prevent inconsistencies between offline training and live inference.

The following features were removed:

- Active Mean
- Active Max
- Active Min
- Idle Mean
- Idle Max
- Idle Min

The team also confirmed that `Destination Port` would be retained as an input feature.

The final approved configuration consists of **46 retained features and 6 excluded features**.

The approved feature names and ordering are maintained in `data/schema/feature_schema.json`.

Feature selection is performed before dataset splitting, scaling, and SMOTE. This ensures that the training datasets, saved scaler, and live detection pipeline use the same feature configuration.

The original cleaned dataset remains unchanged to preserve the source data.

## 4. Stratified Dataset Splitting

The dataset was divided using stratified random sampling with `random_state=42`, preserving approximately the same class proportions across all subsets.

| Dataset | Percentage | Records |
|---|---|---|
| Training | 70% | 1,764,413 |
| Validation | 15% | 378,088 |
| Testing | 15% | 378,089 |
| **Total** | **100%** | **2,520,590** |

Assertions confirmed that the training, validation, and testing sets contain no overlapping original row indices.

The unscaled datasets were saved to `data/interim/` for reproducibility.

The test set was reserved for final evaluation and must not be used for model training, hyperparameter tuning, or preprocessing decisions.

## 5. Missing-Value Handling

No median imputation was performed because the cleaned dataset contained no missing or infinite values.

Therefore, no imputer was required or saved.

## 6. Feature Scaling

Feature scaling was performed using scikit-learn's `StandardScaler`.

The scaler was fitted exclusively on the original training dataset using `fit()`.

The training, validation, and testing datasets were then transformed using the same fitted scaler through `transform()`.

This approach prevents information from validation or testing records from influencing the training preprocessing parameters.

The fitted scaler was saved as:

`models/scaler.pkl`

The final 46 input features were verified against `data/schema/feature_schema.json` to confirm consistent feature names and ordering.

The saved scaler is configured to accept exactly 46 numerical features, matching the approved live detection schema.

## 7. Class Imbalance Handling Using SMOTE

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

## 8. Processed Dataset Outputs

The following datasets were saved in `data/processed/`:

| File | Records | Description |
|---|---:|---|
| `train_scaled.parquet` | 1,764,413 | Scaled original training records |
| `train_smote_floor10000.parquet` | 1,785,144 | Scaled training records with synthetic samples |
| `val_scaled.parquet` | 378,088 | Scaled validation records |
| `test_scaled.parquet` | 378,089 | Scaled testing records |

Each processed dataset contains:

- 46 numerical input features
- 1 numerically encoded target column named `label`
- **47 columns in total**

The processed datasets follow the approved feature schema required for live model inference.

## 9. Data Leakage Prevention

The following safeguards were implemented:

1. Feature selection was performed before dataset splitting and scaling.
2. Dataset splitting was performed before feature scaling and SMOTE.
3. The scaler was fitted exclusively on training data.
4. Validation and testing data were transformed without refitting the scaler.
5. SMOTE was applied only to the training dataset.
6. Original row indices were checked to ensure no overlap between splits.
7. The test set was reserved for final model evaluation.

These safeguards reduce the risk of data leakage during preprocessing.

## 10. Limitations and Considerations

**Random splitting:** The dataset was split randomly rather than by capture day or attack session. Related network flows may therefore appear in multiple subsets, potentially producing optimistic evaluation results.

**Minority-class representation:** Bots and Web Attacks have relatively few original observations. Their validation and testing subsets contain approximately 300 records per class, which may lead to variability in class-specific evaluation metrics.

**Synthetic samples:** SMOTE generates artificial records through interpolation. These samples may contain feature combinations that do not perfectly represent real network traffic.

**Feature characteristics:** The original dataset contains highly correlated features, extreme values, and unusual negative measurements. These findings should be considered during model development.

**Live feature compatibility:** The six Active/Idle features were excluded based on the team's live CICFlowMeter compatibility findings. The model's input features must remain consistent with the approved 46-feature schema during both training and inference.

**Sampling strategy:** The 10,000-record SMOTE floor is an initial configuration, not necessarily the optimal setting. Alternative sampling floors or class-weighting approaches may be evaluated using validation data.

## 11. Conclusion

The Kalasag preprocessing pipeline successfully prepared the cleaned CICIDS2017 dataset for machine learning development and live network traffic detection.

The pipeline selected 46 approved numerical features, encoded the seven traffic categories, performed stratified dataset splitting, standardized the features using training-only statistics, and partially rebalanced the training dataset using SMOTE.

The resulting datasets and saved preprocessing artifacts provide a reproducible foundation for model training, evaluation, and live inference while maintaining consistency with the team's approved feature schema.