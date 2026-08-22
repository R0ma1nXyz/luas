import re
import os

blu_file = "/home/romain/luas/GearSwap/data/Tenroh/Tenroh_Blu_Gear.lua"
temp_file = blu_file + ".tmp"

with open(blu_file, 'r', encoding='utf-8') as f, open(temp_file, 'w', encoding='utf-8') as out:
    lines = f.readlines()
    for i, line in enumerate(lines):
        # Fix Burst Affinity
        if "sets.buff['Burst Affinity']" in line:
            line = line.replace('legs="Assim. Shalwar +3"', 'legs="Assim. Shalwar +1"')
        # Fix Chain Affinity
        if "sets.buff['Chain Affinity']" in line:
            line = line.replace('feet="Hashi. Basmak +3"', 'feet="Assim. Charuqs +1"')
        # Fix Convergence
        if "sets.buff.Convergence" in line:
            line = line.replace('head="Hashishin Kavuk +3"', 'head="Luh. Keffiyeh +1"')
        # Fix Diffusion
        if "sets.buff.Diffusion" in line:
            line = line.replace('feet="Hashi. Basmak +3"', 'feet="Luhlaza Charuqs +1"')
        # Fix Enchainment
        if "sets.buff.Enchainment" in line and "{}" in line:
            line = line.replace("{}", '{body="Luhlaza Jubbah +1"} -- BiS: Luhlaza Jubbah +3')
            
        # Fix Blue Magic Skill (around lines 200-210)
        if "head=\"Hashishin Kavuk +3\"" in line and "-- BiS: Luh. Keffiyeh +3" in line:
            line = line.replace('head="Hashishin Kavuk +3"', 'head="Luh. Keffiyeh +1"')
        if "body=\"Hashishin Mintan +3\"" in line and "-- BiS: Assim. Jubbah +3" in line:
            line = line.replace('body="Hashishin Mintan +3"', 'body="Assim. Jubbah +2"')
        if "feet=\"Luhlaza Charuqs +3\"" in line:
            line = line.replace('feet="Luhlaza Charuqs +3"', 'feet="Luhlaza Charuqs +1"')
        if "feet=\"Luhlaza Charuqs +3\"" in line and "-- BiS:" not in line:
            line = line.replace('\n', ' -- BiS: Luhlaza Charuqs +3\n')

        out.write(line)

os.replace(temp_file, blu_file)
print("Fixed BLU JA sets!")
