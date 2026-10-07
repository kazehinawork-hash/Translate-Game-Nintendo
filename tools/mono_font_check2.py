"""MONOPOLY: kiem tra do phu tieng Viet cua cac font dong trong bundle."""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '01002C201BC40000'
vi = json.load(open(os.path.join(ROOT, 'games', f'{TID}_Monopoly', 'translations', 'mono_vi.json'),
                   encoding='utf-8'))
used = {c for v in vi.values() for c in str(v) if c.isprintable()}

import UnityPy
from fontTools.ttLib import TTFont

env = UnityPy.load(r'E:\MONO_work\data.unity3d')
n_ok = n_bad = 0
worst = (999, '')
samples = []
for o in env.objects:
    if o.type.name != 'Font':
        continue
    try:
        d = o.read()
        raw = getattr(d, 'm_FontData', None)
        if raw is None:
            continue
        if isinstance(raw, (list, tuple)):
            raw = bytes(raw)
        elif isinstance(raw, str):
            raw = raw.encode('latin-1')
        if not isinstance(raw, (bytes, bytearray)) or len(raw) < 1000:
            continue
        f = TTFont(io.BytesIO(bytes(raw)), lazy=True)
        cm = set(f.getBestCmap())
        miss = [c for c in used if ord(c) not in cm and ord(c) < 0xE000]
        if len(miss) < worst[0]:
            worst = (len(miss), f'{getattr(d,"m_Name","?")} ({len(cm):,} glyph)')
        if not miss:
            n_ok += 1
        else:
            n_bad += 1
        samples.append((getattr(d, 'm_Name', '?'), len(cm), len(miss)))
    except Exception:
        n_bad += 1

print(f'Font doc duoc: {n_ok} du 100%, {n_bad} thieu/khong doc duoc')
print(f'Font thieu it nhat: {worst[1]} -> thieu {worst[0]} ky tu')
print('\n5 font dau:')
for nm, g, m in samples[:5]:
    print(f'  {nm:<45} {g:>7,} glyph | thieu {m}')
