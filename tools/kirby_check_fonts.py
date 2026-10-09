"""Kiem tra nhanh 3 file font trong mod Kirby."""
import io
import json
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import zstandard
from fontTools.ttLib import TTFont

TID = '01004D300C5AE000'
M = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'font', 'ScalableFontBin')
MAGIC = 0x36F81A1E
CAND = (0x4F54544F, 0x00010000, 0x74746366)

vi = json.load(open(os.path.join(ROOT, 'games', f'{TID}_Kirby', 'translations', 'kirby_vi.json'),
                    encoding='utf-8'))
used = set()
for ents in vi.values():
    for v in ents.values():
        used |= set(str(v))
need = {ord(c) for c in used if c.isprintable() and 0x20 <= ord(c) <= 0xFFFF}


def rd(b):
    d = zstandard.ZstdDecompressor()
    try:
        data = d.decompress(b[4:], max_output_size=256 << 20)
    except zstandard.ZstdError:
        with d.stream_reader(b[4:]) as r:
            data = r.read(256 << 20)
    w8, = struct.unpack_from('>I', data, 8)
    for e in CAND:
        k = w8 ^ e
        body = b''.join(struct.pack('>I', struct.unpack_from('>I', data, i)[0] ^ k)
                        for i in range(8, len(data), 4))
        if body[:4] != struct.pack('>I', e):
            continue
        try:
            TTFont(io.BytesIO(body), lazy=True).getBestCmap()
            return body
        except Exception:
            continue
    return None


for fn in ('FOT-RodinNTLGPro-B.bfotf.cmp', 'CHI-FOT-RodinNTLGPro-B.bfttf.cmp',
           'K15-LocalCharacter-M.bfttf.cmp', 'VDL-LogoMaru-Ultra.bfotf.cmp'):
    p = os.path.join(M, fn)
    f = rd(open(p, 'rb').read())
    if f is None:
        print(f'  {fn[:38]:<40} KHONG GIAI MA DUOC')
        continue
    t = TTFont(io.BytesIO(f), lazy=True)
    cm = set(t.getBestCmap())
    miss = sorted(c for c in need if c not in cm)
    print(f'  {fn[:38]:<40} {len(cm):>5} ky tu | thieu {len(miss):>2} '
          f'| "o"={0x00F4 in cm} "a."={0x1EA1 in cm} "o."={0x1EDB in cm} '
          f'| {t["name"].getDebugName(4)}')
