import time
import paramiko
from netmiko import ConnectHandler

# Enable Paramiko logging for debugging
paramiko.util.log_to_file("/home/umairalam/Python-VE/Automation_Program/paramiko_debug.log")

# Define SSH connection parameters (without 'look_for_keys')
router = {
    "device_type": "cisco_ios",
    "host": "192.168.10.144",
    "username": "R1",
    "password": "ciscoR1",
    "secret": "cisco",
    "conn_timeout": 90,  
    "banner_timeout": 90,
    "auth_timeout": 90,
    "allow_agent": False,  
    "global_delay_factor": 2  # Extra delay to stabilize connection
}

# Retry mechanism for SSH connection
def connect_with_retries(router, retries=3, delay=10):
    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1} to connect to {router['host']}...")
            ssh_conn = ConnectHandler(**router)

            # Ensure session remains stable
            ssh_conn.enable()
            ssh_conn.send_command("terminal length 0")  # Disable pagination
            return ssh_conn
        except Exception as e:
            print(f"Connection attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"All {retries} attempts failed.")
                raise

try:
    # Attempt SSH connection with retries
    ssh_conn = connect_with_retries(router)

    # Execute show commands
    output_1 = ssh_conn.send_command("show ip interface brief")
    output_2 = ssh_conn.send_command("show running-config")

    print("\n✅ Command Output (show ip interface brief):")
    print(output_1)
    
    print("\n✅ Command Output (show running-config):")
    print(output_2)

    # Close SSH session
    ssh_conn.disconnect()
except Exception as e:
    print(f"\n🚨 SSH Connection Failed: {e}")
