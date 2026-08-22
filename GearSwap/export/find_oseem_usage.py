import re
import glob

oseem_aliases = set()
for lua_file in glob.glob("/home/romain/luas/GearSwap/data/Tenroh/Tenroh_*_Gear.lua"):
    with open(lua_file, 'r', encoding='utf-8') as f:
        for line in f:
            matches = re.findall(r'gear\.(grioavolr|chironic|merlinic|herculean|odyssean|valorous|taeon)[a-zA-Z0-9_]*', line)
            for m in re.finditer(r'gear\.(grioavolr|chironic|merlinic|herculean|odyssean|valorous|taeon)[a-zA-Z0-9_]*', line):
                oseem_aliases.add(m.group(0))

print("Used Oseem Aliases:")
for a in sorted(oseem_aliases):
    print(a)
