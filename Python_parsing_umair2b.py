

from collections import defaultdict

region_count = defaultdict(int)

# Step 1: Extract region lines and write them to Regionfile.txt
with open("/home/umairalam/Python-VE/Automation_Program/Logfile.txt", 'r') as file:
    region_lines = [line.strip() for line in file if "Region" in line]

with open("/home/umairalam/Python-VE/Automation_Program/Regionfile.txt", 'w') as file2:
    for line in region_lines:
        file2.write(line + '\n')

# Step 2: Count devices per region
with open("/home/umairalam/Python-VE/Automation_Program/Regionfile.txt", 'r') as file3:
    for line in file3:
        words = line.strip().split()
        region = words[-1]  # assuming region name is last word
        region_count[region] += 1

# Step 3: Print region-wise device count
for region, count in region_count.items():
    print(f"{region}: {count}")
