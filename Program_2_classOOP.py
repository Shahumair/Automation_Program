from netmiko import ConnectHandler


class NetworkDevice:
    """Base network device with minimal OOP for SSH and show commands."""
    def __init__(self, hostname, mgmt_ip, username, password, enable_secret):
        self.hostname = hostname
        self.mgmt_ip = mgmt_ip
        self.username = username
        self.password = password
        self.enable_secret = enable_secret
        self.conn = None  # Netmiko connection handle

    # Subclasses must provide a Netmiko device_type string
    @property
    def device_type(self):
        return "generic_term"  # overridden by subclasses

    # Shared/common command for all vendors
    def common_command(self):
        return "show ip interface brief"

    # Vendor-specific extra command (overridden by subclasses)
    def vendor_command(self):
        return "show version"

    # Connect, enable, run a single show command, return output
    def connect(self):
        self.conn = ConnectHandler(
            device_type=self.device_type,
            host=self.mgmt_ip,
            username=self.username,
            password=self.password,
            secret=self.enable_secret,
        )
        self.conn.enable()

    def run_show(self, command):
        return self.conn.send_command(command)

    def disconnect(self):
        self.conn.disconnect()

    # Convenience workflow
    def run_basic_checks(self):
        print(f"\n=== {self.hostname} ({self.mgmt_ip}) ===")
        self.connect()
        output1 = self.run_show(self.common_command())
        output2 = self.run_show(self.vendor_command())
        print(f"\n# {self.common_command()}\n{output1}")
        print(f"\n# {self.vendor_command()}\n{output2}")
        self.disconnect()


class CiscoRouter(NetworkDevice):
    @property
    def device_type(self):
        return "cisco_ios"

    def vendor_command(self):
        # A Cisco-specific command to contrast with Arista below
        return "show cdp neighbors"


class AristaRouter(NetworkDevice):
    @property
    def device_type(self):
        return "arista_eos"

    def vendor_command(self):
        # Arista-specific counterpart
        return "show lldp neighbors"


def build_lab_devices():
    """Create your three devices (R1, R2 = Cisco ; R3 = Arista)."""
    r1 = CiscoRouter(
        hostname="R1",
        mgmt_ip="192.168.10.144",
        username="R1",
        password="ciscoR1",
        enable_secret="cisco",
    )
    r2 = CiscoRouter(
        hostname="R2",
        mgmt_ip="192.168.10.145",
        username="R2",
        password="ciscoR2",
        enable_secret="cisco",
    )
    r3 = AristaRouter(
        hostname="R3",
        mgmt_ip="192.168.10.146",
        username="R3",
        password="aristaR3",
        enable_secret="arista",
    )
    return [r1, r2, r3]


if __name__ == "__main__":
    devices = build_lab_devices()
    for dev in devices:
        dev.run_basic_checks()
