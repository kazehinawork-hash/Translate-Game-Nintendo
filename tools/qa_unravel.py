"""Kiem tra chat luong ban dich Unravel Two: key khop, the <...> khop, khong rong."""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
G = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\games\0100E5D00CC0C000_UnravelTwo'
T = os.path.join(G, 'translations')

TAG = re.compile(r'<[^<>]{1,40}>')
PH = re.compile(r'%[sd]|\{\d+\}')
BAD_CHARS = re.compile(r'[\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff00-\uffef'
                       r'\u1100-\u11ff\u3130-\u318f\uac00-\ud7ff\u3040-\u30ff'
                       r'\u0600-\u06ff\u0400-\u04ff]')

pairs = []
for f in sorted(os.listdir(T)):
    if not f.startswith('todo_'):
        continue
    out = os.path.join(T, 'vi_' + f[5:])
    if not os.path.exists(out):
        print('THIEU BAN DICH:', f)
        continue
    src = json.load(open(os.path.join(T, f), encoding='utf-8'))
    dst = json.load(open(out, encoding='utf-8'))
    if len(src) != len(dst):
        print(f'{f}: SO LUONG LECH {len(src)} vs {len(dst)}')
    for a, b in zip(src, dst):
        if a['key'] != b['key']:
            print(f'{f}: KEY LECH {a["key"]} vs {b["key"]}')
        pairs.append((f, a['key'], a['en'], b.get('vi', '')))

print(f'\ntong cap: {len(pairs)}')
bad_tag = bad_ph = empty = bad_char = 0
for f, k, en, vi in pairs:
    if sorted(TAG.findall(en)) != sorted(TAG.findall(vi)):
        bad_tag += 1
        if bad_tag <= 5:
            print(f'  LECH THE [{k}]\n    en: {en[:110]}\n    vi: {vi[:110]}')
    if sorted(PH.findall(en)) != sorted(PH.findall(vi)):
        bad_ph += 1
        if bad_ph <= 5:
            print(f'  LECH PLACEHOLDER [{k}]: {PH.findall(en)} vs {PH.findall(vi)}')
    if not vi.strip():
        empty += 1
        print(f'  RONG [{k}]')
    m = BAD_CHARS.findall(vi)
    if m:
        bad_char += 1
        if bad_char <= 5:
            print(f'  KY TU LA [{k}]: {set(m)}')
print(f'\n=== KET QUA: lech the {bad_tag} | lech placeholder {bad_ph} | rong {empty} | ky tu la {bad_char} ===')
print('PASS' if not (bad_tag or bad_ph or empty or bad_char) else 'CO LOI')
