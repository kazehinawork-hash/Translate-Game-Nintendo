"""add_glyphs_glyf.py — THEM glyph tieng Viet vao font glyf (TTF) ma GIU nguyen toan bo glyph goc.

Dung cho cac bo font .bfttf cua Kirby (CHI-/KOR-/TWN- va K15-LocalCharacter).
KHONG dung fontTools.merge.Merger vi no loi tren cac font nay
(AssertionError: Expected all items to be equal: [0, NotImplemented...]).

Cach lam: ve glyph moi bang TTGlyphPen roi chen thang vao bang glyf/hmtx/cmap cua font goc.
"""
import io

from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.ttLib import TTFont


def add_glyphs_glyf(base_bytes: bytes, supply_path: str, needed, verbose: bool = False) -> bytes:
    base = TTFont(io.BytesIO(base_bytes))
    if 'glyf' not in base:
        raise ValueError('font dich khong phai glyf/TTF')
    upem = base['head'].unitsPerEm

    glyf = base['glyf']
    hmtx = base['hmtx']
    cmap = base.getBestCmap()
    have = set(cmap)
    order = list(base.getGlyphOrder())

    sup = TTFont(supply_path)
    scale = upem / sup['head'].unitsPerEm
    sup_gs = sup.getGlyphSet()
    sup_cmap = sup.getBestCmap()
    sup_hmtx = sup['hmtx']

    n = 0
    for cp in sorted(set(needed)):
        if cp in have or cp not in sup_cmap:
            continue
        name = 'uni%04X' % cp
        if name in glyf:
            continue
        aw = sup_hmtx[sup_cmap[cp]][0]
        # ⚠️ TTGlyphPen(glyphSet) VAN giu glyph o dang GHEP -> ten thanh phan (acute/breve/
        # tilde/circumflex) khong co trong font dich -> KeyError luc font.save().
        # Phai D U O I han bang DecomposingRecordingPen roi replay vao TTGlyphPen(None).
        rec = DecomposingRecordingPen(sup_gs)
        sup_gs[sup_cmap[cp]].draw(TransformPen(rec, (scale, 0, 0, scale, 0, 0)))
        pen = TTGlyphPen(None)
        rec.replay(pen)
        g = pen.glyph()
        glyf[name] = g
        hmtx[name] = (int(round(aw * scale)), getattr(g, 'xMin', 0))
        order.append(name)
        cmap[cp] = name
        for t in base['cmap'].tables:
            if t.isUnicode():
                t.cmap[cp] = name
        n += 1

    if not n:
        return base_bytes
    base.setGlyphOrder(order)
    base['maxp'].numGlyphs = len(order)
    if verbose:
        print(f'    them {n} glyph (upem {upem}, scale {scale:.4f})')
    out = io.BytesIO()
    base.save(out)
    return out.getvalue()
