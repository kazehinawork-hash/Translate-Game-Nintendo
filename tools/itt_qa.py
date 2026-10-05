"""QA + gop ban dich It Takes Two, roi GHI NGUOC vao JSON asset."""
import json
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
G = os.path.join(ROOT, 'games', '010092A0172E4000_ItTakesTwo')
T = os.path.join(G, 'translations')

keys = json.load(open(os.path.join(T, 'uniq_en.json'), encoding='utf-8'))
assert len(keys) == len(set(keys)), 'uniq_en.json co trung'
print(f'{len(keys):,} chuoi nguon duy nhat')

BAD = re.compile(r'[\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff00-\uffef'
                 r'\u1100-\u11ff\u3130-\u318f\uac00-\ud7ff\u3040-\u30ff\u0600-\u06ff\u0400-\u04ff]')
vi = {}
bad = missing = cjk = nl = 0
for n in range(1, 9):
    p = os.path.join(T, f'vi_{n}.json')
    d = json.load(open(p, encoding='utf-8'))
    for k, v in d.items():
        if k in vi:
            continue
        vi[k] = v
        if not str(v).strip():
            bad += 1
        if BAD.search(str(v)):
            cjk += 1
            if cjk <= 3:
                print(f'  KY TU LA: {k[:40]!r} -> {v[:50]!r}')
        if str(k).count('\n') != str(v).count('\n'):
            nl += 1
            if nl <= 3:
                print(f'  LECH XUONG DONG: {k[:40]!r} ({k.count(chr(10))}) vs {v[:40]!r} ({str(v).count(chr(10))})')
miss = [k for k in keys if k not in vi]
print(f'\ngop {len(vi):,} kep | thieu {len(miss)} | rong {bad} | ky tu la {cjk} | lech xuong dong {nl}')
if miss:
    for k in miss[:5]:
        print('  thieu:', repr(k[:60]))

json.dump(vi, open(os.path.join(T, 'itt_vi.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('da luu translations/itt_vi.json')
print('KET QUA:', 'PASS' if not (bad or miss) else 'CAN XEM LAI')
