import os
import sys
import struct
import json

sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect MAIN-frFR (17737 entries) and SUB-deDE (17737 entries)
def parse_avaf(path):
    with open(path, 'rb') as f:
        data = f.read()
    entry_count, hdr_len, off1, off2, off3 = struct.unpack('<QQQQQ', data[0x20:0x48])
    entries = {}
    table_offset = 0x48
    for i in range(entry_count):
        k_off, k_unk, k_len = struct.unpack('<III', data[table_offset + i*24 : table_offset + i*24 + 12])
        v_off, v_unk, v_len = struct.unpack('<III', data[table_offset + i*24 + 12 : table_offset + i*24 + 24])
        k_str = data[off2 + k_off : off2 + k_off + k_len].decode('utf-8', errors='replace')
        v_str = data[off2 + v_off : off2 + v_off + v_len].decode('utf-8', errors='replace')
        entries[k_str] = v_str
    return entries

ar_main = parse_avaf('games/0100F7E00C70E000_Hogwarts/source/raw_text/en-US/MAIN-frFR.bin')
zh_main = parse_avaf('games/0100F7E00C70E000_Hogwarts/source/raw_text/en-US/SUB-deDE.bin')

print(f'Total keys in Main: {len(ar_main)}')

# Let's check categories in keys
categories = {}
for k in ar_main.keys():
    prefix = k.split('_')[0]
    categories[prefix] = categories.get(prefix, 0) + 1

print('Top key prefixes:')
for p, c in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:25]:
    print(f'  {p:20}: {c}')

# Save a clean bilingual reference (Key, English_ID, Chinese_Source) to games/0100F7E00C70E000_Hogwarts/source/extracted_json/hogwarts_main_raw.json
out_list = []
for k, zh in zh_main.items():
    out_list.append({
        "Key": k,
        "Source_ZH": zh,
        "Source_AR": ar_main.get(k, "")
    })

os.makedirs('games/0100F7E00C70E000_Hogwarts/source/extracted_json', exist_ok=True)
with open('games/0100F7E00C70E000_Hogwarts/source/extracted_json/hogwarts_main_raw.json', 'w', encoding='utf-8') as f:
    json.dump(out_list, f, ensure_ascii=False, indent=2)

print('Saved games/0100F7E00C70E000_Hogwarts/source/extracted_json/hogwarts_main_raw.json!')
