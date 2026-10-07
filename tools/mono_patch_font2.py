"""MONOPOLY: ghep glyph tieng Viet vao font TTF thieu (toi uu: cat gon font nguon truoc)."""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '01002C201BC40000'
G = os.path.join(ROOT, 'games', f'{TID}_Monopoly')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from fontTools.subset import Options, Subsetter, load_font, save_font
from fontTools.ttLib import TTFont

vi = json.load(open(os.path.join(G, 'translations', 'mono_vi.json'), encoding='utf-8'))
# Chi tinh ky tu cua cac CHUOI DA DICH (bo qua muc giu nguyen - vd ten ngon ngu mojibake co san cua game)
changed = {k: v for k, v in vi.items() if str(v) != str(k)}
used = sorted({ord(c) for v in changed.values() for c in str(v) if c.isprintable() and ord(c) < 0xE000})
print(f'ky tu can co (tu {len(changed):,} chuoi da dich): {len(used)}')
SUPPLY = r'C:\Windows\Fonts\ARIALUNI.TTF'

# 1. cat Arial chi con ky tu can (nhanh hon nhieu khi ghep)
opts = Options(layout_features=[], notdef_outline=True, recalc_bounds=True, glyph_names=False,
               legacy_kern=False, drop_tables=['DSIG'], hinting=False)
f = load_font(SUPPLY, opts)
s = Subsetter(options=opts)
s.populate(unicodes=used)
s.subset(f)
SMALL = r'E:\MONO_work\vi_subset.ttf'
save_font(f, SMALL, opts)
print(f'font nguon rut gon: {os.path.getsize(SMALL):,} byte ({len(TTFont(SMALL,lazy=True).getBestCmap())} glyph)', flush=True)

from merge_vi_font import merge_vn_font   # helper nay TU dong bo unitsPerEm (BH-7)

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
        cm = set(TTFont(io.BytesIO(bytes(raw)), lazy=True).getBestCmap())
        miss = [c for c in used if c not in cm]
        if not miss:
            skip += 1
            continue
        b = merge_vn_font(bytes(raw), SMALL)      # giu glyph goc + them glyph thieu (dong bo upem)
        m2 = set(TTFont(io.BytesIO(b), lazy=True).getBestCmap())
        still = [c for c in used if c not in m2]
        if still:
            fail += 1
            print(f'  {getattr(d,"m_Name","?"):<38} van thieu {len(still)}', flush=True)
            continue
        d.m_FontData = b
        o.save()
        fixed += 1
        print(f'  [+] {getattr(d,"m_Name","?"):<38} {len(cm):>6} -> {len(m2):>6} glyph', flush=True)
    except Exception as e:
        fail += 1
        if fail <= 3:
            print(f'  loi: {type(e).__name__} {str(e)[:60]}', flush=True)

print(f'\nfont da ghep: {fixed} | da du: {skip} | loi: {fail}', flush=True)
if fixed:
    OUT = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'Data')
    os.makedirs(OUT, exist_ok=True)
    env.save(pack='original', out_path=OUT)
    print(f'da ghi bundle: {os.path.getsize(os.path.join(OUT,"data.unity3d"))/1e6:.1f} MB', flush=True)
