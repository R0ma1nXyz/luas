import re
import os

blu_file = "/home/romain/luas/GearSwap/data/Tenroh/Tenroh_Blu_Gear.lua"
temp_blu = blu_file + ".tmp"
todo_file = "/home/romain/luas/GearSwap/data/Tenroh/TODO_BiS_Blu.md"
temp_todo = todo_file + ".tmp"

bad_bis = [
    "Hashi. Basmak +1",
    "Hashi. Bazu. +1",
    "Hashishin Mintan +1",
    "Hashishin Tayt +1",
    "Dark Ring",
    "Shadow Ring",
    "Ethereal Earring",
    "Oneiros Grip",
    "Regal Cuffs"
]

with open(blu_file, 'r', encoding='utf-8') as f, open(temp_blu, 'w', encoding='utf-8') as out:
    for line in f:
        match = re.search(r'^(.*?)-- BiS:\s*(.+)$', line)
        if match:
            code_part = match.group(1)
            bis_items = [i.strip() for i in match.group(2).split(',')]
            
            # Filter out the bad BiS items
            new_bis_items = [item for item in bis_items if item not in bad_bis]
            
            if new_bis_items:
                line = f"{code_part}-- BiS: {', '.join(new_bis_items)}\n"
            else:
                # No BiS items left, strip the comment entirely
                line = f"{code_part.rstrip()}\n"
                
        out.write(line)

os.replace(temp_blu, blu_file)

with open(todo_file, 'r', encoding='utf-8') as f, open(temp_todo, 'w', encoding='utf-8') as out:
    for line in f:
        # Check if the line is one of the bad items
        is_bad = False
        for bad in bad_bis:
            if f"- [ ] {bad}" in line:
                is_bad = True
                break
        if not is_bad:
            out.write(line)

os.replace(temp_todo, todo_file)

print("Cleaned up outdated BiS targets from Lua and TODO list.")
