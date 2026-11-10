'''Does scapy count Ethernet padding as payload?  Usage: python tools/check_padding.py capture.pcap'''
import sys
from scapy.all import PcapReader, IP, TCP, UDP

bad = total = 0
for p in PcapReader(sys.argv[1]):
    if IP not in p:
        continue
    if TCP in p:
        l4_len = p[TCP].dataofs * 4
        shown = len(p[TCP].payload)
    elif UDP in p:
        l4_len = 8
        shown = len(p[UDP].payload)
    else:
        continue
    true = p[IP].len - p[IP].ihl * 4 - l4_len
    total += 1
    if shown != true:
        bad += 1
        if bad <= 5:
            print('mismatch: tool counts', shown, 'bytes, IP header says', true, '|', p.summary())
print('packets checked:', total, '| mismatches:', bad)
