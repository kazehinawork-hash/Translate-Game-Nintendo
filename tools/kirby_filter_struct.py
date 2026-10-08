"""Soi cau truc Filter.bin: la bang bitmap ky tu hay danh sach?"""
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, 'dump', '01004D300C5AE000', 'romfs', 'msg', 'Kirby15')

for lang in ('EU_English', 'EU_French', 'JP_Japanese'):
    p = os.path.join(BASE, lang, 'Filter.bin')
    b = open(p, 'rb').read()
    print(f'\n=== {lang} ({len(b):,} b) ===')
    print(f'  header 48 byte: {b[:48].hex(" ")}')
    # phan sau header: xem co phai bitmap khong
    body = b[48:]
    ones = sum(bin(x).count('1') for x in body)
    print(f'  body {len(body):,} b | so bit = 1: {ones:,} ({ones/ (len(body)*8) *100:.1f}% = mat do ky tu)')
    print(f'  64 byte dau body: {body[:64].hex(" ")}')
    # thu doc vai gia tri u32 dau
    if len(body) >= 32:
        vals = struct.unpack_from('<8I', body, 0)
        print(f'  8 u32 dau: {[hex(v) for v in vals]}')
    # tim xem co danh sach cap (start,end) khong
    print(f'  32 byte cuoi: {b[-32:].hex(" ")}')
