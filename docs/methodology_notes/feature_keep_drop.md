## CICFlowMeter Feature List
Tool: Python cicflowmeter v0.4.2 (Source patched for payload lengths, transport headers, init window, and IAT min)
Date: 2026-11-05
PCAP used: test.pcap (43,364 packets, 543 flows)

| Feature | Status | CICFlowMeter column name | Note |
|---|---|---|---|
| Destination Port | KEEP | dst_port | Same scale; read directly from packet header |
| Flow Duration | KEEP | flow_duration | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Total Fwd Packets | KEEP | tot_fwd_pkts | Same scale; direct packet count |
| Total Length of Fwd Packets | KEEP | totlen_fwd_pkts | Same scale (patched tool to sum TCP/UDP payload bytes only) |
| Fwd Packet Length Max | KEEP | fwd_pkt_len_max | Same scale (patched tool to use TCP/UDP payload bytes only) |
| Fwd Packet Length Min | KEEP | fwd_pkt_len_min | Same scale (patched tool to use TCP/UDP payload bytes only) |
| Fwd Packet Length Mean | KEEP | fwd_pkt_len_mean | Same scale (patched tool to use TCP/UDP payload bytes only) |
| Fwd Packet Length Std | KEEP | fwd_pkt_len_std | Same scale (patched tool to use TCP/UDP payload bytes only) |
| Bwd Packet Length Max | KEEP | bwd_pkt_len_max | Same scale (patched tool to use TCP/UDP payload bytes only) |
| Bwd Packet Length Min | KEEP | bwd_pkt_len_min | Same scale (patched tool to use TCP/UDP payload bytes only) |
| Bwd Packet Length Mean | KEEP | bwd_pkt_len_mean | Same scale (patched tool to use TCP/UDP payload bytes only) |
| Bwd Packet Length Std | KEEP | bwd_pkt_len_std | Same scale (patched tool to use TCP/UDP payload bytes only) |
| Flow Bytes/s | KEEP | flow_byts_s | Same scale (computed from patched payload byte totals per second) |
| Flow Packets/s | KEEP | flow_pkts_s | Same scale; packets per second |
| Flow IAT Mean | KEEP | flow_iat_mean | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Flow IAT Std | KEEP | flow_iat_std | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Flow IAT Max | KEEP | flow_iat_max | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Flow IAT Min | KEEP | flow_iat_min | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Fwd IAT Total | KEEP | fwd_iat_tot | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Fwd IAT Mean | KEEP | fwd_iat_mean | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Fwd IAT Std | KEEP | fwd_iat_std | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Fwd IAT Max | KEEP | fwd_iat_max | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Fwd IAT Min | KEEP | fwd_iat_min | Unit difference: multiply by 1000000 (seconds to microseconds; patched 0.0 gap bug) |
| Bwd IAT Total | KEEP | bwd_iat_tot | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Bwd IAT Mean | KEEP | bwd_iat_mean | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Bwd IAT Std | KEEP | bwd_iat_std | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Bwd IAT Max | KEEP | bwd_iat_max | Unit difference: multiply by 1000000 (seconds to microseconds) |
| Bwd IAT Min | KEEP | bwd_iat_min | Unit difference: multiply by 1000000 (seconds to microseconds; patched 0.0 gap bug) |
| Fwd Header Length | KEEP | fwd_header_len | Same scale (patched tool to sum TCP dataofs*4 or UDP 8 bytes) |
| Bwd Header Length | KEEP | bwd_header_len | Same scale (patched tool to sum TCP dataofs*4 or UDP 8 bytes) |
| Fwd Packets/s | KEEP | fwd_pkts_s | Same scale; forward packets per second |
| Bwd Packets/s | KEEP | bwd_pkts_s | Same scale; backward packets per second |
| Min Packet Length | KEEP | pkt_len_min | Same scale (patched tool to use TCP/UDP payload bytes only) |
| Max Packet Length | KEEP | pkt_len_max | Same scale (patched tool to use TCP/UDP payload bytes only) |
| Packet Length Mean | KEEP | pkt_len_mean | Same scale (patched tool to use TCP/UDP payload bytes only) |
| Packet Length Std | KEEP | pkt_len_std | Same scale (patched tool to use TCP/UDP payload bytes only) |
| Packet Length Variance | KEEP | pkt_len_var | Same scale (patched tool to use TCP/UDP payload bytes only) |
| FIN Flag Count | KEEP | fin_flag_cnt | Live rule: convert any count > 0 to 1 (training data is binary 0/1) |
| PSH Flag Count | KEEP | psh_flag_cnt | Live rule: convert any count > 0 to 1 (training data is binary 0/1) |
| ACK Flag Count | KEEP | ack_flag_cnt | Live rule: convert any count > 0 to 1 (training data is binary 0/1) |
| Average Packet Size | KEEP | pkt_size_avg | Same scale (patched tool to use TCP/UDP payload bytes only) |
| Subflow Fwd Bytes | KEEP | subflow_fwd_byts | Same scale (patched tool to use TCP/UDP payload bytes only) |
| Init_Win_bytes_forward | KEEP | init_fwd_win_byts | Same scale (patched tool to default to -1 when no TCP packet is seen) |
| Init_Win_bytes_backward | KEEP | init_bwd_win_byts | Same scale (patched tool to default to -1 when no TCP packet is seen) |
| act_data_pkt_fwd | KEEP | fwd_act_data_pkts | Same scale; counts forward packets with TCP/UDP payload > 0 |
| min_seg_size_forward | KEEP | fwd_seg_size_min | Same scale (patched tool to use min forward transport header size) |
| Active Mean | DROP | none | Unverifiable due to broken subflow/timeout logic in Python cicflowmeter v0.4.2; remained 0 across all 543 test flows |
| Active Max | DROP | none | Unverifiable due to broken subflow/timeout logic in Python cicflowmeter v0.4.2; remained 0 across all 543 test flows |
| Active Min | DROP | none | Unverifiable due to broken subflow/timeout logic in Python cicflowmeter v0.4.2; remained 0 across all 543 test flows |
| Idle Mean | DROP | none | Unverifiable due to broken subflow/timeout logic in Python cicflowmeter v0.4.2; remained 0 across all 543 test flows |
| Idle Max | DROP | none | Unverifiable due to broken subflow/timeout logic in Python cicflowmeter v0.4.2; remained 0 across all 543 test flows |
| Idle Min | DROP | none | Unverifiable due to broken subflow/timeout logic in Python cicflowmeter v0.4.2; remained 0 across all 543 test flows |

**Totals:** KEEP: 46, DERIVE: 0, DROP: 6
