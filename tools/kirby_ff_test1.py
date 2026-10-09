"""Thu merge tren 1 font, in ro tung buoc (chay bang -lang=py cua FontForge)."""
import os
import sys
import traceback

import fontforge

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'font_edit')
NUN = os.path.join(ROOT, 'games', '_consistency', 'nunito_sub.ttf')
SRC = os.path.join(DIR, 'FOT-RodinNTLGPro-B.otf')
OUT = os.path.join(ROOT, 'games', '_consistency', 'ff_test.otf')


def log(*a):
    print(*a)
    sys.stdout.flush()


log('FontForge version:', fontforge.version())
log('mo nguon:', NUN, os.path.exists(NUN))
nf = fontforge.open(NUN)
log('  glyph Nunito subset:', len(nf))

log('mo game font:', SRC)
f = fontforge.open(SRC)
log('  glyph truoc:', len(f))
log('  is CID:', f.cidmaster, f.cidfontname if hasattr(f, 'cidfontname') else '?')
log('  encoding:', f.encoding)

# kiem tra 1 ky tu co trong game font chua
log('  U+0102 co san:', fontforge.unicodeFromGlyph if False else (0x0102 in f))

try:
    f.mergeFonts(nf)
    log('  glyph sau merge:', len(f))
    log('  U+0102 sau merge:', 0x0102 in f)
except Exception:
    log('LOI mergeFonts:')
    traceback.print_exc()

try:
    f.generate(OUT)
    log('da ghi:', OUT, os.path.exists(OUT), os.path.getsize(OUT) if os.path.exists(OUT) else 0)
except Exception:
    log('LOI generate:')
    traceback.print_exc()

# doc lai bang fontTools de chac chan
try:
    from fontTools.ttLib import TTFont
    chk = TTFont(OUT)
    cm = chk.getBestCmap()
    log('  doc lai: tong glyph', len(chk.getGlyphOrder()),
        '| co U+0102:', 0x0102 in cm, '| co U+1EA1:', 0x1EA1 in cm)
except Exception:
    log('LOI doc lai:')
    traceback.print_exc()
