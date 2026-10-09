"""Thu cac cach chen glyph vao CFF kieu CID, tim cach dung."""
import os
import re
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
top = f['CFF '].cff.topDictIndex[0]
cs = top.CharStrings
print('kieu CharStrings:', type(cs).__name__, '| isCID:', getattr(cs, 'isCID', '?'))
print('charset kieu:', type(top.charset).__name__, '| 5 dau:', list(top.charset)[:5] if top.charset else None)
print('charStrings kieu:', type(cs.charStrings).__name__ if hasattr(cs, 'charStrings') else '?')
print('co charStringsIndex:', hasattr(cs, 'charStringsIndex'))
if hasattr(cs, 'charStringsIndex'):
    print('  charStringsIndex len:', len(cs.charStringsIndex))
print('top.charset is CID:', getattr(top, 'ROS', None) is not None, '| ROS:', getattr(top, 'ROS', None))

sup = TTFont(SUPPLY)
sup_gs = sup.getGlyphSet()
sup_cmap = sup.getBestCmap()
sup_hmtx = sup['hmtx']
upem = f['head'].unitsPerEm
scale = upem / sup['head'].unitsPerEm
cp = 0x0102
src = sup_cmap[cp]
w = int(round(sup_hmtx[src][0] * scale))
rec = DecomposingRecordingPen(sup_gs)
sup_gs[src].draw(TransformPen(rec, (scale, 0, 0, scale, 0, 0)))
pen = T2CharStringPen(w, None)
rec.replay(pen)
cstr = pen.getCharString()

cids = [int(m.group(1)) for k in cs.keys() if (m := re.fullmatch(r'cid(\d+)', k))]
print(f'\nso CID hien co: {len(cs.keys())} | CID lon nhat: {max(cids) if cids else None}')
newcid = (max(cids) + 1) if cids else 0
print(f'CID moi se dung: {newcid}')

for label, name, fn in [
    ('ten cidNNNNN', 'cid%05d' % newcid, lambda n: cs.__setitem__(n, cstr)),
    ('ten so nguyen', newcid, lambda n: cs.__setitem__(n, cstr)),
    ('ten cid NN', 'cid%d' % newcid, lambda n: cs.__setitem__(n, cstr)),
]:
    ff = TTFont(P)
    c2 = ff['CFF '].cff.topDictIndex[0].CharStrings
    try:
        fn2 = lambda: c2.__setitem__(name, cstr)
        fn2()
        print(f'  OK   {label}: {name!r} -> len={len(c2.keys())}')
    except Exception as e:
        print(f'  LOI  {label}: {name!r} -> {type(e).__name__}: {str(e)[:70]}')

# cach 3: append truc tiep vao charStringsIndex
ff = TTFont(P)
top3 = ff['CFF '].cff.topDictIndex[0]
c3 = top3.CharStrings
try:
    c3.charStringsIndex.append(cstr)
    nm = 'cid%05d' % newcid
    c3.charStrings[nm] = cstr
    if getattr(c3, 'isCID', False):
        pass
    if top3.charset is not None:
        top3.charset.append(nm)
    print(f'  OK   append charStringsIndex: len={len(c3.charStringsIndex)}')
    ff['hmtx'][nm] = (w, 0)
    for t in ff['cmap'].tables:
        if t.isUnicode():
            t.cmap[cp] = nm
    ff.setGlyphOrder(list(c3.keys()))
    for g in ff.getGlyphOrder():
        if g not in ff['hmtx'].metrics:
            ff['hmtx'].metrics[g] = (w, 0)
    out = P + '.test3'
    ff.save(out)
    print('  OK   save (cach 3) ->', out)
    from PIL import Image, ImageDraw, ImageFont
    ft = ImageFont.truetype(out, 26)
    im = Image.new('L', (300, 46), 255)
    ImageDraw.Draw(im).text((4, 6), 'Bạn Ăn ằố', font=ft, fill=0)
    im.save(os.path.join(ROOT, 'games', '_consistency', 'probe3.png'))
    print('  -> xem thu: games/_consistency/probe3.png')
except Exception:
    traceback.print_exc()
