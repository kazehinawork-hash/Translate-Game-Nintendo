"""Kiem tra oasis__global: cac the <l id= text=> co cung khong gian id voi file ngon ngu khong?
Neu co -> mod da BO SOT file nay (day co the la 'ngon ngu master' ma game hien thi).
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUMP = os.path.join(ROOT, 'dump', '01002C201BC40000', 'romfs', 'Data', 'data.unity3d')
import UnityPy

vi = json.load(open(os.path.join(ROOT, 'games', '01002C201BC40000_Monopoly', 'translations', 'mono_vi.json'),
                   encoding='utf-8'))

env = UnityPy.load(DUMP)
for o in env.objects:
    if o.type.name != 'TextAsset':
        continue
    d = o.read()
    if getattr(d, 'm_Name', '') != 'oasis__global':
        continue
    raw = o.get_raw_data()
    j = raw.find(b'<')
    txt = raw[j:].decode('utf-16-le', errors='replace')
    print(f'=== oasis__global ({len(raw):,} b) ===')
    # cac the <l .../> co text
    ls = re.findall(r'<l\b[^>]*/>', txt)
    print(f'  so the <l>: {len(ls)}')
    for t in ls[:8]:
        print('    ' + t[:200])
    ids = {}
    for t in ls:
        m = re.search(r'id="(\d+)"', t)
        mt = re.search(r'text="([^"]*)"', t)
        if m and mt:
            ids[m.group(1)] = mt.group(1)
    print(f'  so <l> co id+text: {len(ids)}')
    # so sanh voi ban dich
    hit = sum(1 for i, t in ids.items() if t in vi)
    print(f'  trong do, text TRUNG voi ban dich (mono_vi.json): {hit}')
    # thu lay vai vi du
    print('  5 vi du:')
    for i, t in list(ids.items())[:5]:
        print(f'    id={i}: {t[:50]!r} -> VI: {vi.get(t, "(khong co)")[:50]!r}')
    # co the <s>/<d> khong
    print(f'  so the <s>: {len(re.findall(r"<s bs[^>]*>|<s [^>]*>", txt))}  | so the <d>: {len(re.findall(r"<d [^>]*>", txt))}')
    break
