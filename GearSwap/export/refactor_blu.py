import re
import os

blu_file = "/home/romain/luas/GearSwap/data/Tenroh/Tenroh_Blu_Gear.lua"
temp_file = blu_file + ".tmp"

replacements = {
    # Weapons
    "Tizona": "Naegling",
    "Almace": "Naegling",
    "Sequence": "Naegling",
    "Vampirism": "Malignance Sword",
    "Iris": "Malignance Sword",
    "Nehushtan": "Malignance Sword",
    "Nibiru Cudgel": "Maxentius",
    
    # AF / Relic / Empy upgrades
    "Hashi. Basmak +1": "Hashi. Basmak +3",
    "Hashi. Bazu. +1": "Hashi. Bazu. +3",
    "Hashishin Mintan +1": "Hashishin Mintan +3",
    "Hashishin Tayt +1": "Hashishin Tayt +3",
    
    "Assim. Bazu. +3": "Hashi. Bazu. +3",
    "Assim. Charuqs +2": "Hashi. Basmak +3",
    "Assim. Jubbah +3": "Hashishin Mintan +3",
    "Assim. Keffiyeh +3": "Hashishin Kavuk +3",
    "Assim. Shalwar +3": "Hashishin Tayt +3",
    
    "Luh. Keffiyeh +3": "Hashishin Kavuk +3",
    "Luhlaza Charuqs +3": "Hashi. Basmak +3",
    "Luhlaza Jubbah +3": "Hashishin Mintan +3",
    
    # Armor
    "Abnoba Kaftan": "Malignance Tabard",
    "Sayadio's Kaftan": "Malignance Tabard",
    "Samnuha Coat": "Malignance Tabard",
    "Mekosu. Harness": "Nyame Mail",
    
    "Dashing Subligar": "Carmine Cuisses +1",
    "Lengo Pants": "Carmine Cuisses +1",
    
    "Skaoi Boots": "Malignance Boots",
    "Thereoid Greaves": "Malignance Boots",
    
    "Lilitu Headpiece": "Malignance Chapeau",
    
    "Buremte Gloves": "Malignance Gloves",
    
    # Accessories
    "Bleating Mantle": "Rosmerta's Cape",
    "Cornflower Cape": "Rosmerta's Cape",
    "Umbra Cape": "Rosmerta's Cape",
    "Oretan. Cape +1": "Rosmerta's Cape",
    "Shadow Mantle": "Rosmerta's Cape",
    
    "Aurgelmir Orb +1": "Oshasha's Treatise",
    "Hasty Pinion +1": "Impatiens",
    
    "Apate Ring": "Epona's Ring",
    "Ifrit Ring +1": "Gere Ring",
    "Ramuh Ring +1": "Ilabrat Ring",
    "Valseur's Ring": "Epona's Ring",
    "Vengeful Ring": "Gere Ring",
    "Weatherspoon Ring": "Stikini Ring +1",
    "Janniston Ring": "Metamor. Ring +1",
    "Kunaji Ring": "Metamor. Ring +1",
    "Dark Ring": "Defending Ring",
    "Shadow Ring": "Defending Ring",
    "Meridian Ring": "Defending Ring",
    
    "Dudgeon Earring": "Suppanomimi",
    "Heartseeker Earring": "Eabani Earring",
    "Handler's Earring +1": "Cessance Earring",
    "Mendicant's Earring": "Telos Earring",
    "Regal Earring": "Telos Earring",
    "Ethereal Earring": "Genmei Earring",
    
    "Olseni Belt": "Kentarch Belt +1",
    "Yamabuki-no-Obi": "Orpheus's Sash",
    
    "Voltsurge Torque": "Sanctity Necklace",
    "Phalaina Locket": "Incanter's Torque",
    
    "Oneiros Grip": "Genmei Shield",
    "Regal Cuffs": "Malignance Gloves"
}

missing_bis = set()

with open(blu_file, 'r', encoding='utf-8') as f, open(temp_file, 'w', encoding='utf-8') as out:
    for line in f:
        original_line = line
        modified = False
        
        # Check if the line has a gear definition
        match = re.search(r'([a-zA-Z0-9_]+)\s*=\s*"{0,1}([^",\}]+)"{0,1}', line)
        if match:
            item_name = match.group(2).strip()
            
            for missing, replacement in replacements.items():
                if missing in line and "-- BiS:" not in line:
                    # Found a missing item
                    missing_bis.add(missing)
                    # Replace it
                    line = line.replace(missing, replacement)
                    # Add comment at the end of the line
                    line = line.rstrip('\n\r')
                    line = f"{line} -- BiS: {missing}\n"
                    modified = True
                    break
                    
        out.write(line)

os.replace(temp_file, blu_file)

print("Refactored BLU.lua")
print("Missing BiS found and replaced:")
for item in sorted(missing_bis):
    print(item)
