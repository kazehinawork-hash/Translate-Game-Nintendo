"""Thu gop font tren BAN DA FLATTEN (khong con CID) -> neu duoc thi tu dong hoa ca quy trinh.

Chay: & "...\\fontforge.exe" -lang=py -script tools/kirby_ff_merge_flat.py
"""
import os
import sys

import fontforge

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'font_edit')
VI = os.path.join(ROOT, 'games', '_consistency', 'vi_only.ttf')
TEST = os.path.join(DIR, 'FOT-RodinNTLGPro-B.otf')
OUT = os.path.join(ROOT, 'games', '_consistency', 'merged_flat.otf')


def log(*a):
    print(*a)
    sys.stdout.flush()


nf = fontforge.open(VI)
log('font Viet: %d glyph' % len(nf))

f = fontforge.open(TEST)
log('mo font game: %d glyph' % len(f))
f.cidFlatten()
log('sau flatten: %d glyph' % len(f))
f.mergeFonts(nf)
log('sau merge: %d glyph' % len(f))
f.generate(OUT, flags=('opentype',))
log('da ghi: %s (%d b)' % (os.path.basename(OUT), os.path.getsize(OUT)))
