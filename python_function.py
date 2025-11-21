
from netmiko import ConnectHandler

class NetworkDevice:
    def __init__(self, host, username, password, device_type="cisco_ios"):
        self.device_info = {
            "device_type": device_type,
            "host": host,
            "username": username,
            "password": password
        }
        self.connection = None

    def connect(self):
        try:
            self.connection = ConnectHandler(**self.device_info)
            print(f"Connected to {self.device_info['host']}")
        except Exception as e:
            print(f"Failed to connect to {self.device_info['host']}: {e}")

    def run_command(self, command):
        if self.connection:
            output = self.connection.send_command(command)
            print(f"\nOutput from {self.device_info['host']}:\n{output}\n")
        else:
            print(f"Not connected to {self.device_info['host']}.")

    def disconnect(self):
        if self.connection:
            self.connection.disconnect()
            print(f"Disconnected from {self.device_info['host']}")

# 🔄 Use the class for two devices
device1 = NetworkDevice("192.168.1.1", "admin", "cisco123")
device2 = NetworkDevice("192.168.1.2", "admin", "cisco123")

# Device 1
device1.connect()
device1.run_command("show version")
device1.disconnect()

# Device 2
device2.connect()
device2.run_command("show version")
device2.disconnect()
