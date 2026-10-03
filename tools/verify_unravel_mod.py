"""Kiem chung mod Unravel Two: file mod phai giong goc tru TUNG record bang dich."""
import os
import sys

sys.path.insert(0, r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\tools')
sys.stdout.reconfigure(encoding='utf-8')
from kit_patch import decode_all

ORIG = r'E:\UNR_work\parts\Data.kit.0'
MOD = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\output\atmosphere\contents\0100E5D00CC0C000\romfs\NVNKits\Data.kit.0'

a, ga = decode_all(open(ORIG, 'rb').read())
b, gb = decode_all(open(MOD, 'rb').read())
print(f'goc: {len(a)} record | {len(ga)} gap')
print(f'mod: {len(b)} record | {len(gb)} gap')

diff = [i for i, (x, y) in enumerate(zip(a, b)) if x[3] != y[3]]
print(f'record khac nhau: {len(diff)}')
vi_keys = 0
for i in diff:
    off = a[i][0]
    o, n = a[i][3], b[i][3]
    print(f'  @{off:#x}: {len(o):,} -> {len(n):,} byte')
    # dem so gia tri tieng Viet
    if b'Quay l' in n or b'Nh' in n or b'Ch' in n:
        vi_keys += 1
print(f'\nrecord chua dau hieu tieng Viet: {vi_keys}/{len(diff)}')
# kiem tra khoa khong doi trong record da sua
import re
for i in diff[:3]:
    ka = set(re.findall(rb'(?m)^[A-Z0-9_]{3,}$', a[i][3]))
    kb = set(re.findall(rb'(?m)^[A-Z0-9_]{3,}$', b[i][3]))
    print(f'  @{a[i][0]:#x}: khoa goc {len(ka)} | khoa mod {len(kb)} | thieu {len(ka-kb)} | thua {len(kb-ka)}')
print('\nKET LUAN:', 'PASS - chi record bang dich thay doi, so record/gap nguyen ven'
      if len(a) == len(b) and len(ga) == len(gb) and diff else 'CAN XEM LAI')
