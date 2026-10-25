"""SIMULATED blocking. Runs only inside the isolated lab VM, never on a host or real network (PRD Section 10)."""
import csv, datetime

def log_alert(src_ip, predicted_class, confidence, path="alerts_log.csv"):
    with open(path, "a", newline="") as f:
        csv.writer(f).writerow([datetime.datetime.now().isoformat(), src_ip, predicted_class, f"{confidence:.3f}"])

def simulate_block(src_ip):
    # Placeholder: print what a real rule would look like. Wire up iptables/netsh in the VM at Step 27.
    print(f"[SIMULATED] would block {src_ip}")
