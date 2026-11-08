import pathlib
pkg = pathlib.Path.home() / 'cfm-work/venv/lib/python3.12/site-packages/cicflowmeter'
f = pkg / 'flow.py'
t = f.read_text()
old = 'self.packets = [(packet, direction)]  # Add the first packet'
new = 'self.packets = []  # first packet is added by add_packet() (patch5: avoids counting it twice)'
assert t.count(old) == 1, 'patch5: expected line not found exactly once'
f.write_text(t.replace(old, new))
print('Patch 5 applied successfully')
