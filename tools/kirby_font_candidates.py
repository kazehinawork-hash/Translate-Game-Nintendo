"""Kiem tra cac font co san tren may: font nao phu DU tieng Viet (theo ban dich Kirby)."""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from fontTools.ttLib import TTFont

TID = '01004D300C5AE000'
vi = json.load(open(os.path.join(ROOT, 'games', f'{TID}_Kirby', 'translations', 'kirby_vi.json'),
                    encoding='utf-8'))
used = set()
for ents in vi.values():
    for v in ents.values():
        used |= set(str(v))
used = {c for c in used if c.isprintable()}
need = {ord(c) for c in used}

CANDS = [
    ('ARIALUNI.TTF', r'C:\Windows\Fonts\ARIALUNI.TTF'),
    ('segoeui.ttf', r'C:\Windows\Fonts\segoeui.ttf'),
    ('tahoma.ttf', r'C:\Windows\Fonts\tahoma.ttf'),
    ('verdana.ttf', r'C:\Windows\Fonts\verdana.ttf'),
    ('calibri.ttf', r'C:\Windows\Fonts\calibri.ttf'),
    ('Lato-Regular (du an)', os.path.join(ROOT, 'tools', 'fonts_hades2', 'Lato-Regular.ttf')),
    ('Nunito-Bold (du an)', os.path.join(ROOT, 'tools', 'Nunito-Bold.ttf')),
    ('Nunito-Black (du an)', os.path.join(ROOT, 'tools', 'Nunito-Black.ttf')),
]
print(f'Ban dich can {len(need)} ky tu\n')
for name, p in CANDS:
    if not os.path.exists(p):
        print(f'  {name:<24} (khong co)')
        continue
    try:
        f = TTFont(p, lazy=True)
        cm = set(f.getBestCmap())
        miss = sorted(need - cm)
        kind = 'CFF' if 'CFF ' in f else 'glyf'
        print(f'  {name:<24} {kind:>4} upem={f["head"].unitsPerEm:>5} glyph={f["maxp"].numGlyphs:>6,} '
              f'| thieu {len(miss):>3} ky tu' + (f': {"".join(chr(c) for c in miss[:20])}' if miss else ' ✓ DU'))
    except Exception as e:
        print(f'  {name:<24} loi {type(e).__name__}')
