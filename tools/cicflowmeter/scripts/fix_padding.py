import pathlib

pkg = pathlib.Path.home() / 'cfm-work/venv/lib/python3.12/site-packages/cicflowmeter/features'
old = '(len(packet["TCP"].payload) if "TCP" in packet else (len(packet["UDP"].payload) if "UDP" in packet else 0))'
new = '(max(0, packet["IP"].len - packet["IP"].ihl * 4 - (packet["TCP"].dataofs * 4 if "TCP" in packet else 8)) if "IP" in packet and ("TCP" in packet or "UDP" in packet) else 0)'

for name in ('flow_bytes.py', 'packet_length.py'):
    p = pkg / name
    t = p.read_text()
    if new in t:
        print(f'{name}: already patched')
        continue
    count = t.count(old)
    assert count > 0, f'Expected pattern not found in {name}'
    p.write_text(t.replace(old, new))
    print(f'Patched {name}: {count} occurrences replaced')
