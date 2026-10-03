"""Boc archive .kit Unravel Two: LZ4 CO TU DIEN + record raw JSON.

- record = [u32 len][payload]
- payload: LZ4 block (tu dien = du lieu da giai ma truoc do, toi da 64 KB) HOAC JSON tho
- tu dong dong bo lai khi gap record le
"""
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

from kit_lz4dict import Lz4DictError, decode_block


def looks_json(b):
    s = b.lstrip()[:1]
    return s in (b'{', b'[') and b'"' in b[:200]


def try_record(data, off, hist):
    """Tra ve (len, out, kind) hoac None."""
    if off + 4 > len(data):
        return None
    ln = struct.unpack_from('<I', data, off)[0]
    if not (4 <= ln <= 40_000_000) or off + 4 + ln > len(data):
        return None
    pl = data[off + 4:off + 4 + ln]
    try:
        out = decode_block(pl, hist[-65535:])
        return (ln, out, 'lz4')
    except Lz4DictError:
        pass
    if looks_json(pl):
        return (ln, pl, 'raw')
    return None


def scan(path, stop_marker=None):
    data = open(path, 'rb').read()
    off = 0
    hist = b''
    recs = []
    resync = 0
    found = None
    while off + 4 <= len(data):
        got = try_record(data, off, hist)
        if not got:
            done = False
            for d in range(1, 64):
                g2 = try_record(data, off + d, hist)
                if g2:
                    off += d
                    resync += 1
                    got = g2
                    done = True
                    break
            if not done:
                off += 64
                continue
        ln, out, kind = got
        recs.append((off, ln, kind, len(out)))
        if stop_marker and stop_marker in out:
            found = (off, out)
        hist = (hist + out)[-131070:]
        off += 4 + ln
        if found:
            break
    return recs, resync, len(data), found


if __name__ == '__main__':
    path = sys.argv[1]
    marker = sys.argv[2].encode() if len(sys.argv) > 2 else b'Coldwood'
    recs, resync, size, found = scan(path, marker)
    n_lz4 = sum(1 for r in recs if r[2] == 'lz4')
    print(f'{os.path.basename(path)}: {len(recs)} record ({n_lz4} LZ4, {len(recs)-n_lz4} raw) | resync {resync}')
    if found:
        off, out = found
        print(f'\n>>> TIM THAY "{marker.decode()}" trong record @{off:#x} ({len(out):,} byte)')
        p = rf'E:\UNR_work\textrec\localization_{off:x}.json'
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'wb').write(out)
        print('   da luu:', p)
        s = out.decode('utf-8', 'replace')
        i = s.find(marker.decode())
        print('   quanh dau vet:')
        print('   ...' + s[max(0, i - 400):i + 500].replace('\r\n', '\n      ') + '...')
    else:
        print('khong thay marker')
