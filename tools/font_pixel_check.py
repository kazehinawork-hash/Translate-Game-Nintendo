"""Kiem chung kieu PIXEL: ky tu co dau co bi ve thanh O VUONG khong?

So anh render cua mot ky tu voi anh render cua ky tu chac chan KHONG CO trong font (PUA).
Neu giong nhau -> dang ve .notdef (o vuong).
"""
import io
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

TID = '01004D300C5AE000'
MAGIC = 0x36F81A1E
CAND = (0x4F54544F, 0x00010000, 0x74746366)


def unwrap(b):
    import zstandard
    if len(b) > 8 and b[4:8] == b'\x28\xb5\x2f\xfd':
        b = zstandard.ZstdDecompressor().decompress(b[4:], max_output_size=128 << 20)
    if struct.unpack_from('>I', b, 0)[0] != MAGIC:
        return None
    w8, = struct.unpack_from('>I', b, 8)
    for expect in CAND:
        key = w8 ^ expect
        body = b''.join(struct.pack('>I', struct.unpack_from('>I', b, i)[0] ^ key)
                        for i in range(8, len(b), 4))
        if body[:4] == struct.pack('>I', expect):
            try:
                TTFont(io.BytesIO(body), lazy=True).getBestCmap()
                return body
            except Exception:
                continue
    return None


def sig(path, ch, size=64):
    im = Image.new('L', (100, 110), 255)
    ImageDraw.Draw(im).text((10, 10), ch, font=ImageFont.truetype(path, size), fill=0)
    return im


def ink(im):
    px = im.load()
    return [(x, y) for y in range(im.height) for x in range(im.width) if px[x, y] < 128]


OUT = os.path.join(ROOT, 'games', '_consistency')
os.makedirs(OUT, exist_ok=True)

MFILE = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'font', 'ScalableFontBin',
                     'FOT-RodinNTLGPro-B.bfotf.cmp')
p_mod = os.path.join(OUT, 't_mod.otf')
open(p_mod, 'wb').write(unwrap(open(MFILE, 'rb').read()))

for label, path in (('MOD (dung lai)', p_mod), ('ARIAL', r'C:\Windows\Fonts\ARIALUNI.TTF')):
    a = sig(path, 'ạ')
    b = sig(path, '\ue123')          # PUA chac chan khong co -> .notdef (o vuong)
    c = sig(path, 'a')
    ia, ib, ic = set(ink(a)), set(ink(b)), set(ink(c))
    print(f'\n{label}:')
    print(f'  ink "ạ"={len(ia)} | ink "a"={len(ic)} | ink PUA(.notdef)={len(ib)}')
    print(f'  "ạ" == .notdef ?  {"YES -> O VUONG" if ia == ib else "khong"}')
    print(f'  "ạ" == "a"      ?  {"YES -> bi mat dau" if ia == ic else "khong"}')
    a.save(os.path.join(OUT, f'px_{label.split()[0]}_a.png'))
    b.save(os.path.join(OUT, f'px_{label.split()[0]}_box.png'))
