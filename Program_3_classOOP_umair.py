

from netmiko import ConnectHandler
from datetime import datetime

class NetworkDevice:
    def __init__(self, device_type, host, username, password, secret, name):
        self.device = {
            "device_type": device_type,
            "host": host,
            "username": username,
            "password": password,
            "secret": secret,
        }
        self.name = name
        self.conn = None
        self.config = ""

    def connect(self):
        self.conn = ConnectHandler(**self.device)
        self.conn.enable()

    def get_info(self):
        common = "show ip interface brief"
        if self.device["device_type"] == "cisco_ios":
            vendor_cmd = "show cdp neighbors"
        else:  # arista_eos
            vendor_cmd = "show lldp neighbors"

        print(f"\n=== {self.name} ({self.device['host']}) ===")
        print(f"\n# {common}\n{self.conn.send_command(common)}")
        print(f"\n# {vendor_cmd}\n{self.conn.send_command(vendor_cmd)}")
        self.config = self.conn.send_command("show running-config")

    def save_config(self):
        fn = f"{self.name}_running_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(fn, "w") as f:
            f.write(self.config)
        print(f"\n[Saved] {fn}")

# ---- Your three devices
devices = [
    NetworkDevice("cisco_ios",  "192.168.10.144", "R1", "ciscoR1",   "cisco",  "R1_Cisco"),
    NetworkDevice("cisco_ios",  "192.168.10.145", "R2", "ciscoR2",   "cisco",  "R2_Cisco"),
    NetworkDevice("arista_eos", "192.168.10.146", "R3", "aristaR3",  "arista", "R3_Arista"),
]

if __name__ == "__main__":
    for d in devices:
        d.connect()
        d.get_info()
        d.save_config()
        d.conn.disconnect()
