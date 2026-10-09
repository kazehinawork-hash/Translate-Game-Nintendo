"""Kiem tra: font DA FLATTEN (bo CID) thi fontTools co ghi duoc khong -> co tu dong hoa duoc khong.

Neu duoc: chen glyph tieng Viet bang fontTools (duong ten 'uniXXXX' binh thuong).
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from fontTools.ttLib import TTFont
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.boundsPen import BoundsPen

DIR = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'font_edit')
FLAT = os.path.join(DIR, 'FOT-RodinNTLGPro-B.otf.flat.otf')
SUPPLY = os.path.join(ROOT, 'tools', 'Nunito-Bold.ttf')
OUT = os.path.join(ROOT, 'games', '_consistency', 'flat_patched.otf')

vi = json.load(open(os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'translations', 'kirby_vi.json'),
                    encoding='utf-8'))
u = set()
for ents in vi.values():
    for v in ents.values():
        u |= set(str(v))
need = sorted({ord(c) for c in u if c.isprintable() and
               (0x20 <= ord(c) <= 0x2FF or 0x1EA0 <= ord(c) <= 0x1EFF)})

f = TTFont(FLAT)
cm = f.getBestCmap()
print(f'font flat: {len(f.getGlyphOrder())} glyph | cmap {len(cm)} ky tu')
top = f['CFF '].cff.topDictIndex[0]
try:
    is_cid = getattr(top, 'ROS', None) is not None
except Exception:
    is_cid = 'khong doc duoc'
print(f'  la CID: {is_cid}')
try:
    print(f'  Private: {getattr(top, "Private", None)}')
except Exception:
    print('  Private: khong doc duoc')
print(f'  ten glyph mau: {f.getGlyphOrder()[1:6]}')

sup = TTFont(SUPPLY)
sup_gs = sup.getGlyphSet()
sc = sup.getBestCmap()
sup_hmtx = sup['hmtx']
upem = f['head'].unitsPerEm
scale = upem / sup['head'].unitsPerEm
is_cff = 'CFF ' in f
cs = None if not is_cff else f['CFF '].cff.topDictIndex[0].CharStrings
hmtx = f['hmtx']
order = list(f.getGlyphOrder())
have = set(cm)
added = 0
for cp in need:
    if cp in have or cp not in sc:
        continue
    gname = 'uni%04X' % cp
    w = int(round(sup_hmtx[sc[cp]][0] * scale))
    rec = DecomposingRecordingPen(sup_gs)
    sup_gs[sc[cp]].draw(TransformPen(rec, (scale, 0, 0, scale, 0, 0)))
    if is_cff:
        pen = T2CharStringPen(w, None)
        rec.replay(pen)
        cs[gname] = pen.getCharString()
    else:
        from fontTools.pens.ttGlyphPen import TTGlyphPen
        pen = TTGlyphPen(None)
        rec.replay(pen)
        f['glyf'][gname] = pen.glyph()
    hmtx[gname] = (w, 0)
    order.append(gname)
    for t in f['cmap'].tables:
        if t.isUnicode():
            t.cmap[cp] = gname
    added += 1
print(f'  da chen {added} glyph')
f.setGlyphOrder(order)
if 'maxp' in f:
    f['maxp'].numGlyphs = len(order)
for g in f.getGlyphOrder():
    if g not in hmtx.metrics:
        hmtx.metrics[g] = (int(upem * 0.5), 0)
try:
    f.save(OUT)
    print(f'  GHI DUOC -> {os.path.basename(OUT)} ({os.path.getsize(OUT):,} b)')
except Exception as e:
    print(f'  GHI LOI: {type(e).__name__}: {str(e)[:90]}')
    raise SystemExit(1)

chk = TTFont(OUT)
c2 = chk.getBestCmap()
g2 = chk.getGlyphSet()
print(f'  doc lai: {len(chk.getGlyphOrder())} glyph | cmap {len(c2)}')
net = 0
for c in need:
    if c in c2:
        bp = BoundsPen(g2)
        try:
            g2[c2[c]].draw(bp)
        except Exception:
            pass
        if bp.bounds:
            net += 1
print(f'  ky tu tieng Viet co net: {net}/{len(need)}')
latin = 0
for c in range(0x20, 0x7F):
    gn = c2.get(c)
    if gn:
        bp = BoundsPen(g2)
        try:
            g2[gn].draw(bp)
        except Exception:
            pass
        if bp.bounds:
            latin += 1
print(f'  ASCII goc co net: {latin}/95')
from PIL import Image, ImageDraw, ImageFont
ft = ImageFont.truetype(OUT, 30)
im = Image.new('L', (520, 52), 255)
ImageDraw.Draw(im).text((4, 8), 'Bạn có muốn kết nối? ABC xyz 123', font=ft, fill=0)
p = os.path.join(ROOT, 'games', '_consistency', 'flat_patched.png')
im.save(p)
print(f'  anh: {p}')
