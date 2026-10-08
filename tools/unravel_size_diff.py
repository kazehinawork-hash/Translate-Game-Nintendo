"""Tim vi tri dau tien 2 file Data.kit.0 khac nhau + liet ke cac record bi doi."""
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = r'E:\UNR_work\parts\Data.kit.0'
M = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '0100E5D00CC0C000', 'romfs', 'NVNKits', 'Data.kit.0')

g = open(G, 'rb').read()
m = open(M, 'rb').read()
print(f'goc {len(g):,} | mod {len(m):,} | lech {len(m)-len(g):+,}')

# byte khac dau tien
n = min(len(g), len(m))
first = next((i for i in range(n) if g[i] != m[i]), None)
print(f'byte khac dau tien: {first:,} ({first:#x})' if first is not None else 'khong khac trong phan chung')
if first is not None:
    print(f'  ^ ti le {first/len(g)*100:.2f}% cua file')

# liet ke record thay doi (theo offset)
def rec_offsets(data):
    off = 0
    out = []
    while off + 4 <= len(data):
        ln, = struct.unpack_from('<I', data, off)
        if not (4 <= ln <= 40_000_000) or off + 4 + ln > len(data):
            break
        out.append((off, ln))
        off += 4 + ln
    return out, off


rg, endg = rec_offsets(g)
rm, endm = rec_offsets(m)
print(f'\nrecord: goc {len(rg):,} (doc het {endg:,}/{len(g):,}) | mod {len(rm):,} (doc het {endm:,}/{len(m):,})')

# so record giong nhau cho toi khi lech
k = 0
while k < min(len(rg), len(rm)) and rg[k][1] == rm[k][1]:
    k += 1
print(f'so record dau GIONG kich thuoc: {k}')
if k < min(len(rg), len(rm)):
    print(f'  record lech dau tien #{k}: goc off={rg[k][0]:,} len={rg[k][1]:,} | mod off={rm[k][0]:,} len={rm[k][1]:,}')
# liet ke tat ca record lech kich thuoc
diff = [(i, rg[i][1], rm[i][1]) for i in range(min(len(rg), len(rm))) if rg[i][1] != rm[i][1]]
print(f'so record LECH KICH THUOC: {len(diff)}')
for i, a, b in diff[:12]:
    print(f'  #{i}: {a:,} -> {b:,} ({b-a:+,})')
# co record nao chua tieng Viet khong
print(f'\nrecord cuoi cung: goc off={rg[-1][0]:,} len={rg[-1][1]:,} ket thuc {rg[-1][0]+4+rg[-1][1]:,}')
print(f'                  mod off={rm[-1][0]:,} len={rm[-1][1]:,} ket thuc {rm[-1][0]+4+rm[-1][1]:,}')
