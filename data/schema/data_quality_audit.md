# CICIDS2017 Data Quality Audit

## Dataset Overview
- Total records: 2,520,751
- Total columns: 53
- Input features: 52
- Target column: Attack Type
- Traffic classes: 7

## Quality Checks
- Missing values: 0
- Infinite values: 0
- Duplicate records: 161
- Constant columns: 0
- Records with suspicious negative values: 2,910

## Findings
- Normal Traffic represents 83.11% of the dataset.
- All 161 duplicate records belong to Normal Traffic.
- Some timing, rate, header-length, and segment-size features contain negative values.
- TCP window-size features contain -1 values that may represent undefined measurements.
- Numeric features have substantially different ranges and do not appear standardized.

## Preprocessing Considerations
- Review suspicious negative values before deciding whether to remove or correct records.
- Evaluate duplicate removal before model training.
- Split the dataset before fitting a scaler.
- Fit scaling parameters using training data only.
- Apply SMOTE only to the training partition, if selected.
- Preserve the original CSV.
