"""Codec cho archive .kit cua Unravel Two (Coldwood engine).
Record = [u32 compressed_len][LZ4 block] -> JSON.
"""
import struct, sys, json

import lz4.block


def read_records(path, max_records=None):
    """Doc tung record trong file .kit.N, tra ve (offset, compressed_len, json_bytes|None)."""
    data = open(path, 'rb').read()
    out = []
    off = 0
    n = 0
    while off + 4 <= len(data):
        ln = struct.unpack_from('<I', data, off)[0]
        if ln == 0 or off + 4 + ln > len(data):
            break
        payload = data[off + 4:off + 4 + ln]
        raw = None
        for size in (len(payload) * 8, len(payload) * 4, 1 << 20):
            try:
                raw = lz4.block.decompress(payload, uncompressed_size=size)
                break
            except Exception:
                try:
                    raw = lz4.block.decompress(payload)
                    break
                except Exception:
                    continue
        out.append((off, ln, raw))
        off += 4 + ln
        n += 1
        if max_records and n >= max_records:
            break
    return out, off, len(data)


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else r'E:\UNR_work\Data.kit.0'
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    recs, consumed, total = read_records(path, limit or None)
    ok = sum(1 for _, _, r in recs if r)
    print(f'{path}: {len(recs)} record ({ok} giai nen OK) | doc {consumed:,}/{total:,} byte')
    # tim record chua nhan UI
    keys = [b'Options', b'Pause', b'Resume', b'AssistMode', b'SecondPlay', b'Volume']
    for off, ln, raw in recs:
        if not raw:
            continue
        score = sum(1 for k in keys if k in raw)
        if score >= 3:
            print(f'\n>>> record @{off:#x} ({ln} byte nen -> {len(raw)} byte) co {score}/6 nhan UI')
            print(raw[:400].decode('utf-8', 'replace'))
