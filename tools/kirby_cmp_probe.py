"""Do cach doc/ghi file .cmp cua Kirby: thu nhieu API zstd khac nhau."""
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import zstandard

P = os.path.join(ROOT, 'dump', '01004D300C5AE000', 'romfs', 'font', 'ScalableFontBin',
                 'CHI-FOT-RodinNTLGPro-B.bfttf.cmp')
b = open(P, 'rb').read()
print(f'file {len(b):,} b')
print(f'  4 byte dau (u32): {struct.unpack_from("<I", b, 0)[0]:,}')
print(f'  12 byte dau     : {b[:12].hex(" ")}')
print(f'  frame bat dau @4: {b[4:12].hex(" ")}')
try:
    print(f'  frame_content_size = {zstandard.frame_content_size(b[4:]):,}')
except Exception as e:
    print(f'  frame_content_size loi: {type(e).__name__}: {e}')

tests = {
    'decompress(max_output_size)': lambda: zstandard.ZstdDecompressor().decompress(
        b[4:], max_output_size=256 << 20),
    'decompressobj': lambda: zstandard.ZstdDecompressor().decompressobj().decompress(b[4:]),
    'stream_reader': lambda: zstandard.ZstdDecompressor().stream_reader(b[4:]).read(256 << 20),
    'frame_content_size + decompress': None,
    'bo 4 byte dau (b[8:])': lambda: zstandard.ZstdDecompressor().decompress(
        b[8:], max_output_size=256 << 20),
}
for name, fn in tests.items():
    if fn is None:
        continue
    try:
        d = fn()
        print(f'  {name:<34} OK -> {len(d):,} b')
    except Exception as e:
        print(f'  {name:<34} LOI {type(e).__name__}: {str(e)[:60]}')
