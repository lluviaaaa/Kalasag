'''Simulated detect -> flag/block for Kalasag.

SAFETY: this module only WRITES two CSV files (alerts.csv, blocklist.csv) and returns
the firewall command as TEXT. It cannot run any command, and it refuses public IPs.
'''
import csv
import ipaddress
from datetime import datetime
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[2] / 'runtime'
ALERT_COLS = ['time', 'mode', 'src_ip', 'predicted_class', 'confidence']
BLOCK_COLS = ['time', 'src_ip', 'reason', 'command_not_executed']


def check_ip(src_ip):
    '''Return the IP as text, or raise ValueError if it is not a private/lab address.'''
    ip = ipaddress.ip_address(str(src_ip).strip())
    if not ip.is_private:
        raise ValueError(f'Refusing {ip}: only private or documentation addresses are allowed')
    return str(ip)


def firewall_command(src_ip):
    return f'sudo iptables -A INPUT -s {check_ip(src_ip)} -j DROP'


def _append(path, cols, row):
    path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not path.exists()
    with path.open('a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=cols, lineterminator=chr(10))
        if is_new:
            writer.writeheader()
        writer.writerow(row)


def _blocked_ips(path):
    if not path.exists():
        return set()
    with path.open(newline='', encoding='utf-8') as f:
        return {r['src_ip'] for r in csv.DictReader(f)}


def simulate_block(src_ip, predicted, confidence, mode='offline', runtime=None):
    '''Log an alert and 'block' the source by writing it to blocklist.csv. Nothing is executed.'''
    runtime = Path(runtime) if runtime else RUNTIME
    ip = check_ip(src_ip)                      # raises before anything is written
    command = firewall_command(ip)
    now = datetime.now().isoformat(timespec='seconds')
    _append(runtime / 'alerts.csv', ALERT_COLS, {
        'time': now, 'mode': mode, 'src_ip': ip,
        'predicted_class': predicted, 'confidence': round(float(confidence), 4)})
    newly = ip not in _blocked_ips(runtime / 'blocklist.csv')
    if newly:
        _append(runtime / 'blocklist.csv', BLOCK_COLS, {
            'time': now, 'src_ip': ip, 'reason': predicted, 'command_not_executed': command})
    return {'src_ip': ip, 'command': command, 'newly_blocked': newly, 'executed': False}
