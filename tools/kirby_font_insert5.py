"""VA FONT KIRBY - ban 5: SUA vmtx bang cach NOI THEM vao CUOI FILE (khong xê dich gi).

Van de: vmtx cua Nintendo bi cat ngan -> fontTools khong load noi.
Cach sua: ghi mot bang vmtx MOI (toan so 0, dung kich thuoc = 4 + 2*numGlyphs)
vao CUOI file, roi sua 1 dong trong bang muc luc (offset + length).
=> Khong bang nao khac bi xê dich => an toan.
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

vi = json.load(open(os.path.join(ROOT, 'games', f'{TID}_Kirby', 'translations', 'kirby_vi.json'),
                    encoding='utf-8'))
used = set()
for ents in vi.values():
    for v in ents.values():
        used |= set(str(v))
need = sorted({ord(c) for c in used if c.isprintable() and
               (0x20 <= ord(c) <= 0x2FF or 0x1EA0 <= ord(c) <= 0x1EFF)})


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


def num_glyphs(data):
    n = struct.unpack_from('>H', data, 4)[0]
    for i in range(n):
        tag, cks, off, ln = struct.unpack_from('>4sIII', data, 12 + 16 * i)
        if tag == b'maxp':
            return struct.unpack_from('>H', data, off + 4)[0], 12 + 16 * i
    return None, None


def fix_vmtx(data):
    """Noi them vmtx dung kich thuoc vao cuoi file; sua 1 entry trong bang muc luc."""
    ntab = struct.unpack_from('>H', data, 4)[0]
    ng, _ = num_glyphs(data)
    if ng is None:
        return data, False
    need_len = 4 + 2 * ng
    idx = None
    cur = None
    for i in range(ntab):
        tag, cks, off, ln = struct.unpack_from('>4sIII', data, 12 + 16 * i)
        if tag == b'vmtx':
            idx, cur = 12 + 16 * i, ln
    if idx is None or cur >= need_len:
        return data, False
    out = bytearray(data)
    while len(out) % 4:
        out += b'\x00'
    newoff = len(out)
    tbl = b'\x00' * need_len
    out += tbl
    cks = 0
    out[idx:idx + 16] = struct.pack('>4sIII', b'vmtx', cks, newoff, need_len)
    return bytes(out), True


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
        fixed, did = fix_vmtx(orig)
        f = TTFont(io.BytesIO(fixed))
        orig_tags = {struct.unpack_from('>4s', fixed, 12 + 16 * i)[0].decode('latin1')
                     for i in range(struct.unpack_from('>H', fixed, 4)[0])}
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
        buf = io.BytesIO()
        f.save(buf)
        chk = TTFont(io.BytesIO(buf.getvalue()))
        gs = chk.getGlyphSet()
        cm = chk.getBestCmap()
        base_ok = all(cm.get(ord(c)) is not None for c in 'Kanhocdi')
        if base_ok:
            for c in 'Kanhoc':
                bp = BoundsPen(gs)
                gs[cm[ord(c)]].draw(bp)
                if bp.bounds is None:
                    base_ok = False
                    break
        vi_ok = all(c in cm for c in need)
        if not (base_ok and vi_ok):
            print(f'  [!] {fn[:40]}: kiem chung base={base_ok} vi={vi_ok}')
            continue
        for tag in list(chk.keys()):
            if tag not in orig_tags:
                del chk[tag]
        buf2 = io.BytesIO()
        chk.save(buf2)
        # render thu bang FreeType
        from PIL import Image, ImageDraw, ImageFont
        tmpf = os.path.join(ROOT, 'games', '_consistency', 'probe.ttf')
        os.makedirs(os.path.dirname(tmpf), exist_ok=True)
        open(tmpf, 'wb').write(buf2.getvalue())
        im = Image.new('L', (300, 44), 255)
        ImageDraw.Draw(im).text((4, 4), 'Bạn có muốn kết nối', font=ImageFont.truetype(tmpf, 24), fill=0)
        px = im.load()
        cols = sum(1 for x in range(im.width) if any(px[x, y] < 128 for y in range(im.height)))
        im2 = Image.new('L', (70, 44), 255)
        ImageDraw.Draw(im2).text((4, 4), '\ue123', font=ImageFont.truetype(tmpf, 24), fill=0)
        px2 = im2.load()
        box = sum(1 for x in range(im2.width) if any(px2[x, y] < 128 for y in range(im2.height)))
        if cols < 30 or cols == box:
            print(f'  [!] {fn[:40]}: render khong dat ({cols} cot)')
            continue
        data = write_cmp(buf2.getvalue(), key)
        open(os.path.join(MOD, fn), 'wb').write(data)
        n_ok += 1
        print(f'  [+] {fn[:40]:<42} +{added:>3} glyph | vmtx sua:{did} | render {cols} cot')
    except Exception as e:
        print(f'  [!!] {fn[:40]}: {type(e).__name__}: {str(e)[:60]}')
print(f'\n  {n_ok}/45 font da va + tu render kiem chung DAT')
