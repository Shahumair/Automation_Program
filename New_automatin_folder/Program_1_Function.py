# simple_show_ip_int_brief.py

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetmikoTimeoutException, NetmikoAuthenticationException


class NetworkDevice:
    def __init__(self, name, host, username, password, secret, device_type):
        self.name = name
        self.host = host
        self.username = username
        self.password = password
        self.secret = secret      # enable password
        self.device_type = device_type

    def show_ip_int_brief(self):
        """Connects, runs the command, returns the output (very simple)."""
        params = {
            "device_type": self.device_type,
            "host": self.host,
            "username": self.username,
            "password": self.password,
            "secret": self.secret,
            "fast_cli": True,
        }
        try:
            conn = ConnectHandler(**params)
            if self.secret:
                conn.enable()
            out = conn.send_command("show ip interface brief")
            conn.disconnect()
            return out
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
            return f"[ERROR] {e}"


class CiscoDevice(NetworkDevice):
    def __init__(self, name, host, username, password, secret):
        super().__init__(name, host, username, password, secret, "cisco_ios")


class AristaDevice(NetworkDevice):
    def __init__(self, name, host, username, password, secret):
        super().__init__(name, host, username, password, secret, "arista_eos")


def main():
    # Change IPs if yours differ
    devices = [
        CiscoDevice("R1", "192.168.10.144", "R1", "ciscoR1", "cisco"),
        CiscoDevice("R2", "192.168.10.145", "R2", "ciscoR2", "cisco"),
        AristaDevice("R3", "192.168.10.140", "R3", "aristaR3", "arista"),
    ]

    for d in devices:
        print("=" * 60)
        print(f"{d.name}  ({d.host})")
        print(d.show_ip_int_brief().strip())
        print("=" * 60)


if __name__ == "__main__":
    main()
