"""Xac minh doc lap: font trong mod Kirby da la Nunito + du dau tieng Viet chua."""
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
        if body[:4] == struct.pack('>I', e):
            return body
    return None


n_ok = n_bad = 0
worst = None
for fn in sorted(os.listdir(M)):
    if not fn.endswith('.cmp'):
        continue
    f = rd(open(os.path.join(M, fn), 'rb').read())
    if f is None:
        print(f'  [!] {fn}: khong giai ma duoc'); n_bad += 1; continue
    t = TTFont(io.BytesIO(f), lazy=True)
    cm = set(t.getBestCmap())
    miss = [c for c in need if c not in cm]
    name = t['name'].getDebugName(4) or '?'
    if miss:
        n_bad += 1
        if worst is None or len(miss) < worst[1]:
            worst = (fn, len(miss), ''.join(chr(c) for c in miss[:12]))
    else:
        n_ok += 1
    if n_ok + n_bad <= 3 or miss:
        print(f'  {fn[:38]:<40} {len(cm):>5} ky tu | thieu {len(miss):>3} | {name}')

print(f'\n  {n_ok} font DU dau tieng Viet | {n_bad} font con thieu')
if worst:
    print(f'  thieu it nhat: {worst[0]} ({worst[1]}): {worst[2]}')
