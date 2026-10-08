"""Audit tham so zstd cho CA 2 dinh dang: .zs (zstd truc tiep) va .cmp (4 byte size + zstd)."""
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from zs_util import frame_params

GAMES = [('01004D300C5AE000_Kirby', '01004D300C5AE000'),
         ('0100D2F00D5C0000_SwitchSports', '0100D2F00D5C0000'),
         ('010061D00DB74000_OriAndTheBlindForest', '010061D00DB74000'),
         ('01008DD013200000_OriAndTheWillOfTheWisps', '01008DD013200000'),
         ('010092A0172E4000_ItTakesTwo', '010092A0172E4000'),
         ('0100E5D00CC0C000_UnravelTwo', '0100E5D00CC0C000')]

FIND = {}
for folder, tid in GAMES:
    gdir = os.path.join(ROOT, 'games', folder)
    if not os.path.isdir(gdir):
        continue
    srcs = {}
    for r, _, fs in os.walk(gdir):
        for f in fs:
            srcs.setdefault(f, os.path.join(r, f))
    FIND[tid] = srcs

for folder, tid in GAMES:
    odir = os.path.join(ROOT, 'output', 'atmosphere', 'contents', tid)
    if not os.path.isdir(odir):
        continue
    print(f'\n{"="*74}\n{folder}\n{"="*74}')
    srcs = FIND.get(tid, {})
    n = bad = 0
    for r, _, fs in os.walk(odir):
        for f in fs:
            po = os.path.join(r, f)
            b = open(po, 'rb').read()
            off = None
            if b[:4] == b'\x28\xb5\x2f\xfd':
                off = 0
            elif len(b) > 8 and b[4:8] == b'\x28\xb5\x2f\xfd':
                off = 4
            if off is None:
                continue
            pg = srcs.get(f)
            if not pg:
                print(f'  [khong co goc] {f} (offset zstd {off})')
                continue
            n += 1
            gb = open(pg, 'rb').read()
            goff = 0 if gb[:4] == b'\x28\xb5\x2f\xfd' else 4
            try:
                gp = frame_params(gb[goff:])
                mp = frame_params(b[off:])
            except Exception as e:
                print(f'  [loi] {f}: {type(e).__name__}'); continue
            note = ''
            if off == 4:
                gsize, = struct.unpack_from('<I', gb, 0)
                msize, = struct.unpack_from('<I', b, 0)
                note = f' | prefix goc={gsize:,} mod={msize:,}'
            if gp['window_log'] != mp['window_log'] or gp['checksum'] != mp['checksum']:
                bad += 1
                print(f'  [LECH] {f}')
                print(f'        goc WL={gp["window_log"]} ck={gp["checksum"]} <-> mod WL={mp["window_log"]} ck={mp["checksum"]}{note}')
    print(f'  -> so {n} file | LECH: {bad}')
