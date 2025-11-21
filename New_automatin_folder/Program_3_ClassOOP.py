
from netmiko import ConnectHandler
from datetime import datetime

class NetworkDevice:
    COMMON_CMD = "show ip interface brief"

    def __init__(self, hostname, mgmt_ip, username, password, secret):
        self.hostname = hostname
        self.mgmt_ip = mgmt_ip
        self.username = username
        self.password = password
        self.secret = secret
        self.conn = None
        self.config = ""

    # --- overridden by subclasses ---
    device_type = None
    def extra_command(self):
        return "show version"

    # --- shared workflow ---
    def connect(self):
        self.conn = ConnectHandler(
            device_type=self.device_type,
            host=self.mgmt_ip,
            username=self.username,
            password=self.password,
            secret=self.secret,
        )
        self.conn.enable()

    def get_info(self):
        print(f"\n=== {self.hostname} ({self.mgmt_ip}) [{self.device_type}] ===")
        out1 = self.conn.send_command(self.COMMON_CMD)
        print(f"\n# {self.COMMON_CMD}\n{out1}")

        extra = self.extra_command()
        out2 = self.conn.send_command(extra)
        print(f"\n# {extra}\n{out2}")

        self.config = self.conn.send_command("show running-config")

    def save_config(self):
        fname = f"{self.hostname}_running_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(fname, "w") as f:
            f.write(self.config)
        print(f"\n[Saved] {fname}")

    def disconnect(self):
        self.conn.disconnect()


class CiscoDevice(NetworkDevice):
    device_type = "cisco_ios"
    def extra_command(self):
        return "show cdp neighbors"


class AristaDevice(NetworkDevice):
    device_type = "arista_eos"
    def extra_command(self):
        return "show lldp neighbors"


if __name__ == "__main__":
    devices = [
        CiscoDevice("R1", "192.168.10.144", "R1", "ciscoR1", "cisco"),
        CiscoDevice("R2", "192.168.10.145", "R2", "ciscoR2", "cisco"),
        AristaDevice("R3", "192.168.10.146", "R3", "aristaR3", "arista"),
    ]

    for d in devices:
        d.connect()
        d.get_info()
        d.save_config()
        d.disconnect()