"""rebuild_cff_font.py — dung lai font CFF/OTF GIU NGUYEN dinh dang, upem va TOAN BO glyph goc,
chi THEM cac glyph tieng Viet con thieu (BH-20).

Khac voi cff_add_glyphs.py (khong chen duoc vao CharStrings vi fontTools chan them glyph moi),
tool nay dung FontBuilder de dung lai CFF tu chinh glyph set cua font goc:

  - Ve lai tung glyph goc bang T2CharStringPen  -> giu nguyen hinh dang + so luong glyph
  - Ve them glyph tieng Viet tu font nguon (co scale ve dung upem dich)
  - Giu upem, dinh dang CFF; chep lai GPOS/GSUB/vhea/vmtx/VORG neu co

Dung:
    from rebuild_cff_font import rebuild
    out = rebuild(otf_bytes, 'C:/Windows/Fonts/ARIALUNI.TTF', {0x1EA1, ...})
"""
import io
import sys

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

# vhea/vmtx la bang con cua hmtx (fontTools dung chung metrics) -> chep vao se lam hong hmtx
# khi ta da them glyph moi. Font Latin khong can metric doc.
COPY_TABLES = ('GPOS', 'GSUB', 'GDEF', 'VORG', 'BASE')


def _draw_charstrings(font, glyph_names):
    gs = font.getGlyphSet()
    hmtx = font['hmtx']
    out = {}
    for name in glyph_names:
        pen = T2CharStringPen(int(hmtx[name][0]), gs)
        gs[name].draw(pen)
        out[name] = pen.getCharString()
    return out


def rebuild(otf_bytes: bytes, supply_path: str, needed, verbose: bool = False) -> bytes:
    src = TTFont(io.BytesIO(otf_bytes))
    if 'CFF ' not in src:
        raise ValueError('khong phai font CFF')
    upem = src['head'].unitsPerEm
    order = list(src.getGlyphOrder())
    hmtx = {n: src['hmtx'][n] for n in order}
    cmap = dict(src.getBestCmap())
    have = set(cmap)

    # 1) ve lai glyph goc -> charstrings
    charstrings = _draw_charstrings(src, order)

    # 2) them glyph tieng Viet
    sup = TTFont(supply_path)
    scale = upem / sup['head'].unitsPerEm
    sup_gs = sup.getGlyphSet()
    sup_cmap = sup.getBestCmap()
    sup_hmtx = sup['hmtx']
    added = 0
    for cp in sorted(set(needed)):
        if cp in have or cp not in sup_cmap:
            continue
        gname = 'uni%04X' % cp
        if gname in charstrings:
            continue
        aw = sup_hmtx[sup_cmap[cp]][0]
        w = int(round(aw * scale))
        pen = T2CharStringPen(w, sup_gs)
        sup_gs[sup_cmap[cp]].draw(TransformPen(pen, (scale, 0, 0, scale, 0, 0)))
        charstrings[gname] = pen.getCharString()
        hmtx[gname] = (w, 0)
        cmap[cp] = gname
        order.append(gname)
        added += 1

    # 3) dung lai font
    name_rec = src['name']
    ps_name = name_rec.getDebugName(6) or 'Rebuilt'
    fb = FontBuilder(upem, isTTF=False)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    fb.setupCFF(ps_name, {'FullName': name_rec.getDebugName(4) or ps_name}, charstrings, {})
    fb.setupHorizontalMetrics({n: hmtx[n] for n in order})
    hhea = src['hhea']
    fb.setupHorizontalHeader(ascent=hhea.ascent, descent=hhea.descent, lineGap=hhea.lineGap)
    os2 = src['OS/2']
    fb.setupOS2(
        sTypoAscender=os2.sTypoAscender, sTypoDescender=os2.sTypoDescender,
        sTypoLineGap=getattr(os2, 'sTypoLineGap', 0),
        usWinAscent=os2.usWinAscent, usWinDescent=os2.usWinDescent,
        sxHeight=getattr(os2, 'sxHeight', None), sCapHeight=getattr(os2, 'sCapHeight', None),
        usWeightClass=getattr(os2, 'usWeightClass', 400),
        fsSelection=getattr(os2, 'fsSelection', 0),
        achVendID=getattr(os2, 'achVendID', None),
        ulUnicodeRange1=getattr(os2, 'ulUnicodeRange1', 0),
    )
    fb.setupNameTable({
        'familyName': name_rec.getDebugName(1) or ps_name,
        'styleName': name_rec.getDebugName(2) or 'Regular',
        'uniqueFontIdentifier': ps_name + ':rebuilt',
        'fullName': name_rec.getDebugName(4) or ps_name,
        'psName': ps_name,
    })
    fb.setupPost()

    # 4) chep lai cac bang phu neu co
    built = fb.font
    copied = []
    for tag in COPY_TABLES:
        if tag in src:
            try:
                built[tag] = src[tag]
                copied.append(tag)
            except Exception:
                pass
    if verbose:
        print(f'    upem {upem} | giu {len(order) - added} glyph goc + them {added} | '
              f'chep bang: {",".join(copied) or "khong"}')
    out = io.BytesIO()
    built.save(out)
    return out.getvalue()


def _selftest():
    sys.stdout.reconfigure(encoding='utf-8')
    import os
    import struct as _s
    import zstandard
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(root, 'games', '01004D300C5AE000_Kirby', 'source', 'font', 'ScalableFontBin',
                     'FOT-ComicReggaeStd-B.bfotf.cmp')
    d = zstandard.ZstdDecompressor().decompress(open(p, 'rb').read()[4:], max_output_size=64 << 20)
    w8, = _s.unpack_from('>I', d, 8)
    otf = None
    for expect in (0x4F54544F, 0x00010000, 0x74746366):
        key = w8 ^ expect
        body = b''.join(_s.pack('>I', _s.unpack_from('>I', d, i)[0] ^ key) for i in range(8, len(d), 4))
        if body[:4] == _s.pack('>I', expect):
            try:
                TTFont(io.BytesIO(body), lazy=True).getBestCmap()
                otf = body
                break
            except Exception:
                continue
    src = TTFont(io.BytesIO(otf))
    cg = set(src.getBestCmap())
    need = [ord(c) for c in 'ăâêôơưđáàảãạấầẩẫậắằẳẵặéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵĂÂÊÔƠƯĐ']
    out = rebuild(otf, r'C:\Windows\Fonts\ARIALUNI.TTF', need, verbose=True)
    f = TTFont(io.BytesIO(out))
    cm = set(f.getBestCmap())
    lost = [c for c in cg if c not in cm]
    miss = [c for c in need if c not in cm]
    print(f'  goc: CFF={("CFF " in src)} upem={src["head"].unitsPerEm} cmap={len(cg):,}')
    print(f'  moi: CFF={("CFF " in f)} upem={f["head"].unitsPerEm} cmap={len(cm):,} '
          f'glyph={f["maxp"].numGlyphs:,}')
    print(f'  MAT {len(lost)} glyph goc | thieu VI {len(miss)}')
    from fontTools.pens.boundsPen import BoundsPen
    gsh = f.getGlyphSet()
    for ch in 'ăâờ':
        nm = f.getBestCmap().get(ord(ch))
        bp = BoundsPen(gsh)
        gsh[nm].draw(bp)
        print(f'  outline "{ch}": bounds={bp.bounds}')


if __name__ == '__main__':
    _selftest()
