import re
import os
import glob

# 1. Load valid Oseem aliases
items_file = "/home/romain/luas/GearSwap/data/Tenroh/Tenroh-Items.lua"
valid_oseem = set()
with open(items_file, 'r', encoding='utf-8') as f:
    for line in f:
        match = re.search(r'^(gear\.[a-z0-9_]+)\s*=', line)
        if match:
            valid_oseem.add(match.group(1))

# 2. Load owned items
export_file = "/home/romain/luas/GearSwap/export/Tenroh 2026-08-22 12-06-56.lua"
owned = set()
with open(export_file, 'r', encoding='utf-8') as f:
    for line in f:
        match_str = re.search(r'\s*\w+\s*=\s*"([^"]+)"', line)
        if match_str: owned.add(match_str.group(1).lower())
        match_tbl = re.search(r'name\s*=\s*"([^"]+)"', line)
        if match_tbl: owned.add(match_tbl.group(1).lower())

def owns(item_name):
    return item_name.lower() in owned

# Helper to check if they own the +3 version of an Empyrean/AF/Relic
def owns_plus3(item_name):
    if "+1" in item_name or "+2" in item_name:
        base = item_name.rsplit(" +", 1)[0]
        plus3 = f"{base} +3"
        return plus3.lower() in owned
    return False

modern_bis_mapping = {
    "Vampirism": "Naegling", 
    "Iris": "Almace",
    "Nibiru Cudgel": "Maxentius",
    "Nehushtan": "Maxentius",
    "Aetosaur": "Fomalhaut",
    "Doomsday": "Fomalhaut",
    "Fettering Blade": "Naegling",
    "Eminent Flute": "Gjallarhorn",
    "Abnoba Kaftan": "Gleti's Cuirass",
    "Sayadio's Kaftan": "Gleti's Cuirass",
    "Mekosu. Harness": "Malignance Tabard",
    "Skaoi Boots": "Malignance Boots",
    "Buremte Gloves": "Malignance Gloves",
    "Dashing Subligar": "Malignance Tights",
    "Lengo Pants": "Carmine Cuisses +1",
    "Samnuha Coat": "Nyame Mail",
    "Lilitu Headpiece": "Nyame Helm",
    "Valseur's Ring": "Epona's Ring",
    "Vengeful Ring": "Gere Ring",
    "Weatherspoon Ring": "Metamor. Ring +1",
    "Janniston Ring": "Metamor. Ring +1",
    "Dudgeon Earring": "Crep. Earring",
    "Heartseeker Earring": "Crep. Earring",
    "Handler's Earring +1": "Crep. Earring",
    "Mendicant's Earring": "Regal Earring",
    "Voltsurge Torque": "Sibyl Scarf",
    "Phalaina Locket": "Incanter's Torque",
    "Dark Ring": "Defending Ring",
    "Shadow Ring": "Defending Ring",
    "Ethereal Earring": "Genmei Earring",
    "Oneiros Grip": "Genmei Shield",
}

# 3. Process jobs
jobs = ["Brd", "Cor", "Drg", "Nin", "Pld", "Thf", "Whm"]
for job in jobs:
    lua_file = f"/home/romain/luas/GearSwap/data/Tenroh/Tenroh_{job}_Gear.lua"
    temp_lua = lua_file + ".tmp"
    missing_modern_bis = set()
    
    if not os.path.exists(lua_file): continue
    
    with open(lua_file, 'r', encoding='utf-8') as f, open(temp_lua, 'w', encoding='utf-8') as out:
        for line in f:
            # Fix Oseem variables
            def oseem_repl(match):
                alias = match.group(0)
                if alias in valid_oseem:
                    return alias
                else:
                    # Generic fallback based on name
                    if "head" in alias: return '"Nyame Helm"'
                    elif "body" in alias: return '"Nyame Mail"'
                    elif "hands" in alias or "gloves" in alias: return '"Nyame Gauntlets"'
                    elif "legs" in alias: return '"Nyame Flanchard"'
                    elif "feet" in alias: return '"Nyame Sollerets"'
                    elif "staff" in alias: return 'empty'
                    return 'empty'
                    
            # Replace broken Oseem variables
            line = re.sub(r'gear\.(grioavolr|chironic|merlinic|herculean|odyssean|valorous)[a-zA-Z0-9_]*', oseem_repl, line)
            
            # Modernize BiS comments
            match_comment = re.search(r'^(.*?)-- BiS:\s*(.+)$', line)
            if match_comment:
                code_part = match_comment.group(1)
                old_bis_items = [i.strip() for i in match_comment.group(2).split(',')]
                
                new_bis_items = []
                for old_bis in old_bis_items:
                    # Strip +1/+2 if they own +3
                    if owns_plus3(old_bis):
                        continue
                        
                    if old_bis in modern_bis_mapping:
                        modern = modern_bis_mapping[old_bis]
                        if owns(modern):
                            pass # Remove from comment
                        else:
                            new_bis_items.append(modern)
                            missing_modern_bis.add(modern)
                    else:
                        if not owns(old_bis):
                            new_bis_items.append(old_bis)
                            missing_modern_bis.add(old_bis)
                
                if new_bis_items:
                    line = f"{code_part}-- BiS: {', '.join(new_bis_items)}\n"
                else:
                    line = f"{code_part.rstrip()}\n"
            
            out.write(line)
            
    os.replace(temp_lua, lua_file)
    
    # Write TODO list
    todo_file = f"/home/romain/luas/GearSwap/data/Tenroh/TODO_BiS_{job}.md"
    with open(todo_file, 'w', encoding='utf-8') as f:
        f.write(f"# Modern Best in Slot TODO - {job.upper()}\n\n")
        f.write(f"You are missing the following modern Best in Slot (BiS) items for {job.upper()}.\n\n")
        for item in sorted(missing_modern_bis):
            f.write(f"- [ ] {item}\n")

print("Successfully updated all 7 job Luas and regenerated TODO lists!")
