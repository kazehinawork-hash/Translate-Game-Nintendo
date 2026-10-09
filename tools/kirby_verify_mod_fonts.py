"""Xac minh font trong MOD: da co du ky tu tieng Viet, va file da doi so voi goc."""
import io
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import zstandard
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

TID = '01004D300C5AE000'
M = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'font', 'ScalableFontBin')
S = os.path.join(ROOT, 'dump', TID, 'romfs', 'font', 'ScalableFontBin')
need = [0x102, 0x1EA1, 0x1EDB, 0x1EC7, 0x1EDF, 0x1EE3, 0x1ED9, 0x1ED1, 0x1EC1, 0x1EDD]


def unwrap(b):
    d = zstandard.ZstdDecompressor()
    data = d.decompress(b[4:], max_output_size=256 << 20)
    w8, = struct.unpack_from('>I', data, 8)
    for e in (0x4F54544F, 0x00010000, 0x74746366):
        k = w8 ^ e
        body = b''.join(struct.pack('>I', struct.unpack_from('>I', data, i)[0] ^ k)
                        for i in range(8, len(data), 4))
        if body[:4] == struct.pack('>I', e):
            return body
    return None


def coverage(body):
    try:
        f = TTFont(io.BytesIO(body))
        cm = f.getBestCmap()
        gs = f.getGlyphSet()
        n = 0
        for c in need:
            if c in cm:
                bp = BoundsPen(gs)
                try:
                    gs[cm[c]].draw(bp)
                except Exception:
                    pass
                if bp.bounds:
                    n += 1
        return n, len(f.getGlyphOrder())
    except Exception as e:
        return -1, str(e)[:30]


n_ok = n_chg = n_otf = 0
for fn in sorted(os.listdir(M)):
    if not fn.endswith('.bfotf.cmp'):
        continue
    n_otf += 1
    a = os.path.getsize(os.path.join(S, fn))
    b = os.path.getsize(os.path.join(M, fn))
    if a != b:
        n_chg += 1
    body = unwrap(open(os.path.join(M, fn), 'rb').read())
    if body is None:
        print(f'  [loi] {fn}: khong giai ma duoc')
        continue
    cov, tot = coverage(body)
    flag = 'DAT' if cov == len(need) else 'LOI'
    if cov == len(need):
        n_ok += 1
    print(f'  [{flag}] {fn[:36]:<38} viet {cov}/10 | {tot} glyph')

tot_mb = sum(os.path.getsize(os.path.join(r, f))
             for r, d, fs in os.walk(os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID))
             for f in fs) / 1e6
print(f'\n  ==> {n_ok}/{n_otf} font .bfotf trong MOD co du 10 ky tu tieng Viet')
print(f'  ==> {n_chg} file doi kich thuoc so voi ban goc')
print(f'  ==> tong mod: {tot_mb:.1f} MB')
