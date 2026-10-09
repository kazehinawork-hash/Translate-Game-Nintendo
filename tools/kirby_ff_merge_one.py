"""Gop 1 font duy nhat (chay rieng tung tien trinh FontForge).

Dung: fontforge -lang=py -script tools/kirby_ff_merge_one.py <ten_file.otf>
"""
import os
import sys

import fontforge

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'font_edit')
VI = os.path.join(ROOT, 'games', '_consistency', 'vi_only.ttf')


def log(*a):
    print(*a)
    sys.stdout.flush()


args = [a for a in sys.argv[1:] if a.endswith('.otf')]
if not args:
    log('thieu ten file')
    raise SystemExit(1)
name = args[0]
p = os.path.join(DIR, name)
log('xu ly %s' % name)

nf = fontforge.open(VI)
f = fontforge.open(p)
before = len(f)
f.cidFlatten()
f.mergeFonts(nf)
after = len(f)
f.generate(p, flags=('opentype',))
f.close()
nf.close()
log('  XONG %s: %d -> %d glyph | %d b' % (name, before, after, os.path.getsize(p)))
