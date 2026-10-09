"""VA FONT KIRBY (ban 3) - chen glyph vao font GOC, CO KIEM CHUNG TUNG BUOC.

Khac 2 ban truoc:
  - Kiem chung GLYPH GOC con nguyen (K, a, n...) TRUOC khi ghi -> phat hien loi lien ket
  - Cat bang bang chinh fontTools (del f[tag]) thay vi tu ghep lai sfnt (ban truoc lam hong)
  - Frame zstd chuan + doc lai xac minh
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
KEEP_ALWAYS = {'CFF ', 'glyf', 'loca', 'cmap', 'head', 'hhea', 'hmtx', 'maxp'}

vi = json.load(open(os.path.join(ROOT, 'games', f'{TID}_Kirby', 'translations', 'kirby_vi.json'),
                    encoding='utf-8'))
used = set()
for ents in vi.values():
    for v in ents.values():
        used |= set(str(v))
need = sorted({ord(c) for c in used if c.isprintable() and 0x20 <= ord(c) <= 0xFFFF})
# bo cac ky tu tham so ma dieu khien (khong phai chu)
need = [c for c in need if not (0x3000 <= c <= 0xFFFF and c not in range(0x3000, 0x3100))][:1000]


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
        if body[:4] != struct.pack('>I', e):
            continue
        try:
            TTFont(io.BytesIO(body), lazy=True).getBestCmap()
            return body, k
        except Exception:
            pass
    raise ValueError('khong tim thay key')


def write_cmp(font, key):
    t = font if len(font) % 4 == 0 else font + b'\x00' * (4 - len(font) % 4)
    words = [MAGIC, len(font) ^ key]
    for i in range(0, len(t), 4):
        words.append(struct.unpack_from('>I', t, i)[0] ^ key)
    blob = struct.pack(f'>{len(words)}I', *words)
    return struct.pack('<I', len(blob)) + zstandard.ZstdCompressor(level=15).compress(blob)


def sfnt_tags(data):
    n = struct.unpack_from('>H', data, 4)[0]
    return {struct.unpack_from('>4s', data, 12 + 16 * i)[0].decode('latin1') for i in range(n)}


def drop_tables_from_dir(data, drop):
    """Viet lai BANG MUC LUC sfnt, bo cac bang trong `drop` (du lieu bang giu nguyen, thanh mo coi).
    Can thiet vi vmtx/vhea cua Nintendo bi cat ngan -> fontTools khong load noi."""
    ver, n = struct.unpack_from('>IH', data, 0)
    recs = []
    for i in range(n):
        tag, cks, off, ln = struct.unpack_from('>4sIII', data, 12 + 16 * i)
        t = tag.decode('latin1')
        if t in drop:
            continue
        recs.append((tag, cks, off, ln))
    out = bytearray(struct.pack('>IH', ver, len(recs)))
    out += b'\x00' * 6
    for tag, cks, off, ln in recs:
        out += struct.pack('>4sIII', tag, cks, off, ln)
    out += data[12 + 16 * n:]
    return bytes(out)


sup = TTFont(SUPPLY)
sup_gs = sup.getGlyphSet()
sup_cmap = sup.getBestCmap()
sup_hmtx = sup['hmtx']

n_ok = n_skip = 0
for fn in sorted(os.listdir(DUMP)):
    if not fn.endswith('.cmp'):
        continue
    orig, key = read_cmp(open(os.path.join(DUMP, fn), 'rb').read())
    orig_tags = sfnt_tags(orig)
    # loai vmtx/vhea (Nintendo cat ngan, fontTools khong doc noi, khong dung cho chu Latin)
    orig2 = drop_tables_from_dir(orig, {'vmtx', 'vhea'})
    orig_tags2 = orig_tags - {'vmtx', 'vhea'}
    try:
        f = TTFont(io.BytesIO(orig2))
        upem = f['head'].unitsPerEm
        scale = upem / sup['head'].unitsPerEm
        is_cff = 'CFF ' in f
        have = set(f.getBestCmap())
        order = list(f.getGlyphOrder())
        hmtx = f['hmtx']
        if is_cff:
            cs = f['CFF '].cff.topDictIndex[0].CharStrings
        else:
            glyf = f['glyf']
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
                cs[gname] = pen.getCharString(private=getattr(f['CFF '].cff.topDictIndex[0], 'Private', None))
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
            n_skip += 1
            continue
        f.setGlyphOrder(order)
        if 'maxp' in f:
            f['maxp'].numGlyphs = len(order)

        # ---- KIEM CHUNG GLYPH TRUOC KHI GHI ----
        buf = io.BytesIO()
        f.save(buf)
        chk = TTFont(io.BytesIO(buf.getvalue()))
        gs = chk.getGlyphSet()
        cm = chk.getBestCmap()
        base_ok = True
        for ch in 'Kanhoc':
            gn = cm.get(ord(ch))
            bp = BoundsPen(gs)
            if gn is None:
                base_ok = False
                break
            try:
                gs[gn].draw(bp)
            except Exception:
                base_ok = False
                break
            if bp.bounds is None:
                base_ok = False
                break
        vi_ok = all(c in cm for c in need if c < 0x1F00)
        if not (base_ok and vi_ok):
            print(f'  [!] {fn[:40]}: kiem chung that bai (base={base_ok} vi={vi_ok}) -> giu font goc')
            n_skip += 1
            continue

        # ---- CAT BANG du bang chinh fontTools ----
        for tag in list(chk.keys()):
            if tag not in orig_tags2:
                del chk[tag]
        buf2 = io.BytesIO()
        chk.save(buf2)
        out_font = buf2.getvalue()
        data = write_cmp(out_font, key)
        open(os.path.join(MOD, fn), 'wb').write(data)
        # doc lai
        back, _ = read_cmp(open(os.path.join(MOD, fn), 'rb').read())
        same = sfnt_tags(back) == orig_tags2
        n_ok += 1
        if not same:
            print(f'  [!!] {fn[:40]}: bang khong khop sau khi ghi')
    except Exception as e:
        print(f'  [!!] {fn[:40]}: loi {type(e).__name__}: {str(e)[:60]}')
        n_skip += 1
print(f'\n  {n_ok} font da va + xac minh OK | {n_skip} giu nguyen ban goc')
