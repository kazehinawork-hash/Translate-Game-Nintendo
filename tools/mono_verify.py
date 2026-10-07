"""MONOPOLY: kiem chung bundle da build + tim muc chua dich."""
import html
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '01002C201BC40000'
G = os.path.join(ROOT, 'games', f'{TID}_Monopoly')
vi = json.load(open(os.path.join(G, 'translations', 'mono_vi.json'), encoding='utf-8'))
OUTB = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'Data', 'data.unity3d')
NS = '{http://schemas.ubisoft.com/oasis/2011/extractor}'

import UnityPy
env = UnityPy.load(OUTB)
for o in env.objects:
    if o.type.name != 'TextAsset':
        continue
    d = o.read()
    if getattr(d, 'm_Name', '') != 'oasis_englishgb':
        continue
    raw = o.get_raw_data()
    j = raw.find(b'<')
    txt = raw[j:].decode('utf-16-le')
    root = ET.fromstring(txt)
    tr = root.find(f'{NS}translations')
    ents = list(tr)
    print(f'{len(ents)} muc trong bundle moi')
    n_vi = sum(1 for e in ents if any(ord(c) > 127 for c in (e.get('text') or '')))
    print(f'  muc co ky tu tieng Viet: {n_vi}')
    untrans = [(e.get('id'), e.get('text')) for e in ents if (e.get('text') or '') in vi is False and (e.get('text') or '') not in (None, '') and all(ord(c) < 128 for c in (e.get('text') or ''))]
    # liet ke muc goc tieng Anh ma KHONG duoc dich (con nguyen)
    left = []
    for e in ents:
        t = e.get('text') or ''
        if t and t in vi:
            left.append((e.get('id'), t))
    print(f'  muc VAN CON nguyen chuoi goc: {len(left)}')
    for i, t in left[:15]:
        print(f'    #{i}: {t[:60]!r}')
    print('\n  10 muc dau (kiem tra tieng Viet):')
    for e in ents[:10]:
        print(f'    #{e.get("id"):<6} {e.get("text","")[:60]!r}')
    break
