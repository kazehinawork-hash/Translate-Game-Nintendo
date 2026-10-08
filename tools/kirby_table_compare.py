"""So cau truc BANG giua font .bfttf GOC va font da va (tim ly do game tu choi)."""
import io
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import zstandard
from fontTools.ttLib import TTFont

TID = '01004D300C5AE000'
G = os.path.join(ROOT, 'games', f'{TID}_Kirby')
SRC = os.path.join(G, 'source', 'font', 'ScalableFontBin')
OUT = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'font', 'ScalableFontBin')
MAGIC = 0x36F81A1E
CAND = (0x4F54544F, 0x00010000, 0x74746366)


def unwrap(b):
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
            return body
    return None


for fn in ('TWN-FOT-RodinNTLGPro-B.bfttf.cmp', 'FOT-RodinNTLGPro-B.bfotf.cmp'):
    print(f'\n===== {fn} =====')
    for label, d in (('GOC', SRC), ('MOD', OUT)):
        p = os.path.join(d, fn)
        fnt = unwrap(open(p, 'rb').read())
        f = TTFont(io.BytesIO(fnt))
        tabs = sorted(f.keys())
        num = f['maxp'].numGlyphs
        go = f.getGlyphOrder()
        print(f'  {label}: {len(fnt):,} b | glyph={num:,} | order={len(go):,}')
        print(f'        bang: {tabs}')
        if 'post' in f:
            post = f['post']
            print(f'        post format={post.formatType}')
        else:
            print('        post: KHONG CO')
        print(f'        head flags=0x{f["head"].flags:04x}')
        print(f'        hmtx={len(f["hmtx"].metrics):,}')
        print(f'        cmap: {[(t.platformID, t.platEncID, t.format) for t in f["cmap"].tables]}')
