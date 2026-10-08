"""So bang BLOCK (blocksInfo) giua bundle goc va bundle mod cua MONOPOLY."""
import lz4.block
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = r'E:\MONO_work\data.unity3d'
DST = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01002C201BC40000', 'romfs', 'Data', 'data.unity3d')


def header(b):
    off = b.index(b'\x00') + 1
    off += 4
    off = b.index(b'\x00', off) + 1
    off = b.index(b'\x00', off) + 1
    size, = struct.unpack_from('>q', b, off); off += 8
    cbis, = struct.unpack_from('>I', b, off); off += 4
    ubis, = struct.unpack_from('>I', b, off); off += 4
    flags, = struct.unpack_from('>I', b, off); off += 4
    return off, size, cbis, ubis, flags


def blocks_info(b):
    off, size, cbis, ubis, flags = header(b)
    comp = flags & 0x3F
    info = b[off:off + cbis]
    if comp == 2 or comp == 3:
        raw = lz4.block.decompress(info, uncompressed_size=ubis)
    elif comp == 1:
        raw = info
    else:
        raw = info
    # hash(16) + blockCount(4) + blocks[16 each] + nodeCount(4) + nodes
    p = 16
    nblk, = struct.unpack_from('>I', raw, p); p += 4
    blocks = []
    for _ in range(nblk):
        u, c, f = struct.unpack_from('>IIH', raw, p); p += 10
        blocks.append((u, c, f))
    return nblk, blocks, raw, off, cbis


for label, p in (('GOC', SRC), ('MOD', DST)):
    b = open(p, 'rb').read()
    nblk, blocks, raw, off, cbis = blocks_info(b)
    print(f'\n=== {label} ({len(b):,} b) ===')
    print(f'  header {off} b | blocksInfo nen {cbis:,} -> raw {len(raw):,} | so block du lieu: {nblk}')
    print(f'  5 block dau: {blocks[:5]}')
    print(f'  5 block cuoi: {blocks[-5:]}')
    tot_u = sum(x[0] for x in blocks)
    tot_c = sum(x[1] for x in blocks)
    print(f'  tong uncompressed {tot_u:,} | tong compressed {tot_c:,}')
    al = set(x[1] % 16 for x in blocks)
    print(f'  compressed-size mod 16: {sorted(al)}')
