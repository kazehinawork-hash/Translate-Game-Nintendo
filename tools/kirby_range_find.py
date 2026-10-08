"""Tim dai ky tu ASCII (20 00 00 00 01 00 00 00 7f 00 00 00) trong Filter.bin va trong config."""
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, 'dump', '01004D300C5AE000', 'romfs')

PATS = {
    '20/1/7F (ASCII)': struct.pack('<III', 0x20, 1, 0x7F),
    '20/1/7E': struct.pack('<III', 0x20, 1, 0x7E),
    '00/1/7F': struct.pack('<III', 0, 1, 0x7F),
}

files = [
    ('msg/EU_English/Filter.bin', os.path.join(BASE, 'msg', 'Kirby15', 'EU_English', 'Filter.bin')),
    ('msg/EU_French/Filter.bin', os.path.join(BASE, 'msg', 'Kirby15', 'EU_French', 'Filter.bin')),
    ('msg/JP_Japanese/Filter.bin', os.path.join(BASE, 'msg', 'Kirby15', 'JP_Japanese', 'Filter.bin')),
    ('font/Region/STD/FOT-RodinNTLGPro-B.bin', os.path.join(BASE, 'font', 'Region', 'STD', 'FOT-RodinNTLGPro-B.bin')),
    ('font/Region/STD/FOT-RodinNTLGPro-B-ASCII.bin', os.path.join(BASE, 'font', 'Region', 'STD', 'FOT-RodinNTLGPro-B-ASCII.bin')),
]

for label, p in files:
    if not os.path.exists(p):
        print(f'{label}: khong co'); continue
    b = open(p, 'rb').read()
    print(f'\n=== {label} ({len(b):,} b) ===')
    for name, pat in PATS.items():
        c = b.count(pat)
        if c:
            i = b.find(pat)
            print(f'  {name}: {c} lan | dau tien @{i:#x}')
    # liet ke cac cap u32 tang dan co dang (start, count, end) trong toan file
    hits = []
    for i in range(0, len(b) - 12, 4):
        a, x, y = struct.unpack_from('<III', b, i)
        if 0x20 <= a <= 0x2000 and x in (1, 2) and a < y <= 0xFFFF and y - a < 0x2000:
            hits.append((i, a, x, y))
    print(f'  cac bo (start,?,end) nghi la dai ky tu: {len(hits)}')
    for i, a, x, y in hits[:8]:
        print(f'     @{i:#06x}: {a:#06x} .. {y:#06x}  (x={x})')
