"""Encoder LZ4 block CO TU DIEN (khop voi kit_lz4dict.decode_block).

Nen bang literal + match tren cua so 64 KB (gom ca du lieu da giai nen truoc do).
Muc dich: record bi sua KHONG phinh to -> giu nguyen kich thuoc file .kit.
"""
import struct
import sys

HASHLOG = 16
MINMATCH = 4
MAX_OFF = 65535
MAX_CHAIN = 512         # so ung vien toi da xet cho moi vi tri (cang cao cang nho file)


def _h4(buf, p):
    v = buf[p] | (buf[p + 1] << 8) | (buf[p + 2] << 16) | (buf[p + 3] << 24)
    return ((v * 2654435761) & 0xFFFFFFFF) >> (32 - HASHLOG)


def _emit_lit(out, tpos, lit):
    if lit >= 15:
        out[tpos] |= 0xF0
        l = lit - 15
        while l >= 255:
            out.append(255)
            l -= 255
        out.append(l)
    else:
        out[tpos] |= (lit << 4)


def _emit_match(out, tpos, m):
    if m >= 15:
        out[tpos] |= 0x0F
        mm = m - 15
        while mm >= 255:
            out.append(255)
            mm -= 255
        out.append(mm)
    else:
        out[tpos] |= m


def encode_block(data, hist=b''):
    """-> khoi LZ4 giai ma duoc bang decode_block(khoi, hist)."""
    data = bytes(data)
    hist = bytes(hist)[-MAX_OFF:]
    buf = hist + data
    n_hist = len(hist)
    n = len(data)
    out = bytearray()
    if n == 0:
        return bytes(out)

    head = {}
    prev = {}

    def insert(p):
        h = _h4(buf, p)
        prev[p] = head.get(h, -1)
        head[h] = p

    for p in range(0, max(0, n_hist - MINMATCH + 1)):
        insert(p)

    def best_match(gp, max_len):
        """Tra ve (cand, length) tot nhat trong MAX_CHAIN ung vien."""
        h = _h4(buf, gp)
        cand = head.get(h, -1)
        best_c = -1
        best_l = 0
        tries = 0
        while cand >= 0 and gp - cand <= MAX_OFF and tries < MAX_CHAIN:
            tries += 1
            if buf[cand + best_l] == buf[gp + best_l]:
                l = 0
                while l < max_len and buf[cand + l] == buf[gp + l]:
                    l += 1
                if l > best_l:
                    best_l = l
                    best_c = cand
                    if l >= max_len:
                        break
            cand = prev.get(cand, -1)
        return best_c, best_l

    anchor = 0
    i = 0
    while i + MINMATCH <= n:
        gp = n_hist + i
        max_len = n - i
        cand, l = best_match(gp, max_len)
        insert(gp)
        if l < MINMATCH:
            i += 1
            continue
        # lazy: thu vi tri ke tiep xem co match dai hon khong
        if i + 1 + MINMATCH <= n:
            gp2 = n_hist + i + 1
            c2, l2 = best_match(gp2, n - i - 1)
            if l2 > l + 1:
                i += 1
                continue
        lit = i - anchor
        tpos = len(out)
        out.append(0)
        _emit_lit(out, tpos, lit)
        out += data[anchor:anchor + lit]
        off = gp - cand
        out.append(off & 0xFF)
        out.append((off >> 8) & 0xFF)
        _emit_match(out, tpos, l - MINMATCH)
        # nap cac vi tri trong doan match vao bang bam
        end = i + l
        j = i + 1
        while j < end and j + MINMATCH <= n:
            insert(n_hist + j)
            j += 1
        i = end
        anchor = i

    lit = n - anchor
    tpos = len(out)
    out.append(0)
    _emit_lit(out, tpos, lit)
    out += data[anchor:anchor + lit]
    return bytes(out)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from kit_lz4dict import decode_block
    # thu nghiem tren record that cua Unravel
    p = r'E:\UNR_work\parts\Data.kit.0'
    d = open(p, 'rb').read()
    # record @0x865b1aa
    off = 0x865b1aa
    ln, = struct.unpack_from('<I', d, off)
    print(f'record @{off:#x}: nen {ln:,} byte')
    hist = b''
    o = 0
    while o < off:
        l2, = struct.unpack_from('<I', d, o)
        if not (4 <= l2 <= 40_000_000):
            o += 1
            continue
        try:
            r = decode_block(d[o + 4:o + 4 + l2], hist[-MAX_OFF:])
            hist += r
            hist = hist[-MAX_OFF:]
            o += 4 + l2
        except Exception:
            o += 1
    raw = decode_block(d[off + 4:off + 4 + ln], hist[-MAX_OFF:])
    print(f'  giai nen {len(raw):,} byte | tu dien {len(hist):,} byte')
    enc = encode_block(raw, hist[-MAX_OFF:])
    print(f'  nen lai: {len(enc):,} byte (goc {ln:,}) | {"DAT" if len(enc) <= ln else "VAN TO HON"}')
    back = decode_block(enc, hist[-MAX_OFF:])
    print(f'  giai nen lai: {len(back):,} byte | {"KHOP" if back == raw else "KHONG KHOP!"}')
