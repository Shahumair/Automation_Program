
from netmiko import ConnectHandler

# Dictionary of all devices
devices = {
    "R1": {
        "device_type": "cisco_ios",
        "host": "192.168.10.144",
        "username": "R1",
        "password": "ciscoR1",
        "secret": "cisco",   # enable password
    },
    "R2": {
        "device_type": "cisco_ios",
        "host": "192.168.10.145",
        "username": "R2",
        "password": "ciscoR2",
        "secret": "cisco",
    },
    "R3": {
        "device_type": "arista_eos",
        "host": "192.168.10.146",
        "username": "R3",
        "password": "aristaR3",
        "secret": "arista",
    },
    "R4": {
        "device_type": "cisco_ios",
        "host": "192.168.10.89",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    },
}

for name, dev in devices.items():
    print(f"\n========== {name} ({dev['host']}) ==========")
    try:
        # Connect to device
        conn = ConnectHandler(**dev)

        # Enter enable mode (if needed)
        conn.enable()

        # Run command
        output = conn.send_command("show ip interface brief")

        # Print output
        print(output)

        # Disconnect
        conn.disconnect()

    except Exception as e:
        print(f"Failed to connect to {name} ({dev['host']}): {e}")
