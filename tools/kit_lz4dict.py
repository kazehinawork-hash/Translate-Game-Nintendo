"""Giai ma LZ4 block CO TU DIEN (dictionary / solid archive) cho archive .kit Unravel Two.

LZ4 block chuan:
  loop:
    token = byte; lit = token>>4; match = token&15
    lit == 15  -> cong don cac byte 0xFF tiep theo
    copy lit byte literal
    neu het input -> ket thuc
    offset = 2 byte little-endian
    match == 15 -> cong don cac byte 0xFF tiep theo
    match += 4
    copy match byte tu (vi tri hien tai - offset)  <-- co the nam trong TU DIEN
"""
import struct
import sys


class Lz4DictError(Exception):
    pass


def decode_block(src, dict_bytes=b''):
    out = bytearray()
    hist = bytes(dict_bytes)
    i = 0
    n = len(src)
    while i < n:
        token = src[i]
        i += 1
        lit = token >> 4
        if lit == 15:
            while True:
                if i >= n:
                    raise Lz4DictError('het input khi doc lit_len')
                b = src[i]
                i += 1
                lit += b
                if b != 255:
                    break
        if lit:
            if i + lit > n:
                raise Lz4DictError('literal vuot input')
            out += src[i:i + lit]
            i += lit
        if i >= n:
            break  # sequence cuoi
        if i + 2 > n:
            raise Lz4DictError('thieu offset')
        offset = src[i] | (src[i + 1] << 8)
        i += 2
        if offset == 0:
            raise Lz4DictError('offset = 0')
        ml = token & 15
        if ml == 15:
            while True:
                if i >= n:
                    raise Lz4DictError('het input khi doc match_len')
                b = src[i]
                i += 1
                ml += b
                if b != 255:
                    break
        ml += 4
        total = len(hist) + len(out)
        pos = total - offset
        if pos < 0:
            raise Lz4DictError('offset vuot ca tu dien')
        for k in range(ml):
            idx = pos + k
            if idx < len(hist):
                out.append(hist[idx])
            else:
                out.append(out[idx - len(hist)])
    return bytes(out)


if __name__ == '__main__':
    path = sys.argv[1]
    start = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0
    stop_at = int(sys.argv[3], 0) if len(sys.argv) > 3 else None
    data = open(path, 'rb').read()
    off = start
    hist = b''
    n_ok = n_bad = 0
    while off + 4 <= len(data):
        ln = struct.unpack_from('<I', data, off)[0]
        if not (8 <= ln <= 40_000_000) or off + 4 + ln > len(data):
            break
        pl = data[off + 4:off + 4 + ln]
        try:
            r = decode_block(pl, hist[-65535:])
            n_ok += 1
            hist += r
            hist = hist[-65535 * 2:]
            if stop_at and off >= stop_at:
                print(f'--- record @{off:#x} len={ln:,} -> {len(r):,} byte ---')
                print(r[:700].decode('utf-8', 'replace'))
                break
        except Lz4DictError as e:
            n_bad += 1
            if n_bad <= 3:
                print(f'  loi @{off:#x} len={ln:,}: {e}')
        off += 4 + ln
    print(f'\nket qua tu {start:#x}: {n_ok} record OK | {n_bad} loi | doc den {off:,}/{len(data):,}')
