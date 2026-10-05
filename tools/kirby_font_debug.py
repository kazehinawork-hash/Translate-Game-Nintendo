"""Mo truc tiep file font mod de xem hong o dau."""
import io
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
import zstandard
from fontTools.ttLib import TTFont

ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
MOD = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01004D300C5AE000', 'romfs', 'font', 'ScalableFontBin')
SRC = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'source', 'font', 'ScalableFontBin')
FN = 'VDL-LogoG-Ultra.bfotf.cmp'


def decomp(b):
    return zstandard.ZstdDecompressor().decompress(b[4:], max_output_size=64 << 20)


for tag, d in (('GOC', SRC), ('MOD', MOD)):
    data = decomp(open(os.path.join(d, FN), 'rb').read())
    w0, w4, w8 = struct.unpack_from('>III', data, 0)
    print(f'\n=== {tag} ===')
    print(f'  len={len(data):,} | w0={w0:#010x} w4={w4:#010x} w8={w8:#010x}')
    print(f'  raw 16 byte dau: {data[:16].hex(" ")}')
    key = w8 ^ 0x4F54544F
    print(f'  key (gia thuyet OTTO) = {key:#010x}')
    out = bytearray()
    for i in range(8, len(data), 4):
        w, = struct.unpack_from('>I', data, i)
        out += struct.pack('>I', w ^ key)
    print(f'  giai ma 16 byte dau font: {bytes(out[:16]).hex(" ")}')
    try:
        t = TTFont(io.BytesIO(bytes(out)), lazy=True)
        print(f'  -> doc OK: {len(t.getBestCmap()):,} glyph | bang: {sorted(t.keys())[:10]}')
    except Exception as e:
        print(f'  -> loi: {type(e).__name__} {str(e)[:70]}')
        # thu doc header sfnt thu cong
        try:
            ntab, = struct.unpack_from('>H', out, 4)
            print(f'     so bang trong header: {ntab} (neu vo ly => du lieu lech)')
        except Exception:
            pass
