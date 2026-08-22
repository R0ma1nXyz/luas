import re
import os

export_file = "/home/romain/luas/GearSwap/export/Tenroh 2026-08-22 12-06-56.lua"
lua_dir = "/home/romain/luas/GearSwap/data/Tenroh"

def get_owned_items():
    items = set()
    with open(export_file, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.search(r'item="([^"]+)"', line)
            if match:
                items.add(match.group(1).lower())
    return items

def check_missing_in_file(filepath, owned):
    missing = set()
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            # Match standard gear slots like head="Item", or head={name="Item"}
            # This is a basic regex, could be improved based on actual lua structure
            matches = re.findall(r'(?:head|body|hands|legs|feet|neck|waist|ear1|ear2|ring1|ring2|back|main|sub|range|ammo)\s*=\s*"([^"]+)"', line)
            for m in matches:
                if m.lower() not in owned and m.lower() != 'empty' and m.lower() != '':
                    missing.add(m)
            
            # Match augmented items like head={name="Item", augments={...}}
            matches_aug = re.findall(r'name\s*=\s*"([^"]+)"', line)
            for m in matches_aug:
                if m.lower() not in owned and m.lower() != 'empty' and m.lower() != '':
                    missing.add(m)
    return missing

owned = get_owned_items()
print(f"Total owned items: {len(owned)}")

files_to_check = [f for f in os.listdir(lua_dir) if f.endswith('_Gear.lua')]

for f in files_to_check:
    filepath = os.path.join(lua_dir, f)
    missing = check_missing_in_file(filepath, owned)
    if missing:
        print(f"\nMissing in {f}:")
        for m in sorted(missing):
            print(f"  - {m}")
