"""Vá DAI KY TU trong cau hinh font Kirby (font/Region/<REGION>/*.bin).

Phat hien: trong file XBIN co vung  20 00 00 00 | 01 00 00 00 | 7f 00 00 00
= dai ky tu 0x20..0x7F (ASCII). Game chi hoi font scalable cac ky tu ASCII,
moi ky tu co dau roi xuong font du phong (bitmap Ext-*.bffnt) -> O VUONG.

Vá: doi gia tri ket thuc 0x7F -> 0x2FFF (bao gom Latin-1 + Latin Extended + Vietnamese).
"""
import os
import shutil
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'dump', '01004D300C5AE000', 'romfs', 'font', 'Region')
OUT = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01004D300C5AE000', 'romfs', 'font', 'Region')

PAT = struct.pack('<III', 0x20, 1, 0x7F)          # 20 00 00 00 01 00 00 00 7f 00 00 00
NEW = struct.pack('<III', 0x20, 1, 0x1EFF)        # mo rong toi het Latin Extended Additional (tieng Viet)

n_file = n_patch = 0
for reg in sorted(os.listdir(SRC)):
    d = os.path.join(SRC, reg)
    if not os.path.isdir(d):
        continue
    out_dir = os.path.join(OUT, reg)
    os.makedirs(out_dir, exist_ok=True)
    for fn in sorted(os.listdir(d)):
        if not fn.endswith('.bin'):
            continue
        p = os.path.join(d, fn)
        b = open(p, 'rb').read()
        c = b.count(PAT)
        if c:
            b = b.replace(PAT, NEW)
            n_patch += c
        open(os.path.join(out_dir, fn), 'wb').write(b)
        n_file += 1
        if c:
            print(f'  [{reg}] {fn[:44]:<46} thay {c} dai ASCII -> 0x2FFF')
print(f'\n{n_file} file cau hinh -> {OUT} | tong {n_patch} dai duoc mo rong')
