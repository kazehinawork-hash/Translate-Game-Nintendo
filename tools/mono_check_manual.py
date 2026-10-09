"""1) In thuoc tinh cua <t> trong oasis_englishgb (de biet co 'key' khong).
2) Tim 'Manual', 'CATEGORY_GAMEBASICS' trong toan bo TextAsset (ca utf16/utf8).
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUMP = os.path.join(ROOT, 'dump', '01002C201BC40000', 'romfs', 'Data', 'data.unity3d')
import UnityPy

env = UnityPy.load(DUMP)

# 1) thuoc tinh cua cac the <t>
for o in env.objects:
    if o.type.name != 'TextAsset':
        continue
    d = o.read()
    if getattr(d, 'm_Name', '') != 'oasis_englishgb':
        continue
    raw = o.get_raw_data()
    j = raw.find(b'<')
    txt = raw[j:].decode('utf-16-le', errors='replace')
    tags = re.findall(r'<t\b[^>]*/?>', txt)
    print(f'=== oasis_englishgb: {len(tags)} the <t> ===')
    for t in tags[:12]:
        print('  ' + t[:230])
    # co thuoc tinh 'key' khong
    nk = sum(1 for t in tags if 'key=' in t)
    print(f'  so the co thuoc tinh "key=": {nk}')
    break

# 2) tim cac khoa Manual
print('\n=== tim "Manual" / "CATEGORY_GAMEBASICS" / "Generic/Back" ===')
needles = []
for k in ('CATEGORY_GAMEBASICS', 'Menu/Manual', 'Generic/Back', 'MENU/MANUAL'):
    needles.append((k, k.encode('utf-16-le')))
    needles.append((k + '[u8]', k.encode('utf-8')))
found_any = False
for o in env.objects:
    if o.type.name != 'TextAsset':
        continue
    d = o.read()
    nm = getattr(d, 'm_Name', '')
    raw = o.get_raw_data()
    hits = [(lab, raw.count(nb)) for lab, nb in needles if nb in raw]
    if hits:
        found_any = True
        print(f'  {nm}: {hits}')
if not found_any:
    print('  KHONG co TextAsset nao chua cac khoa nay')
