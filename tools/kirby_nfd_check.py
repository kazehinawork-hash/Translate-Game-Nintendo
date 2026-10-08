"""KIEM CHUNG gia thuyet NFD: font Kirby (goc va mod) co DẤU TỔ HỢP (U+0300..) khong?

Neu game render NFD: 'ô' = 'o' + U+0302. 'đ' khong tach duoc -> hien binh thuong.
=> khop dung hien tuong trong anh (đ hien, ô/ồ/ạ o vuong).
"""
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

TESTS = {
    'đ U+0111 (khong tach)': 0x0111,
    'Đ U+0110 (khong tach)': 0x0110,
    'ô U+00F4 (tach duoc)': 0x00F4,
    'a U+0061 (co ban)': 0x0061,
    'a+U+0323 (NFD cua ạ)': None,
    'dau sac U+0301': 0x0301,
    'dau huyen U+0300': 0x0300,
    'dau mu U+0302': 0x0302,
    'dau nga U+0303': 0x0303,
    'dau hoi U+0309': 0x0309,
    'dau nga(breve) U+0306': 0x0306,
    'dau moc U+031B': 0x031B,
    'dau nang U+0323': 0x0323,
}


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
            try:
                TTFont(io.BytesIO(body), lazy=True).getBestCmap()
                return body
            except Exception:
                continue
    return None


for label, path in (('GOC  FOT-RodinNTLGPro-B.bfotf', os.path.join(SRC, 'FOT-RodinNTLGPro-B.bfotf.cmp')),
                    ('MOD  FOT-RodinNTLGPro-B.bfotf', os.path.join(OUT, 'FOT-RodinNTLGPro-B.bfotf.cmp')),
                    ('GOC  K15-LocalCharacter-M.bfttf', os.path.join(SRC, 'K15-LocalCharacter-M.bfttf.cmp')),
                    ('MOD  K15-LocalCharacter-M.bfttf', os.path.join(OUT, 'K15-LocalCharacter-M.bfttf.cmp'))):
    fnt = unwrap(open(path, 'rb').read())
    if fnt is None:
        print(f'{label}: khong doc duoc'); continue
    cm = set(TTFont(io.BytesIO(fnt), lazy=True).getBestCmap())
    print(f'\n{label}: {len(cm):,} ky tu')
    for name, cp in TESTS.items():
        if cp is None:
            continue
        print(f'   {name:<28} {"CO" if cp in cm else "KHONG"}')
