import json
import os
import sys

src = json.load(open(sys.argv[1], encoding="utf-8"))
out = sys.argv[2]
os.makedirs(out, exist_ok=True)
ids = [k for k in src if k.strip()]
print("ids", len(ids))
size = 350
for i in range(0, len(ids), size):
    chunk = {k: src[k] for k in ids[i:i + size]}
    p = os.path.join(out, f"repair_{i // size:02d}.json")
    json.dump(chunk, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", p, len(chunk))
