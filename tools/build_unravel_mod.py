"""Dong goi mod LayeredFS cho Unravel Two (Nintendo Switch).

- Thay bang dich trong cac record localization cua Data.kit.0 bang tieng Viet.
- Thay the theo REGEX (khong phu thuoc ranh gioi chunk).
- Va day chuyen: record nao bi lech do tham chieu cheo -> tra ve noi dung goc.
"""
import json
import os
import re
import struct
import sys

sys.path.insert(0, r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\tools')
sys.stdout.reconfigure(encoding='utf-8')
from kit_patch import decode_all
from kit_repack import HIST_KEEP
from kit_lz4dict_encode import encode_block

ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
GAME = os.path.join(ROOT, 'games', '0100E5D00CC0C000_UnravelTwo')
TID = '0100E5D00CC0C000'
OUTDIR = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'NVNKits')
PART0 = r'E:\UNR_work\parts\Data.kit.0'


def rebuild(data, recs, gaps, changes):
    """Dung lai file: record doi -> nen bang LZ4-CO-TU-DIEN (khong phai literal-only).

    ⚠️ Truoc day dung `lz4_literal_block` -> record bang dich 64 KB phinh thanh ~1,5 MB
    (=> file mod LON HON goc 1,46 MB, nghi lam game treo o logo). Nay nen co match,
    va phai theo dung lich su tu dien (HIST_KEEP) nhu luc giai ma.
    """
    events = [(g[0], 0, g[1]) for g in gaps] + [(r[0], 1, r) for r in recs]
    events.sort(key=lambda e: (e[0], e[1]))
    buf = bytearray()
    hist = b''
    for eoff, k, obj in events:
        if k == 0:
            buf += obj
            continue
        roff, rln, rpl, rout, rkind = obj
        if roff in changes:
            cur = changes[roff]
            blk = encode_block(cur, hist[-HIST_KEEP:])
            buf += struct.pack('<I', len(blk)) + blk
        else:
            cur = rout
            buf += struct.pack('<I', len(rpl)) + rpl
        hist += cur
        if len(hist) > 4 * HIST_KEEP:          # cat thua (amortized, tranh copy moi record)
            hist = hist[-HIST_KEEP:]
    return bytes(buf)


def replace_values(text, vi):
    """Thay gia tri cho moi khoa co trong bang, dung regex tren toan van ban."""
    n = 0
    for k, v in vi.items():
        pat = re.compile(r'(^|\r\n)' + re.escape(k) + r'\r\n(.*?)(?=\r\n[A-Z0-9_]{2,}\r\n|\r\n\Z|$)',
                         re.S | re.M)
        def sub(m):
            nonlocal n
            n += 1
            return m.group(1) + k + '\r\n' + v
        text = pat.sub(sub, text, count=1)
    return text, n


def main():
    vi = {x['key']: x['vi'] for x in
          json.load(open(os.path.join(GAME, 'translations', 'vi_all.json'), encoding='utf-8'))}
    data = open(PART0, 'rb').read()
    recs, gaps = decode_all(data)
    print(f'{len(recs)} record | {len(gaps)} gap')

    changes = {}
    n_rep = 0
    for off, ln, pl, out, kind in recs:
        if not ((b'<NEWLINE>' in out and b'<loca>' in out) or b'AFTER_CREDITS' in out or b'CREDITS_' in out):
            continue
        try:
            text = out.decode('utf-8')
        except UnicodeDecodeError:
            continue
        if '\r\n' not in text[:200]:
            continue
        new_text, cnt = replace_values(text, vi)
        if cnt:
            changes[off] = new_text.encode('utf-8')
            n_rep += cnt
    print(f'{len(changes)} record can thay | tong {n_rep} gia tri')

    cur = rebuild(data, recs, gaps, changes)
    # va day chuyen: record bi lech do tham chieu cheo (match tro vao vung da doi)
    # KHONG the "giu byte goc" duoc — phai NEN LAI chinh record do voi lich su MOI,
    # de no giai ma ra dung noi dung GOC.
    for it in range(6):
        recs2, gaps2 = decode_all(cur)
        if len(recs2) != len(recs):
            print(f'  !! so record doi: {len(recs)} -> {len(recs2)}'); break
        bad = [i for i, (a, b) in enumerate(zip(recs, recs2))
               if a[3] != b[3] and recs[i][0] not in changes]
        print(f'  vong {it+1}: {len(bad)} record lech ngoai du kien')
        if not bad:
            break
        for i in bad:
            changes[recs[i][0]] = recs[i][3]     # nen lai -> giai ma ra noi dung goc
        cur = rebuild(data, recs, gaps, changes)

    recs3, _ = decode_all(cur)
    ok = len(recs3) == len(recs) and all(a[3] == b[3] for a, b in zip(recs, recs3))
    print(f'\nkiem chung cuoi: {len(recs3)} record | noi dung khop: {ok}')
    print(f'tong record da sua: {len(changes)}')
    os.makedirs(OUTDIR, exist_ok=True)
    p = os.path.join(OUTDIR, 'Data.kit.0')
    open(p, 'wb').write(cur)
    print(f'da ghi: {p} ({len(cur):,} byte)')
    print('KET QUA:', 'PASS' if ok else 'CAN XEM LAI')


if __name__ == '__main__':
    main()
