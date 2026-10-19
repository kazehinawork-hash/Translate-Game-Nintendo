"""Vá font Switch Sports theo phương pháp NATIVE (BH-38 / BH-20) — an toàn tuyệt đối.

Khác với `build_custom_font.py` (thay hẳn font bằng Nunito -> mất 7.888/8.207 glyph, game crash)
và `patch_font_switchsports.py` (thay hẳn bằng Arial Unicode -> đổi định dạng CID & style):

  - GIỮ NGUYÊN 100% cấu trúc font gốc: số glyph, charset, CID-Keyed (VDL-LOGOG),
    FDSelect/FDArray/PrivateDict, GPOS/GSUB/GDEF, advance width...
  - Chỉ GHÉP thêm glyph tiếng Việt từ CHÍNH font gốc (chữ cái cơ sở + dấu tổ hợp có sẵn)
    vào các slot CID/glyph CHƯA DÙNG -> không đổi GID nào đang tồn tại (fcpx index không bị lệch).

Cách dựng glyph tiếng Việt: NFD tách thành chữ cái cơ sở + dấu; dấu lấy từ glyph tổ hợp
có sẵn trong font (0x0300/0x0301/0x0302/0x0303/0x0306/0x0307); riêng móc (horn), dấu hỏi (hook),
dấu nặng (dot below) và gạch ngang Đ/đ thì VẼ bằng nét chỉnh theo x-height/stem của chính font.

Chạy: python tools/patch_font_switchsports_native.py   (từ gốc dự án)
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
sys.path.insert(0, os.path.join(ROOT, 'tools'))

import zstandard
import oead
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from zs_util import compress_like

GAME = os.path.join(ROOT, 'games', '0100D2F00D5C0000_SwitchSports')
BASE = os.path.join(GAME, 'source', 'orig_font', 'Font.Nin_NX_NVN.bfarc.zs')
OUTDIR = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '0100D2F00D5C0000', 'romfs', 'Font')
OUT = os.path.join(OUTDIR, 'Font.Nin_NX_NVN.bfarc.zs')

K = 2785117442
MAGIC = 0xD99B871A

TARGET = ['scft/VDL-LOGOG-BOLD.bfotf', 'scft/VDL-LOGOG-ULTRA.bfotf',
          'scft/VDL-GigaJr-ExtraBold-003_Gaiji.bfotf', 'scft/VDL-GigaJr-Ultra-003_Gaiji.bfotf']

VI = ('àáâãèéêìíòóôõùúýăđĩũơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ'
      'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝĂĐĨŨƠƯẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼẾỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴỶỸ')

COMB = {0x0300: 'grave', 0x0301: 'acute', 0x0302: 'circumflex', 0x0303: 'tilde',
        0x0306: 'breve', 0x0307: 'dot'}
SHAPE_MARKS = (0x0302, 0x0306)
TONE_ABOVE = (0x0301, 0x0300, 0x0303)


def unwrap(d):
    assert struct.unpack_from('>I', d, 0)[0] == MAGIC, 'magic .bfotf sai'
    return b''.join(struct.pack('>I', struct.unpack_from('>I', d, i)[0] ^ K) for i in range(8, len(d), 4))


def wrap(b):
    if len(b) % 4:
        b += b'\x00' * (4 - len(b) % 4)
    words = [MAGIC, len(b) ^ K]
    for i in range(0, len(b), 4):
        w, = struct.unpack_from('>I', b, i)
        words.append(w ^ K)
    return struct.pack(f'>{len(words)}I', *words)


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
    return [('moveTo', (pts[0],))] + [('lineTo', (p,)) for p in pts[1:]] + [('closePath', ())]


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
    return [('moveTo', (pts[0],))] + [('lineTo', (p,)) for p in pts[1:]] + [('closePath', ())]


def needed_chars():
    used = set(VI)
    tdir = os.path.join(GAME, 'translations')
    if os.path.isdir(tdir):
        for fn in os.listdir(tdir):
            if fn.endswith('.json'):
                for v in json.load(open(os.path.join(tdir, fn), encoding='utf-8')).values():
                    used |= set(str(v))
    return used


def patch_bfotf(fdata, need_all):
    f = TTFont(io.BytesIO(unwrap(fdata)))
    gs = f.getGlyphSet()
    cm = f.getBestCmap()
    hmtx = f['hmtx'].metrics
    upem = f['head'].unitsPerEm

    def value_of(name):
        pen = DecomposingRecordingPen(gs)
        gs[name].draw(pen)
        return pen.value

    mark = {cp: value_of(cm[cp]) for cp in COMB if cp in cm}
    o_b = v_bounds(value_of(cm[0x006F])) if 0x006F in cm else None
    l_b = v_bounds(value_of(cm[0x006C])) if 0x006C in cm else None
    xh = o_b[3] if o_b else int(upem * 0.55)
    stem = (l_b[2] - l_b[0]) if l_b else int(upem * 0.14)
    s = xh / 567.0

    top = f['CFF '].cff.topDictIndex[0]
    cs = top.CharStrings
    order = list(f.getGlyphOrder())
    has_fd = hasattr(top, 'FDArray') and hasattr(top, 'FDSelect') and len(getattr(top, 'FDArray', [])) > 0
    if has_fd:
        cid_e = cm.get(ord('e')) or cm.get(ord('o'))
        gid_e = order.index(cid_e)
        target_fd = top.FDSelect[gid_e]
        target_priv = top.FDArray[target_fd].Private
    else:
        target_fd = None
        target_priv = top.Private
    nom_w = getattr(target_priv, 'nominalWidthX', 0)

    def compose(ch):
        if ch in ('đ', 'Đ'):
            base_cp = ord('d') if ch == 'đ' else ord('D')
            nfd_marks = [0x0335]
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

        tone = next((cp for cp in (0x0301, 0x0300, 0x0303, 0x0309, 0x0323, 0x0335) if cp in nfd_marks), None)
        if tone in TONE_ABOVE:
            m = mark[tone]
            mb = v_bounds(m)
            dy = (top_y + 8 * s) - mb[1] if shape in SHAPE_MARKS else 0
            val += v_translate(m, cx - (mb[0] + mb[2]) / 2.0, dy)
        elif tone == 0x0309:
            val += crescent(cx, top_y + 40 * s, 95 * s, stem * 0.72, math.radians(200), math.radians(20))
        elif tone == 0x0323:
            dot = mark[0x0307]
            db = v_bounds(dot)
            val += v_translate(dot, cx - (db[0] + db[2]) / 2.0, (bb[1] - 45 * s) - db[3])
        elif tone == 0x0335:
            high_x = [p[0] for cmd in bv for p in cmd[1] if p and p[1] > bb[3] * 0.85]
            if high_x:
                cx_stem = (min(high_x) + max(high_x)) / 2.0
                bar_half_w = (max(high_x) - min(high_x)) * 0.95
            else:
                cx_stem = cx
                bar_half_w = 60 * s
            y = bb[1] + (bb[3] - bb[1]) * 0.75
            val += tapered_stroke([(cx_stem - bar_half_w, y), (cx_stem + bar_half_w, y)], stem * 0.85, stem * 0.85)
        return val, W

    used_cids = set(cm.values())
    unused = [g for g in cs.keys() if g not in used_cids and g != '.notdef']

    todo = [c for c in sorted(need_all) if ord(c) not in cm]
    made = 0
    failed = []
    for ch in todo:
        r = compose(ch)
        if r is None:
            failed.append(ch)
            continue
        val, W = r
        cid = unused[made]
        gid = order.index(cid)
        if has_fd:
            top.FDSelect[gid] = target_fd
        pen = T2CharStringPen(W - nom_w, cs)
        for op, args in val:
            getattr(pen, op)(*args)
        t2 = pen.getCharString()
        t2.private = target_priv
        cs[cid] = t2
        f['hmtx'].metrics[cid] = (int(W), int(v_bounds(val)[0]))
        for sub in f['cmap'].tables:
            if sub.isUnicode():
                sub.cmap[ord(ch)] = cid
        made += 1

    buf = io.BytesIO()
    f.save(buf)
    return wrap(buf.getvalue()), made, failed, len(cm)


def main():
    need = needed_chars()
    print(f'Ký tự cần (VI + bản dịch): {len(need)}')
    src_zs = open(BASE, 'rb').read()
    sarc = oead.Sarc(zstandard.ZstdDecompressor().decompress(src_zs))
    files = {f.name: f.data for f in sarc.get_files()}
    for name in TARGET:
        if name not in files:
            print(f'  [!] thiếu {name}')
            continue
        new, made, failed, ncmap = patch_bfotf(files[name], need)
        files[name] = new
        # xác minh: giải mã lại phải ra font đọc được + đủ ký tự VI
        chk = TTFont(io.BytesIO(unwrap(new)), lazy=True)
        cm2 = set(chk.getBestCmap())
        miss_vi = [c for c in VI if ord(c) not in cm2]
        print(f'  [+] {name:<38} thêm {made:>3} | cmap {ncmap}->{len(cm2)} | còn thiếu VI {len(miss_vi)} '
              f'{""if not miss_vi else "".join(miss_vi[:10])} | CID={getattr(chk["CFF "].cff.topDictIndex[0],"ROS",None) is not None}')
        if failed:
            print(f'      (không ghép được: {len(failed)} ký tự: {"".join(failed[:20])})')

    w = oead.SarcWriter.from_sarc(sarc)
    for n, d in files.items():
        w.files[n] = oead.Bytes(d)
    ns = w.write()[1]
    comp = compress_like(src_zs, ns)
    assert zstandard.ZstdDecompressor().decompress(comp) == ns
    os.makedirs(OUTDIR, exist_ok=True)
    open(OUT, 'wb').write(comp)
    print(f'\nĐã ghi {OUT} ({len(comp):,} byte / SARC {len(ns):,})')


if __name__ == '__main__':
    main()
