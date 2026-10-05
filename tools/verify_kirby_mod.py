"""Mo lai thanh pham MSBT da build de kiem chung (BAI-HOC #9)."""
import json
import os
import sys

sys.path.insert(0, r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\tools')
sys.stdout.reconfigure(encoding='utf-8')
from extract_msbt import parse_msbt_bytes

ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '01004D300C5AE000'
MOD = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'msg', 'Kirby15')
G = os.path.join(ROOT, 'games', f'{TID}_Kirby')
vi = json.load(open(os.path.join(G, 'translations', 'kirby_vi.json'), encoding='utf-8'))

tot = ok = miss = 0
for lang in ('US_English', 'EU_German'):
    d = os.path.join(MOD, lang)
    if not os.path.isdir(d):
        continue
    print(f'\n=== {lang} ===')
    for fn in sorted(os.listdir(d)):
        if not fn.endswith('.msbt'):
            continue
        built = parse_msbt_bytes(open(os.path.join(d, fn), 'rb').read())
        want = vi.get(fn, {})
        for k, v in want.items():
            tot += 1
            if built.get(k, '') == v:
                ok += 1
            else:
                miss += 1
                if miss <= 5:
                    print(f'  LECH [{fn}/{k}]')
                    print(f'    mong doi: {v[:70]!r}')
                    print(f'    thuc te : {built.get(k,"")[:70]!r}')
print(f'\nkiem chung {tot:,} chuoi | khop {ok:,} | lech {miss}')
print('KET QUA:', 'PASS' if miss == 0 else 'CO LOI')

print('\n=== vi du doc lai tu thanh pham (US_English) ===')
for fn in ('Cmn.msbt', 'Credit.msbt'):
    p = os.path.join(MOD, 'US_English', fn)
    if os.path.exists(p):
        e = parse_msbt_bytes(open(p, 'rb').read())
        print(f'  {fn}: {len(e)} chuoi')
        for k, v in list(e.items())[:4]:
            print(f'    {k} = {str(v)[:70]!r}')
