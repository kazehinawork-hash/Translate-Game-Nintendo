"""Kirby and the Forgotten Land: ghep glyph tieng Viet TU CHINH font goc (11 font CFF .bfotf).

Cach lam (khong dung font ngoai => kieu chu dong nhat voi game):
  1. Giai ma .bfotf.cmp -> OTF (XOR magic 0x36F81A1E + zstd).
  2. Voi moi ky tu tieng Viet con thieu: ghep tu chinh font:
       - chu cai co so (a,e,i,o,u,y,d,...) lay nguyen tu font;
       - dau sac/huyen/nga/mu/breve lay tu GLYPH DAU ROI (combining) co san trong font;
       - chi VE THEM 2 dau: moc (horn: o+u) va dau hoi (hook).
     Giu nguyen advance width = chu cai co so => khong lech khoang cach.
  3. Chen vao cac CID chua dung, cap nhat cmap, dong goi lai .bfotf.cmp.

Chay: python tools/kirby_patch_all_fonts_native.py   (tu goc du an)
"""
import io
import json
import math
import os
import struct
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TID = '01004D300C5AE000'
SRC_DIR = os.path.join(ROOT, 'games', f'{TID}_Kirby', 'source', 'font', 'ScalableFontBin')
OUT_DIR = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'font', 'ScalableFontBin')
os.makedirs(OUT_DIR, exist_ok=True)

import zstandard
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen

MAGIC_KIRBY = 0x36F81A1E
CAND = (0x4F54544F, 0x00010000, 0x74746366)
compressor = zstandard.ZstdCompressor(level=15)
decompressor = zstandard.ZstdDecompressor()

# Nguon dau roi (combining) co san trong cac font nay
COMB = {0x0300: 'grave', 0x0301: 'acute', 0x0302: 'circumflex', 0x0303: 'tilde',
        0x0306: 'breve', 0x0307: 'dot'}
SHAPE_MARKS = (0x0302, 0x0306)
TONE_ABOVE = (0x0301, 0x0300, 0x0303)


def unwrap(raw):
    d = decompressor.decompress(raw[4:], max_output_size=256 << 20)
    assert struct.unpack_from('>I', d, 0)[0] == MAGIC_KIRBY, 'magic sai'
    w8, = struct.unpack_from('>I', d, 8)
    for e in CAND:
        key = w8 ^ e
        body = b''.join(struct.pack('>I', struct.unpack_from('>I', d, i)[0] ^ key)
                        for i in range(8, len(d), 4))
        if body[:4] == struct.pack('>I', e):
            return body, key
    raise ValueError('khong giai ma duoc')


def wrap(otf, key):
    pad = (4 - (len(otf) % 4)) % 4
    if pad:
        otf += b'\x00' * pad
    enc = b''.join(struct.pack('>I', struct.unpack_from('>I', otf, i)[0] ^ key)
                   for i in range(0, len(otf), 4))
    hdr = struct.pack('>II', MAGIC_KIRBY, len(otf) ^ key)
    data = hdr + enc
    return len(data).to_bytes(4, 'little') + compressor.compress(data)


def v_bounds(value):
    xs = []; ys = []
    for op, args in value:
        for a in args:
            if a is None:
                continue
            xs.append(a[0]); ys.append(a[1])
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None


def v_translate(value, dx, dy):
    out = []
    for op, args in value:
        if op == 'closePath':
            out.append((op, ()))
        else:
            out.append((op, tuple(None if a is None else (a[0] + dx, a[1] + dy) for a in args)))
    return out


def crescent(cx, cy, r, t, a0, a1, n=24):
    outp = []; inp = []
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        outp.append((cx + (r + t / 2) * math.cos(a), cy + (r + t / 2) * math.sin(a)))
        inp.append((cx + (r - t / 2) * math.cos(a), cy + (r - t / 2) * math.sin(a)))
    pts = outp + list(reversed(inp))
    val = [('moveTo', (pts[0],))] + [('lineTo', (p,)) for p in pts[1:]] + [('closePath', ())]
    return val


def tapered_stroke(center, w0, w1):
    n = len(center)
    left = []; right = []
    for i, p in enumerate(center):
        if i == 0:
            dx = center[1][0] - p[0]; dy = center[1][1] - p[1]
        elif i == n - 1:
            dx = p[0] - center[i - 1][0]; dy = p[1] - center[i - 1][1]
        else:
            dx = center[i + 1][0] - center[i - 1][0]; dy = center[i + 1][1] - center[i - 1][1]
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        w = (w0 + (w1 - w0) * i / (n - 1)) / 2.0 if n > 1 else w0 / 2
        left.append((p[0] + nx * w, p[1] + ny * w))
        right.append((p[0] - nx * w, p[1] - ny * w))
    pts = left + list(reversed(right))
    val = [('moveTo', (pts[0],))] + [('lineTo', (p,)) for p in pts[1:]] + [('closePath', ())]
    return val


def needed_chars():
    vi = json.load(open(os.path.join(ROOT, 'games', f'{TID}_Kirby', 'translations', 'kirby_vi.json'),
                        encoding='utf-8'))
    used = set()
    for ents in vi.values():
        for v in ents.values():
            used |= set(str(v))

    def is_real(ch):
        o = ord(ch)
        return o > 0x7F and not ((0x3000 <= o <= 0x9FFF) or (0xAC00 <= o <= 0xD7FF) or (0xF900 <= o <= 0xFFFF))
    return sorted({c for c in used if is_real(c)})


def patch_bfotf(fn, need):
    raw = open(os.path.join(SRC_DIR, fn), 'rb').read()
    body, key = unwrap(raw)
    f = TTFont(io.BytesIO(body))
    gs = f.getGlyphSet()
    cm = f.getBestCmap()
    hmtx = f['hmtx'].metrics
    upem = f['head'].unitsPerEm

    def value_of(name):
        pen = DecomposingRecordingPen(gs)
        gs[name].draw(pen)
        return pen.value

    mark = {cp: value_of(cm[cp]) for cp in COMB if cp in cm}
    # x-height va be net do tu chinh font
    def gb(cp):
        return v_bounds(value_of(cm[cp])) if cp in cm else None
    o_b = gb(0x006F) or gb(0x004F)
    l_b = gb(0x006C) or gb(0x0069)
    xh = o_b[3] if o_b else int(upem * 0.55)
    stem = (l_b[2] - l_b[0]) if l_b else int(upem * 0.14)
    s = xh / 567.0

    top = f['CFF '].cff.topDictIndex[0]
    cs = top.CharStrings
    priv = top.FDArray[0].Private
    used_cids = set(cm.values())
    unused = [cid for cid in cs.keys() if cid not in used_cids and cid != '.notdef']

    def compose(ch):
        if ch in ('đ', 'Đ'):
            base_cp, nfd_marks = (ord('d'), [0x0335]) if ch == 'đ' else (ord('D'), [0x0335])
        else:
            nfd = unicodedata.normalize('NFD', ch)
            base_cp = ord(nfd[0])
            nfd_marks = [ord(c) for c in nfd[1:]]
        if base_cp not in cm:
            return None
        bv = value_of(cm[base_cp])
        bb = v_bounds(bv)
        cx = (bb[0] + bb[2]) / 2.0
        val = list(bv)
        W = hmtx[cm[base_cp]][0]
        top_y = bb[3]

        shape = 0x0302 if 0x0302 in nfd_marks else (0x0306 if 0x0306 in nfd_marks else
                                                    ('horn' if 0x031B in nfd_marks else None))
        if shape in SHAPE_MARKS:
            m = mark[shape]
            mb = v_bounds(m)
            mm = v_translate(m, cx - (mb[0] + mb[2]) / 2.0, 0)
            val += mm
            top_y = v_bounds(mm)[3]
        elif shape == 'horn':
            x1 = bb[2]
            center = [(x1 - 15 * s, top_y - 20 * s), (x1 + 38 * s, top_y + 18 * s),
                      (x1 + 52 * s, top_y + 78 * s)]
            val += tapered_stroke(center, stem * 1.0, stem * 0.5)

        tone = next((cp for cp in (0x0301, 0x0300, 0x0303, 0x0309, 0x0323) if cp in nfd_marks), None)
        if tone in TONE_ABOVE:
            m = mark[tone]
            mb = v_bounds(m)
            dy = (top_y + 8 * s) - mb[1] if shape in SHAPE_MARKS else 0
            val += v_translate(m, cx - (mb[0] + mb[2]) / 2.0, dy)
        elif tone == 0x0309:
            val += crescent(cx, top_y + 40 * s, 95 * s, stem * 0.72,
                            math.radians(200), math.radians(20))
        elif tone == 0x0323:
            dot = mark[0x0307]
            db = v_bounds(dot)
            val += v_translate(dot, cx - (db[0] + db[2]) / 2.0, (bb[1] - 45 * s) - db[3])
        elif tone == 0x0335:
            y = bb[1] + (bb[3] - bb[1]) * 0.80
            val += tapered_stroke([(bb[0] - 25 * s, y), (bb[2] + 25 * s, y)], stem * 0.9, stem * 0.9)
        return val, W

    todo = [c for c in need if ord(c) not in cm]
    made = 0
    for i, ch in enumerate(todo):
        r = compose(ch)
        if r is None:
            continue
        val, W = r
        cid = unused[i]
        pen = T2CharStringPen(W, cs)
        for op, args in val:
            getattr(pen, op)(*args)
        t2 = pen.getCharString()
        t2.private = priv
        cs[cid] = t2
        f['hmtx'].metrics[cid] = (int(W), int(v_bounds(val)[0]))
        for sub in f['cmap'].tables:
            if sub.isUnicode():
                sub.cmap[ord(ch)] = cid
        made += 1

    buf = io.BytesIO()
    f.save(buf)
    new_otf = buf.getvalue()
    out = wrap(new_otf, key)
    open(os.path.join(OUT_DIR, fn), 'wb').write(out)
    # doc lai xac minh
    chk_body, _ = unwrap(out)
    cm2 = TTFont(io.BytesIO(chk_body)).getBestCmap()
    left = [c for c in need if ord(c) not in cm2]
    print(f'  [+] {fn:<36} them {made:>3} glyph | con thieu {len(left)} | {len(out):,} bytes')


def main():
    need = needed_chars()
    print(f'Ky tu tieng Viet can: {len(need)}')
    print('=== GHEP GLYPH TIENG VIET CHO 11 FONT CFF (.bfotf) ===')
    for fn in sorted(os.listdir(SRC_DIR)):
        if fn.endswith('.bfotf.cmp'):
            patch_bfotf(fn, need)
    print('\nHoan tat ghep 11 font CFF Kirby!')


if __name__ == '__main__':
    main()
