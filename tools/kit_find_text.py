"""Quet ca record nen lan khong nen de tim kho text."""
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import lz4.block

BIG = 32 << 20
KW = [b'Options', b'Pause', b'Resume', b'Restart', b'Checkpoint', b'Trophy',
      b'Collectible', b'Credits', b'Language', b'Subtitle', b'New Game', b'Continue',
      b'Chapter', b'Quit', b'Loading', b'Press', b'Settings', b'Volume']
LANG = [b'English', b'French', b'German', b'Spanish', b'Italian', b'Japanese',
        b'Korean', b'Russian', b'Portuguese', b'Chinese', b'Dutch']


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
for f in sorted(os.listdir(out_dir)):
    data = open(os.path.join(out_dir, f), 'rb').read()
    n = len(data)
    off = 0
    n_rec = n_lz4 = n_raw = 0
    kw_total = {}
    best = (0, None)
    while off + 4 <= n:
        ln = struct.unpack_from('<I', data, off)[0]
        if not (8 <= ln <= 40_000_000) or off + 4 + ln > n:
            off += 4
            continue
        pl = data[off + 4:off + 4 + ln]
        r = lz4_once(pl)
        n_rec += 1
        buf = r if r else pl
        if r:
            n_lz4 += 1
        else:
            n_raw += 1
        c = 0
        for k in KW + LANG:
            if k in buf:
                kw_total[k] = kw_total.get(k, 0) + 1
                c += 1
        if c > best[0]:
            best = (c, (off, ln, bool(r), buf[:0], len(buf)))
            if c >= 5:
                os.makedirs(r'E:\UNR_work\textrec', exist_ok=True)
                open(rf'E:\UNR_work\textrec\{f}_{off:x}.bin', 'wb').write(buf)
        off += 4 + ln
    top = sorted(kw_total.items(), key=lambda x: -x[1])[:6]
    print(f'{f}: {n_rec} rec ({n_lz4} LZ4, {n_raw} raw) | best hits={best[0]} | {[(k.decode(), v) for k, v in top]}', flush=True)
    if best[0] >= 4:
        print(f'   >>> @{best[1][0]:#x} len={best[1][1]:,} lz4={best[1][2]}', flush=True)
