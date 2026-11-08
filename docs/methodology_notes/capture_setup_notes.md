# CICFlowMeter setup notes (Aleah, Nov 8, 2026)

## What this is
The live-capture feature extractor: Python cicflowmeter v0.4.2 on Ubuntu 24.04 (Python 3.12.3) with source patches. Final feature table: docs/methodology_notes/feature_keep_drop.md. Version 0.5.0 crashes on start (a bool/split error), so 0.4.2 is pinned.

## Install (the victim VM needs a temporary internet connection for this)
    sudo apt update
    sudo apt install python3-venv python3-pip libpcap-dev build-essential python3-dev patch
    python3 -m venv ~/cfm-work/venv
    source ~/cfm-work/venv/bin/activate
    pip install cicflowmeter==0.4.2
    cd ~/cfm-work/venv/lib/python3.12/site-packages/cicflowmeter
    patch -p1 < REPO/tools/cicflowmeter/cicflowmeter-0.4.2-kalasag.patch
    find . -name __pycache__ -type d -prune -exec rm -rf {} +

The last line is REQUIRED. The patch changes utils.py without changing its file size, so Python can keep running the old compiled copy. On the first clean-install test this gave wrong Flow IAT Min values (52.6% zeros instead of 21.9%) with no error message.

## Run (offline mode, the mode that was validated)
    cicflowmeter -f capture.pcap -c flows.csv

## What the patch changes, and why
1. Packet lengths: the tool used the whole Ethernet frame (never below 54 bytes). Training counts payload only. Now TCP/UDP payload.
2. Header lengths: the tool used the IP header (always 20). Training uses the transport header. Now TCP data offset x 4, and 20 for UDP (approximate: training UDP/DNS rows use 20 or 32, never 8).
3. Initial window: starts at -1, as in training, when no TCP packet was seen in that direction.
4. Library bug: the first packet was added to every flow twice (flow.py).
5. Library bug: statistics returned zeros for a list with one value, which hid the only gap of 2-packet flows (utils.py).
6. Not patched: Active and Idle are always 0, so those 6 features are dropped.
Retired and not used: patch3 (Active/Idle timeout) and patch4 (zero-gap filter). Their scripts are not in the repo.

## Rules applied in the live layer (src/live/convert.py)
Multiply the 15 time features by 1,000,000 (seconds to microseconds). Any flag count above 0 becomes 1.

## Validation (one Wi-Fi capture, 543 flows, pcap not committed)
- Totals: 43,217 packets and 38,276,976 payload bytes match the pcap (difference 0). Before the duplicate-first-packet fix: 543 extra packets, 84,057 extra bytes.
- Three flows checked by hand against the pcap: packet counts and IAT min, max, mean match.
- Flow IAT Min equal to 0 (flows with 2 or more packets): 100% before the fixes, 21.9% after (pcap 22.4% by conversation, from Wi-Fi frames with identical timestamps; training 2.8%).
- A clean install plus the patch file reproduces flows.csv exactly (0 of 82 columns differ), after clearing __pycache__.
- Init window: UDP flows 246 of 246 show -1; TCP flows with no reply show -1; only 5 forward and 1 backward TCP flows show 0 (likely resets).

## Known limits
- One Wi-Fi capture of browsing, no attack traffic yet.
- UDP header length and min_seg_size_forward are approximate (training mixes 20 and 32).
- Ethernet padding on very small frames is untested.
- Flows can run past 120 s (longest seen 143 s; training stops at 120 s).
- Zero-duration flows: 22 of 543, all single-packet, with rates of 0 (not NaN or infinity).

## Pinned versions (pip freeze of the working venv)

    cicflowmeter==0.4.2
    numpy==2.5.4
    requests==2.34.2
    scapy==2.8.0
    scipy==1.18.1
