"""Nen/dong goi archive .kit Unravel Two.

Chien luoc:
- record = [u32 len][khoi LZ4 (co the dung tu dien = du lieu truoc do)]
- Giu NGUYEN byte nen cua record khong sua (nhanh + an toan).
- Record sua/them: nen bang khoi literal (hop le voi LZ4, khong dung match).
- Sau khi dung lai: GIAI MA LAI toan bo va doi chieu voi ban goc -> phat hien
  record bi anh huong do tham chieu cheo, nen lai bang literal.
"""
import struct
import sys

sys.path.insert(0, r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\tools')
sys.stdout.reconfigure(encoding='utf-8')
from kit_lz4dict import Lz4DictError, decode_block

HIST_KEEP = 262140


def lz4_literal_block(data):
    """Khoi LZ4 hop le chi gom literal (khong match)."""
    out = bytearray()
    n = len(data)
    if n < 15:
        out.append(n << 4)
    else:
        out.append(0xF0)
        rem = n - 15
        while rem >= 255:
            out.append(255)
            rem -= 255
        out.append(rem)
    out += data
    return bytes(out)


def scan_records(data):
    """Tra ve (recs, gaps). gaps = cac byte khong thuoc record nao (giu nguyen khi dung lai)."""
    off = 0
    hist = b''
    recs = []
    gaps = []
    n = len(data)
    while off + 4 <= n:
        ln = struct.unpack_from('<I', data, off)[0]
        good = 4 <= ln <= 40_000_000 and off + 4 + ln <= n
        out = kind = None
        if good:
            pl = data[off + 4:off + 4 + ln]
            try:
                out = decode_block(pl, hist[-HIST_KEEP:])
                kind = 'lz4'
            except Lz4DictError:
                s = pl.lstrip()[:1]
                if s in (b'{', b'['):
                    out = pl
                    kind = 'raw'
        if kind is None:
            # dong bo lai: tim record ke tiep trong 64 KB, giu byte bo qua lam gap
            found = False
            for d in range(1, 65536):
                if off + d + 4 > n:
                    break
                ln2 = struct.unpack_from('<I', data, off + d)[0]
                if not (4 <= ln2 <= 40_000_000) or off + d + 4 + ln2 > n:
                    continue
                pl2 = data[off + d + 4:off + d + 4 + ln2]
                try:
                    o2 = decode_block(pl2, hist[-HIST_KEEP:])
                    k2 = 'lz4'
                except Lz4DictError:
                    s2 = pl2.lstrip()[:1]
                    if s2 not in (b'{', b'['):
                        continue
                    o2, k2 = pl2, 'raw'
                gaps.append((off, data[off:off + d]))
                off += d
                recs.append((off, ln2, pl2, o2, k2))
                hist = (hist + o2)[-HIST_KEEP:]
                off += 4 + ln2
                found = True
                break
            if not found:
                gaps.append((off, data[off:]))
                off = n
            continue
        recs.append((off, ln, data[off + 4:off + 4 + ln], out, kind))
        hist = (hist + out)[-HIST_KEEP:]
        off += 4 + ln
    return recs, gaps


def rebuild(data, replace_fn):
    """replace_fn(out_bytes, off) -> out_bytes moi (hoac None neu giu nguyen)."""
    recs, gaps = scan_records(data)
    new_out = {}
    for off, ln, pl, out, kind in recs:
        r = replace_fn(out, off)
        if r is not None and r != out:
            new_out[off] = r
    out_buf = bytearray()
    hist = b''
    changed = 0
    gap_map = dict(gaps)
    for off, ln, pl, out, kind in recs:
        if off in gap_map:
            out_buf += gap_map[off]
        cur = new_out.get(off, out)
        if off in new_out:
            blk = lz4_literal_block(cur)
            changed += 1
        else:
            blk = pl
        out_buf += struct.pack('<I', len(blk))
        out_buf += blk
        hist = (hist + cur)[-HIST_KEEP:]
    # mo cuoi (neu co)
    end_gap = [o for o, _ in gaps if o >= (recs[-1][0] if recs else 0)]
    for o in sorted(end_gap):
        if o > (recs[-1][0] if recs else 0):
            out_buf += gap_map[o]
    return bytes(out_buf), changed, recs, gaps


def verify(newdata, recs, gaps):
    off = 0
    hist = b''
    diffs = []
    i = 0
    gap_map = dict(gaps)
    while i < len(recs):
        r_off, r_len, r_pl, r_out, r_kind = recs[i]
        if r_off in gap_map:
            off += len(gap_map[r_off])
        ln = struct.unpack_from('<I', newdata, off)[0]
        if not (4 <= ln <= 40_000_000) or off + 4 + ln > len(newdata):
            return (None, [('DESYNC', off)])
        pl = newdata[off + 4:off + 4 + ln]
        try:
            out = decode_block(pl, hist[-HIST_KEEP:])
        except Lz4DictError as e:
            return (None, [('DECODE_LOI', off, str(e))])
        if out != r_out:
            diffs.append((r_off, len(r_out), len(out)))
        hist = (hist + out)[-HIST_KEEP:]
        off += 4 + ln
        i += 1
    return (off, i), diffs


if __name__ == '__main__':
    path = sys.argv[1]
    data = open(path, 'rb').read()
    recs, gaps = scan_records(data)
    print(f'{len(recs)} record | {len(gaps)} khoang trong (byte giu nguyen)')
    new, changed, recs, gaps = rebuild(data, lambda o, f: None)
    print(f'dung lai (khong doi gi): {len(data):,} -> {len(new):,} byte | doi {changed} record')
    known, diffs = verify(new, recs, gaps)
    print('xac minh:', known, '| lech:', diffs[:5])
    print('KET QUA:', 'PASS' if known and not diffs else 'CO VAN DE')
