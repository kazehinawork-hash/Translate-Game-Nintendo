"""Liet ke 43 chuoi MOI cua v1.6 (co trong bundle moi nhung khong co ban dich)."""
import json
import os
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = '{http://schemas.ubisoft.com/oasis/2011/extractor}'
import UnityPy

DUMP = os.path.join(ROOT, 'dump', '01002C201BC40000', 'romfs', 'Data', 'data.unity3d')
vi = json.load(open(os.path.join(ROOT, 'games', '01002C201BC40000_Monopoly', 'translations',
                                 'mono_vi.json'), encoding='utf-8'))

env = UnityPy.load(DUMP)
for o in env.objects:
    if o.type.name != 'TextAsset':
        continue
    d = o.read()
    if getattr(d, 'm_Name', '') != 'oasis_englishgb':
        continue
    raw = o.get_raw_data()
    j = raw.find(b'<')
    txt = raw[j:].decode('utf-16-le')
    root = ET.fromstring(txt)
    ents = {e.get('id'): (e.get('text') or '') for e in list(root.find(f'{NS}translations'))}
    break

new = [(i, t) for i, t in ents.items() if t not in vi]
print(f'v1.6 co {len(ents)} id | ban dich hien co {len(vi)} khoa | CHUA DICH: {len(new)}\n')
json.dump([{'id': i, 'en': t} for i, t in sorted(new, key=lambda x: int(x[0]))],
          open(os.path.join(ROOT, 'games', '01002C201BC40000_Monopoly', 'translations', 'v16_new.json'),
               'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for i, t in sorted(new, key=lambda x: int(x[0])):
    print(f'  #{i:<6} {t[:95]!r}')
