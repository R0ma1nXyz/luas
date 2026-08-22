import re

export_file = "/home/romain/luas/GearSwap/export/Tenroh 2026-08-22 12-06-56.lua"
owned = []
with open(export_file, 'r', encoding='utf-8') as f:
    for line in f:
        match = re.search(r'item="([^"]+)"', line)
        if match:
            owned.append(match.group(1))

keywords = ['Hashishin', 'Luhlaza', 'Assim.', 'Ayanmo', 'Jhakri', 'Adhemar', 'Herculean', 'Rawhide', 'Carmine', 'Rosmerta', 'Amalric', 'Taeon', 'Gleti', 'Bunzi', 'Nyame', 'Malignance']

found = {k: [] for k in keywords}

for item in owned:
    for k in keywords:
        if k.lower() in item.lower():
            found[k].append(item)

for k, items in found.items():
    if items:
        print(f"{k}: {', '.join(set(items))}")
