as_path = [123, 6556, 456, 123, 650109, 512, 310, 64512, 64513, 332]
def check_as_path(as_path):
    """Prints a warning if duplicates exist and returns loop_present (True/False)."""
    seen = set()
    duplicates = []

    for asn in as_path:
        if asn in seen:
            if asn not in duplicates:
                duplicates.append(asn)
        else:
            seen.add(asn)

    loop_present = len(duplicates) > 0
    print(seen)
    if loop_present:
        print("WARNING: as_path has duplicate item(s):", duplicates)
    else:
        print("OK: no duplicate items in as_path")

    return loop_present


# Example use

loop_present = check_as_path(as_path)
print("loop_present =", loop_present)

