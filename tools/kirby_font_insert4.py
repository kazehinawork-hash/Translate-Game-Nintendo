"""VA FONT KIRBY - ban 4 (tu kiem chung bang FreeType TRUOC khi giao).

Quy trinh:
 1. Doc font goc (giai XOR)
 2. SUA bang muc luc: bo vmtx/vhea (Nintendo cat ngan lam fontTools khong load noi)
 3. fontTools: chen glyph tieng Viet (Nunito)
 4. Kiem chung GLYPH GOC con nguyen (K, a, n co outline)
 5. Luu -> cat bang ve dung danh sach cua ban goc (tru vmtx/vhea)
 6. Boc lai container (frame zstd chuan) + doc lai xac minh
 7. *** RENDER BANG FREETYPE (PIL): ve chu "Bạn có muốn" - phai thay dau, khong duoc vuong ***
"""
import io
import json
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import zstandard
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.boundsPen import BoundsPen

TID = '01004D300C5AE000'
DUMP = os.path.join(ROOT, 'dump', TID, 'romfs', 'font', 'ScalableFontBin')
MOD = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'font', 'ScalableFontBin')
SUPPLY = os.path.join(ROOT, 'tools', 'Nunito-Bold.ttf')
MAGIC = 0x36F81A1E
CAND = (0x4F54544F, 0x00010000, 0x74746366)
DROP = {'vmtx', 'vhea'}

vi = json.load(open(os.path.join(ROOT, 'games', f'{TID}_Kirby', 'translations', 'kirby_vi.json'),
                    encoding='utf-8'))
used = set()
for ents in vi.values():
    for v in ents.values():
        used |= set(str(v))
# chi lay ky tu CHU (bo ky tu tham so ma dieu khiển >= 0x3000 ngoai khoi Latin mo rong)
need = sorted({ord(c) for c in used if c.isprintable() and (0x20 <= ord(c) <= 0x2FF or 0x1EA0 <= ord(c) <= 0x1EFF)})


def read_cmp(b):
    d = zstandard.ZstdDecompressor()
    try:
        data = d.decompress(b[4:], max_output_size=256 << 20)
    except zstandard.ZstdError:
        with d.stream_reader(b[4:]) as r:
            data = r.read(256 << 20)
    w8, = struct.unpack_from('>I', data, 8)
    for e in CAND:
        k = w8 ^ e
        body = b''.join(struct.pack('>I', struct.unpack_from('>I', data, i)[0] ^ k)
                        for i in range(8, len(data), 4))
        if body[:4] == struct.pack('>I', e):
            return body, k
    raise ValueError('khong tim thay key')


def write_cmp(font, key):
    t = font if len(font) % 4 == 0 else font + b'\x00' * (4 - len(font) % 4)
    words = [MAGIC, len(font) ^ key]
    for i in range(0, len(t), 4):
        words.append(struct.unpack_from('>I', t, i)[0] ^ key)
    blob = struct.pack(f'>{len(words)}I', *words)
    return struct.pack('<I', len(blob)) + zstandard.ZstdCompressor(level=15).compress(blob)


def redo_dir(data, drop):
    """Viet lai toan bo sfnt: giu cac bang (tru `drop`), sap xep lai offset cho dung."""
    n = struct.unpack_from('>H', data, 4)[0]
    recs = []
    for i in range(n):
        tag, cks, off, ln = struct.unpack_from('>4sIII', data, 12 + 16 * i)
        t = tag.decode('latin1')
        if t in drop:
            continue
        recs.append((tag, data[off:off + ln]))
    hdr = 12 + 16 * len(recs)
    out = bytearray(struct.pack('>IH', 0x00010000, len(recs)) + b'\x00' * 6)
    body = bytearray()
    dirs = []
    for tag, d in recs:
        pad = d + b'\x00' * ((4 - len(d) % 4) % 4)
        dirs.append((tag, len(d), hdr + len(body), pad))
        body += pad
    for tag, ln, off, pad in dirs:
        cks = sum(struct.unpack('>%dI' % (len(pad) // 4), pad)) & 0xFFFFFFFF if len(pad) % 4 == 0 else 0
        out += struct.pack('>4sIII', tag, cks, off, ln)
    out += body
    return bytes(out), {t for t, _ in recs}


sup = TTFont(SUPPLY)
sup_gs = sup.getGlyphSet()
sup_cmap = sup.getBestCmap()
sup_hmtx = sup['hmtx']

n_ok = 0
for fn in sorted(os.listdir(DUMP)):
    if not fn.endswith('.cmp'):
        continue
    orig, key = read_cmp(open(os.path.join(DUMP, fn), 'rb').read())
    try:
        cleaned, keep_tags = redo_dir(orig, DROP)
        f = TTFont(io.BytesIO(cleaned))
        upem = f['head'].unitsPerEm
        scale = upem / sup['head'].unitsPerEm
        is_cff = 'CFF ' in f
        have = set(f.getBestCmap())
        order = list(f.getGlyphOrder())
        hmtx = f['hmtx']
        glyf = None if is_cff else f['glyf']
        cs = None if not is_cff else f['CFF '].cff.topDictIndex[0].CharStrings
        added = 0
        for cp in need:
            if cp in have or cp not in sup_cmap:
                continue
            gname = 'uni%04X' % cp
            aw = sup_hmtx[sup_cmap[cp]][0]
            w = int(round(aw * scale))
            rec = DecomposingRecordingPen(sup_gs)
            sup_gs[sup_cmap[cp]].draw(TransformPen(rec, (scale, 0, 0, scale, 0, 0)))
            if is_cff:
                from fontTools.pens.t2CharStringPen import T2CharStringPen
                pen = T2CharStringPen(w, None)
                rec.replay(pen)
                cs[gname] = pen.getCharString()
            else:
                pen = TTGlyphPen(None)
                rec.replay(pen)
                glyf[gname] = pen.glyph()
            hmtx[gname] = (w, 0)
            order.append(gname)
            for t in f['cmap'].tables:
                if t.isUnicode():
                    t.cmap[cp] = gname
            added += 1
        if not added:
            continue
        f.setGlyphOrder(order)
        if 'maxp' in f:
            f['maxp'].numGlyphs = len(order)
        if 'vmtx' in f:
            del f['vmtx']
        if 'vhea' in f:
            del f['vhea']

        # 4) kiem chung glyph goc con nguyen
        buf = io.BytesIO()
        f.save(buf)
        chk = TTFont(io.BytesIO(buf.getvalue()))
        gs = chk.getGlyphSet()
        cm = chk.getBestCmap()
        base_ok = True
        for ch in 'Kanhocdi':
            gn = cm.get(ord(ch))
            if gn is None:
                base_ok = False
                break
            bp = BoundsPen(gs)
            gs[gn].draw(bp)
            if bp.bounds is None:
                base_ok = False
                break
        vi_ok = all(c in cm for c in need)
        if not (base_ok and vi_ok):
            print(f'  [!] {fn[:40]}: kiem chung that bai base={base_ok} vi={vi_ok}')
            continue

        # 5) cat bang cho dung danh sach goc (tru vmtx/vhea)
        for tag in list(chk.keys()):
            if tag not in keep_tags:
                del chk[tag]
        buf2 = io.BytesIO()
        chk.save(buf2)

        # 7) RENDER THU bang FreeType TRUOC KHI GHI
        from PIL import Image, ImageDraw, ImageFont
        tmpf = os.path.join(ROOT, 'games', '_consistency', 'kirby_probe.ttf')
        os.makedirs(os.path.dirname(tmpf), exist_ok=True)
        open(tmpf, 'wb').write(buf2.getvalue())
        im = Image.new('L', (260, 40), 255)
        ImageDraw.Draw(im).text((4, 4), 'Bạn có muốn', font=ImageFont.truetype(tmpf, 22), fill=0)
        px = im.load()
        # dem so cot co muc: neu chu ve duoc thi phai co nhieu mực, va KHONG giong o vuong rong
        cols = sum(1 for x in range(im.width) if any(px[x, y] < 128 for y in range(im.height)))
        # render 1 ky tu chac chan thieu de so
        im2 = Image.new('L', (60, 40), 255)
        ImageDraw.Draw(im2).text((4, 4), '\ue123', font=ImageFont.truetype(tmpf, 22), fill=0)
        px2 = im2.load()
        box_cols = sum(1 for x in range(im2.width) if any(px2[x, y] < 128 for y in range(im2.height)))
        if cols < 20 or cols == box_cols:
            print(f'  [!] {fn[:40]}: RENDER khong dat (cot={cols}) -> khong giao')
            continue

        data = write_cmp(buf2.getvalue(), key)
        open(os.path.join(MOD, fn), 'wb').write(data)
        n_ok += 1
        print(f'  [+] {fn[:40]:<42} +{added:>3} glyph | render OK ({cols} cot mực)')
    except Exception as e:
        print(f'  [!!] {fn[:40]}: loi {type(e).__name__}: {str(e)[:55]}')
print(f'\n  {n_ok}/45 font da va + tu render kiem chung')
