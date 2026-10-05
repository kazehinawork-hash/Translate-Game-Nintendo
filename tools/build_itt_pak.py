"""Kiem chung asset da ghi (doc lai) + dong goi patch pak cho It Takes Two."""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import repak

# 1. build patch pak tu assets_vi (giu dung duong dan goc)
SRC = r'E:\ITT_work\assets_vi'
OUTDIR = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '010092A0172E4000', 'romfs', 'Nuts', 'Content', 'Paks')
os.makedirs(OUTDIR, exist_ok=True)
PAKOUT = os.path.join(OUTDIR, 'Nuts-Switch_p.pak')

# duong dan trong pak = duong dan goc (Nuts/Content/...) -> tinh tu chinh thu muc nguon
files = []
for r, _, fs in os.walk(SRC):
    for f in fs:
        p = os.path.join(r, f)
        rel = os.path.relpath(p, SRC).replace('\\', '/')   # <- SRC, khong phai 'base'
        files.append((rel, p))
print(f'{len(files)} file de dong pak')
assert all(f[0].startswith('Nuts/') for f in files), 'duong dan phai bat dau bang Nuts/'

builder = repak.PakBuilder().compression([repak.Compression.ZLIB])
with builder.writer(PAKOUT, version=repak.Version.V11, mount_point='../../../') as w:
    for rel, p in sorted(files):
        w.write_file(rel, open(p, 'rb').read())
print(f'da ghi {PAKOUT}')

# 2. verify pak
r = repak.PakBuilder().reader(PAKOUT)
ents = list(r.entries())
print(f'verify: {len(ents)} entry | version={r.version} | mount={r.mount_point!r}')
ok = True
for rel, _ in sorted(files)[:3]:
    try:
        r.read_file(rel, os.path.join(os.environ['TEMP'], 'vg.bin'))
        print(f'  doc lai OK: {rel}')
    except Exception as e:
        ok = False
        print(f'  LOI doc {rel}: {e}')
print('KET QUA PAK:', 'PASS' if ok and len(ents) == len(files) else 'CAN XEM LAI')
