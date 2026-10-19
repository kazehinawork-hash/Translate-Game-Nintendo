import json
import os
import struct
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ge3_build_mod import is_text_table, load_mapping, parse_pkh, translate_table

game_dir = sys.argv[1]
romfs = sys.argv[2]
mapping = load_mapping(os.path.join(game_dir, "translations", "chunks"))
stem = os.path.join(romfs, "resource", "target", "nx", "pack", "mount", "retail", "archive00")
entries = parse_pkh(stem + ".pkh")
count = 0
changed_total = 0
import time
t0 = time.time()
for i, (h, z1, z2, off, unc, comp) in enumerate(entries):
    with open(stem + ".pk", "rb") as f:
        f.seek(off)
        raw = f.read(comp if comp > 0 else unc)
    data = zlib.decompress(raw) if comp > 0 else raw
    if not is_text_table(data):
        continue
    count += 1
    new_data, changed = translate_table(data, mapping)
    if new_data is not None:
        changed_total += changed
        if count <= 5:
            print("entry", i, "changed rows", changed, "new size", len(new_data))
    if count % 500 == 0:
        print("text tables", count, "changed", changed_total, "t", round(time.time()-t0, 1))
print("done text tables", count, "changed rows", changed_total)
