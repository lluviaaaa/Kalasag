import pathlib
pkg = pathlib.Path.home() / 'cfm-work/venv/lib/python3.12/site-packages/cicflowmeter'
f_time = pkg / 'features/packet_time.py'
t = f_time.read_text()

old_iat = """        return [
            float(packets[i].time - packets[i - 1].time) for i in range(1, len(packets))
        ]"""
new_iat = """        return [
            float(packets[i].time - packets[i - 1].time) for i in range(1, len(packets))
            if float(packets[i].time - packets[i - 1].time) > 0.0
        ] or [0.0]"""

t = t.replace(old_iat, new_iat)
f_time.write_text(t)
print("IAT calculation patched successfully!")
