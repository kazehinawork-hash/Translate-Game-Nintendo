"""Rut thuat ngu tu ban dich Unravel Two + kiem tra nhat quan (format {key,vi,en})."""
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
G = os.path.join(ROOT, 'games', '0100E5D00CC0C000_UnravelTwo')
d = json.load(open(os.path.join(G, 'translations', 'vi_all.json'), encoding='utf-8'))
print(f'{len(d)} muc')

by_en = defaultdict(set)
for x in d:
    by_en[str(x.get('en', '')).strip()].add(str(x.get('vi', '')).strip())
dup = {k: v for k, v in by_en.items() if len(v) > 1}
print(f'nhat quan: {len(dup)} cau nguon dich nhieu kieu')
for k, v in list(dup.items())[:8]:
    print(f'  EN {k[:45]!r} -> {list(v)}')

cnt = Counter()
ex = {}
for x in d:
    for w in re.findall(r"\b[A-Z][A-Za-z'\-]{2,}\b", str(x.get('en', ''))):
        cnt[w] += 1
        ex.setdefault(w, (str(x.get('en', ''))[:55], str(x.get('vi', ''))[:60]))
print('\nthuat ngu viet hoa hay gap (goi y glossary):')
for w, c in cnt.most_common(22):
    s, v = ex[w]
    print(f'  {c:>4}  {w:<22} {s!r} -> {v!r}')
