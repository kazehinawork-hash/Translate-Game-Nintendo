"""GOP font tieng Viet vao TAT CA font .otf cua Kirby - ban chuan da kiem chung.

Quy trinh dung (da kiem chung thanh cong):
    1. fontforge.open(otf)
    2. f.cidFlatten()            <- QUAN TRONG: bo kieu CID truoc, neu khong merge se crash
    3. f.mergeFonts(vi_only.ttf)
    4. f.generate(out, 'opentype')
    5. doc lai bang fontTools: so glyph phai ~9000+, ASCII phai con, tieng Viet phai co

Chay:
    & "C:\\Program Files\\FontForgeBuilds\\bin\\fontforge.exe" -lang=py -script tools/kirby_ff_merge_all.py
"""
import json
import os
import sys

import fontforge

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'font_edit')
VI = os.path.join(ROOT, 'games', '_consistency', 'vi_only.ttf')
REPORT = os.path.join(ROOT, 'games', '_consistency', 'merge_report.txt')


def log(*a):
    print(*a)
    sys.stdout.flush()


vi = json.load(open(os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'translations', 'kirby_vi.json'),
                    encoding='utf-8'))
u = set()
for ents in vi.values():
    for v in ents.values():
        u |= set(str(v))
need = sorted({ord(c) for c in u if c.isprintable() and
               (0x20 <= ord(c) <= 0x2FF or 0x1EA0 <= ord(c) <= 0x1EFF)})

nf = fontforge.open(VI)
log('font Viet nguon: %d ky tu' % (len([g for g in nf.glyphs() if g.unicode >= 0])))

names = sorted(n for n in os.listdir(DIR) if n.endswith('.otf'))
log('se xu ly %d font .otf' % len(names))
lines = []
ok = 0
for n in names:
    p = os.path.join(DIR, n)
    try:
        f = fontforge.open(p)
        before = len(f)
        f.cidFlatten()
        f.mergeFonts(nf)
        after = len(f)
        f.generate(p, flags=('opentype',))
        f.close()
        sz = os.path.getsize(p)
        lines.append('%s\t%d\t%d\t%d' % (n, before, after, sz))
        log('  [ok] %-32s %d -> %d glyph | %d b' % (n, before, after, sz))
        ok += 1
    except Exception as e:
        log('  [loi] %s: %s' % (n, str(e)[:60]))
        lines.append('%s\tLOI\t%s' % (n, str(e)[:60]))
log('xong %d/%d' % (ok, len(names)))
open(REPORT, 'w', encoding='utf-8').write('\n'.join(lines))

# doc lai xac minh bang fontTools
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

vok = 0
for n in names:
    p = os.path.join(DIR, n)
    try:
        chk = TTFont(p)
        cm = chk.getBestCmap()
        gs = chk.getGlyphSet()
        nvi = 0
        for c in need:
            if c in cm:
                bp = BoundsPen(gs)
                try:
                    gs[cm[c]].draw(bp)
                except Exception:
                    pass
                if bp.bounds:
                    nvi += 1
        nlat = 0
        for c in range(0x20, 0x7F):
            if c in cm:
                bp = BoundsPen(gs)
                try:
                    gs[cm[c]].draw(bp)
                except Exception:
                    pass
                if bp.bounds:
                    nlat += 1
        good = (nvi == len(need)) and nlat >= 90 and len(chk.getGlyphOrder()) > 8000
        if good:
            vok += 1
        log('  [%s] %-32s viet %d/%d | latin %d/95 | %d glyph'
            % ('DAT' if good else 'LOI', n, nvi, len(need), nlat, len(chk.getGlyphOrder())))
    except Exception as e:
        log('  [LOI] %s: %s' % (n, str(e)[:50]))
log('=== %d/%d font DAT ===' % (vok, len(names)))
log('tiep theo: python tools/kirby_font_reencrypt.py')
