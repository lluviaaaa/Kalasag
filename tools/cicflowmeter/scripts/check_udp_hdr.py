import os, pandas as pd
tr = pd.read_parquet(os.path.expanduser('~/cfm-work/cleaned.parquet'),
    columns=['Destination Port','Total Fwd Packets','Fwd Header Length','min_seg_size_forward','Init_Win_bytes_forward'])
d = tr[(tr['Destination Port'] == 53) & (tr['Init_Win_bytes_forward'] == -1)]
print('training UDP-like rows (port 53, window -1):', len(d))
print('--- training min_seg_size_forward ---')
print(d['min_seg_size_forward'].value_counts().head(5))
print('--- training Fwd Header Length per fwd packet ---')
print((d['Fwd Header Length'] / d['Total Fwd Packets']).round(1).value_counts().head(5))
tl = pd.read_csv(os.path.expanduser('~/cfm-work/flows.csv'))
u = tl[tl['protocol'] == 17]
print('--- tool UDP flows:', len(u), '---')
print(u['fwd_seg_size_min'].value_counts().head(5))
print((u['fwd_header_len'] / u['tot_fwd_pkts']).round(1).value_counts().head(5))
