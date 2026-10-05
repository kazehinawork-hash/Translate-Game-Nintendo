"""Test vong tron .bfotf Kirby (chay tu tools/)."""
import io
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
import zstandard
from fontTools.ttLib import TTFont

ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
SRC = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'source', 'font', 'ScalableFontBin')
MOD = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01004D300C5AE000', 'romfs', 'font', 'ScalableFontBin')
MAGIC = 0x36F81A1E


def decomp(b):
    return zstandard.ZstdDecompressor().decompress(b[4:], max_output_size=64 << 20)


def try_read(data):
    w0, = struct.unpack_from('>I', data, 0)
    body, = struct.unpack_from('>I', data, 8)
    info = [f'magic={w0:#010x}({w0 == MAGIC})', f'word8={body:#010x}']
    for e, lab in ((0x4F54544F, 'OTTO'), (0x00010000, 'TTF'), (0x74746366, 'ttcf')):
        key = body ^ e
        out = bytearray()
        for i in range(8, len(data), 4):
            w, = struct.unpack_from('>I', data, i)
            out += struct.pack('>I', w ^ key)
        head = bytes(out[:4])
        if head in (b'OTTO', b'\x00\x01\x00\x00', b'ttcf'):
            try:
                t = TTFont(io.BytesIO(bytes(out)), lazy=True)
                return lab, key, f'{lab} OK {len(t.getBestCmap()):,} glyph'
            except Exception as ex:
                return lab, key, f'{lab} DOI TUONG LOI: {type(ex).__name__} {str(ex)[:50]}'
    return None, None, 'khong nhan dang duoc'


for tag, d in (('GOC', SRC), ('MOD', MOD)):
    fn = 'VDL-LogoG-Ultra.bfotf.cmp'
    b = open(os.path.join(d, fn), 'rb').read()
    data = decomp(b)
    lab, key, msg = try_read(data)
    print(f'{tag} {fn}: file {len(b):,} -> decomp {len(data):,}')
    print(f'   -> {msg}')
