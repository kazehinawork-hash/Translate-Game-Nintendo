"""Hop nhat font Switch Sports (thu cong): giu TOAN BO glyph goc + them glyph tieng Viet.

- Goc la OTTO (CFF) -> chuyen sang TTF (glyf) bang Cu2QuPen.
- Copy tung glyph con thieu tu Nunito (kem ca glyph thanh phan neu la composite).
"""
import collections
import copy
import io
import os
import struct
import sys

import zstandard
import oead
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont, newTable

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
GAME = os.path.join(ROOT, 'games', '0100D2F00D5C0000_SwitchSports')
BASE = os.path.join(GAME, 'source', 'orig_font', 'Font.Nin_NX_NVN.bfarc.zs')
OUTDIR = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '0100D2F00D5C0000', 'romfs', 'Font')
OUT = os.path.join(OUTDIR, 'Font.Nin_NX_NVN.bfarc.zs')
K = 2785117442
MAGIC = 0xD99B871A

TARGET = {'scft/VDL-LOGOG-BOLD.bfotf': 'tools/Nunito-Bold.ttf',
          'scft/VDL-LOGOG-ULTRA.bfotf': 'tools/Nunito-Black.ttf',
          'scft/VDL-GigaJr-ExtraBold-003_Gaiji.bfotf': 'tools/Nunito-Bold.ttf',
          'scft/VDL-GigaJr-Ultra-003_Gaiji.bfotf': 'tools/Nunito-Black.ttf'}
VI = 'àáâãèéêìíòóôõùúýăđĩũơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹĂÂĐÊÔƠƯÁÀẢÃẠẾỆỐỘỚỜỢỨỪỰỤỦỸỲÝỶỵ'


def unwrap(d):
    out = bytearray()
    for i in range(8, len(d), 4):
        w, = struct.unpack_from('>I', d, i)
        out += struct.pack('>I', w ^ K)
    return bytes(out)


def wrap(b):
    if len(b) % 4:
        b += b'\x00' * (4 - len(b) % 4)
    words = [MAGIC, len(b) ^ K]
    for i in range(0, len(b), 4):
        w, = struct.unpack_from('>I', b, i)
        words.append(w ^ K)
    return struct.pack(f'>{len(words)}I', *words)


def otf_to_ttf(font, max_err=1.0):
    go = font.getGlyphOrder()
    font['loca'] = newTable('loca')
    font['glyf'] = glyf = newTable('glyf')
    glyf.glyphOrder = go
    gs = font.getGlyphSet()
    q = {}
    for n in go:
        pen = TTGlyphPen(gs)
        gs[n].draw(Cu2QuPen(pen, max_err))
        q[n] = pen.glyph()
    glyf.glyphs = q
    for tag in ('CFF ', 'CFF2', 'VORG'):
        if tag in font:
            del font[tag]
    glyf.compile(font)
    font['maxp'] = maxp = newTable('maxp')
    maxp.tableVersion = 0x00010000
    for a in ('maxZones', 'maxTwilightPoints', 'maxStorage', 'maxFunctionDefs',
              'maxInstructionDefs', 'maxStackElements', 'maxSizeOfInstructions'):
        setattr(maxp, a, 1 if a == 'maxZones' else 0)
    maxp.maxComponentElements = max((len(g.components) if hasattr(g, 'components') and g.components else 0)
                                    for g in q.values())
    maxp.compile(font)
    post = font['post']
    post.formatType = 2.0
    post.extraNames = []
    post.mapping = {}
    post.glyphOrder = go
    try:
        post.compile(font)
    except OverflowError:
        post.formatType = 3
    font.sfntVersion = '\x00\x01\x00\x00'
    return font


def add_missing(orig, nun, need):
    """Them glyph tu `nun` vao `orig` cho cac codepoint trong `need` chua co."""
    og, ng = orig['glyf'], nun['glyf']
    oh, nh = orig['hmtx'], nun['hmtx']
    ocmap = orig.getBestCmap()
    ncmap = nun.getBestCmap()
    tables = [t for t in orig['cmap'].tables if t.isUnicode()]
    uni = tables[0] if tables else orig['cmap'].tables[0]
    order = list(orig.getGlyphOrder())
    added = 0
    for cp in need:
        if cp in ocmap or cp not in ncmap:
            continue
        src = ncmap[cp]
        todo, seen = [src], set()
        while todo:
            gname = todo.pop()
            if gname in seen or gname in og.glyphs:
                continue
            seen.add(gname)
            g = copy.deepcopy(ng[gname])
            og.glyphs[gname] = g
            try:
                aw, lsb = nh[gname]
            except KeyError:
                aw, lsb = 1000, 0
            oh.metrics[gname] = (aw, lsb)
            order.append(gname)
            if getattr(g, 'isComposite', lambda: False)():
                todo += [c.glyphName for c in g.components]
        uni.cmap[cp] = src
        added += 1
    # cap nhat glyph order + DUNG LAI hmtx/maxp cho day du
    for gname in og.glyphs:
        if gname not in order:
            order.append(gname)
    orig.setGlyphOrder(order)
    orig['glyf'].glyphOrder = order
    # cung cap moi ten trong glyph order (ke ca ten den tu post/CFF cu)
    try:
        for extra in (orig['post'].glyphOrder or []):
            if extra not in order:
                order.append(extra)
    except Exception:
        pass
    default_aw = oh.metrics.get('.notdef', (1000, 0))[0] if '.notdef' in oh.metrics else 1000
    full = collections.defaultdict(lambda: (default_aw, 0))
    for gname in order:
        if gname in oh.metrics:
            full[gname] = oh.metrics[gname]
    new_hmtx = newTable('hmtx')
    new_hmtx.metrics = full
    orig['hmtx'] = new_hmtx
    orig['maxp'].numGlyphs = len(order)
    orig['maxp'].compile(orig)
    return added


def main():
    sarc = oead.Sarc(zstandard.ZstdDecompressor().decompress(open(BASE, 'rb').read()))
    files = {f.name: f.data for f in sarc.get_files()}
    print(f'SARC goc: {len(files)} file')
    vips = [ord(c) for c in VI]

    for name, npath in TARGET.items():
        if name not in files:
            continue
        otf = TTFont(io.BytesIO(unwrap(files[name])), lazy=False)
        n_orig = len(otf.getBestCmap())
        otf_to_ttf(otf)
        nun = TTFont(os.path.join(ROOT, npath))
        have = otf.getBestCmap()
        need = [c for c in range(0x20, 0x300)] + vips
        added = add_missing(otf, nun, need)
        out = io.BytesIO()
        try:
            otf.save(out)
        except Exception as e:
            import traceback
            print('    LOI khi luu font:')
            traceback.print_exc()
            raise
        data = out.getvalue()
        cm = set(TTFont(io.BytesIO(data), lazy=True).getBestCmap())
        miss = [hex(c) for c in vips if c not in cm]
        files[name] = wrap(data)
        print(f'  {name}\n    goc {n_orig:,} glyph -> {len(cm):,} | them {added} | thieu VI: {len(miss)} {miss[:6]} | {len(data):,} byte')

    w = oead.SarcWriter.from_sarc(sarc)
    for n, d in files.items():
        w.files[n] = oead.Bytes(d)
    ns = w.write()[1]
    comp = zstandard.ZstdCompressor(level=16).compress(ns)
    os.makedirs(OUTDIR, exist_ok=True)
    open(OUT, 'wb').write(comp)
    print(f'\nda ghi {OUT} ({len(comp):,} byte)')


if __name__ == '__main__':
    main()
