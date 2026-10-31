# CICIDS2017 Data Cleaning Log

## 1. Dataset Overview

- **Dataset:** CICIDS2017 Cleaned
- **Source:** `data/raw/cicids2017_cleaned.csv`
- **Output:** `data/interim/cleaned.parquet`
- **Target column:** `Attack Type`
- **Number of classes:** 7

## 2. Cleaning Procedures

1. Loaded the original dataset and standardized column names by removing surrounding whitespace.
2. Checked numerical features for positive and negative infinity and replaced any such values with `NaN`.
3. Inspected missing values and duplicate records.
4. Removed exact duplicate records while retaining the first occurrence.
5. Checked for constant feature columns. No columns required removal.
6. Standardized attack labels by removing surrounding whitespace.
7. Updated the feature schema and exported the cleaned dataset in Parquet format.

## 3. Before and After Cleaning

| Metric | Before | After |
|---|---:|---:|
| Total records | 2,520,751 | 2,520,590 |
| Total columns | 53 | 53 |
| Exact duplicates | 161 | 0 |
| Missing values | 0 | 0 |
| Infinite values | 0 | 0 |
| Attack classes | 7 | 7 |

**Total records removed:** 161 (approximately 0.0064% of the original dataset).

## 4. Class Distribution Comparison

| Attack Type | Before | After | Removed |
|---|---:|---:|---:|
| Normal Traffic | 2,095,057 | 2,094,896 | 161 |
| DoS | 193,745 | 193,745 | 0 |
| DDoS | 128,014 | 128,014 | 0 |
| Port Scanning | 90,694 | 90,694 | 0 |
| Brute Force | 9,150 | 9,150 | 0 |
| Web Attacks | 2,143 | 2,143 | 0 |
| Bots | 1,948 | 1,948 | 0 |
| **Total** | **2,520,751** | **2,520,590** | **161** |

## 5. Cleaning Decisions

- **Duplicate removal:** Removed 161 exact duplicates, all belonging to Normal Traffic.
- **Missing and infinite values:** No missing or infinite values remained after cleaning; no row removal or imputation was necessary for these issues.
- **Constant features:** No constant columns were found, so all 52 input features were retained.
- **Class preservation:** All seven original traffic classes were preserved.
- **Class imbalance:** No oversampling, undersampling, or SMOTE was performed during cleaning. Class imbalance will be handled separately during model preparation.
- **Original dataset:** Preserved without modification.

## 6. Final Validation

The cleaned dataset contains 2,520,590 records and 53 columns, including the target label. Validation confirmed zero missing values, zero infinite values, and zero exact duplicates.

The cleaned dataset was saved to `data/interim/cleaned.parquet` for subsequent analysis and preprocessing.