
# Kalasag Model Development Results

## 1. Overview

This document records the model training, validation, comparison, feature importance analysis, CPU inference benchmarking, and Destination Port ablation experiment conducted for the Kalasag intrusion detection system.

Four machine learning models were evaluated:

1. Decision Tree
2. Logistic Regression
3. Random Forest
4. XGBoost

The experiments used Jaymie's processed dataset and the prepared training and validation splits. The test dataset was not used for model selection or tuning.

## 2. Dataset and Training Configuration

The processed dataset contained 46 input features and one target column, `Attack Type`.

Dataset split:

| Dataset | Rows |
|---|---:|
| Training before SMOTE | 1,762,376 |
| Training after SMOTE | 1,783,111 |
| Validation | 377,652 |
| Test | 377,653 |

The seven target classes were:

- Bots
- Brute Force
- DDoS
- DoS
- Normal Traffic
- Port Scanning
- Web Attacks

SMOTE was applied only to the training dataset. The existing scaler and prepared datasets were reused. No new split or scaling operation was performed.

### Model configurations

| Model | Configuration |
|---|---|
| Decision Tree | max_depth=25, random_state=42 |
| Logistic Regression | max_iter=100, random_state=42 |
| Random Forest | n_estimators=100, max_depth=25, max_samples=0.5, random_state=42 |
| XGBoost | n_estimators=200, max_depth=8, learning_rate=0.2, random_state=42 |

XGBoost used histogram-based tree construction and GPU acceleration during training.

## 3. Validation Results

The following results were obtained using the validation dataset.

| Model | Macro F1 | Macro Recall | Macro Precision | Attack Recall | FPR | Training Time |
|---|---:|---:|---:|---:|---:|---:|
| Decision Tree | 0.9648 | 0.9737 | 0.9572 | 0.9966 | 0.0009 | 108.58 s |
| Logistic Regression | 0.6863 | 0.6901 | 0.6977 | 0.9479 | 0.0162 | 104.49 s |
| Random Forest | 0.9674 | 0.9797 | 0.9574 | 0.9976 | 0.0009 | 369.70 s |
| XGBoost | 0.9661 | 0.9809 | 0.9544 | 0.9990 | 0.0009 | 37.65 s |

### Per-class performance

The following table summarizes the validation recall and F1-score for each class.

| Class | DT Recall | DT F1 | LR Recall | LR F1 | RF Recall | RF F1 | XGB Recall | XGB F1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bots | 0.85 | 0.79 | 0.02 | 0.03 | 0.89 | 0.80 | 0.89 | 0.78 |
| Brute Force | 1.00 | 1.00 | 0.76 | 0.78 | 1.00 | 1.00 | 1.00 | 1.00 |
| DDoS | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| DoS | 1.00 | 1.00 | 0.93 | 0.96 | 1.00 | 1.00 | 1.00 | 1.00 |
| Normal Traffic | 1.00 | 1.00 | 0.98 | 0.99 | 1.00 | 1.00 | 1.00 | 1.00 |
| Port Scanning | 0.99 | 0.99 | 0.97 | 0.85 | 1.00 | 0.99 | 1.00 | 0.99 |
| Web Attacks | 0.98 | 0.98 | 0.18 | 0.20 | 0.98 | 0.98 | 0.98 | 0.99 |

Classification reports and confusion matrices are preserved in the model training notebook.

### Initial observations

- Random Forest achieved the highest Macro F1-score.
- XGBoost achieved the highest Macro Recall and Attack Recall.
- XGBoost also had the shortest training time among the four models.
- Logistic Regression performed poorly on Bots and Web Attacks.
- Random Forest and XGBoost demonstrated strong performance across the seven classes.

## 4. CPU Inference Latency

The trained models were evaluated using CPU inference to assess their potential use in the Kalasag detection pipeline.

| Model | Median Total Time | Mean Total Time | Median Time per Record |
|---|---:|---:|---:|
| Decision Tree | 1.529508 ms | 1.528969 ms | 0.005098 ms |
| Logistic Regression | 1.787436 ms | 1.740076 ms | 0.005958 ms |
| XGBoost | 15.731684 ms | 17.285937 ms | 0.052439 ms |
| Random Forest | 38.847260 ms | 41.608186 ms | 0.129491 ms |

All four models remained below the project's target of 100 milliseconds per record based on the recorded benchmark.

Random Forest had the highest inference time, while Decision Tree had the lowest.

XGBoost provided a balance between detection performance and inference speed.

## 5. Feature Importance Analysis

Feature importance was examined for Random Forest and XGBoost to identify which input features contributed most to their predictions.

### Random Forest: Top 15 Features

| Rank | Feature | Importance |
|---:|---|---:|
| 1 | Bwd Packet Length Std | 0.077218 |
| 2 | Packet Length Std | 0.072007 |
| 3 | Packet Length Variance | 0.070055 |
| 4 | Bwd Packet Length Mean | 0.059178 |
| 5 | Bwd Packet Length Max | 0.048635 |
| 6 | Total Length of Fwd Packets | 0.047881 |
| 7 | Average Packet Size | 0.039661 |
| 8 | Fwd Packet Length Max | 0.036436 |
| 9 | Packet Length Mean | 0.030415 |
| 10 | Max Packet Length | 0.029944 |
| 11 | Subflow Fwd Bytes | 0.029810 |
| 12 | Fwd Header Length | 0.027555 |
| 13 | Destination Port | 0.026620 |
| 14 | Fwd Packet Length Mean | 0.025144 |
| 15 | Total Fwd Packets | 0.022462 |

### XGBoost: Top 15 Features

| Rank | Feature | Importance |
|---:|---|---:|
| 1 | Bwd Packet Length Std | 0.252803 |
| 2 | act_data_pkt_fwd | 0.085178 |
| 3 | Bwd Packet Length Mean | 0.071548 |
| 4 | Bwd IAT Max | 0.059070 |
| 5 | Average Packet Size | 0.050011 |
| 6 | Total Length of Fwd Packets | 0.047072 |
| 7 | Destination Port | 0.044373 |
| 8 | Flow Packets/s | 0.042445 |
| 9 | Flow Bytes/s | 0.037099 |
| 10 | Fwd Packet Length Max | 0.036802 |
| 11 | Flow IAT Max | 0.029046 |
| 12 | Flow IAT Min | 0.026225 |
| 13 | Flow IAT Mean | 0.024044 |
| 14 | Bwd Header Length | 0.021150 |
| 15 | Max Packet Length | 0.019950 |

Bwd Packet Length Std ranked first in both models. Destination Port also appeared among the top 15 features in both models.

Feature importance indicates how much a model uses a feature. It does not independently establish a causal relationship between that feature and an attack.

## 6. Destination Port Ablation Experiment

An additional experiment was conducted to evaluate the effect of removing Destination Port from the input features.

The original configuration used 46 features. The ablation configuration used 45 features.

The same training and validation datasets and model hyperparameters were retained.

### Results

| Metric | RF with Port | RF without Port | XGB with Port | XGB without Port |
|---|---:|---:|---:|---:|
| Macro F1 | 0.9674 | 0.9628 | 0.9661 | 0.9630 |
| Macro Recall | 0.9797 | 0.9750 | 0.9809 | 0.9820 |
| Attack Recall | 0.9976 | 0.9960 | 0.9990 | 0.9987 |
| FPR | 0.0009 | 0.0010 | 0.0009 | 0.0011 |
| Training Time | 369.70 s | 363.74 s | 37.65 s | 42.30 s |

### Interpretation

Both Random Forest and XGBoost achieved slightly better Macro F1, Attack Recall, and FPR when Destination Port was included.

XGBoost achieved a slightly higher Macro Recall without Destination Port. Therefore, the effect was not identical across all metrics.

The overall differences were modest, but retaining Destination Port provided better results on several important detection metrics.

### Recommendation

Retain Destination Port and maintain the 46-feature configuration.

This recommendation is supported by the validation comparison and feature importance results. However, the results should be interpreted with consideration of possible dataset-specific port patterns.

## 7. Dataset Overlap Investigation

An additional investigation compared the original training dataset and validation dataset to identify overlapping records.

The investigation found:

- Exact full-row overlap: 3 records.
- Exact overlap percentage: approximately 0.0008% of validation records.
- Duplicate rows in training: 5.
- Duplicate rows in validation: 0.
- Feature-only matching records: 144.
- Unique feature combinations with conflicting labels: 141.

The conflicting labels were mainly:

- Normal Traffic versus Port Scanning: 117 cases.
- Normal Traffic versus DoS: 24 cases.

These findings may indicate duplicate flows, label inconsistencies, or ambiguous feature representations.

However, the overlap investigation does not independently establish data leakage.

No records or labels were manually changed or removed. The findings were documented as a potential dataset limitation.

## 8. Model Recommendation

Based on the validation results, XGBoost is recommended as the leading candidate for the final model.

Reasons:

1. Highest Attack Recall among the evaluated models at 0.9990.
2. Highest Macro Recall at 0.9809.
3. Strong Macro F1 of 0.9661.
4. Low False Positive Rate of 0.0009.
5. Shortest training time among the four models.
6. Lower CPU inference latency than Random Forest.

Random Forest remains a strong alternative because it achieved the highest Macro F1-score of 0.9674.

The final model selection remains subject to team discussion and approval.

## 9. Pending Work

The following activities remain subject to team coordination:

- Confirm the final model selection with the team.
- Obtain approval before opening the prepared test dataset.
- Evaluate the selected model on the test dataset only once.
- Record final test metrics, per-class results, and confusion matrix.
- Complete any agreed final explainability analysis.
- Integrate the approved results into the project's Results chapter.

The test dataset was not used in the experiments documented above.

## 10. Conclusion

The validation experiments show that Random Forest and XGBoost are strong candidates for the Kalasag intrusion detection system.

Random Forest achieved the highest Macro F1-score, while XGBoost provided the highest Macro Recall and Attack Recall with considerably lower training and CPU inference times than Random Forest.

The Destination Port ablation experiment supports retaining the feature in the 46-feature configuration.

XGBoost is therefore recommended as the leading candidate, pending final team approval and acceptance of the historical test evaluation documented in Section 12.

## 11. Clean Model Reproduction Run (November 19, 2026)

A clean model reproduction was conducted using the new notebook `05_model_training.ipynb`.

The purpose was to verify the training and validation results using the prepared datasets without changing the existing data splits, scaler, or SMOTE processing.

### Dataset Verification

| Dataset | Shape |
|---|---|
| Training features | 1,783,111 rows × 46 features |
| Training labels | 1,783,111 rows |
| Validation features | 377,652 rows × 46 features |
| Validation labels | 377,652 rows |

The prepared training and validation datasets were reused. No new splitting, scaling, or SMOTE operation was performed. The test dataset was not opened or evaluated during this reproduction run.

### Reproduced Training Times

| Model | Training Time |
|---|---:|
| Decision Tree | 109.43 seconds |
| Logistic Regression | 96.32 seconds |
| Random Forest | 379.95 seconds |
| XGBoost | 35.74 seconds |

The validation metrics were consistent with the results recorded in Section 3, subject to rounding.

### Updated CPU Inference Benchmark

The updated benchmark used 300 validation records across 10 repetitions. XGBoost inference was benchmarked using a CPU-configured copy of the trained model.

| Model | Median Total Time | Mean Total Time | Median Time per Record |
|---|---:|---:|---:|
| Logistic Regression | 1.716638 ms | 1.906803 ms | 0.005722 ms |
| Decision Tree | 5.702554 ms | 5.554997 ms | 0.019009 ms |
| XGBoost | 27.593101 ms | 29.452042 ms | 0.091977 ms |
| Random Forest | 52.589287 ms | 55.769704 ms | 0.175298 ms |

All four models remained below the project's target of 100 milliseconds per record in this benchmark.

### Runtime Environment

The clean reproduction was conducted in Google Colab using the following package versions:

| Package | Version |
|---|---|
| Python | 3.13 |
| pandas | 2.2.3 |
| NumPy | 2.4.6 |
| scikit-learn | 1.6.1 |
| imbalanced-learn | 0.14.2 |
| joblib | 1.6.0 |
| pyarrow | 23.0.1 |
| XGBoost | 3.4.1 |

The Colab environment did not exactly match the versions in the repository's `requirements.lock.txt`. This should be considered when reproducing the experiment in another environment.

### Scaler Version Compatibility

The notebook's saved scaler-loading output reported that `scaler.pkl` was
saved using scikit-learn 1.9.1 but was loaded in an environment using
scikit-learn 1.6.1. This produced an `InconsistentVersionWarning`.
Although the scaler loaded and reported 46 features, the version mismatch
may affect compatibility. Reproduction should use a consistent
scikit-learn version. The scaler should not be refitted or replaced
without team approval.

### Notes and Limitations

- All four models were trained and saved in the reproduction output folder in Google Drive.
- XGBoost displayed a CPU/GPU device mismatch warning during prediction because the trained model used GPU acceleration while the validation input was on CPU. Prediction continued using a fallback path.
- The updated CPU latency benchmark used a CPU-configured copy of XGBoost to avoid changing the saved GPU-trained model.
- The test dataset was not accessed during this clean reproduction.
- Previously recorded test results remain historical results and were not reproduced in this run.

This reproduction provides updated training-time and CPU-latency measurements while preserving the existing validation results. Final model selection and acceptance of the historical test evaluation remain subject to team approval.

## 12. Historical XGBoost Test Evaluation

A one-time XGBoost test evaluation was previously performed using the prepared test dataset. The recorded notebook outputs were recovered from the historical model-training notebook.

This evaluation is separate from the clean model reproduction documented in Section 11. The November 19 reproduction used training and validation data only and did not repeat the test evaluation.

### Test Dataset Verification

| Item | Recorded Result |
|---|---|
| Test dataset shape | 377,653 rows × 47 columns |
| Input features | 46 |
| Target column | label |
| Feature order | Matched the XGBoost model's expected feature order |
| Evaluation model | XGBoost |
| Test evaluation | Completed once |

The historical notebook recorded the following test dataset path:

`/content/drive/MyDrive/kalasag/processed/test_scaled.parquet`

A separate earlier path was checked and reported as unavailable. The path above was confirmed to exist and was used to load the test dataset in the recorded execution. The official team-approved Drive location should still be confirmed.

### Overall Test Results

| Metric | Result |
|---|---:|
| Accuracy | 0.9990 |
| Macro F1 | 0.9630 |
| Macro Recall | 0.9821 |
| Macro Precision | 0.9485 |
| Macro False Positive Rate | 0.0003 |

The Macro False Positive Rate was calculated using a one-vs-rest approach and averaged across the seven classes.

### Per-Class Test Results

| Class | Precision | Recall | F1-Score | Support |
|---|---:|---:|---:|---:|
| Bots | 0.6718 | 0.8973 | 0.7683 | 292 |
| Brute Force | 0.9993 | 0.9985 | 0.9989 | 1,371 |
| DDoS | 1.0000 | 0.9996 | 0.9998 | 19,200 |
| DoS | 0.9986 | 0.9993 | 0.9990 | 29,038 |
| Normal Traffic | 0.9998 | 0.9990 | 0.9994 | 313,827 |
| Port Scanning | 0.9889 | 0.9995 | 0.9942 | 13,604 |
| Web Attacks | 0.9813 | 0.9813 | 0.9813 | 321 |

### Test Result Artifacts

The historical notebook outputs confirmed that the following files were successfully saved in the Google Drive model results folder:

- `xgboost_test_confusion_matrix.csv`
- `xgboost_test_normalized_confusion_matrix.csv`
- `xgboost_test_normalized_confusion_matrix.png`
- `xgboost_test_classification_report.csv`

The notebook also recorded a successful handoff check for `final_model.joblib`.

### Notes and Limitations

- These results are recovered from the saved outputs of the historical notebook execution.
- The test evaluation must not be repeated merely to reproduce these numbers.
- The historical notebook displayed an XGBoost CPU/GPU device mismatch warning during prediction. Prediction nevertheless completed and produced the recorded metrics.
- Bots had the lowest F1-score at 0.7683, indicating weaker classification performance for this minority class compared with the other classes.
- The official acceptance of this historical evaluation and confirmation of its dataset lineage remain subject to team review.
