"""Suy ra khoa XOR cua .bfotf Kirby roi kiem tra do phu glyph + tieng Viet."""
import io
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
import zstandard
from fontTools.ttLib import TTFont

ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
D = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'source', 'font', 'ScalableFontBin')
MAGIC = 0x36F81A1E


def decomp(b):
    size, = struct.unpack_from('<I', b, 0)
    return zstandard.ZstdDecompressor().decompress(b[4:], max_output_size=64 << 20)


def unwrap(data):
    """[u32 magic][u32 size^key][tung word ^ key]; suy key tu chu ky 'OTTO'/'\\x00\\x01'."""
    if len(data) < 12:
        return None, None, None
    w0, = struct.unpack_from('>I', data, 0)
    if w0 != MAGIC:
        return None, None, w0
    body, = struct.unpack_from('>I', data, 8)
    # thu 2 kha nang: OTTO (CFF) va 0x00010000 (TTF)
    for expect, label in ((0x4F54544F, 'OTTO'), (0x00010000, 'TTF'), (0x74746366, 'ttcf')):
        key = body ^ expect
        out = bytearray()
        for i in range(8, len(data), 4):
            w, = struct.unpack_from('>I', data, i)
            out += struct.pack('>I', w ^ key)
        if bytes(out[:4]) in (b'OTTO', b'\x00\x01\x00\x00', b'ttcf'):
            return bytes(out), key, label
    return None, None, None


VI = 'àáâãèéêìíòóôõùúýăđĩũơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝĂĐĨŨƠƯẠẢ'
print('=== giai ma .bfotf + kiem tra ===')
for fn in sorted(os.listdir(D)):
    if not fn.endswith('.bfotf.cmp'):
        continue
    b = open(os.path.join(D, fn), 'rb').read()
    data = decomp(b)
    ttf, key, label = unwrap(data)
    if not ttf:
        print(f'  {fn[:38]:<40} KHONG giai ma duoc (magic {data[:4].hex()})')
        continue
    try:
        t = TTFont(io.BytesIO(ttf), lazy=True)
        cm = set(t.getBestCmap())
        missvi = [c for c in VI if ord(c) not in cm]
        print(f'  {fn[:38]:<40} {label} {len(cm):>7,} glyph | thieu VI {len(missvi):>2} | '
              f'fullwidth {0xFF10 in cm} | so-vong {0x2460 in cm} | mui ten {0x2192 in cm}')
    except Exception as e:
        print(f'  {fn[:38]:<40} {label} nhung fontTools loi: {type(e).__name__}')
