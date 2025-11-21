from collections import defaultdict

region_count = defaultdict(int)
region_line_list = []

region_name = []
count = 0
count_list =[]

with open("/home/umairalam/Python-VE/Automation_Program/Logfile.txt", 'r') as file:
    for line in file:
        words = line.strip().split()
        if "Region" in line:
            region_line_list.append(line.strip())

with open("/home/umairalam/Python-VE/Automation_Program/Regionfile.txt", 'w') as file2:
    for line in region_line_list:
        file2.write(line + '\n')


with open("/home/umairalam/Python-VE/Automation_Program/Regionfile.txt", 'r') as file3:
    for line in file3:
        words = line.strip().split()
        print(words)
        #reg_name = words[-1]
        name = words[-1]
        region_name.append(words[-1])

        unique_reg_list = list(set(region_name))
        region_count[name] += 1


for region, count in region_count.items():
    print(f"{region}: {count}")








           
