"""Danh gia 3 game: nguon vs thanh pham, va liet ke viec can lam."""
import csv
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'

# 1. Don 2 dong glossary bao nham (chi la the [Map]/[Interact] trong nguon)
gp = os.path.join(ROOT, 'glossary', 'ori.csv')
rows = [l for l in open(gp, encoding='utf-8').read().splitlines()
        if not l.startswith(('Map,', 'Interact,'))]
open(gp, 'w', encoding='utf-8').write('\n'.join(rows) + '\n')
print(f'glossary/ori.csv: {len(rows)-1} thuat ngu (da bo 2 dong trung the [Map]/[Interact])')

# 2. Kiem tra nguon 3 game
def load(p):
    d = json.load(open(p, encoding='utf-8'))
    if isinstance(d, list):
        k = 'VI' if d and 'VI' in d[0] else 'vi'
        return [(str(x.get('Id', x.get('key', ''))), str(x.get('EN', x.get('en', ''))), str(x.get(k, ''))) for x in d]
    return [(k2, '', str(v)) for k2, v in d.items()]

for tag, p in (('Ori WotW', r'games\01008DD013200000_OriAndTheWillOfTheWisps\translations\ori_vi.json'),
               ('Ori BF', r'games\010061D00DB74000_OriAndTheBlindForest\translations\obf_vi.json'),
               ('Unravel', r'games\0100E5D00CC0C000_UnravelTwo\translations\vi_all.json')):
    f = os.path.join(ROOT, p)
    if not os.path.exists(f):
        print(f'{tag}: khong co file')
        continue
    try:
        items = load(f)
        vi_ok = sum(1 for _, _, v in items if any(ord(c) > 127 for c in v))
        print(f'{tag:<10}: {len(items):>5} muc | co tieng Viet {vi_ok:>5} ({vi_ok*100//max(1,len(items))}%)')
    except Exception as e:
        print(f'{tag:<10}: doc loi {type(e).__name__}')

print('\n=== glossary hien co ===')
for f in sorted(os.listdir(os.path.join(ROOT, 'glossary'))):
    n = len(open(os.path.join(ROOT, 'glossary', f), encoding='utf-8').read().splitlines()) - 1
    print(f'  {f:<24} {n:>4} thuat ngu')
