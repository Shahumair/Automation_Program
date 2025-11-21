
import pandas as pd
import os
import datetime
from netmiko import ConnectHandler

# Path to the Excel file containing device details
excel_path = "/home/umairalam/Python-VE/Automation_Program/Device_inventory.xlsx"

# Read the Excel file
df = pd.read_excel(excel_path, engine="openpyxl")

# Clean column names (strip spaces, convert to lowercase)
df.columns = df.columns.str.strip().str.lower()

# Ensure required columns exist
required_columns = ["hostname", "ip address", "username", "password", "enable password"]
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Column '{col}' not found in the Excel file. Please check column names.")

# Extract device details
devices = []
for _, row in df.iterrows():
    if pd.notnull(row["hostname"]) and pd.notnull(row["ip address"]):  # Ensure valid entries
        device = {
            "hostname": row["hostname"],
            "ip": row["ip address"],
            "username": row["username"],
            "password": row["password"],
            "enable_password": row["enable password"]
        }
        devices.append(device)

# Store the output data
output_data = {}

# SSH and execute commands
for device in devices:
    try:
        # Netmiko device configuration
        router = {
            "device_type": "cisco_ios",
            "host": device["ip"],
            "username": device["username"],
            "password": device["password"],
            "secret": device["enable_password"],
            "conn_timeout": 20 
        }

        # Connect to the device
        print(f"Connecting to {device['hostname']} ({device['ip']})...")
        ssh_conn = ConnectHandler(**router)

        # Enter enable mode
        ssh_conn.enable()

        # Run command
        command = "show ip interface brief"
        output = ssh_conn.send_command(command)

        # Store the output
        output_data[device["hostname"]] = output

        # Close SSH connection
        ssh_conn.disconnect()
        print(f"Successfully retrieved data from {device['hostname']}.")

    except Exception as e:
        print(f"Failed to connect to {device['hostname']} ({device['ip']}): {e}")
        output_data[device["hostname"]] = f"Connection failed: {e}"

# Generate a timestamped filename for the output Excel file
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"/home/umairalam/Python-VE/Automation_Program/Generated_Config_{timestamp}.xlsx"

# Write output to Excel file
with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
    for hostname, output in output_data.items():
        # Split output into rows for better readability
        output_lines = output.split("\n")
        output_df = pd.DataFrame(output_lines, columns=[f"Command: show ip interface brief"])
        
        # Write to a new sheet named after the hostname
        output_df.to_excel(writer, sheet_name=hostname, index=False)

print(f"\n✅ Output saved to: {output_file}")
