import re
import sys

export_file = "/home/romain/luas/GearSwap/export/Tenroh 2026-08-22 12-06-56.lua"
blu_file = "/home/romain/luas/GearSwap/data/Tenroh/Tenroh_Blu_Gear.lua"

owned = set()
with open(export_file, 'r', encoding='utf-8') as f:
    for line in f:
        # Match string assignments like item="Name" or head="Name"
        match_str = re.search(r'\s*\w+\s*=\s*"([^"]+)"', line)
        if match_str:
            owned.add(match_str.group(1).lower())
        
        # Match table assignments like head={ name="Name", ... }
        match_tbl = re.search(r'name\s*=\s*"([^"]+)"', line)
        if match_tbl:
            owned.add(match_tbl.group(1).lower())

print(f"Total owned items parsed: {len(owned)}")

missing_in_blu = set()
with open(blu_file, 'r', encoding='utf-8') as f:
    for line in f:
        # Check standard slots
        matches = re.findall(r'(?:head|body|hands|legs|feet|neck|waist|left_ear|right_ear|ear1|ear2|left_ring|right_ring|ring1|ring2|back|main|sub|range|ammo)\s*=\s*"([^"]+)"', line)
        for m in matches:
            if m.lower() not in owned and m.lower() not in ['empty', '']:
                missing_in_blu.add(m)
        
        # Check augmented slots
        matches_aug = re.findall(r'name\s*=\s*"([^"]+)"', line)
        for m in matches_aug:
            if m.lower() not in owned and m.lower() not in ['empty', '']:
                missing_in_blu.add(m)

print("Missing in BLU:")
for m in sorted(missing_in_blu):
    print(m)
