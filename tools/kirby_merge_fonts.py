"""Gop glyph tieng Viet vao font Kirby bang FontForge - ban chuan.

1. Loc Nunito xuong chi con cac ky tu thuc su can (tranh keo 65k glyph -> crash)
2. Voi tung font game: mergeFonts(ban da loc) -> generate
3. Doc lai bang fontTools de xac minh tung font

Chay:
    & "C:\\Program Files\\FontForgeBuilds\\bin\\fontforge.exe" -lang=py -script tools/kirby_merge_fonts.py
"""
import json
import os
import sys
import traceback

import fontforge

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'font_edit')
NUN = os.path.join(ROOT, 'tools', 'Nunito-Bold.ttf')


def log(*a):
    print(*a)
    sys.stdout.flush()


# --- 1. danh sach ky tu can ---
vi = json.load(open(os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'translations', 'kirby_vi.json'),
                    encoding='utf-8'))
u = set()
for ents in vi.values():
    for v in ents.values():
        u |= set(str(v))
need = sorted({ord(c) for c in u if c.isprintable() and
               (0x20 <= ord(c) <= 0x2FF or 0x1EA0 <= ord(c) <= 0x1EFF)})
log('can %d ky tu' % len(need))

# --- 2. font nguon: font NHO chi gom 214 ky tu tieng Viet (da dung san) ---
VI = os.path.join(ROOT, 'games', '_consistency', 'vi_only.ttf')
if not os.path.exists(VI):
    log('CHUA CO %s - chay truoc: python tools/kirby_build_vi_font.py' % VI)
    raise SystemExit(1)
nf = fontforge.open(VI)
log('font nguon %s: %d glyph' % (os.path.basename(VI), len(nf)))

# --- 3. gop vao tung font .otf (nhom .ttf thieu bang head, FontForge khong mo duoc) ---
names = sorted(n for n in os.listdir(DIR) if n.endswith('.otf'))
n_skip = len([n for n in os.listdir(DIR) if n.endswith('.ttf')])
log('se xu ly %d font .otf (bo qua %d .ttf khong mo duoc)' % (len(names), n_skip))
done = 0
for n in names:
    p = os.path.join(DIR, n)
    try:
        f = fontforge.open(p)
        f.mergeFonts(nf)
        f.generate(p)
        f.close()
        done += 1
        log('  [ok] %s' % n)
    except Exception as e:
        log('  [loi] %s: %s' % (n, str(e)[:60]))
log('xong %d/%d font' % (done, len(names)))

# --- 4. doc lai xac minh ---
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

ok = 0
for n in names:
    p = os.path.join(DIR, n)
    try:
        chk = TTFont(p)
        cm = chk.getBestCmap()
        gs = chk.getGlyphSet()
        miss = [c for c in need if c not in cm]
        blank = 0
        for c in need[:60]:
            if c in cm:
                bp = BoundsPen(gs)
                try:
                    gs[cm[c]].draw(bp)
                except Exception:
                    pass
                if bp.bounds is None:
                    blank += 1
        if not miss and blank == 0:
            ok += 1
            log('  [XAC MINH OK] %s (glyph=%d)' % (n, len(chk.getGlyphOrder())))
        else:
            log('  [XAC MINH LOI] %s: thieu %d, rong %d' % (n, len(miss), blank))
    except Exception as e:
        log('  [XAC MINH LOI] %s: %s' % (n, str(e)[:50]))
log('=== %d/%d font da co du glyph tieng Viet ===' % (ok, len(names)))
log('tiep theo: python tools/kirby_font_reencrypt.py')
