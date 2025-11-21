

from netmiko import ConnectHandler

# ARP IPs to check
ARP_LIST = [
    "192.168.10.1",
    "192.168.0.1",
    "192.168.10.104",
    "192.168.10.144",
    "192.168.10.145",
    "192.168.10.146",
    "192.168.10.89",
    "192.168.10.145",
]

# Devices
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


for dev in devices:
    print(f"\n===== {dev['name']} ({dev['mgmt_ip']}) =====")

    # SSH login
    conn = ConnectHandler(
        device_type=dev["device_type"],
        host=dev["mgmt_ip"],
        username=dev["username"],
        password=dev["password"],
        secret=dev["secret"],
    )
    conn.enable()

    for ip in ARP_LIST:
        # 1) Check ARP entry
        arp_output = conn.send_command(f"show ip arp {ip}")

        # Find line that contains the IP
        arp_line = ""
        for line in arp_output.splitlines():
            if ip in line:
                arp_line = line
                break

        if arp_line == "":
            # IP not present in ARP table on this device
            continue

        # 2) Get MAC + ARP interface (simple parsing)
        parts = arp_line.split()

        if dev["platform"] == "cisco":
            # Example: Internet  192.168.10.1  0   aaaa.bbbb.cccc  ARPA  GigabitEthernet0/0
            mac = parts[3]
            arp_intf = parts[-1]
        else:
            # Arista example: 192.168.10.1  0:02:34  aaaa.bbbb.cccc  Ethernet1
            mac = parts[-2]
            arp_intf = parts[-1]

        # 3) Find outgoing interface
        if dev["platform"] == "cisco":
            cef_output = conn.send_command(f"show ip cef {ip}")
            out_intf = arp_intf  # default

            for line in cef_output.splitlines():
                line = line.strip()
                if not line or "/" in line:
                    continue
                # take last word if it looks like an interface
                last = line.split()[-1]
                if any(last.startswith(x) for x in ["GigabitEthernet", "FastEthernet",
                                                    "TenGigabitEthernet", "Ethernet",
                                                    "Vlan", "Loopback", "Port-channel"]):
                    out_intf = last
                    break
        else:
            # Arista: no CEF; use ARP interface as outgoing
            out_intf = arp_intf

        # 4) Print in required format
        print(f"Device: {dev['mgmt_ip']}")
        print(f"IP: {ip}  Hardware address: {mac}  Outgoing interface: {out_intf}\n")

    conn.disconnect()
