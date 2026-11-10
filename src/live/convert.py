'''Live-layer rules from docs/methodology_notes/feature_keep_drop.md.
Apply them to CICFlowMeter output BEFORE the saved scaler.'''
import numpy as np
import pandas as pd

# CICFlowMeter v0.4.2 (patched) column -> training feature name (the 46 KEEP features)
COLUMN_MAP = {
    'dst_port': 'Destination Port', 'flow_duration': 'Flow Duration',
    'tot_fwd_pkts': 'Total Fwd Packets', 'totlen_fwd_pkts': 'Total Length of Fwd Packets',
    'fwd_pkt_len_max': 'Fwd Packet Length Max', 'fwd_pkt_len_min': 'Fwd Packet Length Min',
    'fwd_pkt_len_mean': 'Fwd Packet Length Mean', 'fwd_pkt_len_std': 'Fwd Packet Length Std',
    'bwd_pkt_len_max': 'Bwd Packet Length Max', 'bwd_pkt_len_min': 'Bwd Packet Length Min',
    'bwd_pkt_len_mean': 'Bwd Packet Length Mean', 'bwd_pkt_len_std': 'Bwd Packet Length Std',
    'flow_byts_s': 'Flow Bytes/s', 'flow_pkts_s': 'Flow Packets/s',
    'flow_iat_mean': 'Flow IAT Mean', 'flow_iat_std': 'Flow IAT Std',
    'flow_iat_max': 'Flow IAT Max', 'flow_iat_min': 'Flow IAT Min',
    'fwd_iat_tot': 'Fwd IAT Total', 'fwd_iat_mean': 'Fwd IAT Mean', 'fwd_iat_std': 'Fwd IAT Std',
    'fwd_iat_max': 'Fwd IAT Max', 'fwd_iat_min': 'Fwd IAT Min',
    'bwd_iat_tot': 'Bwd IAT Total', 'bwd_iat_mean': 'Bwd IAT Mean', 'bwd_iat_std': 'Bwd IAT Std',
    'bwd_iat_max': 'Bwd IAT Max', 'bwd_iat_min': 'Bwd IAT Min',
    'fwd_header_len': 'Fwd Header Length', 'bwd_header_len': 'Bwd Header Length',
    'fwd_pkts_s': 'Fwd Packets/s', 'bwd_pkts_s': 'Bwd Packets/s',
    'pkt_len_min': 'Min Packet Length', 'pkt_len_max': 'Max Packet Length',
    'pkt_len_mean': 'Packet Length Mean', 'pkt_len_std': 'Packet Length Std',
    'pkt_len_var': 'Packet Length Variance',
    'fin_flag_cnt': 'FIN Flag Count', 'psh_flag_cnt': 'PSH Flag Count', 'ack_flag_cnt': 'ACK Flag Count',
    'pkt_size_avg': 'Average Packet Size', 'subflow_fwd_byts': 'Subflow Fwd Bytes',
    'init_fwd_win_byts': 'Init_Win_bytes_forward', 'init_bwd_win_byts': 'Init_Win_bytes_backward',
    'fwd_act_data_pkts': 'act_data_pkt_fwd', 'fwd_seg_size_min': 'min_seg_size_forward',
}
TIME_FEATURES = [
    'Flow Duration',
    'Flow IAT Mean', 'Flow IAT Std', 'Flow IAT Max', 'Flow IAT Min',
    'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min',
    'Bwd IAT Total', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min',
]
FLAG_FEATURES = ['FIN Flag Count', 'PSH Flag Count', 'ACK Flag Count']


def tool_to_training_frame(raw):
    '''Keep the 46 KEEP columns and rename them to the training names.'''
    missing = [c for c in COLUMN_MAP if c not in raw.columns]
    if missing:
        raise ValueError(f'CICFlowMeter output is missing columns: {missing}')
    return raw[list(COLUMN_MAP)].rename(columns=COLUMN_MAP).astype('float64')


def apply_live_rules(frame):
    '''Rule 1: seconds -> microseconds (x 1,000,000). Rule 2: flag counts > 0 become 1.'''
    x = frame.replace([np.inf, -np.inf], np.nan)
    x[TIME_FEATURES] = x[TIME_FEATURES] * 1_000_000
    flags = x[FLAG_FEATURES]
    x[FLAG_FEATURES] = (flags > 0).astype('float64').where(flags.notna())
    return x


def to_scaled(raw, scaler):
    '''Tool output -> scaled model input. Returns (scaled rows, mask of usable rows).
    Rows that still hold NaN cannot be classified; the caller logs and skips them.'''
    x = apply_live_rules(tool_to_training_frame(raw))
    cols = list(scaler.feature_names_in_)
    missing = [c for c in cols if c not in x.columns]
    if missing:
        raise ValueError(f'The scaler expects features the live layer does not provide: {missing}')
    x = x[cols]
    ok = x.notna().all(axis=1)
    scaled = pd.DataFrame(scaler.transform(x[ok]), columns=cols, index=x.index[ok])
    return scaled, ok
