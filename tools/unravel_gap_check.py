"""Xem vung ngay sau record @0x865b1aa (gap) va cac gap khac co phai padding khong."""
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
G = r'E:\UNR_work\parts\Data.kit.0'
d = open(G, 'rb').read()

off = 0x865b1aa
ln, = struct.unpack_from('<I', d, off)
after = off + 4 + ln
print(f'record @{off:#x}: len={ln:,} -> ket thuc {after:#x}')
print(f'  32 byte sau record: {d[after:after+32].hex(" ")}')
print(f'  co toan so 0 khong? {all(b == 0 for b in d[after:after+32])}')

# thu giai ma record ngay sau do xem no bat dau o dau
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.kit_lz4dict import decode_block, Lz4DictError
hist = b''
o = 0
recs = []
while o + 4 <= len(d):
    l2, = struct.unpack_from('<I', d, o)
    if 4 <= l2 <= 40_000_000 and o + 4 + l2 <= len(d):
        try:
            r = decode_block(d[o + 4:o + 4 + l2], hist[-262140:])
            recs.append((o, l2, len(r)))
            hist += r
            hist = hist[-262140:]
            o += 4 + l2
            continue
        except Lz4DictError:
            pass
    o += 1
print(f'\ntong record giai ma duoc: {len(recs):,}')
# cac gap
gaps = []
prev_end = 0
for roff, rlen, _ in recs:
    if roff > prev_end:
        gaps.append((prev_end, roff - prev_end))
    prev_end = roff + 4 + rlen
if prev_end < len(d):
    gaps.append((prev_end, len(d) - prev_end))
print(f'tong gap: {len(gaps)} | tong byte gap: {sum(g[1] for g in gaps):,}')
for go, gl in gaps[:10]:
    samp = d[go:go + min(gl, 24)]
    print(f'  gap @{go:#x} len={gl:,} | dau: {samp.hex(" ")} | toan 0? {all(b==0 for b in d[go:go+gl])}')
# gap ngay sau record dang xet
for go, gl in gaps:
    if go >= after:
        print(f'\nGAP ngay sau record: @{go:#x} len={gl:,} | toan 0? {all(b==0 for b in d[go:go+gl])}')
        print(f'  dau: {d[go:go+min(gl,32)].hex(" ")}')
        break
