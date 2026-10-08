"""Quet TAT CA game: so sanh tham so frame zstd giua file trong mod va file GOC tuong ung.

Doi chieu file theo TEN FILE (bo qua duong dan), chi voi cac file nen zstd.
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from zs_util import frame_params

GAMES = {
    '0100D2F00D5C0000_SwitchSports': '0100D2F00D5C0000',
    '01004D300C5AE000_Kirby': '01004D300C5AE000',
    '010061D00DB74000_OriAndTheBlindForest': '010061D00DB74000',
    '01008DD013200000_OriAndTheWillOfTheWisps': '01008DD013200000',
    '010092A0172E4000_ItTakesTwo': '010092A0172E4000',
    '0100E5D00CC0C000_UnravelTwo': '0100E5D00CC0C000',
}

def kind_of(b):
    if b[:4] == b'\x28\xb5\x2f\xfd':
        return 'zstd'
    if b[:4] == b'\x28\xb5\x2f\xfd'[::-1]:
        return 'zstd?'
    return None

for folder, tid in GAMES.items():
    gdir = os.path.join(ROOT, 'games', folder)
    odir = os.path.join(ROOT, 'output', 'atmosphere', 'contents', tid)
    if not os.path.isdir(odir):
        print(f'\n### {folder}: khong co trong output')
        continue
    print(f'\n{"="*74}\n{folder}\n{"="*74}')
    # index file goc theo ten
    srcs = {}
    for r, _, fs in os.walk(gdir):
        for f in fs:
            if f.endswith(('.zs', '.cmp', '.sarc.zs', '.bfarc.zs')):
                srcs.setdefault(f, os.path.join(r, f))
    n_chk = n_bad = 0
    for r, _, fs in os.walk(odir):
        for f in fs:
            po = os.path.join(r, f)
            b = open(po, 'rb').read(64)
            if b[:4] != b'\x28\xb5\x2f\xfd':
                continue
            pg = srcs.get(f)
            if not pg:
                print(f'  [khong co goc] {f}')
                continue
            n_chk += 1
            try:
                g = frame_params(open(pg, 'rb').read())
                m = frame_params(open(po, 'rb').read())
            except Exception as e:
                print(f'  [loi doc] {f}: {type(e).__name__}')
                continue
            if g['window_log'] != m['window_log'] or g['checksum'] != m['checksum']:
                n_bad += 1
                print(f'  [LECH] {f}')
                print(f'         goc windowLog={g["window_log"]} checksum={g["checksum"]} <-> '
                      f'mod windowLog={m["window_log"]} checksum={m["checksum"]}')
    print(f'  -> da so {n_chk} file nen | LECH: {n_bad}')
