"""So sanh bundle BASE v1.0 vs DUMP v1.6: co khoa Menu/Manual/* khong, va TextAsset nao khac nhau."""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = r'E:\MONO_work\data.unity3d'
V16 = os.path.join(ROOT, 'dump', '01002C201BC40000', 'romfs', 'Data', 'data.unity3d')
import UnityPy

NEEDLES = []
for k in ('CATEGORY_GAMEBASICS', 'Menu/Manual', 'Generic/Back', 'MENU/MANUAL', 'TempLocalizations'):
    NEEDLES.append((k, k.encode('utf-16-le')))
    NEEDLES.append((k + '[u8]', k.encode('utf-8')))


def dump(path, label):
    print(f'\n=== {label} ({os.path.getsize(path):,} b) ===')
    env = UnityPy.load(path)
    tas = {}
    for o in env.objects:
        if o.type.name != 'TextAsset':
            continue
        d = o.read()
        tas[getattr(d, 'm_Name', '')] = o.get_raw_data()
    print(f'  TextAsset: {len(tas)}')
    for nm, raw in tas.items():
        hits = [(lab, raw.count(nb)) for lab, nb in NEEDLES if nb in raw]
        if hits:
            print(f'    {nm}: {hits}')
    return set(tas.keys())


a = dump(BASE, 'BASE v1.0')
b = dump(V16, 'DUMP v1.6')
print('\n  chi co o BASE :', sorted(a - b))
print('  chi co o v1.6 :', sorted(b - a))
