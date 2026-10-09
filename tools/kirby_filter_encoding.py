"""Tim cach ma hoa ky tu trong Filter.bin (tieng Phap co dau -> xac dinh encoding)."""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'dump', '01004D300C5AE000', 'romfs', 'msg', 'Kirby15', 'EU_French', 'Filter.bin')
b = open(P, 'rb').read()

CAND = {
    'é UTF-8 (C3 A9)': b'\xc3\xa9',
    'é UTF-16LE (E9 00)': b'\xe9\x00',
    'à UTF-8 (C3 A0)': b'\xc3\xa0',
    'à UTF-16LE (E0 00)': b'\xe0\x00',
    'ç UTF-8 (C3 A7)': b'\xc3\xa7',
    'ç UTF-16LE (E7 00)': b'\xe7\x00',
    'ù UTF-8 (C3 B9)': b'\xc3\xb9',
    'ù UTF-16LE (F9 00)': b'\xf9\x00',
}
print(f'{P.split(chr(92))[-2]}/Filter.bin ({len(b):,} b)\n')
for name, pat in CAND.items():
    i = b.find(pat)
    print(f'  {name:<24} {"THAY @%#x" % i if i >= 0 else "khong thay"}')

# neu la UTF-16LE thi thu giai ma vung chuoi
i = b.find(b'\xe9\x00')
if i >= 0:
    seg = b[max(0, i - 40):i + 60]
    print(f'\n  vung quanh é @{i:#x}:')
    print(f'    hex: {seg.hex(" ")}')
    print(f'    ascii: {"".join(chr(x) if 32 <= x < 127 else "." for x in seg)}')
    # thu giai ma thanh UTF-16LE
    try:
        print(f'    utf-16le: {seg.decode("utf-16-le", "replace")!r}')
    except Exception as e:
        print(f'    utf-16le loi: {e}')
