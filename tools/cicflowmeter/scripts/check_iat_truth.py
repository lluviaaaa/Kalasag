import os, numpy as np, pandas as pd
from scapy.all import PcapReader, IP, TCP, UDP
g = {}
for p in PcapReader(os.path.expanduser('~/cfm-work/test.pcap')):
    if IP not in p:
        continue
    if TCP in p:
        pr, l4 = 6, p[TCP]
    elif UDP in p:
        pr, l4 = 17, p[UDP]
    else:
        continue
    a = (p[IP].src, l4.sport); b = (p[IP].dst, l4.dport)
    g.setdefault((pr,) + tuple(sorted([a, b])), []).append(float(p.time))
mins = []
for k, t in g.items():
    if len(t) >= 2:
        mins.append(np.diff(np.sort(t)).min())
mins = np.array(mins)
print('conversations in pcap:', len(g), ' with >=2 packets:', len(mins))
print('real share with min gap exactly 0:', round((mins == 0).mean(), 3), ' (training Flow IAT Min: 0.028)')
print('real share with min gap < 10 microseconds:', round((mins < 1e-5).mean(), 3))
tl = pd.read_csv(os.path.expanduser('~/cfm-work/flows.csv'))
print('--- tool zero-share now: flow / fwd / bwd IAT min ---')
print([round((tl[c] == 0).mean(), 3) for c in ['flow_iat_min', 'fwd_iat_min', 'bwd_iat_min']], ' (training: 0.028 / 0.259 / 0.409)')
print('--- 3 small TCP flows: real gaps vs tool ---')
s = tl[(tl['protocol'] == 6) & (tl['tot_fwd_pkts'] + tl['tot_bwd_pkts'] <= 8)].head(3)
for _, r in s.iterrows():
    a = (r['src_ip'], int(r['src_port'])); b = (r['dst_ip'], int(r['dst_port']))
    t = np.sort(g.get((6,) + tuple(sorted([a, b])), []))
    print(a, '->', b, ' tool fwd/bwd pkts:', r['tot_fwd_pkts'], r['tot_bwd_pkts'], ' pcap pkts:', len(t))
    print('  real gaps (s):', np.round(np.diff(t), 6).tolist())
    print('  tool flow_iat min/max/mean (s):', r['flow_iat_min'], r['flow_iat_max'], round(r['flow_iat_mean'], 6))
