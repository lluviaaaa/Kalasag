# CICIDS2017 Feature Feasibility Assessment

## 1. Purpose

This document evaluates the feasibility of extracting the 52 CICIDS2017 input features from live network traffic for the Kalasag intrusion detection system.

The objective is to ensure that the features used during model training can also be reproduced during live traffic classification.

## 2. Feature Feasibility Categories

- **Directly obtainable:** Information that can generally be read from network packet headers.
- **Calculated:** Features that require packet aggregation, timing measurements, or statistical computations.
- **Requires verification:** Features that depend on specific traffic capture capabilities, protocol support, or CICFlowMeter-compatible calculations.

## 3. Feature Feasibility Table

| # | Feature | Feasibility | Implementation Requirement |
|---|---|---|---|
| 1 | Destination Port | Directly obtainable | Extract from TCP/UDP destination port |
| 2 | Flow Duration | Calculated | Track first and last packet timestamps |
| 3 | Total Fwd Packets | Calculated | Count forward packets |
| 4 | Total Length of Fwd Packets | Calculated | Sum forward packet lengths |
| 5 | Fwd Packet Length Max | Calculated | Track maximum forward packet length |
| 6 | Fwd Packet Length Min | Calculated | Track minimum forward packet length |
| 7 | Fwd Packet Length Mean | Calculated | Compute average forward packet length |
| 8 | Fwd Packet Length Std | Calculated | Compute standard deviation |
| 9 | Bwd Packet Length Max | Calculated | Track maximum backward packet length |
| 10 | Bwd Packet Length Min | Calculated | Track minimum backward packet length |
| 11 | Bwd Packet Length Mean | Calculated | Compute average backward packet length |
| 12 | Bwd Packet Length Std | Calculated | Compute standard deviation |
| 13 | Flow Bytes/s | Calculated | Divide flow bytes by flow duration |
| 14 | Flow Packets/s | Calculated | Divide packet count by flow duration |
| 15 | Flow IAT Mean | Calculated | Compute average packet inter-arrival time |
| 16 | Flow IAT Std | Calculated | Compute standard deviation of inter-arrival times |
| 17 | Flow IAT Max | Calculated | Identify maximum inter-arrival time |
| 18 | Flow IAT Min | Calculated | Identify minimum inter-arrival time |
| 19 | Fwd IAT Total | Calculated | Sum forward inter-arrival times |
| 20 | Fwd IAT Mean | Calculated | Compute average forward inter-arrival time |
| 21 | Fwd IAT Std | Calculated | Compute standard deviation |
| 22 | Fwd IAT Max | Calculated | Identify maximum forward inter-arrival time |
| 23 | Fwd IAT Min | Calculated | Identify minimum forward inter-arrival time |
| 24 | Bwd IAT Total | Calculated | Sum backward inter-arrival times |
| 25 | Bwd IAT Mean | Calculated | Compute average backward inter-arrival time |
| 26 | Bwd IAT Std | Calculated | Compute standard deviation |
| 27 | Bwd IAT Max | Calculated | Identify maximum backward inter-arrival time |
| 28 | Bwd IAT Min | Calculated | Identify minimum backward inter-arrival time |
| 29 | Fwd Header Length | Calculated | Sum forward packet header lengths |
| 30 | Bwd Header Length | Calculated | Sum backward packet header lengths |
| 31 | Fwd Packets/s | Calculated | Compute forward packet rate |
| 32 | Bwd Packets/s | Calculated | Compute backward packet rate |
| 33 | Min Packet Length | Calculated | Identify minimum packet length |
| 34 | Max Packet Length | Calculated | Identify maximum packet length |
| 35 | Packet Length Mean | Calculated | Compute average packet length |
| 36 | Packet Length Std | Calculated | Compute standard deviation |
| 37 | Packet Length Variance | Calculated | Compute packet length variance |
| 38 | FIN Flag Count | Calculated | Count packets with TCP FIN flag |
| 39 | PSH Flag Count | Calculated | Count packets with TCP PSH flag |
| 40 | ACK Flag Count | Calculated | Count packets with TCP ACK flag |
| 41 | Average Packet Size | Calculated | Compute average packet size |
| 42 | Subflow Fwd Bytes | Requires verification | Reproduce CICFlowMeter subflow calculations |
| 43 | Init_Win_bytes_forward | Requires verification | Extract initial TCP window size and handle sentinel values |
| 44 | Init_Win_bytes_backward | Requires verification | Extract initial backward TCP window size and handle sentinel values |
| 45 | act_data_pkt_fwd | Requires verification | Count forward TCP packets containing payload |
| 46 | min_seg_size_forward | Requires verification | Reproduce forward TCP segment-size calculation |
| 47 | Active Mean | Requires verification | Track active periods using compatible thresholds |
| 48 | Active Max | Requires verification | Identify maximum active-period duration |
| 49 | Active Min | Requires verification | Identify minimum active-period duration |
| 50 | Idle Mean | Requires verification | Track idle periods using compatible thresholds |
| 51 | Idle Max | Requires verification | Identify maximum idle-period duration |
| 52 | Idle Min | Requires verification | Identify minimum idle-period duration |

## 4. Implementation Considerations

### Packet Capture

The live capture component must collect sufficient packet information to reconstruct bidirectional network flows.

This includes packet timestamps, lengths, transport-layer headers, TCP flags, and flow direction.

### Feature Calculation

Most dataset features require aggregation over multiple packets rather than extraction from a single packet.

The implementation must maintain consistent flow boundaries and reproduce the same calculation conventions used during dataset generation.

### Timing Consistency

Flow duration, inter-arrival time, active time, and idle time measurements must use consistent time units and compatible calculation rules.

### Protocol Limitations

TCP-specific features may not be available for UDP or other protocols. Missing or unavailable values must be handled consistently with the training data.

### Preprocessing Consistency

Live traffic must use the exact feature names, column ordering, and saved preprocessing artifacts defined in `data/schema/feature_schema.json`.

The live system must not fit a new scaler on incoming traffic.

## 5. Risks and Open Questions

| Risk or Question | Required Action |
|---|---|
| Differences between CICFlowMeter and live feature calculations | Compare outputs using the same captured traffic |
| TCP-specific features unavailable for some flows | Define protocol-specific handling |
| Active/idle period thresholds differ | Verify compatible thresholds |
| Destination Port may influence model generalization | Ask Aleah to evaluate model performance with and without the feature |
| Live capture may not reproduce all 52 features | Coordinate with Pou before finalizing the model schema |
| Timing units or packet-length definitions may differ | Document and test calculation conventions |

## 6. Preliminary Assessment

All 52 features have been identified and documented.

Most are technically obtainable or calculable from packet-level traffic, provided the capture system supports bidirectional flow tracking and the necessary packet metadata.

However, **live compatibility has not yet been validated**. Features requiring CICFlowMeter-specific calculations need further testing before they can be considered fully supported.

## 7. Next Actions

1. Share the feature schema and this assessment with Pou.
2. Confirm which features the planned capture tool can reproduce.
3. Validate feature calculations against representative captured traffic.
4. Coordinate with Aleah before excluding or changing features.
5. Update the schema and documentation if feature compatibility issues are discovered.

**Status:** Preliminary assessment completed; live-capture verification pending.