# CICIDS2017 Data Dictionary

## Dataset Information

- **Dataset:** CICIDS2017 Cleaned & Preprocessed
- **Source:** Kaggle
- **Source file:** `cicids2017_cleaned.csv`
- **Total records:** 2,520,751
- **Total columns:** 53
- **Input features:** 52
- **Target column:** `Attack Type`
- **Number of classes:** 7

## Feature Descriptions

The following table describes all 52 input features in their original schema order. These features represent network traffic characteristics extracted from network flows.

| # | Feature Name | Description |
|---|---|---|
| 1 | Destination Port | Port number of the destination service or device. |
| 2 | Flow Duration | Total duration of the network flow, typically in microseconds. |
| 3 | Total Fwd Packets | Total number of packets sent in the forward direction. |
| 4 | Total Length of Fwd Packets | Combined length, in bytes, of all forward packets. |
| 5 | Fwd Packet Length Max | Maximum forward packet length. |
| 6 | Fwd Packet Length Min | Minimum forward packet length. |
| 7 | Fwd Packet Length Mean | Average forward packet length. |
| 8 | Fwd Packet Length Std | Standard deviation of forward packet lengths. |
| 9 | Bwd Packet Length Max | Maximum backward packet length. |
| 10 | Bwd Packet Length Min | Minimum backward packet length. |
| 11 | Bwd Packet Length Mean | Average backward packet length. |
| 12 | Bwd Packet Length Std | Standard deviation of backward packet lengths. |
| 13 | Flow Bytes/s | Average number of bytes transferred per second during the flow. |
| 14 | Flow Packets/s | Average number of packets transferred per second during the flow. |
| 15 | Flow IAT Mean | Mean time between consecutive packets in the flow. |
| 16 | Flow IAT Std | Standard deviation of packet inter-arrival times in the flow. |
| 17 | Flow IAT Max | Maximum time between consecutive packets in the flow. |
| 18 | Flow IAT Min | Minimum time between consecutive packets in the flow. |
| 19 | Fwd IAT Total | Sum of inter-arrival times between forward packets. |
| 20 | Fwd IAT Mean | Mean inter-arrival time between forward packets. |
| 21 | Fwd IAT Std | Standard deviation of forward packet inter-arrival times. |
| 22 | Fwd IAT Max | Maximum inter-arrival time between forward packets. |
| 23 | Fwd IAT Min | Minimum inter-arrival time between forward packets. |
| 24 | Bwd IAT Total | Sum of inter-arrival times between backward packets. |
| 25 | Bwd IAT Mean | Mean inter-arrival time between backward packets. |
| 26 | Bwd IAT Std | Standard deviation of backward packet inter-arrival times. |
| 27 | Bwd IAT Max | Maximum inter-arrival time between backward packets. |
| 28 | Bwd IAT Min | Minimum inter-arrival time between backward packets. |
| 29 | Fwd Header Length | Total header length of packets in the forward direction. |
| 30 | Bwd Header Length | Total header length of packets in the backward direction. |
| 31 | Fwd Packets/s | Number of forward packets transmitted per second. |
| 32 | Bwd Packets/s | Number of backward packets transmitted per second. |
| 33 | Min Packet Length | Minimum packet length observed in the flow. |
| 34 | Max Packet Length | Maximum packet length observed in the flow. |
| 35 | Packet Length Mean | Average packet length across the flow. |
| 36 | Packet Length Std | Standard deviation of packet lengths across the flow. |
| 37 | Packet Length Variance | Variance of packet lengths across the flow. |
| 38 | FIN Flag Count | Number of packets with the TCP FIN flag set. |
| 39 | PSH Flag Count | Number of packets with the TCP PSH flag set. |
| 40 | ACK Flag Count | Number of packets with the TCP ACK flag set. |
| 41 | Average Packet Size | Average size of packets in the flow. |
| 42 | Subflow Fwd Bytes | Number of forward-direction bytes associated with a subflow. |
| 43 | Init_Win_bytes_forward | Initial TCP window size, in bytes, in the forward direction. |
| 44 | Init_Win_bytes_backward | Initial TCP window size, in bytes, in the backward direction. |
| 45 | act_data_pkt_fwd | Number of forward packets containing at least one byte of TCP payload. |
| 46 | min_seg_size_forward | Minimum TCP segment size observed in the forward direction. |
| 47 | Active Mean | Average duration of active periods within the flow. |
| 48 | Active Max | Maximum duration of an active period within the flow. |
| 49 | Active Min | Minimum duration of an active period within the flow. |
| 50 | Idle Mean | Average duration of idle periods within the flow. |
| 51 | Idle Max | Maximum duration of an idle period within the flow. |
| 52 | Idle Min | Minimum duration of an idle period within the flow. |

## Target Variable

**Column Name:** `Attack Type`

The target variable identifies whether a network flow represents normal traffic or a particular type of cyberattack.

| Class | Description |
|---|---|
| Normal Traffic | Network activity classified as legitimate or non-malicious. |
| DoS | Denial-of-Service attack intended to disrupt service availability. |
| DDoS | Distributed Denial-of-Service attack involving multiple attacking sources. |
| Port Scanning | Attempts to discover available network ports or services. |
| Brute Force | Repeated attempts to guess authentication credentials. |
| Web Attacks | Attacks targeting web applications or services. |
| Bots | Traffic associated with automated malicious activity. |

## Feature Categories

The 52 features can be grouped into the following categories:

- **Network configuration:** Destination Port.
- **Flow characteristics:** Flow Duration, Flow Bytes/s, Flow Packets/s.
- **Packet statistics:** Packet counts, lengths, sizes, and variance.
- **Timing characteristics:** Flow IAT, Fwd IAT, and Bwd IAT measurements.
- **TCP characteristics:** Header lengths, TCP flag counts, window sizes, and segment sizes.
- **Subflow characteristics:** Forward subflow bytes.
- **Activity characteristics:** Active and Idle duration statistics.

## Preprocessing Considerations

- All 52 input features are numeric.
- The target variable is categorical and requires label encoding before model training.
- The dataset has not yet been scaled.
- No constant columns were detected during the initial inspection.
- Destination Port will be retained initially, subject to further evaluation by the modeling team.
- Feature names and ordering must remain consistent between model training and live network traffic processing.

## Documentation Notes

Feature descriptions are based on standard CICFlowMeter terminology. Exact units and implementation-specific calculations should be verified against the dataset's extraction methodology where necessary.

This dictionary documents the original dataset schema. Any feature exclusions made during cleaning must be reflected in `data/schema/feature_schema.json` and the cleaning log.