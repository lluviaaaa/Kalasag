import os, pandas as pd
M = {
 'Destination Port':'dst_port','Flow Duration':'flow_duration','Total Fwd Packets':'tot_fwd_pkts',
 'Total Length of Fwd Packets':'totlen_fwd_pkts',
 'Fwd Packet Length Max':'fwd_pkt_len_max','Fwd Packet Length Min':'fwd_pkt_len_min',
 'Fwd Packet Length Mean':'fwd_pkt_len_mean','Fwd Packet Length Std':'fwd_pkt_len_std',
 'Bwd Packet Length Max':'bwd_pkt_len_max','Bwd Packet Length Min':'bwd_pkt_len_min',
 'Bwd Packet Length Mean':'bwd_pkt_len_mean','Bwd Packet Length Std':'bwd_pkt_len_std',
 'Flow Bytes/s':'flow_byts_s','Flow Packets/s':'flow_pkts_s',
 'Flow IAT Mean':'flow_iat_mean','Flow IAT Std':'flow_iat_std','Flow IAT Max':'flow_iat_max','Flow IAT Min':'flow_iat_min',
 'Fwd IAT Total':'fwd_iat_tot','Fwd IAT Mean':'fwd_iat_mean','Fwd IAT Std':'fwd_iat_std','Fwd IAT Max':'fwd_iat_max','Fwd IAT Min':'fwd_iat_min',
 'Bwd IAT Total':'bwd_iat_tot','Bwd IAT Mean':'bwd_iat_mean','Bwd IAT Std':'bwd_iat_std','Bwd IAT Max':'bwd_iat_max','Bwd IAT Min':'bwd_iat_min',
 'Fwd Header Length':'fwd_header_len','Bwd Header Length':'bwd_header_len',
 'Fwd Packets/s':'fwd_pkts_s','Bwd Packets/s':'bwd_pkts_s',
 'Min Packet Length':'pkt_len_min','Max Packet Length':'pkt_len_max',
 'Packet Length Mean':'pkt_len_mean','Packet Length Std':'pkt_len_std','Packet Length Variance':'pkt_len_var',
 'FIN Flag Count':'fin_flag_cnt','PSH Flag Count':'psh_flag_cnt','ACK Flag Count':'ack_flag_cnt',
 'Average Packet Size':'pkt_size_avg','Subflow Fwd Bytes':'subflow_fwd_byts',
 'Init_Win_bytes_forward':'init_fwd_win_byts','Init_Win_bytes_backward':'init_bwd_win_byts',
 'act_data_pkt_fwd':'fwd_act_data_pkts','min_seg_size_forward':'fwd_seg_size_min',
}
tr = pd.read_parquet(os.path.expanduser('~/cfm-work/cleaned.parquet'), columns=list(M))
tl = pd.read_csv(os.path.expanduser('~/cfm-work/flows.csv'))
rows = []
for name, col in M.items():
    t = tl[col].astype(float)
    if ('IAT' in name) or name == 'Flow Duration':
        t = t * 1e6
    if name in ('FIN Flag Count', 'PSH Flag Count', 'ACK Flag Count'):
        t = (t > 0).astype(float)
    rows.append([name, tr[name].quantile(.5), t.quantile(.5), tr[name].quantile(.9), t.quantile(.9)])
out = pd.DataFrame(rows, columns=['feature','train_p50','tool_p50','train_p90','tool_p90'])
out.to_csv(os.path.expanduser('~/cfm-work/value_check.csv'), index=False)
pd.set_option('display.width', 200)
print(out.to_string(index=False, float_format=lambda x: '%.4g' % x))
