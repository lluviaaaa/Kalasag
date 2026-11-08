## CICFlowMeter Feature List
Tool: Python cicflowmeter v0.4.2, source patched (see Build recipe below)
Date: 2026-11-06
PCAP used: test.pcap (43,364 packets, 43,217 IPv4 TCP/UDP packets, 543 flows). Not committed.

| Feature | Status | CICFlowMeter column name | Note |
|---|---|---|---|
| Destination Port | KEEP | dst_port | Same scale; read directly from the packet header. Provisional KEEP until the model-side confirmation (risk: the model may lean on the port, and lab attacks may use other ports) |
| Flow Duration | KEEP | flow_duration | Unit difference: multiply by 1000000 (seconds to microseconds). Tool flows can run past the training ceiling of about 120 s (longest seen: 143 s) |
| Total Fwd Packets | KEEP | tot_fwd_pkts | Same scale; packet count. Duplicate first packet fixed (patch5); total packets match the pcap exactly (difference 0) |
| Total Length of Fwd Packets | KEEP | totlen_fwd_pkts | Same scale (patched to TCP/UDP payload bytes only); total payload bytes match the pcap (difference 0). Ethernet padding on tiny frames not yet tested on the lab capture |
| Fwd Packet Length Max | KEEP | fwd_pkt_len_max | Same scale (patched to TCP/UDP payload bytes only); only the all-flow payload total was checked against the pcap (difference 0); per-packet values were compared with training by distribution. Ethernet padding on tiny frames not yet tested on the lab capture |
| Fwd Packet Length Min | KEEP | fwd_pkt_len_min | Same scale (patched to TCP/UDP payload bytes only); only the all-flow payload total was checked against the pcap (difference 0); per-packet values were compared with training by distribution. Ethernet padding on tiny frames not yet tested on the lab capture |
| Fwd Packet Length Mean | KEEP | fwd_pkt_len_mean | Same scale (patched to TCP/UDP payload bytes only); only the all-flow payload total was checked against the pcap (difference 0); per-packet values were compared with training by distribution. Ethernet padding on tiny frames not yet tested on the lab capture |
| Fwd Packet Length Std | KEEP | fwd_pkt_len_std | Same scale (patched to TCP/UDP payload bytes only); only the all-flow payload total was checked against the pcap (difference 0); per-packet values were compared with training by distribution. Ethernet padding on tiny frames not yet tested on the lab capture |
| Bwd Packet Length Max | KEEP | bwd_pkt_len_max | Same scale (patched to TCP/UDP payload bytes only); only the all-flow payload total was checked against the pcap (difference 0); per-packet values were compared with training by distribution. Ethernet padding on tiny frames not yet tested on the lab capture |
| Bwd Packet Length Min | KEEP | bwd_pkt_len_min | Same scale (patched to TCP/UDP payload bytes only); only the all-flow payload total was checked against the pcap (difference 0); per-packet values were compared with training by distribution. Ethernet padding on tiny frames not yet tested on the lab capture |
| Bwd Packet Length Mean | KEEP | bwd_pkt_len_mean | Same scale (patched to TCP/UDP payload bytes only); only the all-flow payload total was checked against the pcap (difference 0); per-packet values were compared with training by distribution. Ethernet padding on tiny frames not yet tested on the lab capture |
| Bwd Packet Length Std | KEEP | bwd_pkt_len_std | Same scale (patched to TCP/UDP payload bytes only); only the all-flow payload total was checked against the pcap (difference 0); per-packet values were compared with training by distribution. Ethernet padding on tiny frames not yet tested on the lab capture |
| Flow Bytes/s | KEEP | flow_byts_s | Same units (payload bytes per second, from the patched totals). Values depend on traffic mix; not converted |
| Flow Packets/s | KEEP | flow_pkts_s | Same units (packets per second); not converted. Values depend on traffic mix |
| Flow IAT Mean | KEEP | flow_iat_mean | Unit difference: multiply by 1000000 (seconds to microseconds). Duplicate first packet fixed (patch5) and single-gap statistics fixed (patch6); spot-checked by hand against the pcap on 3 flows (min, max and mean) |
| Flow IAT Std | KEEP | flow_iat_std | Unit difference: multiply by 1000000 (seconds to microseconds). Duplicate first packet fixed (patch5) and single-gap statistics fixed (patch6); same gap list as the hand-checked min, max and mean; the standard deviation itself was not checked by hand |
| Flow IAT Max | KEEP | flow_iat_max | Unit difference: multiply by 1000000 (seconds to microseconds). Duplicate first packet fixed (patch5) and single-gap statistics fixed (patch6); spot-checked by hand against the pcap on 3 flows (min, max and mean) |
| Flow IAT Min | KEEP | flow_iat_min | Unit difference: multiply by 1000000 (seconds to microseconds). Fixed by patch5 and patch6; zeros that remain in the Wi-Fi test pcap are real identical timestamps (tool 21.9% vs pcap 22.4%). Re-check on the lab capture |
| Fwd IAT Total | KEEP | fwd_iat_tot | Unit difference: multiply by 1000000 (seconds to microseconds). Duplicate first packet fixed (patch5) and single-gap statistics fixed (patch6); compared with training by distribution; not checked packet by packet |
| Fwd IAT Mean | KEEP | fwd_iat_mean | Unit difference: multiply by 1000000 (seconds to microseconds). Duplicate first packet fixed (patch5) and single-gap statistics fixed (patch6); compared with training by distribution; not checked packet by packet |
| Fwd IAT Std | KEEP | fwd_iat_std | Unit difference: multiply by 1000000 (seconds to microseconds). Duplicate first packet fixed (patch5) and single-gap statistics fixed (patch6); compared with training by distribution; not checked packet by packet |
| Fwd IAT Max | KEEP | fwd_iat_max | Unit difference: multiply by 1000000 (seconds to microseconds). Duplicate first packet fixed (patch5) and single-gap statistics fixed (patch6); compared with training by distribution; not checked packet by packet |
| Fwd IAT Min | KEEP | fwd_iat_min | Unit difference: multiply by 1000000 (seconds to microseconds). Duplicate first packet fixed (patch5) and single-gap statistics fixed (patch6); compared with training by distribution; not checked packet by packet |
| Bwd IAT Total | KEEP | bwd_iat_tot | Unit difference: multiply by 1000000 (seconds to microseconds). Duplicate first packet fixed (patch5) and single-gap statistics fixed (patch6); compared with training by distribution; not checked packet by packet |
| Bwd IAT Mean | KEEP | bwd_iat_mean | Unit difference: multiply by 1000000 (seconds to microseconds). Duplicate first packet fixed (patch5) and single-gap statistics fixed (patch6); compared with training by distribution; not checked packet by packet |
| Bwd IAT Std | KEEP | bwd_iat_std | Unit difference: multiply by 1000000 (seconds to microseconds). Duplicate first packet fixed (patch5) and single-gap statistics fixed (patch6); compared with training by distribution; not checked packet by packet |
| Bwd IAT Max | KEEP | bwd_iat_max | Unit difference: multiply by 1000000 (seconds to microseconds). Duplicate first packet fixed (patch5) and single-gap statistics fixed (patch6); compared with training by distribution; not checked packet by packet |
| Bwd IAT Min | KEEP | bwd_iat_min | Unit difference: multiply by 1000000 (seconds to microseconds). Duplicate first packet fixed (patch5) and single-gap statistics fixed (patch6); compared with training by distribution; not checked packet by packet |
| Fwd Header Length | KEEP | fwd_header_len | Patched to transport header size (TCP dataofs*4, UDP = 20). Approximate for UDP: training UDP/DNS rows use 20 or 32 per packet |
| Bwd Header Length | KEEP | bwd_header_len | Patched to transport header size (TCP dataofs*4, UDP = 20). Approximate for UDP: training UDP/DNS rows use 20 or 32 per packet |
| Fwd Packets/s | KEEP | fwd_pkts_s | Same units (packets per second); not converted. Values depend on traffic mix |
| Bwd Packets/s | KEEP | bwd_pkts_s | Same units (packets per second); not converted. Values depend on traffic mix |
| Min Packet Length | KEEP | pkt_len_min | Same scale (patched to TCP/UDP payload bytes only); only the all-flow payload total was checked against the pcap (difference 0); per-packet values were compared with training by distribution. Ethernet padding on tiny frames not yet tested on the lab capture |
| Max Packet Length | KEEP | pkt_len_max | Same scale (patched to TCP/UDP payload bytes only); only the all-flow payload total was checked against the pcap (difference 0); per-packet values were compared with training by distribution. Ethernet padding on tiny frames not yet tested on the lab capture |
| Packet Length Mean | KEEP | pkt_len_mean | Same scale (patched to TCP/UDP payload bytes only); only the all-flow payload total was checked against the pcap (difference 0); per-packet values were compared with training by distribution. Ethernet padding on tiny frames not yet tested on the lab capture |
| Packet Length Std | KEEP | pkt_len_std | Same scale (patched to TCP/UDP payload bytes only); only the all-flow payload total was checked against the pcap (difference 0); per-packet values were compared with training by distribution. Ethernet padding on tiny frames not yet tested on the lab capture |
| Packet Length Variance | KEEP | pkt_len_var | Same scale (patched to TCP/UDP payload bytes only); only the all-flow payload total was checked against the pcap (difference 0); per-packet values were compared with training by distribution. Ethernet padding on tiny frames not yet tested on the lab capture |
| FIN Flag Count | KEEP | fin_flag_cnt | Live rule: convert any count > 0 to 1 (training data is binary 0/1) |
| PSH Flag Count | KEEP | psh_flag_cnt | Live rule: convert any count > 0 to 1 (training data is binary 0/1) |
| ACK Flag Count | KEEP | ack_flag_cnt | Live rule: convert any count > 0 to 1 (training data is binary 0/1) |
| Average Packet Size | KEEP | pkt_size_avg | Same scale (patched to TCP/UDP payload bytes only); only the all-flow payload total was checked against the pcap (difference 0); per-packet values were compared with training by distribution. Ethernet padding on tiny frames not yet tested on the lab capture |
| Subflow Fwd Bytes | KEEP | subflow_fwd_byts | Same scale (patched to TCP/UDP payload bytes only); total payload bytes match the pcap (difference 0). Ethernet padding on tiny frames not yet tested on the lab capture |
| Init_Win_bytes_forward | KEEP | init_fwd_win_byts | Same scale. Patched to output -1 when no TCP packet was seen in that direction (checked: UDP flows 246 of 246 are -1; TCP flows without replies -1). No live rule needed |
| Init_Win_bytes_backward | KEEP | init_bwd_win_byts | Same scale. Patched to output -1 when no TCP packet was seen in that direction (checked: UDP flows 246 of 246 are -1; TCP flows without replies -1). No live rule needed |
| act_data_pkt_fwd | KEEP | fwd_act_data_pkts | Counts forward packets with TCP/UDP payload > 0; same kind of count as training. Approximate: not verified beyond scale (longer flows in the test capture) |
| min_seg_size_forward | KEEP | fwd_seg_size_min | Patched to the minimum forward transport header size (TCP dataofs*4, UDP = 20). Approximate for UDP (training uses 20 or 32) |
| Active Mean | DROP | none | DROP: the tool returned 0 in all 543 test flows, including flows with 45 to 48 second gaps in the pcap, so v0.4.2 produces no usable value. Not validated against training |
| Active Max | DROP | none | DROP: the tool returned 0 in all 543 test flows, including flows with 45 to 48 second gaps in the pcap, so v0.4.2 produces no usable value. Not validated against training |
| Active Min | DROP | none | DROP: the tool returned 0 in all 543 test flows, including flows with 45 to 48 second gaps in the pcap, so v0.4.2 produces no usable value. Not validated against training |
| Idle Mean | DROP | none | DROP: the tool returned 0 in all 543 test flows, including flows with 45 to 48 second gaps in the pcap, so v0.4.2 produces no usable value. Not validated against training |
| Idle Max | DROP | none | DROP: the tool returned 0 in all 543 test flows, including flows with 45 to 48 second gaps in the pcap, so v0.4.2 produces no usable value. Not validated against training |
| Idle Min | DROP | none | DROP: the tool returned 0 in all 543 test flows, including flows with 45 to 48 second gaps in the pcap, so v0.4.2 produces no usable value. Not validated against training |

**Totals:** KEEP: 46, DERIVE: 0, DROP: 6

## Live-layer rules (apply before the saved scaler)
1. Multiply the 15 time features (Flow Duration and all 14 IAT columns) by 1000000. Do not convert the packets-per-second rates.
2. FIN, PSH and ACK Flag Count: any value above 0 becomes 1.
3. Init_Win_bytes_forward and backward: no conversion; the patched tool already outputs -1 when no TCP packet was seen.
4. Use only the 46 KEEP columns in the training order from feature_schema.json. Source and destination IP are for the simulated block only, never model features.
5. Rows that still contain NaN or infinity after these steps cannot be classified; log and skip them.

## Build recipe
Install cicflowmeter==0.4.2, then apply in this order: patch2.py (payload lengths, TCP/UDP header sizes with UDP = 20, init window -1), patch5.py (first packet was added to every flow twice), patch6.py (statistics for lists with a single value). patch3 and patch4 are not used. Reproducible form: tools/cicflowmeter/cicflowmeter-0.4.2-kalasag.patch (see docs/methodology_notes/capture_setup_notes.md). The same recipe must be applied on the victim VM.

## Known limits
- Validated on one Wi-Fi browsing capture. Repeat the distribution and total checks on the VirtualBox lab capture with attack traffic.
- UDP header length and min_seg_size_forward are approximate (training mixes 20 and 32 for UDP/DNS).
- Ethernet padding on very small frames has not been tested.
- Active and Idle features cannot be produced by this tool version.
- Single-packet (zero-duration) flows: 22 of 543 in the test capture, all with one packet. Their rates come out as 0 (not NaN or infinity), so they are classified, but the rates are approximate and were not compared with training.
