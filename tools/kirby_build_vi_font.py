"""Dung mot font NHO chi gom 214 ky tu tieng Viet can thiet (de FontForge gop vao font game).

Nguon glyph: Nunito-Bold.ttf. Ket qua: games/_consistency/vi_only.ttf
Font nay nho => FontForge merge nhanh, khong crash.
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from fontTools.fontBuilder import FontBuilder
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import DecomposingRecordingPen

SRC = os.path.join(ROOT, 'tools', 'Nunito-Bold.ttf')
OUT = os.path.join(ROOT, 'games', '_consistency', 'vi_only.ttf')
UPEM = 1000

vi = json.load(open(os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'translations', 'kirby_vi.json'),
                    encoding='utf-8'))
u = set()
for ents in vi.values():
    for v in ents.values():
        u |= set(str(v))
need = sorted({ord(c) for c in u if c.isprintable() and
               (0x20 <= ord(c) <= 0x2FF or 0x1EA0 <= ord(c) <= 0x1EFF)})
print(f'can {len(need)} ky tu')

src = TTFont(SRC)
src_gs = src.getGlyphSet()
src_cmap = src.getBestCmap()
src_hmtx = src['hmtx']
scale = UPEM / src['head'].unitsPerEm

order = ['.notdef']
glyphs = {'.notdef': TTGlyphPen(None).glyph()}
metrics = {'.notdef': (600, 0)}
cmap = {}
for cp in need:
    if cp not in src_cmap:
        continue
    gname = 'v%04X' % cp
    aw = int(round(src_hmtx[src_cmap[cp]][0] * scale))
    rec = DecomposingRecordingPen(src_gs)
    src_gs[src_cmap[cp]].draw(TransformPen(rec, (scale, 0, 0, scale, 0, 0)))
    pen = TTGlyphPen(None)
    rec.replay(pen)
    glyphs[gname] = pen.glyph()
    metrics[gname] = (aw, 0)
    order.append(gname)
    cmap[cp] = gname

fb = FontBuilder(UPEM, isTTF=True)
fb.setupGlyphOrder(order)
fb.setupCharacterMap(cmap)
fb.setupGlyf(glyphs)
fb.setupHorizontalMetrics(metrics)
fb.setupHorizontalHeader(ascent=int(UPEM * 0.8), descent=int(-UPEM * 0.2))
fb.setupNameTable({'familyName': 'VILocalization', 'styleName': 'Regular',
                   'uniqueFontIdentifier': 'VILocalization-Regular',
                   'fullName': 'VILocalization Regular', 'psName': 'VILocalization-Regular',
                   'version': 'Version 1.0'})
fb.setupOS2(sTypoAscender=int(UPEM * 0.8), sTypoDescender=int(-UPEM * 0.2),
            usWinAscent=int(UPEM * 0.8), usWinDescent=int(UPEM * 0.2))
fb.setupPost()
fb.setupMaxp()
os.makedirs(os.path.dirname(OUT), exist_ok=True)
fb.save(OUT)
print(f'da tao {os.path.basename(OUT)} voi {len(order)} glyph')

chk = TTFont(OUT)
cm = chk.getBestCmap()
missing = [c for c in need if c not in cm]
print(f'kiem tra lai: tong glyph {len(chk.getGlyphOrder())} | thieu {len(missing)}')
from PIL import Image, ImageDraw, ImageFont
f = ImageFont.truetype(OUT, 30)
im = Image.new('L', (300, 50), 255)
ImageDraw.Draw(im).text((4, 6), 'Bạn ăn ằốớợệ', font=f, fill=0)
p = os.path.join(ROOT, 'games', '_consistency', 'vi_only_render.png')
im.save(p)
print('anh render thu:', p)
