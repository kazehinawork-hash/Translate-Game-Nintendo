"""VA FONT KIRBY (ban 6) - lam tren file DA GIAI MA, tung buoc tu kiem chung.

Vi sao ban nay khac: truoc day va truc tiep trong container (.cmp) nen khong the
tach loi. Nay:
    buoc A: sua file .otf/.ttf tren dia -> kiem chung (fontTools + RENDER FreeType)
    buoc B: dong goi lai bang tools/kirby_font_reencrypt.py

Chi ghi file khi buoc A DAT (render chu co dau ra muc, khac o vuong).
"""
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.boundsPen import BoundsPen

TID = '01004D300C5AE000'
EDIT = os.path.join(ROOT, 'games', f'{TID}_Kirby', 'font_edit')
SUPPLY = os.path.join(ROOT, 'tools', 'Nunito-Bold.ttf')

vi = json.load(open(os.path.join(ROOT, 'games', f'{TID}_Kirby', 'translations', 'kirby_vi.json'),
                    encoding='utf-8'))
used = set()
for ents in vi.values():
    for v in ents.values():
        used |= set(str(v))
need = sorted({ord(c) for c in used if c.isprintable() and
               (0x20 <= ord(c) <= 0x2FF or 0x1EA0 <= ord(c) <= 0x1EFF)})
print(f'can {len(need)} ky tu')


def render_ok(path, probe='Bạn có muốn kết nối trực tuyến'):
    """Tra True neu ve duoc chu co dau (khong phai o vuong)."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        f = ImageFont.truetype(path, 26)
        im = Image.new('L', (420, 46), 255)
        ImageDraw.Draw(im).text((4, 6), probe, font=f, fill=0)
        px = im.load()
        cols = sum(1 for x in range(im.width) if any(px[x, y] < 128 for y in range(im.height)))
        # so voi 1 ky tu chac chan khong co (o vuong rong)
        im2 = Image.new('L', (80, 46), 255)
        ImageDraw.Draw(im2).text((4, 6), '\ue123', font=f, fill=0)
        px2 = im2.load()
        box = sum(1 for x in range(im2.width) if any(px2[x, y] < 128 for y in range(im2.height)))
        return cols > 40 and cols != box, cols, box
    except Exception as e:
        return False, -1, str(e)[:40]


sup = TTFont(SUPPLY)
sup_gs = sup.getGlyphSet()
sup_cmap = sup.getBestCmap()
sup_hmtx = sup['hmtx']

# --- chi lam nhom .otf/.ttf da giai ma, bo qua file .key ---
targets = [f for f in sorted(os.listdir(EDIT)) if f.endswith(('.otf', '.ttf'))]
n_ok = 0
for name in targets:
    p = os.path.join(EDIT, name)
    ok0, cols0, box0 = render_ok(p)
    print(f'  {name[:34]:<36} truoc: render {"OK" if ok0 else "HONG"} ({cols0})')
    try:
        f = TTFont(p)
        upem = f['head'].unitsPerEm
        scale = upem / sup['head'].unitsPerEm
        is_cff = 'CFF ' in f
        have = set(f.getBestCmap())
        order = list(f.getGlyphOrder())
        hmtx = f['hmtx']
        glyf = None if is_cff else f['glyf']
        cs = None if not is_cff else f['CFF '].cff.topDictIndex[0].CharStrings
        # font CFF kieu CID: TEN GLYPH phai la 'cidNNNNN' (khong duoc dat 'uniXXXX')
        cid_next = 0
        if is_cff:
            import re
            for k in cs.keys():
                m = re.fullmatch(r'cid(\d+)', k)
                if m:
                    cid_next = max(cid_next, int(m.group(1)) + 1)
            print(f'    (CFF kieu CID, cid ke tiep = {cid_next})')
        added = 0
        for cp in need:
            if cp in have or cp not in sup_cmap:
                continue
            if is_cff:
                gname = 'cid%05d' % cid_next
                cid_next += 1
            else:
                gname = 'uni%04X' % cp
            w = int(round(sup_hmtx[sup_cmap[cp]][0] * scale))
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
            print(f'  {name[:34]:<36} khong them duoc glyph nao')
            continue
        f.setGlyphOrder(order)
        if 'maxp' in f:
            f['maxp'].numGlyphs = len(order)
        # CFF: dam bao MOI glyph trong thu tu deu co metric, neu khong hhea.recalc loi KeyError
        default_w = int(round(upem * 0.5))
        for g in f.getGlyphOrder():
            if g not in hmtx.metrics:
                hmtx.metrics[g] = (default_w, 0)
        tmp = p + '.tmp'
        f.save(tmp)
        # kiem chung: nap lai + glyph goc + render
        chk = TTFont(tmp)
        cm = chk.getBestCmap()
        gs = chk.getGlyphSet()
        base_ok = True
        for c in 'Kanhoc':
            gn = cm.get(ord(c))
            if gn is None:
                base_ok = False
                break
            bp = BoundsPen(gs)
            gs[gn].draw(bp)
            if bp.bounds is None:
                base_ok = False
                break
        vi_ok = all(c in cm for c in need)
        # kiem chung SAU HON: moi glyph tieng Viet phai co duong net that
        if vi_ok:
            for c in need:
                if c < 0x20:
                    continue
                try:
                    bp = BoundsPen(gs)
                    gs[cm[c]].draw(bp)
                    if bp.bounds is None:
                        vi_ok = False
                        break
                except Exception:
                    vi_ok = False
                    break
        okr, cols, box = render_ok(tmp)
        if base_ok and vi_ok and okr:
            os.replace(tmp, p)
            n_ok += 1
            print(f'  {name[:34]:<36} +{added:>3} glyph | chu goc OK | cmap du | render DAT ({cols})')
        else:
            os.remove(tmp)
            print(f'  {name[:34]:<36} LOAI: base={base_ok} vi={vi_ok} render={okr}({cols})')
    except Exception as e:
        print(f'  {name[:34]:<36} loi {type(e).__name__}: {str(e)[:50]}')
print(f'\n  {n_ok}/{len(targets)} font da va + render kiem chung DAT')
print('  -> chay tiep: python tools/kirby_font_reencrypt.py')
