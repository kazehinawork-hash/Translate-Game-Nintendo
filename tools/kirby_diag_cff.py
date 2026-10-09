"""Chan doan rieng: chen 1 glyph vao font OTF de tim dung dong loi."""
import os
import sys
import traceback

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from fontTools.ttLib import TTFont
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen

P = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'font_edit', 'FOT-RodinNTLGPro-B.otf')
SUPPLY = os.path.join(ROOT, 'tools', 'Nunito-Bold.ttf')

f = TTFont(P)
sup = TTFont(SUPPLY)
sup_gs = sup.getGlyphSet()
sup_cmap = sup.getBestCmap()
sup_hmtx = sup['hmtx']

upem = f['head'].unitsPerEm
scale = upem / sup['head'].unitsPerEm
print('upem=', upem, 'scale=', scale)
print('co CFF:', 'CFF ' in f)
cs = f['CFF '].cff.topDictIndex[0].CharStrings
print('so charstring truoc:', len(cs))
print('glyph order dau:', f.getGlyphOrder()[:5], '... tong', len(f.getGlyphOrder()))
print('hmtx so metric:', len(f['hmtx'].metrics), '| kieu:', type(f['hmtx']).__name__)

cp = 0x0102  # A*
gn = 'uni%04X' % cp
src = sup_cmap[cp]
print('glyph nguon trong Nunito:', src, '| hmtx co:', src in sup_hmtx.metrics)
try:
    w = int(round(sup_hmtx[src][0] * scale))
    print('advance =', w)
    rec = DecomposingRecordingPen(sup_gs)
    sup_gs[src].draw(TransformPen(rec, (scale, 0, 0, scale, 0, 0)))
    pen = T2CharStringPen(w, None)
    rec.replay(pen)
    cstr = pen.getCharString()
    print('tao duoc charstring OK')
except Exception:
    traceback.print_exc()
    sys.exit(1)

for label, fn in [
    ('cs[gn] = cstr', lambda: cs.__setitem__(gn, cstr)),
    ('hmtx[gn] = (w,0)', lambda: f['hmtx'].__setitem__(gn, (w, 0))),
    ('cmap', lambda: [t.cmap.__setitem__(cp, gn) for t in f['cmap'].tables if t.isUnicode()]),
    ('setGlyphOrder', lambda: f.setGlyphOrder(f.getGlyphOrder() + [gn])),
    ('maxp.numGlyphs', lambda: setattr(f['maxp'], 'numGlyphs', len(f.getGlyphOrder()))),
]:
    try:
        fn()
        print(f'  OK   {label}')
    except Exception as e:
        print(f'  LOI  {label} -> {type(e).__name__}: {str(e)[:80]}')

try:
    f.save(P + '.test')
    print('  OK   save')
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new('L', (260, 46), 255)
    ImageDraw.Draw(im).text((4, 6), 'Bạn Ăn', font=ImageFont.truetype(P + '.test', 26), fill=0)
    im.save(os.path.join(ROOT, 'games', '_consistency', 'probe_test.png'))
    print('  OK   render thu -> games/_consistency/probe_test.png')
except Exception:
    traceback.print_exc()
