"""MONOPOLY: kiem tra font (TTF dong + TMP font asset) co du dau tieng Viet khong."""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '01002C201BC40000'
G = os.path.join(ROOT, 'games', f'{TID}_Monopoly')
vi = json.load(open(os.path.join(G, 'translations', 'mono_vi.json'), encoding='utf-8'))
used = {c for v in vi.values() for c in str(v) if c.isprintable()}
print(f'ky tu dung trong ban dich: {len(used)}')

import UnityPy
env = UnityPy.load(r'E:\MONO_work\data.unity3d')

fonts = []
tmps = []
for o in env.objects:
    if o.type.name == 'Font':
        try:
            d = o.read()
            fonts.append((getattr(d, 'm_Name', '?'), o))
        except Exception:
            pass
    elif o.type.name == 'MonoBehaviour':
        pass

print(f'\n=== Font (TTF dong trong bundle): {len(fonts)} ===')
for nm, o in fonts[:15]:
    print('  ' + nm)

# kiem tra cmap cua cac Font dong
from fontTools.ttLib import TTFont
for nm, o in fonts:
    try:
        d = o.read()
        raw = getattr(d, 'm_FontData', None)
        if not raw:
            continue
        if isinstance(raw, str):
            raw = raw.encode('latin-1')
        f = TTFont(io.BytesIO(raw), lazy=True)
        cm = set(f.getBestCmap())
        miss = [c for c in used if ord(c) not in cm and ord(c) < 0xE000]
        print(f'\n  {nm}: {len(cm):,} glyph | THIEU {len(miss)} ky tu ban dich')
        if miss:
            print(f'    {"".join(sorted(miss)[:60])}')
    except Exception as e:
        print(f'\n  {nm}: khong doc duoc ({type(e).__name__})')
