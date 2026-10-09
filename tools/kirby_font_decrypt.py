"""Giai ma font Kirby (.bfotf/.bfttf) -> file TTF/OTF BINH THUONG de sua bang FontForge.

Sau khi sua xong bang FontForge, chay tools/kirby_font_reencrypt.py de dong goi lai.
"""
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import zstandard

TID = '01004D300C5AE000'
SRC = os.path.join(ROOT, 'dump', TID, 'romfs', 'font', 'ScalableFontBin')
OUT = os.path.join(ROOT, 'games', f'{TID}_Kirby', 'font_edit')
MAGIC = 0x36F81A1E
CAND = (0x4F54544F, 0x00010000, 0x74746366)


def unwrap(b):
    d = zstandard.ZstdDecompressor()
    try:
        data = d.decompress(b[4:], max_output_size=256 << 20)
    except zstandard.ZstdError:
        with d.stream_reader(b[4:]) as r:
            data = r.read(256 << 20)
    if struct.unpack_from('>I', data, 0)[0] != MAGIC:
        return None, None
    w8, = struct.unpack_from('>I', data, 8)
    for e in CAND:
        k = w8 ^ e
        body = b''.join(struct.pack('>I', struct.unpack_from('>I', data, i)[0] ^ k)
                        for i in range(8, len(data), 4))
        if body[:4] == struct.pack('>I', e):
            return body, k
    return None, None


os.makedirs(OUT, exist_ok=True)
n = 0
for fn in sorted(os.listdir(SRC)):
    if not fn.endswith('.cmp'):
        continue
    b = open(os.path.join(SRC, fn), 'rb').read()
    body, key = unwrap(b)
    if body is None:
        print(f'  [!] {fn}')
        continue
    # .bfotf -> .otf ; .bfttf -> .ttf
    ext = '.otf' if fn.endswith('.bfotf.cmp') else '.ttf'
    name = fn.replace('.bfotf.cmp', '').replace('.bfttf.cmp', '') + ext
    open(os.path.join(OUT, name), 'wb').write(body)
    # ghi kem key de dong goi lai
    open(os.path.join(OUT, name + '.key'), 'w').write(f'{key:08x}')
    n += 1
print(f'  da giai ma {n} font -> {OUT}')
print('  -> Mo cac file .ttf/.otf nay bang FontForge, dung Element > Merge Fonts')
print('     de gop font co dau tieng Viet, roi File > Generate Fonts.')
print('     Sau do chay: python tools/kirby_font_reencrypt.py')
