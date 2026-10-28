# CICIDS2017 Data Quality Audit

## Dataset Information

- **Dataset:** CICIDS2017 Cleaned & Preprocessed (Kaggle)
- **Source file:** `cicids2017_cleaned.csv`
- **Total rows:** 2,520,751
- **Total columns:** 53
- **Input features:** 52
- **Target column:** `Attack Type`
- **Number of classes:** 7

## Class Distribution

| Attack Type | Number of Records |
|---|---:|
| Normal Traffic | 2,095,057 |
| DoS | 193,745 |
| DDoS | 128,014 |
| Port Scanning | 90,694 |
| Brute Force | 9,150 |
| Web Attacks | 2,143 |
| Bots | 1,948 |

The dataset is highly imbalanced, with Normal Traffic representing approximately 83.11% of all records. Web Attacks and Bots are the least represented classes.

## Data Quality Findings

- **Missing values:** 0
- **Infinite values:** 0
- **Exact duplicate rows:** 161
- **Constant columns:** 0
- **Non-numeric columns:** `Attack Type` only
- **Feature scaling:** The dataset has not been standardized or normalized.

All 161 exact duplicate records belong to the Normal Traffic class.

## Additional Observations

The inspection identified 2,910 records (approximately 0.1154%) containing suspicious negative values in timing, rate, or header-related features, excluding the TCP window sentinel value of `-1`.

Affected records by class:

| Attack Type | Affected Records |
|---|---:|
| Normal Traffic | 2,722 |
| DoS | 163 |
| DDoS | 19 |
| Brute Force | 6 |

These values require further investigation before deciding whether to retain, correct, or remove the affected records.

## Initial Cleaning Decisions

- No missing-value treatment is currently required.
- No infinite-value replacement is currently required.
- The 161 exact duplicate rows will be removed during the cleaning stage.
- No constant columns require removal.
- Suspicious negative values will be investigated before applying any changes.
- Class distributions will be checked before and after cleaning to protect minority classes.

## Audit Status

Dataset inspection completed. No cleaning transformations have been applied to the original CSV.

The next stage will follow Part 5 of the Kalasag Data Processing Guide.