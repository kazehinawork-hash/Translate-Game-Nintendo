"""Kiem tra nhat quan thuat ngu ban dich Kirby + rut ra glossary."""
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
G = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby')

en = json.load(open(os.path.join(G, 'translations', 'kirby_en.json'), encoding='utf-8'))
vi = json.load(open(os.path.join(G, 'translations', 'kirby_vi.json'), encoding='utf-8'))

# 1. cung cau nguon -> cung ban dich?
by_en = defaultdict(set)
pairs = []
for fn, entries in en.items():
    for k, s in entries.items():
        v = vi.get(fn, {}).get(k)
        if v is None:
            continue
        pairs.append((fn, k, str(s), str(v)))
        by_en[str(s).strip()].add(str(v).strip())

dup = {k: v for k, v in by_en.items() if len(v) > 1}
print(f'=== NHAT QUAN ===')
print(f'  {len(pairs):,} cap | cau nguon xuat hien >1 lan: {sum(1 for v in by_en.values() if True and list(by_en.values()))}')
print(f'  cung cau nguon nhung dich KHAC nhau: {len(dup)}')
for k, v in list(dup.items())[:6]:
    print(f'    EN: {k[:60]!r}')
    for x in list(v)[:3]:
        print(f'      -> {x[:60]!r}')

# 2. thuat ngu xuat hien lap lai (candidate glossary)
term_cnt = Counter()
term_vi = defaultdict(Counter)
WORD = re.compile(r"[A-Za-z][A-Za-z'\- ]{2,30}")
for fn, k, s, v in pairs:
    for w in WORD.findall(s):
        w2 = w.strip()
        if len(w2.split()) == 1 and len(w2) < 4:
            continue
        term_cnt[w2] += 1
        term_vi[w2][v.strip()] += 1

print(f'\n=== THUAT NGU LAP LAI (>=4 lan) ===')
rows = []
for term, c in term_cnt.most_common(400):
    if c < 4:
        continue
    best, bc = term_vi[term].most_common(1)[0]
    # ty le dong nhat: cau dich chua cum dich pho bien nhat
    n_ok = sum(1 for x in term_vi[term].values() if x == best)
    rows.append((c, term, best[:50], len(term_vi[term])))
print(f'  {"lan":>4}  {"EN":<34} {"VI pho bien":<40} so bien the')
for c, t, b, nb in rows[:30]:
    flag = '' if nb == 1 else f'  <-- {nb} bien the'
    print(f'  {c:>4}  {t[:33]:<34} {b[:39]:<40}{flag}')
