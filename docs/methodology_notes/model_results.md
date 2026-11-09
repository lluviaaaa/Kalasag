
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


### Final XGBoost Single-Record Inference Benchmark

An additional CPU inference benchmark was conducted using the selected XGBoost model to measure the time required to make an individual prediction.

The benchmark was repeated 100 times.

| Measurement | Result |
|---|---:|
| Number of repetitions | 100 |
| Median inference time | 4.4272 ms |
| Mean inference time | 5.2784 ms |

The results show that the selected XGBoost model can produce individual predictions within a few milliseconds under the tested environment.

This benchmark measures model prediction time only. It does not represent the total processing time of the complete live detection pipeline.




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


### SHAP Explainability Analysis

SHAP (SHapley Additive exPlanations) was used to further examine the contribution of input features to the XGBoost model's predictions.

The analysis was performed using 500 validation records and all 46 input features. The resulting SHAP values had a shape of (500, 46, 7), representing 500 records, 46 features, and 7 target classes.

The top features based on mean absolute SHAP values were:

| Rank | Feature | Mean Absolute SHAP Value |
|---:|---|---:|
| 1 | Destination Port | 2.873783 |
| 2 | Init_Win_bytes_forward | 1.246348 |
| 3 | min_seg_size_forward | 0.976831 |
| 4 | Init_Win_bytes_backward | 0.647468 |
| 5 | Fwd IAT Min | 0.618400 |
| 6 | Packet Length Std | 0.606323 |
| 7 | Bwd IAT Std | 0.451499 |
| 8 | Fwd IAT Std | 0.450125 |
| 9 | Bwd Packets/s | 0.425260 |
| 10 | Bwd Packet Length Std | 0.392254 |

Destination Port had the highest mean absolute SHAP value, indicating a strong contribution to the model's predictions across the analyzed records.

These results provide additional information about how the model uses its input features. SHAP values describe feature contributions to model predictions and do not establish causal relationships.


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


## 8. Final Model Recommendation

Based on the validation comparison and final test evaluation, XGBoost was selected as the final model for the Kalasag intrusion detection system.

The reasons for selecting XGBoost include:

1. It achieved the highest validation Macro Recall of 0.9809.
2. It achieved the highest validation Attack Recall of 0.9990.
3. It obtained a strong validation Macro F1-score of 0.9661.
4. It achieved a low validation False Positive Rate of 0.0009.
5. It had the shortest training time among the four evaluated models at 37.65 seconds.
6. It demonstrated strong performance during the final test evaluation, achieving a Macro F1-score of 0.9630 and Macro Recall of 0.9821.

Although Random Forest achieved a slightly higher validation Macro F1-score of 0.9674, XGBoost provided a strong balance of detection performance, training efficiency, and inference speed.

The final evaluation supports the selection of XGBoost as the model for the Kalasag system.


## 9. Final Test Evaluation

After model selection, the selected XGBoost model was evaluated using the prepared test dataset. The test dataset was opened only once and was not used for model training, tuning, or model selection.

### Final Test Results

| Metric | Result |
|---|---:|
| Accuracy | 0.9990 |
| Macro Precision | 0.9485 |
| Macro Recall | 0.9821 |
| Macro F1 | 0.9630 |
| Weighted F1 | 0.9990 |
| Macro FPR | 0.0003 |

The results demonstrate strong overall classification performance on the held-out test dataset.

The model achieved high macro recall and a low false positive rate. However, performance varied across classes, particularly for Bots.

### Per-Class Observations

The Bots class showed weaker performance compared with the other classes. Some Bot records were classified as Normal Traffic, while some Normal Traffic records were classified as Bots.

This indicates that minority-class detection remains an area for improvement despite the model's strong overall performance.

### Final Evaluation Status

The final test evaluation has been completed. No additional test evaluation or model tuning was performed using the held-out test dataset.





## 10. Conclusion

The model development experiments evaluated four machine learning algorithms for the Kalasag intrusion detection system: Decision Tree, Logistic Regression, Random Forest, and XGBoost.

The validation results showed that Random Forest achieved the highest Macro F1-score of 0.9674, while XGBoost achieved the highest Macro Recall of 0.9809 and Attack Recall of 0.9990. XGBoost also had the shortest training time among the evaluated models.

Following model selection, XGBoost achieved a final test Macro F1-score of 0.9630, Macro Recall of 0.9821, and False Positive Rate of 0.0003.

The Destination Port ablation experiment supported retaining the feature in the 46-feature configuration. Feature importance and SHAP analysis also provided information about the features contributing to model predictions.

The single-record CPU inference benchmark recorded a median prediction time of 4.4272 milliseconds across 100 repetitions.

Overall, the results support XGBoost as the selected model for the Kalasag intrusion detection system. The model demonstrated strong classification performance and promising prediction speed under the tested conditions. Further system-level testing is still necessary to evaluate its performance within the complete live detection pipeline.
