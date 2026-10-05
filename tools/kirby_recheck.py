"""Kiem tra lai sau khi thong nhat: 'Choi lai' co phai cua 'Replay' khong, va nhat quan moi."""
import json
import os
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
G = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby')
en = json.load(open(os.path.join(G, 'translations', 'kirby_en.json'), encoding='utf-8'))
vi = json.load(open(os.path.join(G, 'translations', 'kirby_vi.json'), encoding='utf-8'))

print('=== chuoi nguon co "Replay"/"Retry" ===')
for fn, entries in en.items():
    for k, s in entries.items():
        if 'Replay' in str(s) or 'Retry' in str(s):
            print(f'  [{fn}/{k}] {str(s)[:50]!r} -> {str(vi.get(fn,{}).get(k,""))[:50]!r}')

print('\n=== nhat quan lai ===')
by_en = defaultdict(set)
for fn, entries in en.items():
    for k, s in entries.items():
        v = vi.get(fn, {}).get(k)
        if v is not None:
            by_en[str(s).strip()].add(str(v).strip())
dup = {k: v for k, v in by_en.items() if len(v) > 1}
print(f'  so cau nguon dich nhieu kieu: {len(dup)}')
for k, v in list(dup.items())[:10]:
    print(f'    EN {k[:45]!r} -> {list(v)}')

print('\n=== thuat ngu chinh da dong nhat chua ===')
c = Counter()
for entries in vi.values():
    for v in entries.values():
        for m in ('Chế Độ Ngậm', 'Há Miệng', 'Mouthful Mode', 'Chế Độ Há Miệng'):
            if m in str(v):
                c[m] += 1
print('  ', dict(c))
