
from netaddr import IPAddress

def extract_ips_netaddr(file_path):
    found_ips = set()
    error_lines = []
    ip_to_count = "192.168.10.1"
    ip_count = 0

    with open(file_path, 'r') as file:
        for line in file:
            words = line.strip().split()

            # Count how many times 192.168.10.1 appears
            if ip_to_count in words:
                ip_count += 1

            # Save lines that contain "ERROR"
            if "ERROR" in line:
                error_lines.append(line.strip())

            # Extract IPs using netaddr
            for word in words:
                try:
                    ip = IPAddress(word)
                    found_ips.add(str(ip))
                except:
                    continue

    # Write ERROR lines to errorlog.txt
    with open("/home/umairalam/Python-VE/Automation_Program/errorlog.txt", "w") as err_file:
        for err_line in error_lines:
            err_file.write(err_line + "\n")

    return ip_count, sorted(found_ips)

# Update with your file path
file_path = "/home/umairalam/Python-VE/Automation_Program/Logfile.txt"

ip_count, ip_list = extract_ips_netaddr(file_path)

# Output
print("✅ 192.168.10.1 appears:", ip_count, "times")
print("\n📍 Unique IPs found in the file:")
for ip in ip_list:
    print(ip)

print("\n❗ ERROR lines have been saved to 'errorlog.txt'")
