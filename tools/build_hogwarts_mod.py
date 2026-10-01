import os
import sys
import json
from avaf_codec import pack_avafdict

sys.stdout.reconfigure(encoding='utf-8')

# Output path in Atmosphere layeredfs:
# output/atmosphere/contents/0100F7E00C70E000/romfs/Phoenix/Content/Localization/SWITCH/
mod_dir = 'output/atmosphere/contents/0100F7E00C70E000/romfs/Phoenix/Content/Localization/SWITCH'
os.makedirs(mod_dir, exist_ok=True)

# Collect all translations
trans_map = {}
split_dir = 'games/0100F7E00C70E000_Hogwarts/translations'
for f in os.listdir(split_dir):
    if f.startswith('translated_') and f.endswith('.json'):
        fp = os.path.join(split_dir, f)
        try:
            with open(fp, 'r', encoding='utf-8') as jf:
                items = json.load(jf)
                for it in items:
                    trans_map[it['Key']] = it['Vietnamese']
        except Exception as e:
            print(f'Error reading {f}: {e}')

print(f'Total translated keys gathered: {len(trans_map)}')

# Load full base dictionary to ensure all 17,737 keys are present
raw_path = 'games/0100F7E00C70E000_Hogwarts/source/extracted_json/hogwarts_main_raw.json'
with open(raw_path, 'r', encoding='utf-8') as f:
    base_items = json.load(f)

final_main = {}
for item in base_items:
    k = item['Key']
    if k in trans_map:
        final_main[k] = trans_map[k]
    else:
        # Fallback to original text until translated
        final_main[k] = item['Source_ZH']

# Pack into MAIN AVAFDICT bin
packed_data = pack_avafdict(final_main)
print(f'Packed final MAIN dictionary: {len(final_main)} entries ({len(packed_data)} bytes)')

# In Hogwarts Legacy Switch, we write to the target language bins:
# English / French / German / Traditional Chinese / Simplified Chinese
target_bins = [
    'MAIN-enUS.bin',
    'MAIN-frFR.bin',
    'MAIN-deDE.bin',
    'MAIN-zhCN.bin',
    'MAIN-zhTW.bin'
]

for tb in target_bins:
    out_file = os.path.join(mod_dir, tb)
    with open(out_file, 'wb') as out_f:
        out_f.write(packed_data)
    print(f'Generated LayeredFS mod: {out_file}')

print('Mod build step completed successfully!')
