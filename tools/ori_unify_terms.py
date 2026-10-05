"""Dem bien the ten goi Ori WotW + thong nhat + loc duong tinh gia cua glossary."""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
G = os.path.join(ROOT, 'games', '01008DD013200000_OriAndTheWillOfTheWisps')
P = os.path.join(G, 'translations', 'ori_vi.json')
d = json.load(open(P, encoding='utf-8'))
print(f'{len(d)} muc | dang: {list(d[0].keys()) if d else "?"}')

CONCEPTS = {
    'Spirit Light': ['Ánh Sáng Linh Hồn', 'Ánh Sáng Tinh Linh'],
    'Silent Woods': ['Rừng Im Lặng', 'Rừng Tĩnh Lặng'],
    'Mouldwood Depths': ['Vực Thẳm Mouldwood', 'Đáy Rừng Mốc', 'ĐÁY RỪNG MỐC'],
    'Wellspring Glades': ['Rừng Suối Nguồn', 'Đồng Cỏ Suối Nguồn', 'ĐỒNG CỎ SUỐI NGUỒN'],
}
print('\n=== dem bien the trong ban dich ===')
counts = {}
for c, variants in CONCEPTS.items():
    for v in variants:
        n = sum(1 for x in d if v.lower() in str(x.get('VI', '') or x.get('vi', '')).lower())
        counts[v] = n
        print(f'  {c:<20} {v:<24} x{n}')

# chon bien the nhieu nhat lam chuan, gop cac bien the it hon
FIX = {
    'Ánh Sáng Tinh Linh': 'Ánh Sáng Linh Hồn',
    'Rừng Tĩnh Lặng': 'Rừng Im Lặng',
    'Đáy Rừng Mốc': 'Vực Thẳm Mouldwood',
    'ĐÁY RỪNG MỐC': 'VỰC THẲM MOULDWOOD',
    'Đồng Cỏ Suối Nguồn': 'Rừng Suối Nguồn',
    'ĐỒNG CỎ SUỐI NGUỒN': 'RỪNG SUỐI NGUỒN',
}
print('\n=== thong nhat theo bien the pho bien ===')
n_fix = 0
key_vi = 'VI' if 'VI' in (d[0] if d else {}) else 'vi'
for x in d:
    v = str(x.get(key_vi, ''))
    nv = v
    for a, b in FIX.items():
        nv = nv.replace(a, b)
    if nv != v:
        x[key_vi] = nv
        n_fix += 1
print(f'  sua {n_fix} muc')
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'  da luu {P}')

# kiem tra lai
d2 = json.load(open(P, encoding='utf-8'))
for c, variants in CONCEPTS.items():
    for v in variants[1:]:
        n = sum(1 for x in d2 if v.lower() in str(x.get(key_vi, '')).lower())
        if n:
            print(f'  CON LAI {v}: x{n}')
print('xong')
