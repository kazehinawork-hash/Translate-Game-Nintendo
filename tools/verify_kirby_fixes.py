"""Kiem chung THANH PHAM Kirby da chua cac sua doi (glossary/thong nhat)."""
import io
import json
import os
import sys

sys.path.insert(0, r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\tools')
sys.stdout.reconfigure(encoding='utf-8')
from extract_msbt import parse_msbt_bytes

ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '01004D300C5AE000'
MODM = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'msg', 'Kirby15')

# gom tat ca chuoi trong thanh pham
built = {}
for lang in os.listdir(MODM):
    d = os.path.join(MODM, lang)
    if not os.path.isdir(d):
        continue
    for fn in os.listdir(d):
        if fn.endswith('.msbt'):
            for k, v in parse_msbt_bytes(open(os.path.join(d, fn), 'rb').read()).items():
                built[f'{lang}|{fn}|{k}'] = str(v)

print(f'thang pham: {len(built):,} chuoi trong 9 khe ngon ngu\n')

checks = [
    ('Mouthful Mode (giu tieng Anh)', lambda s: 'Mouthful Mode' in s, 0),
    ('Chế Độ Há Miệng (kieu cu)', lambda s: 'Chế Độ Há Miệng' in s, 0),
    ('Chế Độ Ngậm (kieu moi)', lambda s: 'Chế Độ Ngậm' in s, 999),
    ('Waddle Dee Thông Thái (chuan hoa)', lambda s: 'Waddle Dee thông thái' in s, 0),
    ('Tàn tích Wondaria', lambda s: 'Wondaria Hoang Tàn' in s, 0),
]
allok = True
for label, fn, expect in checks:
    n = sum(1 for v in built.values() if fn(v))
    if expect == 0:
        ok = n == 0
    else:
        ok = n > 0
    allok &= ok
    print(f'  [{"OK " if ok else "LOI"}] {label:<34} x{n}')

print('\n=== 3 ngoai le ngu canh (phai GIU, khong bi thong nhat) ===')
ctx = [('Dialog.msbt', 'Btn_Continue', 'Nghe tiếp'),
       ('Figure.msbt', '$View', 'Ngắm'),
       ('MgameFish.msbt', 'HowToGuide_Fish', 'Câu cá')]
for fn, k, want in ctx:
    key = f'US_English|{fn}|{k}'
    got = built.get(key, '(khong thay)')
    ok = got == want
    allok &= ok
    print(f'  [{"OK " if ok else "LOI"}] {fn}/{k}: {got!r} (mong doi {want!r})')

print('\n=== 3 cho Retry ===')
for k in ('DestInfo_Retry', 'Btn_Retry'):
    key = f'US_English|Cmn.msbt|{k}' if k == 'DestInfo_Retry' else f'US_English|Dialog.msbt|{k}'
    print(f'  {k}: {built.get(key, "(khong thay)")!r}')

print('\nKET QUA THANH PHAM:', 'PASS - da chua moi sua doi' if allok else 'CAN BUILD LAI')
