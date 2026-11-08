# Feature-Label Conflict Investigation

**Project:** Kalasag  
**Dataset:** CICIDS2017 Cleaned CSV  
**Investigation:** Feature overlap and conflicting class labels

## 1. Background

During model preparation, the Model Training Lead identified matching feature combinations between the training and validation datasets that were associated with different class labels.

The Data & Preprocessing Lead investigated whether these conflicts existed in the source dataset or resulted from feature selection.

## 2. Methodology

The investigation used the original `data/raw/cicids2017_cleaned.csv` file.

The following checks were performed:

1. Generated feature-only hashes using the original 52 input features.
2. Identified hashes associated with multiple attack labels.
3. Repeated the analysis using the selected 46 features.
4. Retrieved conflicting records and verified their complete feature values rather than relying solely on hashes.

The investigation was read-only and did not modify the preprocessing pipeline or datasets.

## 3. Results

| Finding | Result |
|---|---:|
| Original input features | 52 |
| Selected input features | 46 |
| Conflicting combinations with 52 features | 697 |
| Conflicting hashes with 46 features | 697 |
| Verified full-feature conflicts | 697 |
| Records involved in full-feature conflicts | 1,394 |

### Conflicting Class Combinations

| Class Combination | Conflicts |
|---|---:|
| Normal Traffic vs Port Scanning | 564 |
| Normal Traffic vs DoS | 130 |
| Normal Traffic vs DDoS | 3 |
| **Total** | **697** |

## 4. Interpretation

The source CSV contains 697 verified feature combinations associated with different class labels.

The same number of conflicting feature hashes was observed when using 46 features, suggesting that removing the six unsupported features did not introduce additional conflicts.

These findings indicate that the conflicts were present in the source dataset.

However, identical feature values with different labels do not independently establish which labels are incorrect. Additional information about the original network traffic and labeling process would be required.

## 5. Recommendations

- Preserve the current processed datasets until the team agrees on any corrective action.
- Document conflicting labels as a potential source-data quality limitation.
- Avoid interpreting overall accuracy alone as evidence of reliable attack detection.
- Include per-class evaluation metrics and confusion matrices in model assessment.
- Consider further investigation of the affected records before final model selection.

## 6. Conclusion

The investigation verified 697 conflicting full-feature combinations involving 1,394 records in the original dataset.

The evidence suggests that the conflicts identified during model preparation originate from the source data rather than from the removal of six features.

No dataset modifications were performed during this investigation.