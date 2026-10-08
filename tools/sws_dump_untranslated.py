"""Xuat danh sach muc chua dich cua Switch Sports ra file de doc + chia chunk dich.

Dung: python tools/sws_dump_untranslated.py
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.join(ROOT, 'games', '0100D2F00D5C0000_SwitchSports')
d = json.load(open(os.path.join(ROOT, 'games', '_consistency', 'untranslated_switchsports.json'),
                   encoding='utf-8'))

out = []
for name, items in d.items():
    if not items:
        continue
    out.append(f'\n########## {name} ({len(items)} muc)')
    for k, v in sorted(items.items()):
        out.append(f'{k.split("::", 1)[1]}\t{v!r}')
txt = '\n'.join(out)
p = os.path.join(ROOT, 'games', '_consistency', 'sws_untranslated.txt')
open(p, 'w', encoding='utf-8').write(txt)
print(f'-> {p} ({len(txt):,} ky tu)\n')

for name, items in d.items():
    if not items:
        continue
    if any(t in name for t in ('StaffRoll', 'Golf', 'Equipment', 'ProgramMsg__Menu')):
        print(f'===== {name} ({len(items)}) =====')
        for k, v in sorted(items.items())[:16]:
            print(f'  {k.split("::",1)[1][:40]:<40} {v[:72]!r}')
        if len(items) > 16:
            print(f'  ... con {len(items)-16}')
        print()
