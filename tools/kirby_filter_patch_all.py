"""VA Filter.bin cho TAT CA ngon ngu cua Kirby.

Ly do: game nap Filter.bin theo NGON NGU dang dat. Neu may de tieng Phap/Duc/Tay Ban Nha...
thi Filter cua ngon ngu do KHONG co ky tu tieng Viet (nhu 'a.' U+1EA1) -> o vuong.
Truoc day chi va EU_English/US_English -> ngon ngu khac van loi.

Cach lam: lay Filter JP_Japanese (danh sach lon nhat, 21.828 b) lam NEN, thay cac o
Kana/Kanji (khong dung cho tieng Viet) bang ky tu tieng Viet can, roi ghi vao MOI ngon ngu.
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TID = '01004D300C5AE000'
DUMP = os.path.join(ROOT, 'dump', TID, 'romfs', 'msg', 'Kirby15')
MOD = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'msg', 'Kirby15')
BASE = os.path.join(DUMP, 'JP_Japanese', 'Filter.bin')

vi = json.load(open(os.path.join(ROOT, 'games', f'{TID}_Kirby', 'translations', 'kirby_vi.json'),
                    encoding='utf-8'))
used = set()
for ents in vi.values():
    for v in ents.values():
        used |= set(str(v))
used = {c for c in used if c.isprintable() and 0x20 <= ord(c) <= 0xFFFF}


def units_of(b):
    return [b[i] | (b[i + 1] << 8) for i in range(0, len(b) - 1, 2)]


def long_runs(units):
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


b = bytearray(open(BASE, 'rb').read())
units = units_of(b)
runs = long_runs(units)
present = {units[i] for r in runs for i in r}
need = sorted(c for c in used if ord(c) not in present)
print(f'  nen JP: {len(b):,} b | {len(present):,} ky tu | thieu {len(need)}')

REPLACE = [(0x3040, 0x30FF), (0x4E00, 0x9FFF), (0xFF66, 0xFF9F), (0x31F0, 0x31FF),
           (0xAC00, 0xD7FF), (0x1100, 0x11FF)]
keep = {ord(c) for c in used}
slots = [i for r in runs for i in r
         if any(a <= units[i] <= z for a, z in REPLACE) and units[i] not in keep]
print(f'  cho thay duoc: {len(slots):,}')
n = 0
for c, pos in zip(need, slots):
    v = ord(c)
    b[pos * 2] = v & 0xFF
    b[pos * 2 + 1] = (v >> 8) & 0xFF
    n += 1
print(f'  da thay {n} ky tu')

units2 = units_of(b)
present2 = {units2[i] for r in long_runs(units2) for i in r}
still = [c for c in used if ord(c) not in present2]
print(f'  sau khi va con thieu {len(still)}: {"".join(still[:30])}')
for cp in (0x1EA1, 0x1EA0, 0x1EDB, 0x1EC7, 0x1EC1, 0x1EDD):
    print(f'    U+{cp:04X} ({chr(cp)}): {"CO" if cp in present2 else "THIEU"}')

print()
langs = sorted(d for d in os.listdir(MOD) if os.path.isdir(os.path.join(MOD, d)))
for lang in langs:
    dst = os.path.join(MOD, lang, 'Filter.bin')
    if os.path.exists(dst):
        open(dst, 'wb').write(bytes(b))
        print(f'  -> {lang:<14} Filter.bin ({len(b):,} b)')
print(f'\n  da va {len(langs)} ngon ngu')
