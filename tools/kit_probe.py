"""Do tu khoa dac trung trong toan bo record (Unravel Two)."""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import lz4.block

BIG = 32 << 20
PROBES = [b'Coldwood', b'Unravel', b'Electronic Arts', b'localization', b'Localization',
          b'localisation', b'STRING_TABLE', b'StringTable', b'stringtable', b'TEXT_',
          b'text_', b'SUBTITLE', b'Subtitle', b'Dialogue', b'dialogue', b'loc_',
          b'LANG_', b'lang_', b'Fonts/', b'credits', b'Credits']


def lz4_once(pl):
    for size in (1 << 16, 1 << 20, BIG):
        try:
            return lz4.block.decompress(pl, uncompressed_size=size)
        except Exception as e:
            if 'insufficient' in str(e).lower() or 'space' in str(e).lower():
                continue
            return None
    return None


out_dir = r'E:\UNR_work\parts'
hits = {}
for f in sorted(os.listdir(out_dir), key=lambda x: int(x.rsplit('.', 1)[-1])):
    data = open(os.path.join(out_dir, f), 'rb').read()
    n = len(data)
    off = 0
    while off + 4 <= n:
        ln = struct.unpack_from('<I', data, off)[0]
        if not (8 <= ln <= 40_000_000) or off + 4 + ln > n:
            off += 4
            continue
        pl = data[off + 4:off + 4 + ln]
        r = lz4_once(pl)
        buf = r if r else pl
        for k in PROBES:
            if k in buf:
                i = buf.find(k)
                ctx = buf[max(0, i - 45):i + 55].decode('utf-8', 'replace').replace('\r\n', ' ')
                hits.setdefault(k, []).append((f, off, bool(r), ctx))
        off += 4 + ln

for k, lst in hits.items():
    print(f'\n### {k.decode()}  ({len(lst)} record)')
    for f, off, isz, ctx in lst[:3]:
        print(f'   {f} @{off:#x} lz4={isz}: ...{ctx}...')
print('\nkhong thay gi' if not hits else '')
