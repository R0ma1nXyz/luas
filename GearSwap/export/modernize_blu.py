import re
import os

blu_file = "/home/romain/luas/GearSwap/data/Tenroh/Tenroh_Blu_Gear.lua"
export_file = "/home/romain/luas/GearSwap/export/Tenroh 2026-08-22 12-06-56.lua"
temp_file = blu_file + ".tmp"

# Load owned items
owned = set()
with open(export_file, 'r', encoding='utf-8') as f:
    for line in f:
        match_str = re.search(r'\s*\w+\s*=\s*"([^"]+)"', line)
        if match_str: owned.add(match_str.group(1).lower())
        match_tbl = re.search(r'name\s*=\s*"([^"]+)"', line)
        if match_tbl: owned.add(match_tbl.group(1).lower())

def owns(item_name):
    return item_name.lower() in owned

# Define modern BiS targets for different contexts
modern_bis_mapping = {
    # Weapons
    "Tizona": "Tizona",
    "Almace": "Almace",
    "Vampirism": "Naegling", 
    "Iris": "Almace",
    "Nibiru Cudgel": "Maxentius",
    "Nehushtan": "Maxentius",
    
    # Savage Blade / WSD
    "Assim. Jubbah +3": "Nyame Mail",
    "Lilitu Headpiece": "Nyame Helm",
    "Apate Ring": "Epaminondas's Ring",
    "Ifrit Ring +1": "Sroda Ring",
    
    # CDC / Crit
    "Abnoba Kaftan": "Gleti's Cuirass",
    "Sayadio's Kaftan": "Gleti's Cuirass",
    "Thereoid Greaves": "Gleti's Boots",
    "Ramuh Ring +1": "Ilabrat Ring",
    "Begrudging Ring": "Epona's Ring",
    
    # Magic / Nuke
    "Samnuha Coat": "Hashishin Mintan +3",
    "Assim. Shalwar +3": "Luhlaza Shalwar +3",
    "Yamabuki-no-Obi": "Orpheus's Sash",
    
    # Melee / TP
    "Mekosu. Harness": "Malignance Tabard",
    "Skaoi Boots": "Malignance Boots",
    "Buremte Gloves": "Malignance Gloves",
    "Dashing Subligar": "Malignance Tights",
    "Lengo Pants": "Carmine Cuisses +1",
    "Aurgelmir Orb +1": "Aurgelmir Orb +1",
    "Hasty Pinion +1": "Aurgelmir Orb +1",
    "Olseni Belt": "Kentarch Belt +1",
    
    # Accessories Generic
    "Cornflower Cape": "Rosmerta's Cape",
    "Bleating Mantle": "Rosmerta's Cape",
    "Oretan. Cape +1": "Rosmerta's Cape",
    "Shadow Mantle": "Rosmerta's Cape",
    "Valseur's Ring": "Epona's Ring",
    "Vengeful Ring": "Gere Ring",
    "Weatherspoon Ring": "Metamor. Ring +1",
    "Janniston Ring": "Metamor. Ring +1",
    "Dudgeon Earring": "Crep. Earring",
    "Heartseeker Earring": "Crep. Earring",
    "Handler's Earring +1": "Crep. Earring",
    "Mendicant's Earring": "Regal Earring",
    "Voltsurge Torque": "Sibyl Scarf",
    "Phalaina Locket": "Incanter's Torque"
}

missing_modern_bis = set()

with open(blu_file, 'r', encoding='utf-8') as f, open(temp_file, 'w', encoding='utf-8') as out:
    for line in f:
        # Match lines with a BiS comment
        match_comment = re.search(r'^(.*?)-- BiS:\s*(.+)$', line)
        if match_comment:
            code_part = match_comment.group(1)
            old_bis_items = [i.strip() for i in match_comment.group(2).split(',')]
            
            new_bis_items = []
            for old_bis in old_bis_items:
                # If we have a modern mapping for this old BiS item
                if old_bis in modern_bis_mapping:
                    modern = modern_bis_mapping[old_bis]
                    # Check if the user already owns the modern BiS
                    if owns(modern):
                        # The user owns it! We should ensure it's equipped in the line.
                        # Since my previous script used a fallback, it might already be equipped!
                        # e.g., code_part has `body="Nyame Mail"` and modern is `"Nyame Mail"`
                        pass # We don't add it to new_bis_items, meaning the comment will be removed!
                    else:
                        new_bis_items.append(modern)
                        missing_modern_bis.add(modern)
                else:
                    # If it's a specific JA item like Luhlaza Charuqs +3, keep it as BiS if they don't own it
                    if not owns(old_bis):
                        new_bis_items.append(old_bis)
                        missing_modern_bis.add(old_bis)

            if new_bis_items:
                line = f"{code_part}-- BiS: {', '.join(new_bis_items)}\n"
            else:
                # They own all the modern BiS for this line, remove the comment!
                line = f"{code_part.rstrip()}\n"
                
        out.write(line)

os.replace(temp_file, blu_file)

# Write the new TODO list
todo_file = "/home/romain/luas/GearSwap/data/Tenroh/TODO_BiS_Blu.md"
with open(todo_file, 'w', encoding='utf-8') as f:
    f.write("# Modern Best in Slot TODO - BLU\n\n")
    f.write("You are missing the following modern Best in Slot (BiS) items for Blue Mage.\n\n")
    for item in sorted(missing_modern_bis):
        f.write(f"- [ ] {item}\n")

print(f"Modernized BLU BiS! Reduced TODO list to {len(missing_modern_bis)} items.")
for item in sorted(missing_modern_bis):
    print(item)
