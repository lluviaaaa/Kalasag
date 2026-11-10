#!/usr/bin/env bash
# On the victim VM, from the Kalasag folder, venv active:
#   ./tools/run_windows.sh enp0s8 models/local/final_model.joblib
IFACE=$1
MODEL=$2
OUT=runtime/windows
mkdir -p $OUT
sudo -v
while true; do
  T=$(date +%s)
  sudo timeout 10 tcpdump -Z root -i $IFACE -p -w $OUT/$T.pcap 2>/dev/null
  cicflowmeter -f $OUT/$T.pcap -c $OUT/$T.csv > /dev/null 2>&1
  if [ -s $OUT/$T.csv ]; then
    python -m src.live.classify_csv $OUT/$T.csv --model $MODEL --mode live
  fi
done
