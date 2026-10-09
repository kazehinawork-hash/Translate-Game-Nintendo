"""Thu fontTools.merge (duong duoc bao tri, xu ly CFF/CID dung) + in loi day du."""
import os
import sys
import traceback

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))

GAME = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'font_edit', 'FOT-RodinNTLGPro-B.otf')
SUPPLY = os.path.join(ROOT, 'tools', 'Nunito-Bold.ttf')
OUT = GAME + '.merged'

# 1) Loc Nunito chi giu ky tu can + ASCII
from fontTools.subset import Subsetter, Options
from fontTools.ttLib import TTFont

need = []
import json
vi = json.load(open(os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'translations', 'kirby_vi.json'),
                    encoding='utf-8'))
u = set()
for ents in vi.values():
    for v in ents.values():
        u |= set(str(v))
need = sorted({ord(c) for c in u if c.isprintable() and (0x20 <= ord(c) <= 0x2FF or 0x1EA0 <= ord(c) <= 0x1EFF)})
nuni = TTFont(SUPPLY)
opts = Options()
opts.notdef_outline = True
opts.recommended_glyphs = False
opts.layout_features = []
opts.name_IDs = ['*']
s = Subsetter(options=opts)
s.populate(unicodes=need)
s.subset(nuni)
SUB = os.path.join(ROOT, 'games', '_consistency', 'nunito_sub.ttf')
os.makedirs(os.path.dirname(SUB), exist_ok=True)
nuni.save(SUB)
print(f'Nunito loc con {len(need)} ky tu -> {os.path.basename(SUB)}')

# 2) merge
print('\n=== thu fontTools.merge ===')
try:
    from fontTools.merge import Merger
    m = Merger()
    res = m.merge([GAME, SUB])
    res.save(OUT)
    print(f'  OK merge -> {OUT}')
    from PIL import Image, ImageDraw, ImageFont
    ft = ImageFont.truetype(OUT, 26)
    im = Image.new('L', (340, 46), 255)
    ImageDraw.Draw(im).text((4, 6), 'Bạn ăn ằốớợệ Kết nối', font=ft, fill=0)
    p = os.path.join(ROOT, 'games', '_consistency', 'probe_merge.png')
    im.save(p)
    print('  -> thu: games/_consistency/probe_merge.png')
except Exception:
    print('  LOI merge:')
    traceback.print_exc()

# 3) in loi day du cua cach tu chen (de hieu)
print('\n=== thu lai cach tu chen, in loi day du ===')
try:
    f = TTFont(GAME)
    top = f['CFF '].cff.topDictIndex[0]
    cs = top.CharStrings
    from fontTools.pens.transformPen import TransformPen
    from fontTools.pens.recordingPen import DecomposingRecordingPen
    from fontTools.pens.t2CharStringPen import T2CharStringPen
    sup = TTFont(SUPPLY)
    sup_gs = sup.getGlyphSet()
    sc = sup.getBestCmap()
    w = int(round(sup['hmtx'][sc[0x0102]][0] * (f['head'].unitsPerEm / sup['head'].unitsPerEm)))
    rec = DecomposingRecordingPen(sup_gs)
    sup_gs[sc[0x0102]].draw(TransformPen(rec, (1, 0, 0, 1, 0, 0)))
    pen = T2CharStringPen(w, None)
    rec.replay(pen)
    cstr = pen.getCharString()
    cs.charStringsIndex.append(cstr)
    newcid = len(cs.charStringsIndex) - 1
    nm = 'cid%05d' % newcid
    cs.charStrings[nm] = cstr
    top.charset.append(nm)
    print(f'  them {nm} vao charset; charset len={len(top.charset)} index len={len(cs.charStringsIndex)}')
    f['hmtx'][nm] = (w, 0)
    for t in f['cmap'].tables:
        if t.isUnicode():
            t.cmap[0x0102] = nm
    f.setGlyphOrder(list(cs.charStrings.keys()))
    print('  glyph order len:', len(f.getGlyphOrder()))
    f.save(GAME + '.test4')
    print('  OK save')
except Exception:
    print('  LOI day du:')
    traceback.print_exc()
