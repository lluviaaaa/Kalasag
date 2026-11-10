import csv
from pathlib import Path

import pytest

from src.response import simulated_block
from src.response.simulated_block import simulate_block


def test_public_ip_is_refused_and_nothing_is_written(tmp_path):
    with pytest.raises(ValueError):
        simulate_block('8.8.8.8', 'DoS', 0.99, runtime=tmp_path)
    assert not (tmp_path / 'alerts.csv').exists()


def test_block_is_logged_once_and_never_executed(tmp_path):
    r = simulate_block('192.0.2.7', 'DoS', 0.97, runtime=tmp_path)
    assert r['executed'] is False and r['newly_blocked'] is True
    assert r['command'] == 'sudo iptables -A INPUT -s 192.0.2.7 -j DROP'
    again = simulate_block('192.0.2.7', 'DoS', 0.95, runtime=tmp_path)
    assert again['newly_blocked'] is False
    with (tmp_path / 'blocklist.csv').open() as f:
        assert len(list(csv.DictReader(f))) == 1
    with (tmp_path / 'alerts.csv').open() as f:
        assert len(list(csv.DictReader(f))) == 2


def test_module_has_no_way_to_run_commands():
    text = Path(simulated_block.__file__).read_text()
    for word in ('subprocess', 'os.system', 'Popen', 'import os'):
        assert word not in text
