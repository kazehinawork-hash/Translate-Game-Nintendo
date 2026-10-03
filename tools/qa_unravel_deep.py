"""QC sau: kiem tra day du, nhat quan, do dai UI, bo ky tu (Unravel Two)."""
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')
G = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\games\0100E5D00CC0C000_UnravelTwo'
T = os.path.join(G, 'translations')
src_all = json.load(open(os.path.join(G, 'source', 'unravel_en.json'), encoding='utf-8'))
huge = json.load(open(os.path.join(T, 'huge.json'), encoding='utf-8'))

vi = {}
for f in sorted(os.listdir(T)):
    if f.startswith('vi_'):
        for x in json.load(open(os.path.join(T, f), encoding='utf-8')):
            vi.setdefault(x['key'], []).append(x['vi'])

print('=== 1. DO PHU ===')
print(f'  kho nguon: {len(src_all)} muc | da dich: {len(vi)} key')
missing = [x['key'] for x in src_all if x['key'] not in vi]
print(f'  thieu: {len(missing)} {missing[:10]}')
dupe = {k: v for k, v in vi.items() if len(v) > 1}
print(f'  trung key: {len(dupe)} {list(dupe)[:5]}')

print('\n=== 2. CHUOI CHUA DICH (giong y nguyen tieng Anh) ===')
same = []
for x in src_all:
    if x['key'] in vi and x['en'].strip() == vi[x['key']][0].strip():
        same.append((x['key'], x['en'][:60]))
for k, v in same:
    print(f'  {k} = {v!r}')
print(f'  -> {len(same)} muc (kiem tra xem co phai co y giu nguyen khong)')

print('\n=== 3. NHAT QUAN (cung cau tieng Anh -> cung ban dich?) ===')
by_en = defaultdict(set)
for x in src_all:
    if x['key'] in vi:
        by_en[x['en'].strip()].add(vi[x['key']][0].strip())
bad = {k: v for k, v in by_en.items() if len(v) > 1}
print(f'  cau nguon xuat hien nhieu lan: {sum(1 for v in by_en.values() if len(v) > 1 or True)} | dich khac nhau: {len(bad)}')
for k, v in list(bad.items())[:5]:
    print(f'    EN: {k[:60]!r}\n      -> {[s[:60] for s in v]}')

print('\n=== 4. DO DAI UI (nguy co tran khung) ===')
over = []
for x in src_all:
    if x['key'] not in vi:
        continue
    e, v = x['en'], vi[x['key']][0]
    if len(e) <= 40 and len(v) > len(e) * 1.5 + 6:
        over.append((x['key'], len(e), len(v), e[:40], v[:50]))
over.sort(key=lambda t: -(t[2] - t[1]))
print(f'  chuoi UI dai hon 50%+6: {len(over)}')
for k, le, lv, e, v in over[:12]:
    print(f'    {k}: {le}->{lv} | {e!r} -> {v!r}')

print('\n=== 5. BO KY TU (cho font) ===')
chars = Counter()
for k, lst in vi.items():
    for c in lst[0]:
        chars[c] += 1
vn = sorted(c for c in chars if ord(c) > 127)
print(f'  tong ky tu khac ASCII: {len(vn)}')
print('  ', ''.join(vn))
