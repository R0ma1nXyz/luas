import re

export_file = "/home/romain/luas/GearSwap/export/Tenroh 2026-08-22 12-06-56.lua"
owned = []
with open(export_file, 'r', encoding='utf-8') as f:
    for line in f:
        match_str = re.search(r'\s*\w+\s*=\s*"([^"]+)"', line)
        if match_str:
            owned.append(match_str.group(1))
        
        match_tbl = re.search(r'name\s*=\s*"([^"]+)"', line)
        if match_tbl:
            owned.append(match_tbl.group(1))

print("Assim pieces:")
for item in set(owned):
    if "assim" in item.lower():
        print(item)

print("\nLuhlaza pieces:")
for item in set(owned):
    if "luhlaza" in item.lower() or "luh." in item.lower():
        print(item)

print("\nHashishin pieces:")
for item in set(owned):
    if "hashi" in item.lower():
        print(item)
