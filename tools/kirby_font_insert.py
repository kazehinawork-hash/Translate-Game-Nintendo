"""VA FONT KIRBY CACH 1: chen glyph tieng Viet vao font GOC, GIU Y NGuyen danh sach bang.

Y tuong:
  1. Doc font goc -> ghi nho DANH SACH BANG (tag) cua no (vd .bfttf thieu maxp/post).
  2. Dung fontTools them glyph tieng Viet (lay tu Nunito, scale ve dung upem).
  3. fontTools.save() se TU THEM cac bang chuan -> ta PHAI CAT LAI:
     viet lai bang muc luc sfnt chi giu dung cac tag nhu ban goc.
  4. Boc lai container [u32 size][zstd CHUAN][XOR key cua goc] + doc lai xac minh.

=> Game thay font "giong y ban goc" nhung co them dau tieng Viet.
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
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen

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
need = sorted({ord(c) for c in used if c.isprintable() and 0x20 <= ord(c) <= 0xFFFF})


# ---------- container ----------
def read_cmp(b):
    d = zstandard.ZstdDecompressor()
    try:
        data = d.decompress(b[4:], max_output_size=256 << 20)
    except zstandard.ZstdError:
        with d.stream_reader(b[4:]) as r:
            data = r.read(256 << 20)
    if struct.unpack_from('>I', data, 0)[0] != MAGIC:
        raise ValueError('khong phai font XOR')
    w8, = struct.unpack_from('>I', data, 8)
    for expect in CAND:
        key = w8 ^ expect
        body = b''.join(struct.pack('>I', struct.unpack_from('>I', data, i)[0] ^ key)
                        for i in range(8, len(data), 4))
        if body[:4] != struct.pack('>I', expect):
            continue
        try:
            TTFont(io.BytesIO(body), lazy=True).getBestCmap()
        except Exception:
            continue
        return body, key
    raise ValueError('khong tim thay key')


def write_cmp(font, key):
    t = font if len(font) % 4 == 0 else font + b'\x00' * (4 - len(font) % 4)
    words = [MAGIC, len(font) ^ key]
    for i in range(0, len(t), 4):
        words.append(struct.unpack_from('>I', t, i)[0] ^ key)
    blob = struct.pack(f'>{len(words)}I', *words)
    return struct.pack('<I', len(blob)) + zstandard.ZstdCompressor(level=15).compress(blob)


# ---------- sfnt ----------
def sfnt_tables(data):
    """-> (sfntVersion, {tag: (off, len)})"""
    ver, ntab = struct.unpack_from('>IH', data, 0)
    tabs = {}
    for i in range(ntab):
        tag, cks, off, ln = struct.unpack_from('>4sIII', data, 12 + 16 * i)
        tabs[tag.decode('latin1')] = (off, ln)
    return ver, tabs


def prune_sfnt(data, keep_tags):
    """Viet lai bang muc luc sfnt CHI giu cac bang trong keep_tags (giu nguyen du lieu bang)."""
    ver, tabs = sfnt_tables(data)
    keep = [(t, o, l) for t, (o, l) in tabs.items() if t in keep_tags]
    keep.sort(key=lambda x: x[1])                       # giu nguyen thu tu offset
    n = len(keep)
    # tinh lai offset: header(12) + 16*n, roi den du lieu tung bang, can 4 byte
    hdr = 12 + 16 * n
    out = bytearray()
    out += struct.pack('>IHHHH', ver, n, 0, 0, 0)        # searchRange.. se sua sau
    body = bytearray()
    new = []
    pos = hdr
    for tag, off, ln in keep:
        d = data[off:off + ln]
        new.append((tag, off, ln, pos, d))
        body += d
        while len(body) % 4:
            body += b'\x00'
        pos = hdr + len(body)
    # bang muc luc
    import binascii
    for tag, off, ln, newoff, d in new:
        out += struct.pack('>4sIII', tag.encode('latin1'), 0, newoff, len(d))
    out += body
    # tinh lai checksum tung bang (khong bat buoc nhung cho dung chuan)
    for i, (tag, off, ln, newoff, d) in enumerate(new):
        pad = d + b'\x00' * ((4 - len(d) % 4) % 4)
        cks = sum(struct.unpack('>%dI' % (len(pad) // 4), pad)) & 0xFFFFFFFF
        out[12 + 16 * i + 4:12 + 16 * i + 8] = struct.pack('>I', cks)
    return bytes(out)


def add_glyphs(font_bytes, supply_path):
    f = TTFont(io.BytesIO(font_bytes))
    upem = f['head'].unitsPerEm
    sup = TTFont(supply_path)
    scale = upem / sup['head'].unitsPerEm
    sup_gs = sup.getGlyphSet()
    sup_cmap = sup.getBestCmap()
    sup_hmtx = sup['hmtx']
    have = set(f.getBestCmap())
    is_cff = 'CFF ' in f

    if is_cff:
        from fontTools.pens.recordingPen import DecomposingRecordingPen
        cff = f['CFF '].cff
        td = cff.topDictIndex[0]
        cs = td.CharStrings
        order = list(f.getGlyphOrder())
        hmtx = f['hmtx']
    else:
        glyf = f['glyf']
        order = list(f.getGlyphOrder())
        hmtx = f['hmtx']

    added = 0
    for cp in need:
        if cp in have or cp not in sup_cmap:
            continue
        gname = 'uni%04X' % cp
        aw = sup_hmtx[sup_cmap[cp]][0]
        w = int(round(aw * scale))
        if is_cff:
            from fontTools.pens.recordingPen import DecomposingRecordingPen
            rec = DecomposingRecordingPen(sup_gs)
            sup_gs[sup_cmap[cp]].draw(TransformPen(rec, (scale, 0, 0, scale, 0, 0)))
            pen = T2CharStringPen(w, None)
            rec.replay(pen)
            cs[gname] = pen.getCharString(private=getattr(td, 'Private', None))
        else:
            from fontTools.pens.recordingPen import DecomposingRecordingPen
            rec = DecomposingRecordingPen(sup_gs)
            sup_gs[sup_cmap[cp]].draw(TransformPen(rec, (scale, 0, 0, scale, 0, 0)))
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
        return font_bytes, 0
    f.setGlyphOrder(order)
    if 'maxp' in f:
        f['maxp'].numGlyphs = len(order)
    out = io.BytesIO()
    f.save(out)
    return out.getvalue(), added


n_ok = n_fail = total_added = 0
for fn in sorted(os.listdir(DUMP)):
    if not fn.endswith('.cmp'):
        continue
    src = os.path.join(DUMP, fn)
    orig, key = read_cmp(open(src, 'rb').read())
    _, tabs = sfnt_tables(orig)
    try:
        if 'CFF ' in TTFont(io.BytesIO(orig), lazy=True):
            # CFF: khong chen truc tiep duoc -> dung rebuild (giu glyph goc + chep GPOS/GSUB)
            from rebuild_cff_font import rebuild
            patched = rebuild(orig, SUPPLY, need)
            added = len(need)
        else:
            patched, added = add_glyphs(orig, SUPPLY)
    except Exception as e:
        print(f'  [!!] {fn[:40]}: loi {type(e).__name__}: {str(e)[:50]}')
        n_fail += 1
        continue
    if added == 0:
        print(f'  [-] {fn[:40]}: khong them duoc glyph nao')
        n_fail += 1
        continue
    # KHONG cat bang muc luc (giu nguyen ket qua fontTools).
    # Ly do: ban "cat bang" truoc do lam hong lien ket glyph (chu goc cung bi vuong).
    pruned = patched
    data = write_cmp(pruned, key)
    open(os.path.join(MOD, fn), 'wb').write(data)
    # DOC LAI XAC MINH
    back, _ = read_cmp(open(os.path.join(MOD, fn), 'rb').read())
    _, t2 = sfnt_tables(back)
    same_tabs = set(t2) == set(tabs)
    try:
        cm = set(TTFont(io.BytesIO(back), lazy=True).getBestCmap())
        cov = all(c in cm for c in need)
    except Exception:
        cov = False
    total_added += added
    if same_tabs and cov:
        n_ok += 1
    else:
        n_fail += 1
        print(f'  [!!] {fn[:40]}: bang khop={same_tabs} phu du={cov}')
print(f'\n  {n_ok} font OK | {n_fail} loi | tong {total_added:,} glyph da them')
print(f'  (bang muc luc giu y danh sach bang cua font goc)')
