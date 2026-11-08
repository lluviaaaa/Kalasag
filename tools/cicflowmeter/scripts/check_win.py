import os, pandas as pd
f = pd.read_csv(os.path.expanduser('~/cfm-work/flows.csv'))
def label(v):
    return '-1' if v == -1 else ('0' if v == 0 else '>0')
for c in ['init_fwd_win_byts', 'init_bwd_win_byts']:
    print('---', c, '---')
    print(pd.crosstab(f['protocol'], f[c].map(label)))
tcp = f[f['protocol'] == 6]
print('--- TCP flows with no backward packets: init_bwd value ---')
print(tcp[tcp['tot_bwd_pkts'] == 0]['init_bwd_win_byts'].value_counts())
print('--- smallest and largest window values overall ---')
print(f[['init_fwd_win_byts', 'init_bwd_win_byts']].agg(['min', 'max']))
