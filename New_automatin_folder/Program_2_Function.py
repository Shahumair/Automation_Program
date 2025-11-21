


# =========================
# Given lists and strings
# =========================

list1 = [1, 3, 5, 7, 9, 11]
list2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
list3 = [1, 1, 2, 2, 3, 3, 4, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
list4 = ["192.168.10.1", "192.168.10.2", "192.16.10.3", "192.168.10.4", "192.168.10.5"]
list5 = ["192.168.10.1", "192.168.10.2", "192.16.10.3", "192.168.10.4", "192.168.10.5", "192.168.10.1"]
list6 = ["192.168.20.1", "192.168.20.2", "192.16.20.3", "192.168.20.4", "192.168.20.5", "192.168.10.1"]

g0 = ["GigabitEthernet0/0", "192.168.10.144", "YES", "manual", "up", "up"]
g1 = ["GigabitEthernet0/1", "unassigned", "YES", "unset", "administratively down", "down"]
g2 = ["GigabitEthernet0/2", "unassigned", "YES", "unset", "administratively down", "down"]
g3 = ["GigabitEthernet0/3", "unassigned", "YES", "unset", "administratively down", "down"]
lo0 = ["Loopback0", "172.16.1.2", "YES", "manual", "up", "up"]

string1 = "My name is Shah Umair Alam. "
string2 = "I live in Czech Republic"
string3 = "I love my home country Pakistan and Pakistan is the atomic power"


# =========================
# Task 1
# Make list1 a string "1357911" and back to list again
# =========================

def task1_make_string_and_back(lst):
    # Make string from list: 1357911
    num_str = ""
    for num in lst:
        num_str += str(num)

    print("Task 1 - String from list1:", num_str)

    # Convert string back to list of integers
    new_list = []
    for ch in num_str:
        new_list.append(int(ch))

    print("Task 1 - List again from string:", new_list)


# =========================
# Task 2
# Even and odd lists from list2
# =========================

def task2_even_odd(lst):
    even_numbers = []
    odd_numbers = []

    for num in lst:
        if num % 2 == 0:
            even_numbers.append(num)
        else:
            odd_numbers.append(num)

    print("Task 2 - Even numbers:", even_numbers)
    print("Task 2 - Odd numbers:", odd_numbers)


# =========================
# Task 3
# Unique set from list3 and list3 in reverse order
# =========================

def task3_unique_and_reverse(lst):
    unique_set = set(lst)
    print("Task 3 - Unique values (set):", unique_set)

    reversed_list = list(reversed(lst))
    print("Task 3 - Original list reversed:", reversed_list)


# =========================
# Task 4
# Join string1 and string2, then make it a list
# =========================

def task4_join_strings_and_to_list(s1, s2):
    joined = s1 + s2
    print("Task 4 - Joined string:", joined)

    # Convert string into list of words
    words_list = joined.split()
    print("Task 4 - Joined string as list of words:", words_list)


# =========================
# Task 5
# Find "Pakistan" in string3 and count how many times
# =========================

def task5_find_pakistan(text):
    keyword = "Pakistan"
    count = text.count(keyword)

    if count > 0:
        print(f"Task 5 - Found '{keyword}' {count} time(s) in string3")
    else:
        print(f"Task 5 - '{keyword}' not found in string3")


# =========================
# Task 6
# Find IP "192.168.10.1" in list4, list5, list6 and count
# =========================

def task6_find_ip_in_lists(ip, l4, l5, l6):
    total = 0

    for item in l4:
        if item == ip:
            total += 1

    for item in l5:
        if item == ip:
            total += 1

    for item in l6:
        if item == ip:
            total += 1

    print(f"Task 6 - IP address {ip} found {total} time(s) in list4, list5, and list6")


# =========================
# Task 7
# Check which interfaces are down from g0, g1, g2, g3, lo0
# =========================

def task7_check_down_interfaces(interfaces):
    down_interfaces = []

    for iface in interfaces:
        name = iface[0]
        status = iface[4]     # e.g. "up" or "administratively down"
        protocol = iface[5]   # e.g. "up" or "down"

        # Interface is "down" if status is not up OR protocol is not up
        if status != "up" or protocol != "up":
            down_interfaces.append(name)

    print("Task 7 - Interfaces in down state:", down_interfaces)


# =========================
# Task 8
# Print all lines with keyword "ERROR" from logfile
# =========================

def task8_print_error_lines(file_path):
    try:
        with open(file_path, "r") as f:
            print("Task 8 - Lines with 'ERROR':")
            for line in f:
                if "ERROR" in line:
                    print(line.rstrip())
    except FileNotFoundError:
        print("Task 8 - Log file not found. Please check the path:", file_path)


# =========================
# Main: call all functions
# =========================

def main():
    task1_make_string_and_back(list1)
    print()

    task2_even_odd(list2)
    print()

    task3_unique_and_reverse(list3)
    print()

    task4_join_strings_and_to_list(string1, string2)
    print()

    task5_find_pakistan(string3)
    print()

    task6_find_ip_in_lists("192.168.10.1", list4, list5, list6)
    print()

    task7_check_down_interfaces([g0, g1, g2, g3, lo0])
    print()

    # Update the path if your log file is somewhere else
    task8_print_error_lines("/home/umairalam/Python-VE/Automation_Program/Logfile.txt")


if __name__ == "__main__":
    main()
