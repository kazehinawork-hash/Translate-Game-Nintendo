"""Kiem tra Filter.bin cua Kirby: danh sach ky tu co du cac ky tu tieng Viet khong."""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01004D300C5AE000', 'romfs', 'msg', 'Kirby15',
                 'EU_English', 'Filter.bin')
S = os.path.join(ROOT, 'dump', '01004D300C5AE000', 'romfs', 'msg', 'Kirby15', 'EU_English', 'Filter.bin')


def chars_in(path):
    b = open(path, 'rb').read()
    out = set()
    for i in range(0, len(b) - 1, 2):
        if b[i + 1] == 0 and 0x20 <= b[i] < 0xFF:
            out.add(b[i])
        for cp in (b[i] | (b[i + 1] << 8),):
            if 0x100 <= cp <= 0x2FFF:
                out.add(cp)
    return out


mod = chars_in(M)
orig = chars_in(S)
vi = json.load(open(os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'translations', 'kirby_vi.json'),
                    encoding='utf-8'))
used = set()
for ents in vi.values():
    for v in ents.values():
        for c in str(v):
            if c.isprintable():
                used.add(ord(c))

miss_mod = sorted(c for c in used if c not in mod)
miss_orig = sorted(c for c in used if c not in orig)
print(f'  ky tu ban dich dung: {len(used)}')
print(f'  Filter GOC thieu   : {len(miss_orig)} ky tu')
print(f'  Filter MOD thieu   : {len(miss_mod)} ky tu')
if miss_mod:
    print('  --- 40 ky tu MOD con thieu ---')
    print('   ', ' '.join('%s(U+%04X)' % (chr(c), c) for c in miss_mod[:40]))
print()
for cp, nm in [(0x1EA1, 'a. (dot below)'), (0x1EA0, 'A.'), (0x1EB9, 'e.'), (0x1ECB, 'i.'),
               (0x1ECD, 'o.'), (0x1EE5, 'u.'), (0x1EF9, 'y~'), (0x1EF3, 'y`')]:
    print(f'  {nm:<18} U+{cp:04X}: mod={"CO" if cp in mod else "THIEU":<5} goc={"CO" if cp in orig else "THIEU"}')
print(f'\n  kich thuoc: goc {os.path.getsize(S):,} b | mod {os.path.getsize(M):,} b')
