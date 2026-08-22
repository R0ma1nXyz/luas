import re
import os
import glob

export_file = "/home/romain/luas/GearSwap/export/Tenroh 2026-08-22 12-06-56.lua"
lua_dir = "/home/romain/luas/GearSwap/data/Tenroh/"

# Parse owned items
owned = set()
owned_names = set() # lower case map to original for case insensitive matching
with open(export_file, 'r', encoding='utf-8') as f:
    for line in f:
        match_str = re.search(r'\s*\w+\s*=\s*"([^"]+)"', line)
        if match_str:
            owned.add(match_str.group(1).lower())
            owned_names.add(match_str.group(1))
        
        match_tbl = re.search(r'name\s*=\s*"([^"]+)"', line)
        if match_tbl:
            owned.add(match_tbl.group(1).lower())
            owned_names.add(match_tbl.group(1))

# Helper to find original case
def get_original_case(item_lower):
    for name in owned_names:
        if name.lower() == item_lower:
            return name
    return None

def get_upgrade(item_name):
    # Try to find a +3 or +2 upgrade if they are missing a +1/+2
    if "+1" in item_name or "+2" in item_name:
        base = item_name.replace("+1", "").replace("+2", "").strip()
        if f"{base} +3".lower() in owned:
            return get_original_case(f"{base} +3".lower())
        if f"{base} +2".lower() in owned:
            return get_original_case(f"{base} +2".lower())
            
    # Also check without plus (some bases don't have plus)
    if f"{item_name} +3".lower() in owned:
        return get_original_case(f"{item_name} +3".lower())
    if f"{item_name} +2".lower() in owned:
        return get_original_case(f"{item_name} +2".lower())
    if f"{item_name} +1".lower() in owned:
        return get_original_case(f"{item_name} +1".lower())
        
    return None

fallbacks = {
    'head': 'Nyame Helm',
    'body': 'Nyame Mail',
    'hands': 'Nyame Gauntlets',
    'legs': 'Nyame Flanchard',
    'feet': 'Nyame Sollerets',
    'neck': 'Lissome Necklace',
    'waist': 'Eschan Stone',
    'left_ear': 'Telos Earring',
    'right_ear': 'Suppanomimi',
    'ear1': 'Telos Earring',
    'ear2': 'Suppanomimi',
    'left_ring': 'Defending Ring',
    'right_ring': 'Shneddick Ring +1',
    'ring1': 'Defending Ring',
    'ring2': 'Shneddick Ring +1',
    'back': 'Moonlight Cape',
    'main': 'empty',
    'sub': 'empty',
    'range': 'empty',
    'ammo': 'empty'
}

jobs = ["Brd", "Cor", "Drg", "Nin", "Pld", "Thf", "Whm"]

for job in jobs:
    file_path = os.path.join(lua_dir, f"Tenroh_{job}_Gear.lua")
    if not os.path.exists(file_path):
        continue
        
    temp_file = file_path + ".tmp"
    missing_bis = set()
    
    with open(file_path, 'r', encoding='utf-8') as f, open(temp_file, 'w', encoding='utf-8') as out:
        for line in f:
            # Pattern matches slot="Item Name" or slot={name="Item Name"
            # It captures: (1) slot, (2) entire value including {}, (3) the actual item name
            match = re.search(r'([a-zA-Z0-9_]+)\s*=\s*([\{]*\s*name\s*=\s*"([^"]+)"[^}]*[\}]*|"\s*([^"]+)\s*")', line)
            
            if match and "-- BiS:" not in line:
                slot = match.group(1).lower()
                item_name = match.group(3) if match.group(3) else match.group(4)
                item_lower = item_name.lower()
                
                if item_lower not in owned and item_lower not in ['empty', '']:
                    missing_bis.add(item_name)
                    
                    # Try to find an upgrade (e.g. +3)
                    upgrade = get_upgrade(item_name)
                    if upgrade:
                        replacement = f'"{upgrade}"'
                    else:
                        # Fallback based on slot
                        fallback_item = fallbacks.get(slot, 'empty')
                        replacement = f'"{fallback_item}"' if fallback_item != 'empty' else 'empty'
                        
                    # Replace the entire value assignment to strip out augments from unowned gear
                    # e.g. head={name="A", augments={...}} -> head="Nyame Helm"
                    
                    old_assignment = match.group(0)
                    new_assignment = f"{match.group(1)}={replacement}"
                    line = line.replace(old_assignment, new_assignment)
                    line = line.rstrip('\n\r')
                    line = f"{line} -- BiS: {item_name}\n"
            
            out.write(line)
            
    os.replace(temp_file, file_path)
    
    # Write missing BiS to a separate file for this job
    todo_file = os.path.join(lua_dir, f"TODO_BiS_{job}.md")
    with open(todo_file, 'w', encoding='utf-8') as f:
        f.write(f"# Best in Slot TODO - {job.upper()}\n\n")
        f.write("You are missing the following Best in Slot (BiS) items for this job. Acquire them and uncomment the lines in your Lua!\n\n")
        for item in sorted(missing_bis):
            f.write(f"- [ ] {item}\n")
            
    print(f"Refactored {job} and generated TODO_BiS_{job}.md with {len(missing_bis)} items.")
    
