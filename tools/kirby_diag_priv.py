"""Thu chen glyph CFF CID sau khi TU TAO Private dict con thieu."""
import os
import sys
import traceback

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from fontTools.ttLib import TTFont
from fontTools.cffLib import PrivateDict, TopDict
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen

GAME = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'font_edit', 'FOT-RodinNTLGPro-B.otf')
SUPPLY = os.path.join(ROOT, 'tools', 'Nunito-Bold.ttf')
OUT = GAME + '.test5'

f = TTFont(GAME)
cff = f['CFF '].cff
top = cff.topDictIndex[0]
cs = top.CharStrings

# --- 1. Tao Private cho FDArray / topDict neu thieu ---
print('top.Private:', getattr(top, 'Private', None))
fda = getattr(top, 'FDArray', None)
print('FDArray:', None if fda is None else len(fda))
ref_priv = None
if fda:
    for i, fd in enumerate(fda):
        p = getattr(fd, 'Private', None)
        print(f'  FD[{i}] Private: {p}')
        if p is not None and ref_priv is None:
            ref_priv = p
    if ref_priv is None:
        ref_priv = PrivateDict()
        ref_priv.defaultWidthX = 0
        ref_priv.nominalWidthX = 0
        fda[0].Private = ref_priv
        print('  -> da tao Private cho FD[0]')
if getattr(top, 'Private', None) is None:
    pd = ref_priv if ref_priv is not None else PrivateDict()
    if ref_priv is None:
        pd.defaultWidthX = 0
        pd.nominalWidthX = 0
    try:
        top.Private = pd
        print('  -> da gan Private cho topDict')
    except Exception as e:
        print('  -> khong gan duoc topDict.Private:', str(e)[:50])

# --- 2. Chen glyph ---
sup = TTFont(SUPPLY)
sup_gs = sup.getGlyphSet()
sc = sup.getBestCmap()
upem = f['head'].unitsPerEm
scale = upem / sup['head'].unitsPerEm
cp = 0x0102
w = int(round(sup['hmtx'][sc[cp]][0] * scale))
rec = DecomposingRecordingPen(sup_gs)
sup_gs[sc[cp]].draw(TransformPen(rec, (scale, 0, 0, scale, 0, 0)))
pen = T2CharStringPen(w, None)
rec.replay(pen)
cstr = pen.getCharString()
private = ref_priv if ref_priv is not None else getattr(top, 'Private', None)
cstr.private = private
try:
    cs.charStringsIndex.append(cstr)
except Exception:
    traceback.print_exc()
newcid = len(cs.charStringsIndex) - 1
nm = 'cid%05d' % newcid
cs.charStrings[nm] = cstr
if top.charset is not None:
    top.charset.append(nm)
f['hmtx'][nm] = (w, 0)
for t in f['cmap'].tables:
    if t.isUnicode():
        t.cmap[cp] = nm
f.setGlyphOrder(list(cs.charStrings.keys()))
for g in f.getGlyphOrder():
    if g not in f['hmtx'].metrics:
        f['hmtx'].metrics[g] = (w, 0)
if 'maxp' in f:
    f['maxp'].numGlyphs = len(f.getGlyphOrder())
print(f'them {nm} | charset={len(top.charset)} | order={len(f.getGlyphOrder())}')

try:
    f.save(OUT)
    print('OK save ->', os.path.basename(OUT))
    from PIL import Image, ImageDraw, ImageFont
    ft = ImageFont.truetype(OUT, 28)
    im = Image.new('L', (340, 50), 255)
    ImageDraw.Draw(im).text((4, 6), 'Ăn ằ ố Bạn Kết', font=ft, fill=0)
    p = os.path.join(ROOT, 'games', '_consistency', 'probe5.png')
    im.save(p)
    im2 = Image.new('L', (340, 50), 255)
    from PIL import ImageFont as IF
    ImageDraw.Draw(im2).text((4, 6), 'Ăn ằ ố Bạn Kết', font=ft, fill=0)
    px = im2.load()
    cols = sum(1 for x in range(im2.width) if any(px[x, y] < 128 for y in range(im2.height)))
    print(f'  render {cols} cot | anh: {p}')
except Exception:
    print('LOI save:')
    traceback.print_exc()
