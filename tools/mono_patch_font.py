"""MONOPOLY: ghep them glyph tieng Viet vao cac font TTF thieu trong bundle (BH-20: giu glyph goc)."""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '01002C201BC40000'
G = os.path.join(ROOT, 'games', f'{TID}_Monopoly')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from merge_vi_font import merge_vn_font
from fontTools.ttLib import TTFont

vi = json.load(open(os.path.join(G, 'translations', 'mono_vi.json'), encoding='utf-8'))
used = sorted({ord(c) for v in vi.values() for c in str(v) if c.isprintable() and ord(c) < 0xE000})
SUPPLY = r'C:\Windows\Fonts\ARIALUNI.TTF'

import UnityPy
env = UnityPy.load(r'E:\MONO_work\data.unity3d')
fixed = skip = fail = 0
for o in env.objects:
    if o.type.name != 'Font':
        continue
    try:
        d = o.read()
        raw = getattr(d, 'm_FontData', None)
        if isinstance(raw, (list, tuple)):
            raw = bytes(raw)
        if not isinstance(raw, (bytes, bytearray)) or len(raw) < 1000:
            continue
        f = TTFont(io.BytesIO(bytes(raw)), lazy=True)
        cm = set(f.getBestCmap())
        miss = [c for c in used if c not in cm]
        if not miss:
            skip += 1
            continue
        merged = merge_vn_font(bytes(raw), SUPPLY)
        m2 = set(TTFont(io.BytesIO(merged), lazy=True).getBestCmap())
        still = [c for c in used if c not in m2]
        if still:
            fail += 1
            if fail <= 3:
                print(f'  {getattr(d,"m_Name","?"):<40} van thieu {len(still)}: {"".join(chr(c) for c in still[:15])}')
            continue
        d.m_FontData = merged
        o.save()
        fixed += 1
        if fixed <= 5:
            print(f'  [+] {getattr(d,"m_Name","?"):<40} {len(cm):>6} -> {len(m2):>6} glyph (thieu {len(miss)})')
    except Exception as e:
        fail += 1

print(f'\nfont da ghep: {fixed} | da du (bo qua): {skip} | loi: {fail}')
if fixed:
    OUT = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'Data')
    os.makedirs(OUT, exist_ok=True)
    env.save(pack='original', out_path=OUT)
    print(f'da ghi bundle: {os.path.join(OUT, "data.unity3d")} ({os.path.getsize(os.path.join(OUT,"data.unity3d"))/1e6:.1f} MB)')
