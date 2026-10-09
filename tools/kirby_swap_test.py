"""PHEP THU: doi cho 2 ky tu n/u trong CA 45 font cua mod Kirby.

Muc dich: kiem tra game co THUC SU dung font trong mod hay khong.
  - Neu chu hien "Bau co muou ket uoi" (n<->u doi cho) => font mod DUOC dung
    => van de nam o cho khac (Filter.bin / font bitmap du phong).
  - Neu chu hien binh thuong (Ban co muon) => font mod KHONG duoc dung
    => phai tim ly do game tu choi file font.
"""
import io
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import zstandard
from fontTools.ttLib import TTFont
from zs_util import frame_params

TID = '01004D300C5AE000'
MODDIR = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'font', 'ScalableFontBin')
MAGIC = 0x36F81A1E
CAND = (0x4F54544F, 0x00010000, 0x74746366)


def decomp(b):
    return zstandard.ZstdDecompressor().decompress(b[4:], max_output_size=128 << 20)


def unwrap(data):
    if struct.unpack_from('>I', data, 0)[0] != MAGIC:
        return None, None
    w8, = struct.unpack_from('>I', data, 8)
    for expect in CAND:
        key = w8 ^ expect
        body = b''.join(struct.pack('>I', struct.unpack_from('>I', data, i)[0] ^ key)
                        for i in range(8, len(data), 4))
        if body[:4] != struct.pack('>I', expect):
            continue
        try:
            TTFont(io.BytesIO(body), lazy=True).getBestCmap()
            return body, key
        except Exception:
            continue
    return None, None


def wrap(font, key, true_len):
    t = font if len(font) % 4 == 0 else font + b'\x00' * (4 - len(font) % 4)
    words = [MAGIC, true_len ^ key]
    for i in range(0, len(t), 4):
        words.append(struct.unpack_from('>I', t, i)[0] ^ key)
    return struct.pack(f'>{len(words)}I', *words)


N, U = 0x6E, 0x75
n_ok = n_skip = 0
for fn in sorted(os.listdir(MODDIR)):
    if not fn.endswith('.cmp'):
        continue
    p = os.path.join(MODDIR, fn)
    ob = open(p, 'rb').read()
    frame = ob[4:]
    raw = zstandard.ZstdDecompressor().decompress(frame, max_output_size=128 << 20)
    font, key = unwrap(raw)
    if not font:
        print(f'  [!] {fn}: khong giai ma duoc'); continue
    f = TTFont(io.BytesIO(font))
    best = None
    for t in f['cmap'].tables:
        if t.isUnicode() and N in t.cmap and U in t.cmap:
            best = t
    if best is None:
        n_skip += 1
        continue
    gn, gu = best.cmap[N], best.cmap[U]
    best.cmap[N], best.cmap[U] = gu, gn           # doi cho
    out = io.BytesIO()
    f.save(out)
    new_font = out.getvalue()
    blob = wrap(new_font, key, len(new_font))
    new_frame = zstandard.ZstdCompressor(
        compression_params=zstandard.ZstdCompressionParameters.from_level(
            15, window_log=frame_params(frame)['window_log'] or 21,
            write_content_size=1, format=zstandard.ZSTD1 if hasattr(zstandard, 'ZSTD1') else zstandard.FORMAT_ZSTD1)
    ).compress(blob)
    open(p, 'wb').write(struct.pack('<I', len(blob)) + new_frame)
    n_ok += 1
print(f'\n  da doi cho n/u trong {n_ok} font | bo qua {n_skip}')
print('  -> chep mod vao Eden va xem: neu chu hien "Bau co muou ket uoi" = FONT MOD DUOC DUNG')
