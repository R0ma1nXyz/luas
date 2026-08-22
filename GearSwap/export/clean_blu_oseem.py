import re
import os

blu_file = "/home/romain/luas/GearSwap/data/Tenroh/Tenroh_Blu_Gear.lua"
temp_file = blu_file + ".tmp"

replacements = {
    "gear.herculean_nuke_feet": '"Hashi. Basmak +3"',
    "gear.herculean_ta_feet": '"Malignance Boots"',
    "gear.herculean_wsd_feet": '"Nyame Sollerets"',
    "gear.herculean_waltz_body": '"Nyame Mail"',
    "gear.herculean_waltz_hands": '"Nyame Gauntlets"',
    "gear.herculean_waltz_feet": '"Nyame Sollerets"',
    "gear.herculean_refresh_hands": '"Nyame Gauntlets"',
    "gear.herculean_refresh_feet": '"Nyame Sollerets"',
    "gear.herculean_fc_head": '"Hashishin Kavuk +3"',
}

with open(blu_file, 'r', encoding='utf-8') as f, open(temp_file, 'w', encoding='utf-8') as out:
    for line in f:
        # Replace the Oseem gear
        for oseem, modern in replacements.items():
            if oseem in line:
                line = line.replace(oseem, modern)
        out.write(line)

os.replace(temp_file, blu_file)

print("Cleaned Oseem gear from BLU!")
