"""Kiem chung pixel cho cac font .bfttf vua va: ky tu co dau phai render THAT (khac .notdef)."""
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

TID = '01004D300C5AE000'
OUTDIR = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'font', 'ScalableFontBin')
MAGIC = 0x36F81A1E
CAND = (0x4F54544F, 0x00010000, 0x74746366)
OUT = os.path.join(ROOT, 'games', '_consistency')


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
                TTFont(__import__('io').BytesIO(body), lazy=True).getBestCmap()
                return body
            except Exception:
                continue
    return None


def ink(path, ch, size=64):
    im = Image.new('L', (110, 120), 255)
    ImageDraw.Draw(im).text((10, 10), ch, font=ImageFont.truetype(path, size), fill=0)
    px = im.load()
    return {(x, y) for y in range(im.height) for x in range(im.width) if px[x, y] < 128}


FILES = ['K15-LocalCharacter-M.bfttf.cmp', 'TWN-FOT-RodinNTLGPro-B.bfttf.cmp',
         'KOR-VDL-LogoG-Ultra.bfttf.cmp', 'CHI-FOT-RodinNTLGPro-B.bfttf.cmp']
print(f'{"file":<40}{"ink ạ":>8}{"ink a":>8}{"ink .notdef":>12}  ket luan')
allok = True
for fn in FILES:
    p = os.path.join(OUTDIR, fn)
    if not os.path.exists(p):
        print(f'{fn:<40} (khong co trong mod)'); allok = False; continue
    body = unwrap(open(p, 'rb').read())
    if body is None:
        print(f'{fn:<40} khong unwrap duoc'); allok = False; continue
    tmp = os.path.join(OUT, 'chk.ttf')
    open(tmp, 'wb').write(body)
    ia, ic, ib = ink(tmp, 'ạ'), ink(tmp, 'a'), ink(tmp, '\ue123')
    ok = (ia and ia != ib and ia != ic)
    allok &= bool(ok)
    print(f'{fn:<40}{len(ia):>8}{len(ic):>8}{len(ib):>12}  {"OK - ve dung" if ok else "LOI"}')
print('\nKET QUA:', 'PASS - cac font deu ve duoc dau tieng Viet' if allok else 'CO VAN DE')
