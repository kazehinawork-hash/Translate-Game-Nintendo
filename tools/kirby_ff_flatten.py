"""Thu: Flatten font CID -> font thuong (de fontTools ghi duoc), kiem tra giu du glyph."""
import os
import sys
import traceback

import fontforge

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'font_edit', 'FOT-RodinNTLGPro-B.otf')


def log(*a):
    print(*a)
    sys.stdout.flush()


f = fontforge.open(SRC)
log('mo duoc. so glyph FontForge thay: %d' % len(f))
log('encoding: %s' % f.encoding)
log('co ham cidFlatten:', hasattr(f, 'cidFlatten'))
log('co ham cidConvert', hasattr(f, 'cidConvertByMD5To'))
log('cac ham CID:', [m for m in dir(f) if 'cid' in m.lower()][:12])

OUT = SRC + '.flat.otf'
try:
    if hasattr(f, 'cidFlatten'):
        f.cidFlatten()
        log('da cidFlatten()')
    f.generate(OUT, flags=('opentype',))
    log('da ghi: %s (%d b)' % (os.path.basename(OUT), os.path.getsize(OUT)))
except Exception:
    log('LOI:')
    traceback.print_exc()

# doc lai bang fontTools
try:
    from fontTools.ttLib import TTFont
    from fontTools.pens.boundsPen import BoundsPen
    chk = TTFont(OUT)
    cm = chk.getBestCmap()
    log('fontTools doc lai: %d glyph | cmap %d ky tu' % (len(chk.getGlyphOrder()), len(cm)))
    net = 0
    for c in range(0x20, 0x7F):
        gn = cm.get(c)
        if gn:
            bp = BoundsPen(chk.getGlyphSet())
            try:
                chk.getGlyphSet()[gn].draw(bp)
            except Exception:
                pass
            if bp.bounds:
                net += 1
    log('  ASCII co net: %d/95' % net)
    log('  la CID:', chk['CFF '].cff.topDictIndex[0].ROS is not None)
except Exception:
    log('doc lai loi:')
    traceback.print_exc()
