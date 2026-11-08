import pathlib

pkg = pathlib.Path.home() / 'cfm-work/venv/lib/python3.12/site-packages/cicflowmeter'
PAYLOAD = '(len(packet["TCP"].payload) if "TCP" in packet else (len(packet["UDP"].payload) if "UDP" in packet else 0))'
HEADER = '(packet["TCP"].dataofs * 4 if "TCP" in packet and packet["TCP"].dataofs else (20 if "UDP" in packet else 0))'

f_flow = pkg / 'flow.py'
t = f_flow.read_text()
t = t.replace('PacketDirection.FORWARD: 0, PacketDirection.REVERSE: 0', 'PacketDirection.FORWARD: -1, PacketDirection.REVERSE: -1')
t = t.replace('self.init_window_size[direction] == 0:', 'self.init_window_size[direction] == -1:')
f_flow.write_text(t)

f_bytes = pkg / 'features/flow_bytes.py'
t = f_bytes.read_text()
old_h = """    def _header_size(self, packet):
        # Calculate IP header size if IP layer exists
        if IP in packet:
            ihl = packet[IP].ihl
            # Handle case where ihl might be None (though ideally shouldn't happen with proper packet construction)
            if ihl is None:
                # Default to 20 bytes (standard IPv4 header without options)
                # TODO: Consider logging a warning here
                return 20
            else:
                return ihl * 4
        else:
            # No IP layer found
            return 0"""
new_h = f"""    def _header_size(self, packet):\n        return {HEADER}"""
t = t.replace(old_h, new_h)
t = t.replace('len(packet)', PAYLOAD)
f_bytes.write_text(t)

f_len = pkg / 'features/packet_length.py'
t = f_len.read_text()
t = t.replace('len(packet)', PAYLOAD)
t = t.replace('packet["IP"].ihl * 4', HEADER)
f_len.write_text(t)
print("Patch applied successfully")
