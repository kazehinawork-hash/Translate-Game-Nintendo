"""So Filter.bin giua cac ngon ngu Kirby: tim bang ky tu / dai ky tu."""
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, 'dump', '01004D300C5AE000', 'romfs', 'msg', 'Kirby15')

for lang in sorted(os.listdir(BASE)):
    p = os.path.join(BASE, lang, 'Filter.bin')
    if not os.path.exists(p):
        continue
    b = open(p, 'rb').read()
    print(f'{lang:<16} {len(b):>7,} b | 24 byte dau: {b[:24].hex(" ")}')

# so chi tiet English vs French
a = open(os.path.join(BASE, 'EU_English', 'Filter.bin'), 'rb').read()
c = open(os.path.join(BASE, 'EU_French', 'Filter.bin'), 'rb').read()
print(f'\nEU_English {len(a):,} b | EU_French {len(c):,} b')
n = min(len(a), len(c))
first = next((i for i in range(n) if a[i] != c[i]), None)
print(f'byte khac dau tien: {first:#x} ({first})' if first is not None else 'giong nhau')
if first is not None:
    print(f'  English quanh do: {a[max(0,first-16):first+32].hex(" ")}')
    print(f'  French  quanh do: {c[max(0,first-16):first+32].hex(" ")}')
# dem so byte khac
print(f'so byte khac nhau: {sum(1 for i in range(n) if a[i] != c[i]):,}/{n:,}')
