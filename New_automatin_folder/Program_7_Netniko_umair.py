

from netmiko import ConnectHandler

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


devices = {
    "R1": {
        "device_type": "cisco_ios",
        "host": "192.168.10.144",
        "username": "R1",
        "password": "ciscoR1",
        "secret": "cisco",
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
    }
}
def cmd_function(cmd_list):
    
    for name,dev in devices.items():
        print(f"\n==========={name}: {dev['host']}===========")
        try:
            conn =ConnectHandler(**dev)
            conn.enable()
            interface_ip = {}
            ip_mac_map = {}
            software = None
            for cmd in cmd_list:
                output = conn.send_command(cmd)

                
                for line in output.splitlines():
                    line = line.strip()
                    parts = line.split()
                    if cmd == "show ip arp":
                        for ip in ARP_LIST:
                            if ip in line:
                                try:
                                    ip_index = parts.index(ip)
                                except ValueError:
                                    continue
                                ipaddress = parts[ip_index]
                                mac_addr = parts[ip_index + 2]
                                ip_mac_map[ipaddress] = mac_addr
                    elif cmd == "show version":
                        if dev['device_type'] == "cisco_ios":
                            if "Cisco IOS Software" in line:
                                software = " ".join(parts)

                        elif dev['device_type']  == "arista_eos":
                            if "Software image version" in line:
                                software = " ".join(parts) 

                    elif cmd == "show ip interface brief":
                        if (
                            line.lower().startswith("interface")
                            or "unassigned" in line.lower()
                            or "---" in line 
                            or len(parts) < 2

                        ):
                            continue

                        else:
                            interface = parts[0]
                            ip_addr = parts[1]
                            interface_ip[interface] = ip_addr




            print(f"++++{dev['host']} ---> Matched IP -> MAC on this device:++++")
            for ip, mac in ip_mac_map.items():
                                
                print(f"{ip} -> {mac}")
            
            if software:
                print(software)
            
            if interface_ip:
                for intname,ipaddress in interface_ip.items():
                    print(f"Interface Name : {intname}  Assigned IP address : {ipaddress}")

 
            conn.disconnect()

        except Exception as e:
            print(f"Failed To connect {name}: {dev['host']}: {e}")

if __name__ == "__main__":
    cmd_list  = ["show ip arp", "show version", "show ip interface brief"]
    cmd_function(cmd_list)

