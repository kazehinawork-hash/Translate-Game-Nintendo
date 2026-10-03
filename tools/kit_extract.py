"""Boc record tu archive .kit cua Unravel Two.

Dinh dang: [u32 compressed_len][khoi LZ4] -> JSON   (mot so record khong nen)
"""
import os
import re
import struct
import sys

import lz4.block

BIG = 32 << 20  # tran giai nen


def lz4_once(pl):
    """Thu vai muc kich thuoc tang dan; chi nang cap khi loi 'thieu cho'."""
    for size in (1 << 16, 1 << 20, BIG):
        try:
            return lz4.block.decompress(pl, uncompressed_size=size)
        except Exception as e:
            if 'insufficient' in str(e).lower() or 'space' in str(e).lower():
                continue
            return None
    return None


def scan(path):
    data = open(path, 'rb').read()
    n = len(data)
    recs = []
    off = 0
    resync = 0
    while off + 4 <= n:
        ln = struct.unpack_from('<I', data, off)[0]
        ok = 8 <= ln <= 40_000_000 and off + 4 + ln <= n
        if ok:
            r = lz4_once(data[off + 4:off + 4 + ln])
            recs.append((off, ln, r))
            off += 4 + ln
            continue
        # dong bo lai: quet 4 byte mot, toi 4 KB
        done = False
        for d in range(4, 4096, 4):
            if off + d + 4 > n:
                break
            ln2 = struct.unpack_from('<I', data, off + d)[0]
            if 8 <= ln2 <= 40_000_000 and off + d + 4 + ln2 <= n:
                r2 = lz4_once(data[off + d + 4:off + d + 4 + ln2])
                if r2:
                    off += d
                    resync += 1
                    done = True
                    break
        if not done:
            off += 4
    return recs, resync, n


if __name__ == '__main__':
    path = sys.argv[1]
    recs, resync, n = scan(path)
    good = [r for r in recs if r[2]]
    print(f'{os.path.basename(path)}: {len(recs)} record | LZ4 OK {len(good)} | resync {resync} | doc {n:,} byte')

    # tim record giau van ban hien thi
    pat = re.compile(rb"[A-Z][a-z']{2,}(?:[ ][A-Za-z']{2,}){2,}[.!?]")
    cands = []
    for off, ln, r in good:
        if not r:
            continue
        sents = pat.findall(r)
        if len(sents) >= 3:
            cands.append((len(sents), off, ln, len(r), sents[:3]))
    cands.sort(reverse=True)
    print(f'\nrecord giau van ban: {len(cands)}')
    for n_s, off, ln, rl, ex in cands[:8]:
        print(f'  @{off:#x} nen={ln:,} -> {rl:,} byte | {n_s} cau | {ex}')
    if cands:
        n_s, off, ln, rl, ex = cands[0]
        out = r'E:\UNR_work\textrec'
        os.makedirs(out, exist_ok=True)
        r = dict((o, rr) for o, l, rr in good)[off]
        open(os.path.join(out, f'{off:x}.json'), 'wb').write(r)
        print(f'\n--- record @{off:#x} (da luu) ---')
        print(r[:900].decode('utf-8', 'replace'))
