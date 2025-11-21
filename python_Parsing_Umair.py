from netaddr import IPAddress


keyword_found =[]
count = 0
ip_addr_list = set()
specific_ip_found = "192.168.10.1"
with open("/home/umairalam/Python-VE/Automation_Program/Logfile.txt", 'r') as file:
    for line in file:
        print(line)
        words = line.strip().split()
        print(words)

        if specific_ip_found in words:
            count += 1

        if "ERROR" in line:
            keyword_found.append(line.strip())
        print(count)

        for word in words:
                try:
                    ip = IPAddress(word)
                    ip_addr_list.add(str(ip))
                   
                   
                except:
                    continue



with open("/home/umairalam/Python-VE/Automation_Program/newerr.txt", 'w') as file2:
    for line in keyword_found:
        file2.write(line + "\n")

print("✅ 192.168.10.1 appears:", count, "times")
print("📍 Unique IPs found in the file:")
for ip in sorted(ip_addr_list):
    print(ip)

