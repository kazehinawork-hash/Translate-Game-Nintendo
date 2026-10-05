"""Truy 18 cho lech giua thanh pham va kirby_vi.json."""
import json
import os
import sys

sys.path.insert(0, r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\tools')
sys.stdout.reconfigure(encoding='utf-8')
from extract_msbt import parse_msbt_bytes

ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '01004D300C5AE000'
G = os.path.join(ROOT, 'games', f'{TID}_Kirby')
MODM = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'msg', 'Kirby15')
vi = json.load(open(os.path.join(G, 'translations', 'kirby_vi.json'), encoding='utf-8'))

n = 0
for lang in sorted(os.listdir(MODM)):
    d = os.path.join(MODM, lang)
    if not os.path.isdir(d):
        continue
    for fn in sorted(os.listdir(d)):
        if not fn.endswith('.msbt'):
            continue
        built = parse_msbt_bytes(open(os.path.join(d, fn), 'rb').read())
        for k, v in vi.get(fn, {}).items():
            got = built.get(k, '')
            if got != v:
                n += 1
                if n <= 6:
                    print(f'[{lang}/{fn}/{k}]')
                    print(f'  mong doi: {v!r}')
                    print(f'  thuc te : {got!r}')
print(f'\ntong lech: {n}')
