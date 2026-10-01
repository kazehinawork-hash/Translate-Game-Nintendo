# -*- coding: utf-8 -*-
import json
import re
import sys

from trans_part1 import translations_0_100
from trans_part2 import translations_100_200
from trans_part3 import translations_200_300
from trans_part4 import translations_300_400
from trans_part4_b import translations_400_500
from trans_part5 import translations_500_600
from trans_part6 import translations_600_end

# Combine all translation parts
all_trans = {}
for p in [translations_0_100, translations_100_200, translations_200_300, 
          translations_300_400, translations_400_500, translations_500_600, translations_600_end]:
    all_trans.update(p)

print(f"Total translations collected: {len(all_trans)}")

# Load original file
src_path = 'working/0100F7E00C70E000_Hogwarts/split_tasks/spells_and_potions.json'
with open(src_path, 'r', encoding='utf-8') as f:
    source_items = json.load(f)

print(f"Total source items: {len(source_items)}")

# Check missing keys
missing = []
out_list = []
for item in source_items:
    k = item['Key']
    if k not in all_trans:
        missing.append(k)
    else:
        out_list.append({
            "Key": k,
            "Vietnamese": all_trans[k]
        })

if missing:
    print(f"WARNING: {len(missing)} keys missing translation!")
    for m in missing[:10]:
        print(f"  Missing: {m}")
    sys.exit(1)

# Check tag validation
print("\n--- Validating Tags ---")
tag_errors = 0
for item, out_item in zip(source_items, out_list):
    k = item['Key']
    zh_text = item.get('Source_ZH', '')
    vi_text = out_item.get('Vietnamese', '')
    
    # Extract tags
    zh_tags = set(re.findall(r'\{[^}]+\}|<[^>]+>', zh_text))
    vi_tags = set(re.findall(r'\{[^}]+\}|<[^>]+>', vi_text))
    
    diff = zh_tags.symmetric_difference(vi_tags)
    if diff:
        print(f"Tag mismatch in Key: {k}")
        print(f"  ZH tags: {zh_tags}")
        print(f"  VI tags: {vi_tags}")
        print(f"  Diff: {diff}")
        tag_errors += 1

if tag_errors == 0:
    print("ALL TAGS VALIDATED SUCCESSFULLY! 100% MATCH!")
else:
    print(f"Found {tag_errors} tag mismatches! Please fix.")
    sys.exit(1)

# Write output file
out_path = 'working/0100F7E00C70E000_Hogwarts/split_tasks/translated_spells_potions.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(out_list, f, ensure_ascii=False, indent=2)

print(f"\nSaved translated output to {out_path} ({len(out_list)} entries)")
