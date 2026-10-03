"""Vá archive .kit Unravel Two tai cho: chi thay record dich, giu nguyen byte con lai.

Quy trinh:
1. Quet record (co dong bo).
2. Voi record can thay: dung file moi = prefix + [u32 len][khoi LZ4 literal] + suffix.
3. Kiem chung: giai ma lai tu record do ve sau; record nao bi lech (do tham chieu
   cheo vao vung vua doi) thi thay luon bang ban goc cua no (nen literal).
"""
import re
import struct
import sys

sys.path.insert(0, r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\tools')
sys.stdout.reconfigure(encoding='utf-8')
from kit_lz4dict import Lz4DictError, decode_block
from kit_repack import HIST_KEEP, lz4_literal_block, scan_records


def build_out(data, start, old_len, new_bytes):
    blk = lz4_literal_block(new_bytes)
    return data[:start] + struct.pack('<I', len(blk)) + blk + data[start + 4 + old_len:]


def apply_changes(data, changes):
    """changes: dict off -> out moi. Dung lai theo thu tu offset giam dan (khong lech)."""
    cur = data
    for off in sorted(changes, reverse=True):
        # tim record tai off trong file hien tai (off khong doi voi cac record TRUOC do)
        recs, _ = scan_records(cur)
        m = [r for r in recs if r[0] == off]
        if not m:
            raise SystemExit(f'khong tim thay record @{off:#x}')
        _, ln, pl, out, kind = m[0]
        cur = build_out(cur, off, ln, changes[off])
    return cur


def decode_all(data):
    recs, gaps = scan_records(data)
    return recs, gaps


if __name__ == '__main__':
    data = open(sys.argv[1], 'rb').read()
    recs, gaps = decode_all(data)
    print(f'{len(recs)} record | {len(gaps)} gap')
    # thu thay 1 record bang chinh no -> phai giai ma y nguyen
    r0 = recs[len(recs) // 2]
    new = build_out(data, r0[0], r0[1], r0[3])
    recs2, gaps2 = decode_all(new)
    same = sum(1 for a, b in zip(recs, recs2) if a[3] == b[3])
    print(f'thay record giua bang chinh no: {len(recs)} -> {len(recs2)} record | giong nhau {same}')
    print('KET QUA:', 'PASS' if len(recs) == len(recs2) and same == len(recs) else f'LECH {len(recs)-same} record')
