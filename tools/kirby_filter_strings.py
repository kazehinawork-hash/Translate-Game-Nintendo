"""Liet ke cac CHUOI trong Filter.bin (ten font / ten config / ten nhom glyph)."""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(ROOT, 'dump', '01004D300C5AE000', 'romfs', 'msg', 'Kirby15')

for lang in ('EU_English', 'EU_French', 'JP_Japanese'):
    p = os.path.join(BASE, lang, 'Filter.bin')
    b = open(p, 'rb').read()
    strs = [m.group(0).decode('utf-8', 'replace') for m in re.finditer(rb'[\x20-\x7e]{4,}', b)]
    print(f'\n=== {lang} ({len(b):,} b) — {len(strs)} chuoi ===')
    for s in strs:
        print(f'   {s}')
