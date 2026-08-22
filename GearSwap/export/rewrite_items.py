import re
import os

export_file = "/home/romain/luas/GearSwap/export/Tenroh 2026-08-22 12-06-56.lua"
items_file = "/home/romain/luas/GearSwap/data/Tenroh/Tenroh-Items.lua"

# We will parse the exact Oseem pieces the user owns and assign them logical variable names based on their augments.
oseem_pieces = []
with open(export_file, 'r', encoding='utf-8') as f:
    for line in f:
        match = re.search(r'^\s*\w+=\{(name="(Chironic|Merlinic|Herculean|Odyssean|Valorous|Grioavolr)[^"]*", augments=\{.*\}),\}', line)
        if match:
            oseem_pieces.append(match.group(1))

# Manually assign aliases based on the augments we found earlier
aliases = {}
for p in oseem_pieces:
    name_match = re.search(r'name="([^"]+)"', p)
    aug_match = re.search(r'augments=\{(.*?)\}', p)
    
    if not name_match or not aug_match: continue
    
    name = name_match.group(1)
    augments = aug_match.group(1)
    
    # Heuristics for naming
    tag = "misc"
    if "Treasure Hunter" in augments:
        tag = "th"
    elif "Fast Cast" in augments:
        tag = "fc"
    elif "Triple Atk" in augments or "Double Atk" in augments:
        tag = "ta"
    elif "Drain" in augments and "Aspir" in augments:
        tag = "aspir"
    elif "Spell interruption rate down" in augments:
        tag = "sird"
    elif "Phalanx" in augments:
        tag = "phalanx"
    elif "Refresh" in augments:
        tag = "refresh"
    elif "Mag.Atk.Bns." in augments or "Mag. Acc." in augments:
        tag = "nuke" # fallback for magic
        
    part = "misc"
    if "Head" in name or "Hat" in name or "Helm" in name or "Hood" in name or "Mask" in name:
        part = "head"
    elif "Body" in name or "Vest" in name or "Doublet" in name or "Mail" in name or "Jupon" in name:
        part = "body"
    elif "Hands" in name or "Gloves" in name or "Dastanas" in name or "Gauntlets" in name:
        part = "hands"
    elif "Legs" in name or "Trousers" in name or "Hose" in name or "Shalwar" in name or "Breeches" in name:
        part = "legs"
    elif "Feet" in name or "Boots" in name or "Greaves" in name or "Crackows" in name or "Slippers" in name:
        part = "feet"
    elif "Grioavolr" in name:
        part = "staff"
        
    alias = f"gear.{name.split()[0].lower()}_{tag}_{part}"
    
    # Handle duplicates by appending _2, _3, etc.
    original_alias = alias
    count = 2
    while alias in aliases:
        alias = f"{original_alias}_{count}"
        count += 1
        
    aliases[alias] = p

new_content = """--Gearsets your character will use among multiple jobs.
sets.BehemothSuit = {body="Behemoth Suit +1",hands=empty,legs=empty,feet=empty}
sets.Sheltered = {ring2="Sheltered Ring"}
sets.Capacity = {back="Mecisto. Mantle"}

sets.buff.RolledEleven = {}
sets.buff.Doom = {waist="Gishdubar Sash"}
sets.TreasureHunter = {head="Volte Cap",hands="Volte Bracers"}

sets.midcast.Item['Hallowed Water'] = {}
sets.midcast.Item['Holy Water'] = {}

--Augmented items that you'll use among multiple jobs.
"""

for alias, p in aliases.items():
    new_content += f"{alias} = {{{p}}}\n"

with open(items_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Generated {len(aliases)} Oseem aliases in Tenroh-Items.lua")
for k, v in aliases.items():
    print(k)

