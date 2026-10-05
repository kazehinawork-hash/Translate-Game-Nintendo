"""Chia chuoi Kirby thanh cac chunk de dich + xem mau the dieu khien."""
import json
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
G = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby')
D = json.load(open(os.path.join(G, 'translations', 'kirby_en.json'), encoding='utf-8'))
T = os.path.join(G, 'translations')
os.makedirs(T, exist_ok=True)
for f in os.listdir(T):
    if f.startswith(('todo_', 'vi_')):
        os.remove(os.path.join(T, f))

items = []
for fn, entries in D.items():
    for k, v in entries.items():
        items.append({'file': fn, 'key': k, 'en': str(v)})

# thong ke the dieu khien
TAG = re.compile(r'\[[A-Za-z_]{2,}\]|<[^<>]{1,30}>|\\u000e[0-9a-fA-F]{2}|[%{][A-Za-z0-9_]+[}]')
c = Counter()
for it in items:
    for t in TAG.findall(it['en']):
        c[t] += 1
print(f'{len(items):,} chuoi | the gap nhieu nhat:')
for k, v in c.most_common(18):
    print(f'  {k!r:<28} x{v}')

print('\n=== 6 chuoi dai nhat (xem the) ===')
for it in sorted(items, key=lambda x: -len(x['en']))[:3]:
    print(f"  [{it['file']}] {it['key']}:\n    {it['en'][:300]!r}")

items.sort(key=lambda x: len(x['en']))
CH = 260
n = 0
for i in range(0, len(items), CH):
    n += 1
    part = items[i:i + CH]
    p = os.path.join(T, f'todo_{n:02d}.json')
    json.dump(part, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'  todo_{n:02d}.json: {len(part)} chuoi | dai nhat {max(len(x["en"]) for x in part)}')
print(f'tong {n} chunk')
