

from netmiko import ConnectHandler

# -------- Input data --------
ARP = [
    "192.168.10.1",
    "192.168.0.1",
    "192.168.10.104",
    "192.168.10.144",
    "192.168.10.145",
    "192.168.10.146",
    "192.168.10.89",
    "192.168.10.145",
]

devices = [
    {
        "name": "R1",
        "mgmt_ip": "192.168.10.144",
        "device_type": "cisco_ios",
        "username": "R1",
        "password": "ciscoR1",
        "secret": "cisco",
        "platform": "cisco",
    },
    {
        "name": "R2",
        "mgmt_ip": "192.168.10.145",
        "device_type": "cisco_ios",
        "username": "R2",
        "password": "ciscoR2",
        "secret": "cisco",
        "platform": "cisco",
    },
    {
        "name": "R3",
        "mgmt_ip": "192.168.10.146",
        "device_type": "arista_eos",
        "username": "R3",
        "password": "aristaR3",
        "secret": "arista",
        "platform": "arista",
    },
    {
        "name": "R4",
        "mgmt_ip": "192.168.10.89",
        "device_type": "cisco_ios",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
        "platform": "cisco",
    },
]


# -------- Helper functions --------
def parse_arp_line(line: str, platform: str):
    """
    Return (mac, interface) from a single ARP line.
    Cisco: Internet  IP  Age  MAC  Type  Interface
    Arista: IP  Age  MAC  Interface
    """
    parts = line.split()
    if platform == "cisco":
        if len(parts) >= 6:
            mac = parts[3]
            iface = parts[-1]
            return mac, iface
    else:  # arista
        if len(parts) >= 4:
            mac = parts[-2]
            iface = parts[-1]
            return mac, iface
    return None, None


def get_arp_info(conn, ip: str, platform: str):
    """Use 'show ip arp <ip>' to get MAC and interface. Returns (mac, iface) or (None, None)."""
    output = conn.send_command(f"show ip arp {ip}")
    for line in output.splitlines():
        if ip in line:
            return parse_arp_line(line, platform)
    return None, None


def get_cef_interface(conn, ip: str):
    """
    Cisco only: use 'show ip cef <ip>' to get outgoing interface.
    If not found, return None.
    """
    output = conn.send_command(f"show ip cef {ip}")
    for line in output.splitlines():
        line = line.strip()
        # Skip prefix line like "192.168.10.1/32"
        if not line or "/" in line:
            continue
        parts = line.split()
        if not parts:
            continue
        last = parts[-1]
        if last.startswith(
            (
                "GigabitEthernet",
                "FastEthernet",
                "TenGigabitEthernet",
                "Ethernet",
                "Vlan",
                "Loopback",
                "Port-channel",
            )
        ):
            return last
    return None


# -------- Main logic --------
def main():
    for dev in devices:
        print(f"\n===== {dev['name']} ({dev['mgmt_ip']}) =====")

        conn = ConnectHandler(
            device_type=dev["device_type"],
            host=dev["mgmt_ip"],
            username=dev["username"],
            password=dev["password"],
            secret=dev["secret"],
        )
        conn.enable()

        for ip in ARP:
            mac, arp_iface = get_arp_info(conn, ip, dev["platform"])
            if not mac:
                continue  # IP not found in ARP on this device

            if dev["platform"] == "cisco":
                out_iface = get_cef_interface(conn, ip) or arp_iface
            else:  # arista: no CEF, use ARP interface as outgoing
                out_iface = arp_iface

            # Template:
            # Device: MGMT IP
            # IP: Hardware address : Outgoing interface
            print(f"Device: {dev['mgmt_ip']}")
            print(f"IP: {ip}  Hardware address: {mac}  Outgoing interface: {out_iface}\n")

        conn.disconnect()


if __name__ == "__main__":
    main()
