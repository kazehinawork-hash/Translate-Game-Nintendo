"""PHEP THU: dung Filter.bin cua tieng Phap cho tieng Anh.

Filter.bin = danh sach ky tu theo ngon ngu (tieng Anh chi co ASCII).
Tieng Phap co them Latin-1 + Latin Extended-A.
=> Neu sau khi thay, cac ky tu nhu o/ó/a/â/ơ/ư/đ hien duoc => dung la Filter.bin.
"""
import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TID = '01004D300C5AE000'
MOD = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'msg', 'Kirby15')
DUMP = os.path.join(ROOT, 'dump', TID, 'romfs', 'msg', 'Kirby15')

# Voi moi khe tieng Anh, lay Filter.bin cua tieng Phap
PAIRS = [('US_English', 'US_French'), ('EU_English', 'EU_French')]
for en, fr in PAIRS:
    src = os.path.join(DUMP, fr, 'Filter.bin')
    dst = os.path.join(MOD, en, 'Filter.bin')
    if os.path.exists(src) and os.path.isdir(os.path.dirname(dst)):
        shutil.copy2(src, dst)
        print(f'  {en}: dung Filter cua {fr} ({os.path.getsize(src):,} b)')
    else:
        print(f'  {en}: thieu nguon/dich')

# Kiem tra nhanh: Filter moi co dai ky tu dai hon khong
for en, _ in PAIRS:
    p = os.path.join(MOD, en, 'Filter.bin')
    if os.path.exists(p):
        b = open(p, 'rb').read()
        import re
        s = max((m.group(0) for m in re.finditer(rb'[\x20-\x7e]{20,}', b)), default=b'', key=len)
        print(f'  {en}: {len(b):,} b | chuoi ky tu dai {len(s)} byte | dau: {s[:40]!r}')
