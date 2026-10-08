"""So header bundle UnityFS giua file GOC va file trong mod MONOPOLY."""
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = r'E:\MONO_work\data.unity3d'
DST = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01002C201BC40000', 'romfs', 'Data', 'data.unity3d')


def read_cstr(b, off):
    e = b.index(b'\x00', off)
    return b[off:e].decode('utf-8', 'replace'), e + 1


for label, p in (('GOC', SRC), ('MOD', DST)):
    if not os.path.exists(p):
        print(f'{label}: khong co file'); continue
    b = open(p, 'rb').read()
    print(f'\n=== {label}: {p} ({len(b):,} byte) ===')
    sig, off = read_cstr(b, 0)
    ver, = struct.unpack_from('>I', b, off); off += 4
    uver, off = read_cstr(b, off)
    urev, off = read_cstr(b, off)
    size, = struct.unpack_from('>q', b, off); off += 8
    cbis, = struct.unpack_from('>I', b, off); off += 4
    ubis, = struct.unpack_from('>I', b, off); off += 4
    flags, = struct.unpack_from('>I', b, off); off += 4
    print(f'  signature={sig} | version={ver}')
    print(f'  unityVersion={uver!r} | unityRevision={urev!r}')
    print(f'  size(header)={size:,} | dung? {size == len(b)}')
    print(f'  compressedBlocksInfoSize={cbis:,} | uncompressedBlocksInfoSize={ubis:,}')
    print(f'  flags=0x{flags:08x}')
    comp = flags & 0x3F
    print(f'    compressionType={comp} (0=none,1=lzma,2=lz4,3=lz4hc, 0x40=dirinfo-at-end)')
    print(f'    blocksInfoAtEnd={bool(flags & 0x80)} | paddingAtStart={bool(flags & 0x200)}')
    print(f'    header size thuc te = {off} byte')
    # alignment cua vung data dau tien
    print(f'  16 byte sau header: {b[off:off+16].hex(" ")}')
    print(f'  header size chia het 16? {off % 16 == 0} | chia het 4? {off % 4 == 0}')

# block table so sanh
print('\n=== SO SANH BLOCK INFO ===')
for label, p in (('GOC', SRC), ('MOD', DST)):
    b = open(p, 'rb').read()
    off = b.index(b'\x00') + 1
    off += 4
    for _ in range(2):
        off = b.index(b'\x00', off) + 1
    off += 8 + 4 + 4
    flags, = struct.unpack_from('>I', b, off)
    off += 4
    comp = flags & 0x3F
    at_end = bool(flags & 0x80)
    print(f'  {label}: flags=0x{flags:08x} comp={comp} atEnd={at_end}')
