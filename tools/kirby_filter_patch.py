"""VA TRIET DE Filter.bin cho Kirby: thay ky tu Kana/Kanji (khong dung) bang
day du ky tu tieng Viet ma ban dich can.

- Nen: Filter.bin cua JP_Japanese (21 KB, danh sach ky tu rat lon, font list giong het EN).
- Ky tu thay: chi nhung ma UTF-16 nam trong RUN DAI (>=8 ma lien tiep khac 0) - tranh
  dong vao offset/number cua XBIN.
- Ghi vao cac khe tieng Anh (US_English, EU_English).
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TID = '01004D300C5AE000'
DUMP = os.path.join(ROOT, 'dump', TID, 'romfs', 'msg', 'Kirby15')
MOD = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'msg', 'Kirby15')

SRC_FILTER = os.path.join(DUMP, 'JP_Japanese', 'Filter.bin')

# 1) tap ky tu tieng Viet ma ban dich can
vi = json.load(open(os.path.join(ROOT, 'games', f'{TID}_Kirby', 'translations', 'kirby_vi.json'),
                    encoding='utf-8'))
used = set()
for ents in vi.values():
    for v in ents.values():
        used |= set(str(v))
used = {c for c in used if c.isprintable() and 0x20 <= ord(c) <= 0xFFFF}


def utf16_units(b):
    return [b[i] | (b[i + 1] << 8) for i in range(0, len(b) - 1, 2)]


def long_runs(units):
    """Cac doan >= 8 ma lien tiep khac 0 (vung du lieu chuoi)."""
    runs, cur = [], []
    for i, u in enumerate(units):
        if u != 0:
            cur.append(i)
        else:
            if len(cur) >= 8:
                runs.append(cur)
            cur = []
    if len(cur) >= 8:
        runs.append(cur)
    return runs


b = bytearray(open(SRC_FILTER, 'rb').read())
units = utf16_units(b)
runs = long_runs(units)
present = {units[i] for r in runs for i in r}
print(f'  Filter JP: {len(b):,} b | {len(runs)} doan chuoi | {len(present):,} ky tu co san')

need_add = sorted(c for c in used if ord(c) not in present)
print(f'  ban dich can {len(used)} ky tu | THIEU trong JP filter: {len(need_add)}')
print(f'    {"".join(need_add[:60])}')

# 2) vi tri co the thay: trong run dai, la Kana/CJK, va KHONG phai ky tu ban dich can
REPLACE_HI = [(0x3040, 0x30FF), (0x4E00, 0x9FFF), (0xFF66, 0xFF9F), (0x31F0, 0x31FF)]
slots = []
for r in runs:
    for i in r:
        u = units[i]
        if any(a <= u <= z for a, z in REPLACE_HI) and u not in {ord(c) for c in used}:
            slots.append(i)
print(f'  cho trong thay duoc (Kana/Kanji): {len(slots):,}')

if len(slots) < len(need_add):
    print('  !! khong du cho -> dung het so co the')
n = 0
for c, pos in zip(need_add, slots):
    v = ord(c)
    b[pos * 2] = v & 0xFF
    b[pos * 2 + 1] = (v >> 8) & 0xFF
    n += 1
print(f'  da thay {n} ky tu')

# 3) kiem chung lai
units2 = utf16_units(b)
present2 = {units2[i] for r in long_runs(units2) for i in r}
still = [c for c in used if ord(c) not in present2]
print(f'  sau khi va: thieu {len(still)}: {"".join(still[:40])}')

# 4) ghi vao cac khe tieng Anh
for lang in ('US_English', 'EU_English'):
    dst = os.path.join(MOD, lang, 'Filter.bin')
    if os.path.isdir(os.path.dirname(dst)):
        open(dst, 'wb').write(bytes(b))
        print(f'  -> {lang}/Filter.bin ({len(b):,} b)')
