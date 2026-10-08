"""Vá DAI KY TU trong cau hinh font Kirby (font/Region/<REGION>/*.bin).

Moi file cau hinh XBIN co 2 dai ky tu:
    dai 1 @~0x120:  0x0020 .. 0x007F     (ASCII)
    dai 2 @~0x144:  0x0440 .. 0x0C00     (Cyrillic/Kana)

Doi thanh:
    dai 1:  0x0020 .. 0x02FF   -> Latin-1 + Latin Extended-A/B
                                  (a a an a e o o u d ...)
    dai 2:  0x1EA0 .. 0x1EFF   -> khoi dau thanh tieng Viet
                                  (Latin Extended Additional)

⚠️ Khong noi dai 1 thanh 0x1EFF (do dai ~7.900 ky tu): dai qua lon co the bi
game bo qua. Hai dai nho (<=720) an toan hon va van phu TRON tieng Viet.
"""
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'dump', '01004D300C5AE000', 'romfs', 'font', 'Region')
OUT = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01004D300C5AE000', 'romfs', 'font', 'Region')

R1_OLD = struct.pack('<III', 0x20, 1, 0x7F)       # 20 00 00 00 01 00 00 00 7f 00 00 00
R1_NEW = struct.pack('<III', 0x20, 1, 0x1EFF)     # ... 0x1EFF: phu tron Latin-1 + Latin Ext + dau tieng Viet
# ⚠️ KHONG dung vao triplet thu 2 (@~0x144): y nghia khac, da kiem chung khong phai dai ky tu.
R2_OLD = None
R2_NEW = None

n1 = n2 = nfile = 0
for reg in sorted(os.listdir(SRC)):
    d = os.path.join(SRC, reg)
    if not os.path.isdir(d):
        continue
    out_dir = os.path.join(OUT, reg)
    os.makedirs(out_dir, exist_ok=True)
    for fn in sorted(os.listdir(d)):
        if not fn.endswith('.bin'):
            continue
        b = open(os.path.join(d, fn), 'rb').read()
        c1 = b.count(R1_OLD)
        c2 = 0
        if c1:
            b = b.replace(R1_OLD, R1_NEW)
            n1 += c1
        open(os.path.join(out_dir, fn), 'wb').write(b)
        nfile += 1
        if c1 or c2:
            print(f'  [{reg}] {fn[:42]:<44} dai1:{c1} dai2:{c2}')
print(f'\n{nfile} file cau hinh -> {OUT}')
print(f'  dai 1 (ASCII -> Latin Ext)  : {n1} cho')
print(f'  dai 2 (Cyr/Kana -> Viet)    : {n2} cho')
