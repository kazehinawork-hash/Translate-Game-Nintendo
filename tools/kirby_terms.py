"""Xem cac bien the cua thuat ngu chinh trong ban dich Kirby."""
import json
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
G = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby')
vi = json.load(open(os.path.join(G, 'translations', 'kirby_vi.json'), encoding='utf-8'))

KEYS = {
    'Mouthful Mode (từ EN)': None,
}

# 1. ban dich cua cac chuoi chua "Mouthful" trong EN
en = json.load(open(os.path.join(G, 'translations', 'kirby_en.json'), encoding='utf-8'))
print('=== cac ban dich cho chuoi co "Mouthful Mode" ===')
seen = Counter()
for fn, entries in en.items():
    for k, s in entries.items():
        if 'Mouthful Mode' in str(s):
            v = str(vi.get(fn, {}).get(k, ''))
            # rut cum viet hoa lien quan
            for m in re.findall(r'(?:Ngậm|Há Miệng|Miệng Đa Năng|Nuốt)[^\s,.!?]*', v):
                seen[m] += 1
            if len(seen) < 40:
                print(f'  [{fn}/{k}] {str(s)[:60]!r}')
                print(f'      -> {v[:90]!r}')
print('\ncum dich cua Mouthful Mode:', dict(seen.most_common(10)))

print('\n=== tim tat ca cum chi "Mouthful" trong ban dich ===')
c = Counter()
for entries in vi.values():
    for v in entries.values():
        for m in re.findall(r'(?:Ngậm|Há Miệng|Miệng|Nuốt)[^\s,.!?]{0,12}', str(v)):
            c[m] += 1
for k, n in c.most_common(14):
    print(f'  {n:>4}  {k}')

print('\n=== cac chuoi nguon trung nhung dich khac nhau (liet ke) ===')
from collections import defaultdict
by_en = defaultdict(set)
for fn, entries in en.items():
    for k, s in entries.items():
        v = vi.get(fn, {}).get(k)
        if v is not None:
            by_en[str(s).strip()].add(str(v).strip())
for k, v in by_en.items():
    if len(v) > 1 and len(k) < 40:
        print(f'  EN {k!r}: {list(v)}')
