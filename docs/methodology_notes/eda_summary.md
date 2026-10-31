# CICIDS2017 Exploratory Data Analysis Summary

## 1. Dataset Overview

The exploratory data analysis was conducted on the cleaned CICIDS2017 dataset stored in `data/interim/cleaned.parquet`.

- Total records: 2,520,590
- Total columns: 53
- Numerical input features: 52
- Target variable: `Attack Type`
- Number of traffic classes: 7

## 2. Class Distribution

The dataset exhibits severe class imbalance. Normal Traffic is the majority class, while Bots is the minority class.

The majority-to-minority imbalance ratio is approximately **1,075.41:1**.

This imbalance may cause machine learning models to favor majority-class predictions. Future evaluation should consider macro-averaged precision, recall, F1-score, and per-class performance rather than relying on accuracy alone.

## 3. Numerical Feature Analysis

All 52 input features are numerical.

Features such as Flow Duration, Fwd IAT Total, Bwd IAT Total, and Flow Bytes/s exhibit large standard deviations and substantially different measurement scales.

Feature scaling may be appropriate for scale-sensitive algorithms. Scaling parameters should be fitted using training data only to prevent data leakage.

## 4. Correlation Analysis

The correlation heatmap reveals strong positive relationships among several packet-length, inter-arrival-time, and idle-time features.

Notable examples include:

| Feature Pair | Pearson Correlation |
|---|---:|
| Total Length of Fwd Packets / Subflow Fwd Bytes | 0.999999 |
| Flow Duration / Fwd IAT Total | 0.998530 |
| Flow IAT Max / Fwd IAT Max | 0.998054 |
| Packet Length Mean / Average Packet Size | 0.997823 |
| Idle Mean / Idle Max | 0.990238 |

These relationships suggest potential feature redundancy. However, no features were removed during EDA.

## 5. Outlier Analysis

The interquartile range (IQR) method was applied to four selected numerical features.

| Feature | Flagged Outliers | Percentage |
|---|---:|---:|
| Flow Duration | 468,153 | 18.57% |
| Flow Bytes/s | 474,908 | 18.84% |
| Flow Packets/s | 252,507 | 10.02% |
| Total Fwd Packets | 252,965 | 10.04% |

The results indicate skewed distributions and numerous extreme observations.

Because unusual network traffic can represent legitimate attack patterns, statistical outliers should not be automatically removed.

## 6. Negative-Value Findings

Several numerical features contain negative measurements.

The most frequent are:

- Init_Win_bytes_backward: 1,215,574 records (48.2258%)
- Init_Win_bytes_forward: 911,012 records (36.1428%)
- Flow IAT Min: 2,874 records (0.1140%)
- Flow Duration: 106 records (0.0042%)
- Flow Packets/s: 106 records (0.0042%)
- Flow Bytes/s: 78 records (0.0031%)

Additional negative values occur in other timing, header-length, and segment-size features.

Negative TCP window-size values may represent undefined measurements. Other negative values require further investigation to determine whether they represent invalid measurements or dataset-specific conventions.

No records were removed or modified during this analysis.

## 7. Generated Visualizations

The following figures were generated:

- `reports/figures/class_distribution.png`
- `reports/figures/class_distribution_log.png`
- `reports/figures/feature_correlation_heatmap.png`
- `reports/figures/feature_outliers.png`

## 8. Recommendations for Subsequent Modeling

1. Use stratified data splitting where feasible to preserve minority-class representation.
2. Evaluate minority-class performance using per-class recall, precision, and F1-score.
3. Investigate highly correlated features before making feature-selection decisions.
4. Review suspicious negative measurements and sentinel values.
5. Assess whether scaling or robust transformations are appropriate for the selected models.
6. Apply any resampling or imbalance-handling techniques only to training data to prevent data leakage.

## 9. Conclusion

The cleaned CICIDS2017 dataset contains substantial class imbalance, strongly correlated features, skewed numerical distributions, and potentially anomalous negative measurements.

These findings provide a basis for subsequent feature preparation and model development. No additional cleaning, feature elimination, or resampling was performed during EDA.