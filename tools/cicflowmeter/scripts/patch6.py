import pathlib
pkg = pathlib.Path.home() / 'cfm-work/venv/lib/python3.12/site-packages/cicflowmeter'
f = pkg / 'utils.py'
t = f.read_text()
old = 'if len(alist) > 1:'
new = 'if len(alist) > 0:'
assert t.count(old) == 1, 'patch6: expected line not found exactly once'
f.write_text(t.replace(old, new))
print('Patch 6 applied successfully')
