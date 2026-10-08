"""Kiem tra glyph BI MAT khi va font: phan loai PUA (icon) / Latin / khac."""
import io
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import zstandard
from fontTools.ttLib import TTFont

MAGIC = 0x36F81A1E
CAND = (0x4F54544F, 0x00010000, 0x74746366)


def unwrap_ok(data):
    if len(data) < 12 or struct.unpack_from('>I', data, 0)[0] != MAGIC:
        return None
    word8, = struct.unpack_from('>I', data, 8)
    for expect in CAND:
        key = word8 ^ expect
        out = bytearray()
        for i in range(8, len(data), 4):
            out += struct.pack('>I', struct.unpack_from('>I', data, i)[0] ^ key)
        if bytes(out[:4]) != struct.pack('>I', expect):
            continue
        try:
            f = TTFont(io.BytesIO(bytes(out)), lazy=True)
            f.getBestCmap()
            return bytes(out)
        except Exception:
            continue
    return None


def kind(c):
    if 0xE000 <= c <= 0xF8FF:
        return 'PUA(icon)'
    if c < 0x20:
        return 'dieu khien'
    if 0x4E00 <= c <= 0x9FFF or 0x3400 <= c <= 0x4DBF:
        return 'CJK'
    if 0x3040 <= c <= 0x30FF:
        return 'Kana'
    if 0xAC00 <= c <= 0xD7FF:
        return 'Hangul'
    if 0x20 <= c < 0x7F:
        return 'ASCII'
    if 0xA0 <= c <= 0x2FFF:
        return 'Latin/dau cau'
    return 'khac'


def report(name, cg, cm_, fn):
    lost = sorted(c for c in cg if c not in cm_)
    from collections import Counter
    k = Counter(kind(c) for c in lost)
    print(f'  {fn[:36]:<38} mat {len(lost):>4}: ' + ', '.join(f'{a}={b}' for a, b in k.most_common()))
    pua = [c for c in lost if 0xE000 <= c <= 0xF8FF]
    if pua:
        print(f'      *** MAT {len(pua)} GLYPH PUA (icon): ' + ' '.join(f'{c:04X}' for c in pua[:14]))
    ascii_lost = [c for c in lost if 0x20 <= c < 0x7F]
    if ascii_lost:
        print(f'      *** mat ASCII: {"".join(chr(c) for c in ascii_lost)}')
    lat = [c for c in lost if 0xA0 <= c <= 0x2FFF]
    if lat:
        print(f'      mat Latin/dau cau ({len(lat)}): {"".join(chr(c) for c in lat[:30])}')


def decomp(b):
    return zstandard.ZstdDecompressor().decompress(b[4:], max_output_size=64 << 20)


# ---------- KIRBY ----------
print('=== KIRBY ===')
G = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'source', 'font', 'ScalableFontBin')
O = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01004D300C5AE000', 'romfs', 'font', 'ScalableFontBin')
for fn in sorted(os.listdir(G)):
    if not fn.endswith('.bfotf.cmp'):
        continue
    a, b = unwrap_ok(decomp(open(os.path.join(G, fn), 'rb').read())), unwrap_ok(decomp(open(os.path.join(O, fn), 'rb').read()))
    if not a or not b:
        continue
    report('kirby', set(TTFont(io.BytesIO(a), lazy=True).getBestCmap()),
           set(TTFont(io.BytesIO(b), lazy=True).getBestCmap()), fn)
