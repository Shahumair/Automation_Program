# Program_1_ClassOOP_v3.py

import socket
import time
from netmiko import ConnectHandler

# Exceptions: works across Netmiko 3/4
try:
    from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
except ImportError:
    from netmiko.ssh_exception import NetmikoTimeoutException, NetmikoAuthenticationException

from paramiko.ssh_exception import SSHException


def tcp_check(host: str, port: int = 22, timeout: int = 5):
    s = socket.socket()
    s.settimeout(timeout)
    t0 = time.time()
    try:
        s.connect((host, port))
        return True, round((time.time() - t0) * 1000), ""
    except Exception as e:
        return False, 0, str(e)
    finally:
        try:
            s.close()
        except Exception:
            pass


class NetworkDevice:
    def __init__(self, name, host, username, password, secret, device_type):
        self.name = name
        self.host = host
        self.username = username
        self.password = password
        self.secret = secret      # enable password
        self.device_type = device_type

    def show_ip_int_brief(self):
        ok, _, err = tcp_check(self.host, 22, timeout=5)
        if not ok:
            return f"[SKIP] TCP/22 not reachable on {self.host}. Error: {err}"

        params = {
            "device_type": self.device_type,
            "host": self.host,
            "username": self.username,
            "password": self.password,
            "secret": self.secret,
            # ✅ Netmiko-friendly auth flags
            "use_keys": False,
            "allow_agent": False,
            # Timeouts that help with slow banners/VMs
            "conn_timeout": 20,
            "auth_timeout": 30,
            "banner_timeout": 60,
            # Faster CLI reads
            "fast_cli": True,
            # Optional: write raw I/O to a log for debugging
            # "session_log": f"/tmp/netmiko_{self.name}.log",
        }

        try:
            with ConnectHandler(**params) as conn:
                if self.secret:
                    try:
                        conn.enable()
                    except Exception:
                        pass  # enable not critical for a 'show'
                out = conn.send_command("show ip interface brief")
                return out.strip() if out else "[INFO] Command returned no output."
        except NetmikoAuthenticationException as e:
            return f"[AUTH ERROR] {self.name} ({self.host}): {e}"
        except NetmikoTimeoutException as e:
            return f"[TIMEOUT] {self.name} ({self.host}): {e}"
        except SSHException as e:
            return f"[SSH ERROR] {self.name} ({self.host}): {e}"
        except Exception as e:
            return f"[UNEXPECTED ERROR] {self.name} ({self.host}): {e}"


class CiscoDevice(NetworkDevice):
    def __init__(self, name, host, username, password, secret):
        super().__init__(name, host, username, password, secret, "cisco_ios")


class AristaDevice(NetworkDevice):
    def __init__(self, name, host, username, password, secret):
        super().__init__(name, host, username, password, secret, "arista_eos")


def main():
    devices = [
        CiscoDevice("R1", "192.168.10.144", "R1", "ciscoR1", "cisco"),
        CiscoDevice("R2", "192.168.10.145", "R2", "ciscoR2", "cisco"),
        AristaDevice("R3", "192.168.10.146", "R3", "aristaR3", "arista"),  # adjust if needed
    ]

    for d in devices:
        print("=" * 60)
        print(f"{d.name}  ({d.host})")
        print(d.show_ip_int_brief())
        print("=" * 60)


if __name__ == "__main__":
    main()



