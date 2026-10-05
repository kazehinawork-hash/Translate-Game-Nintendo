"""Boc toan bo chuoi MSBT cua Kirby and the Forgotten Land (ban tieng Anh)."""
import json
import os
import sys

sys.path.insert(0, r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\tools')
sys.stdout.reconfigure(encoding='utf-8')
from extract_msbt import parse_msbt_bytes

ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
G = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby')
SRC = os.path.join(G, 'source', 'msg', 'Kirby15', 'US_English')
OUT = os.path.join(G, 'translations')
os.makedirs(OUT, exist_ok=True)

per_file = {}
total = 0
empty = 0
for r, _, fs in os.walk(SRC):
    for fn in sorted(fs):
        if not fn.endswith('.msbt'):
            continue
        p = os.path.join(r, fn)
        rel = os.path.relpath(p, SRC).replace('\\', '/')
        try:
            entries = parse_msbt_bytes(open(p, 'rb').read())
        except Exception as e:
            print(f'  LOI {rel}: {type(e).__name__} {str(e)[:60]}')
            continue
        if not entries:
            print(f'  (khong doc duoc) {rel}')
            continue
        per_file[rel] = entries
        total += len(entries)
        empty += sum(1 for v in entries.values() if not str(v).strip())

print(f'\n{len(per_file)} file MSBT | {total:,} chuoi | rong {empty}')
json.dump(per_file, open(os.path.join(OUT, 'kirby_en.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('da luu translations/kirby_en.json')

# thong ke file lon nhat
sizes = sorted(((len(v), k) for k, v in per_file.items()), reverse=True)
print('\nfile nhieu chuoi nhat:')
for n, k in sizes[:12]:
    print(f'  {n:>5}  {k}')
print('\nvi du:')
first = sizes[0][1]
for k, v in list(per_file[first].items())[:8]:
    print(f'  [{first}] {k} = {str(v)[:80]!r}')
