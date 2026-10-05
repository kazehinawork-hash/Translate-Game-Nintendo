"""QA + gop ban dich Kirby: khop key, ma dieu khien, chuoi rong, ky tu la."""
import json
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
G = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby')
T = os.path.join(G, 'translations')

CTRL = re.compile(r'[\u0000-\u001f\u007f-\u009f\ue000-\uf8ff]')
# khu vuc the dieu khien cua game: \u000e + group + type + len + len/2 ky tu du lieu
TAGZONE = re.compile(r'\u000e[\s\S]{0,3}[\s\S]{0,60}?(?=[\u0020-\u007e\u00a0-\u02ff\u1e00-\u1eff]|$)')
BAD = re.compile(r'[\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff00-\uffef'
                 r'\u1100-\u11ff\u3130-\u318f\uac00-\ud7ff\u3040-\u30ff'
                 r'\u0600-\u06ff\u0400-\u04ff]')


def strip_tags(s):
    """Bo cac the dieu khien (\u000e + payload) de soi ky tu la ngoai the."""
    out = []
    i = 0
    while i < len(s):
        if s[i] == '\u000e':
            i += 1
            # group(1) + type(1) + len(1)
            if i < len(s):
                i += 3
            # do dai do khoi tao 1 ky tu dai dien; quet toi khi gap chu thuong tro lai
            while i < len(s) and not ('\u0020' <= s[i] <= '\u007e'):
                i += 1
            continue
        out.append(s[i])
        i += 1
    return ''.join(out)

merged = {}
tot = 0
bad_key = bad_ctrl = empty = bad_char = 0
for i in range(1, 11):
    tp = os.path.join(T, f'todo_{i:02d}.json')
    vp = os.path.join(T, f'vi_{i:02d}.json')
    if not os.path.exists(vp):
        print(f'  !! THIEU vi_{i:02d}.json')
        continue
    a = json.load(open(tp, encoding='utf-8'))
    b = json.load(open(vp, encoding='utf-8'))
    if len(a) != len(b):
        print(f'  !! vi_{i:02d}: so luong {len(a)} -> {len(b)}')
    for x, y in zip(a, b):
        tot += 1
        if x['key'] != y['key'] or x['file'] != y['file']:
            bad_key += 1
        s, v = x['en'], str(y.get('vi', ''))
        if Counter(CTRL.findall(s)) != Counter(CTRL.findall(v)):
            bad_ctrl += 1
            if bad_ctrl <= 4:
                print(f'  LECH MA [{x["file"]}/{x["key"]}]')
                print(f'    en: {[hex(ord(c)) for c in CTRL.findall(s)][:8]}')
                print(f'    vi: {[hex(ord(c)) for c in CTRL.findall(v)][:8]}')
        if not v.strip() and s.strip():
            empty += 1
            if empty <= 4:
                print(f'  RONG [{x["file"]}/{x["key"]}] nguon={s[:40]!r}')
        m = BAD.findall(strip_tags(v))
        if m:
            bad_char += 1
            if bad_char <= 4:
                print(f'  KY TU LA [{x["file"]}/{x["key"]}]: {set(m)}')
        merged.setdefault(x['file'], {})[x['key']] = v

print(f'\ntong {tot:,} chuoi | lech key {bad_key} | lech ma dieu khien {bad_ctrl} | rong {empty} | ky tu la {bad_char}')
print(f'gop {len(merged)} file MSBT')
json.dump(merged, open(os.path.join(T, 'kirby_vi.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('da luu translations/kirby_vi.json')
print('KET QUA:', 'PASS' if not (bad_key or bad_ctrl or empty or bad_char) else 'CAN XEM LAI')
