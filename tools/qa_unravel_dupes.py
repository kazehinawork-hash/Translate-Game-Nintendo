"""Kiem tra cac key bi trung (nguon lan ngon ngu) trong ban dich Unravel Two."""
import json
import os
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')
G = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\games\0100E5D00CC0C000_UnravelTwo'
T = os.path.join(G, 'translations')

# nguon theo tung file todo
per_file = {}
for f in sorted(os.listdir(T)):
    if f.startswith('todo_'):
        per_file[f] = json.load(open(os.path.join(T, f), encoding='utf-8'))

vi_by_file = {}
for f in sorted(os.listdir(T)):
    if f.startswith('vi_'):
        vi_by_file[f] = {x['key']: x['vi'] for x in json.load(open(os.path.join(T, f), encoding='utf-8'))}

print('=== cac key xuat hien o NHIEU chunk ===')
seen = defaultdict(list)
for tf, items in per_file.items():
    vf = 'vi_' + tf[5:]
    for x in items:
        seen[x['key']].append((tf, x['en'][:70], vi_by_file.get(vf, {}).get(x['key'], '')[:70]))
multi = {k: v for k, v in seen.items() if len(v) > 1}
print(f'tong key trung: {len(multi)}')
diff = 0
for k, lst in sorted(multi.items()):
    vals = set(x[2] for x in lst)
    if len(vals) > 1:
        diff += 1
        print(f'\n  !! {k} co {len(vals)} ban dich KHAC NHAU:')
        for tf, en, vi in lst:
            print(f'     [{tf}] en={en!r}\n        vi={vi!r}')
print(f'\n-> {diff}/{len(multi)} key trung co ban dich khac nhau')
