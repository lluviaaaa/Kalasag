## CICFlowMeter Feature List
Tool: Python cicflowmeter v0.4.2 (Source patched for payload and headers)
Date: 2026-11-04
PCAP used: test.pcap

| Feature | Status | CICFlowMeter column name | Note |
|---|---|---|---|
| Destination Port | KEEP | MANUAL_MATCH_NEEDED | Same scale (patched payload sizes) |
| Flow Duration | KEEP | flow_duration | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Total Fwd Packets | KEEP | tot_fwd_pkts | Same scale (patched payload sizes) |
| Total Length of Fwd Packets | KEEP | MANUAL_MATCH_NEEDED | Same scale (patched payload sizes) |
| Fwd Packet Length Max | KEEP | fwd_pkt_len_max | Same scale (patched payload sizes) |
| Fwd Packet Length Min | KEEP | fwd_pkt_len_min | Same scale (patched payload sizes) |
| Fwd Packet Length Mean | KEEP | fwd_pkt_len_mean | Same scale (patched payload sizes) |
| Fwd Packet Length Std | KEEP | fwd_pkt_len_std | Same scale (patched payload sizes) |
| Bwd Packet Length Max | KEEP | bwd_pkt_len_max | Same scale (patched payload sizes) |
| Bwd Packet Length Min | KEEP | bwd_pkt_len_min | Same scale (patched payload sizes) |
| Bwd Packet Length Mean | KEEP | bwd_pkt_len_mean | Same scale (patched payload sizes) |
| Bwd Packet Length Std | KEEP | bwd_pkt_len_std | Same scale (patched payload sizes) |
| Flow Bytes/s | KEEP | flow_byts_s | Same scale (patched payload sizes) |
| Flow Packets/s | KEEP | flow_pkts_s | Same scale (patched payload sizes) |
| Flow IAT Mean | KEEP | flow_iat_mean | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Flow IAT Std | KEEP | flow_iat_std | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Flow IAT Max | KEEP | flow_iat_max | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Flow IAT Min | KEEP | flow_iat_min | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Fwd IAT Total | KEEP | fwd_iat_tot | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Fwd IAT Mean | KEEP | fwd_iat_mean | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Fwd IAT Std | KEEP | fwd_iat_std | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Fwd IAT Max | KEEP | fwd_iat_max | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Fwd IAT Min | KEEP | fwd_iat_min | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Bwd IAT Total | KEEP | bwd_iat_tot | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Bwd IAT Mean | KEEP | bwd_iat_mean | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Bwd IAT Std | KEEP | bwd_iat_std | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Bwd IAT Max | KEEP | bwd_iat_max | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Bwd IAT Min | KEEP | bwd_iat_min | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Fwd Header Length | KEEP | fwd_header_len | Same scale (patched payload sizes) |
| Bwd Header Length | KEEP | bwd_header_len | Same scale (patched payload sizes) |
| Fwd Packets/s | KEEP | fwd_pkts_s | Same scale (patched payload sizes) |
| Bwd Packets/s | KEEP | bwd_pkts_s | Same scale (patched payload sizes) |
| Min Packet Length | KEEP | MANUAL_MATCH_NEEDED | Same scale (patched payload sizes) |
| Max Packet Length | KEEP | MANUAL_MATCH_NEEDED | Same scale (patched payload sizes) |
| Packet Length Mean | KEEP | pkt_len_mean | Same scale (patched payload sizes) |
| Packet Length Std | KEEP | pkt_len_std | Same scale (patched payload sizes) |
| Packet Length Variance | KEEP | MANUAL_MATCH_NEEDED | Same scale (patched payload sizes) |
| FIN Flag Count | KEEP | MANUAL_MATCH_NEEDED | Rule: convert any count > 0 to 1 |
| PSH Flag Count | KEEP | MANUAL_MATCH_NEEDED | Rule: convert any count > 0 to 1 |
| ACK Flag Count | KEEP | MANUAL_MATCH_NEEDED | Rule: convert any count > 0 to 1 |
| Average Packet Size | KEEP | MANUAL_MATCH_NEEDED | Same scale (patched payload sizes) |
| Subflow Fwd Bytes | KEEP | subflow_fwd_byts | Same scale (patched payload sizes) |
| Init_Win_bytes_forward | KEEP | MANUAL_MATCH_NEEDED | Rule: map UDP 0 to negative 1 |
| Init_Win_bytes_backward | KEEP | MANUAL_MATCH_NEEDED | Rule: map UDP 0 to negative 1 |
| act_data_pkt_fwd | KEEP | MANUAL_MATCH_NEEDED | Same scale (patched payload sizes) |
| min_seg_size_forward | KEEP | fwd_seg_size_min | Same scale (patched payload sizes) |
| Active Mean | DROP | none | Tool returns 0; notoriously inconsistent tool to tool |
| Active Max | DROP | none | Tool returns 0; notoriously inconsistent tool to tool |
| Active Min | DROP | none | Tool returns 0; notoriously inconsistent tool to tool |
| Idle Mean | DROP | none | Tool returns 0; notoriously inconsistent tool to tool |
| Idle Max | DROP | none | Tool returns 0; notoriously inconsistent tool to tool |
| Idle Min | DROP | none | Tool returns 0; notoriously inconsistent tool to tool |

**Totals:** KEEP: 46, DERIVE: 0, DROP: 6