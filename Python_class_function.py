
from netmiko import ConnectHandler
from datetime import datetime

class NetworkDevice:
    def __init__(self, device_type, ip, username, password, name):
        self.device = {
            'device_type': device_type,
            'ip': ip,
            'username': username,
            'password': password
        }
        self.name = name
        self.connection = None
        self.config_output = ""

    def connect_ssh(self):
        try:
            print(f"[+] Connecting to {self.name} ({self.device['ip']})...")
            self.connection = ConnectHandler(**self.device)
            print(f"[+] Connected to {self.name}")
        except Exception as e:
            print(f"[-] Connection failed to {self.name}: {e}")

    def get_running_config(self):
        if self.connection:
            print(f"[+] Fetching running config from {self.name}")
            self.config_output = self.connection.send_command("show running-config")
        else:
            print(f"[-] Not connected to {self.name}")

    def save_config_to_file(self):
        if self.config_output:
            filename = f"{self.name}_running_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w") as f:
                f.write(self.config_output)
            print(f"[+] Config saved to {filename}")
        else:
            print(f"[-] No config output available to save for {self.name}")

# --- Create device instances ---
cisco_device = NetworkDevice(
    device_type="cisco_ios",
    ip="192.168.10.1",
    username="admin",
    password="cisco1",
    name="R1_Cisco"
)

arista_device = NetworkDevice(
    device_type="arista_eos",
    ip="192.168.10.2",
    username="admin",
    password="arista1",
    name="R2_Arista"
)

# --- Workflow Execution ---
for device in [cisco_device, arista_device]:
    device.connect_ssh()
    device.get_running_config()
    device.save_config_to_file()
