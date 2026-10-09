"""Xac minh font Kirby bang doc TAY (khong dung fontTools - font thieu maxp).

Kiem tra khoa XOR: giai ma xong phai co bang muc luc sfnt HOP LE
  - so bang 1..40
  - moi tag la 4 ky tu in duoc
  - offset/len nam trong file
"""
import json
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import zstandard

TID = '01004D300C5AE000'
M = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'font', 'ScalableFontBin')
S = os.path.join(ROOT, 'dump', TID, 'romfs', 'font', 'ScalableFontBin')
MAGIC = 0x36F81A1E
CAND = (0x4F54544F, 0x00010000, 0x74746366)

vi = json.load(open(os.path.join(ROOT, 'games', f'{TID}_Kirby', 'translations', 'kirby_vi.json'),
                    encoding='utf-8'))
used = set()
for ents in vi.values():
    for v in ents.values():
        used |= set(str(v))
need = sorted({ord(c) for c in used if c.isprintable() and 0x20 <= ord(c) <= 0xFFFF})


def sfnt_of(body):
    """Tra ve dict tag->(off,len) neu sfnt hop le, nguoc lai None."""
    if len(body) < 12:
        return None
    n = struct.unpack_from('>H', body, 4)[0]
    if not (1 <= n <= 40) or 12 + 16 * n > len(body):
        return None
    out = {}
    for i in range(n):
        tag, cks, off, ln = struct.unpack_from('>4sIII', body, 12 + 16 * i)
        t = tag.decode('latin1')
        if not all(32 <= ord(c) < 127 for c in t):
            return None
        if off + ln > len(body):
            return None
        out[t] = (off, ln)
    return out


def load(p):
    b = open(p, 'rb').read()
    d = zstandard.ZstdDecompressor()
    try:
        data = d.decompress(b[4:], max_output_size=256 << 20)
    except zstandard.ZstdError:
        with d.stream_reader(b[4:]) as r:
            data = r.read(256 << 20)
    w8, = struct.unpack_from('>I', data, 8)
    for e in CAND:
        k = w8 ^ e
        body = b''.join(struct.pack('>I', struct.unpack_from('>I', data, i)[0] ^ k)
                        for i in range(8, len(data), 4))
        if body[:4] != struct.pack('>I', e):
            continue
        if sfnt_of(body):
            return body, k
    return None, None


def cmap_chars(body, tabs):
    if 'cmap' not in tabs:
        return set()
    off, _ = tabs['cmap']
    n = struct.unpack_from('>H', body, off + 2)[0]
    chars = set()
    for i in range(n):
        sub = off + 4 + 8 * i
        pid, eid, so = struct.unpack_from('>HHI', body, sub)
        p = off + so
        fmt = struct.unpack_from('>H', body, p)[0]
        if fmt == 4:
            segX2 = struct.unpack_from('>H', body, p + 6)[0]
            seg = segX2 // 2
            ends = struct.unpack_from('>%dH' % seg, body, p + 14)
            starts = struct.unpack_from('>%dH' % seg, body, p + 16 + segX2)
            for a, b in zip(starts, ends):
                if a == 0xFFFF:
                    continue
                chars.update(range(a, min(b, 0xFFFF) + 1))
        elif fmt == 12:
            ng = struct.unpack_from('>I', body, p + 12)[0]
            for g in range(ng):
                a, b, _ = struct.unpack_from('>III', body, p + 16 + 12 * g)
                chars.update(range(a, min(b, 0x10FFFF) + 1))
    return chars


n_ok = n_bad = 0
for fn in sorted(os.listdir(M)):
    if not fn.endswith('.cmp'):
        continue
    body, key = load(os.path.join(M, fn))
    if body is None:
        print(f'  [!] {fn[:42]}: KHONG giai ma duoc (khoa sai?)')
        n_bad += 1
        continue
    tabs = sfnt_of(body)
    ob, _ = load(os.path.join(S, fn))
    otabs = set(sfnt_of(ob)) if ob else set()
    cm = cmap_chars(body, tabs)
    miss = [c for c in need if c not in cm]
    same = set(tabs) == otabs
    if not miss and same:
        n_ok += 1
    else:
        n_bad += 1
        print(f'  [!!] {fn[:42]:<44} bang goc={len(otabs)} mod={len(tabs)} khop={same} | thieu {len(miss)}')
print(f'\n  {n_ok} font DUNG (du {len(need)} ky tu + danh sach bang y goc) | {n_bad} loi')
