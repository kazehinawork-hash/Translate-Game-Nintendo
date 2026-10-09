"""In TempLocalizations + quet TOAN BO dump tim khoa 'OnlineGame'/'Crossplay' (UTF-16 & UTF-8)."""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUMP = os.path.join(ROOT, 'dump', '01002C201BC40000', 'romfs')
import UnityPy

# 1) in TempLocalizations
env = UnityPy.load(os.path.join(DUMP, 'Data', 'data.unity3d'))
for o in env.objects:
    if o.type.name != 'TextAsset':
        continue
    d = o.read()
    if getattr(d, 'm_Name', '') != 'TempLocalizations':
        continue
    raw = o.get_raw_data()
    print('=== TempLocalizations raw ===')
    print(repr(raw[:400]))
    for enc in ('utf-16-le', 'utf-8'):
        try:
            j = raw.find(b'<' if enc == 'utf-8' else '<'.encode(enc))
            if j >= 0:
                print(f'  [{enc}]')
                print('  ' + raw[j:j + 500].decode(enc, errors='replace'))
                break
        except Exception:
            pass

# 2) quet toan bo romfs
print('\n=== QUET TOAN BO DUMP tim OnlineGame / Crossplay ===')
pats = []
for k in ('OnlineGame', 'Crossplay', 'OnlinePlay', 'NO_TRANS'):
    pats.append((k, k.encode('utf-16-le')))
    pats.append((k + '[u8]', k.encode('utf-8')))

for dirpath, dirnames, filenames in os.walk(DUMP):
    for fn in filenames:
        p = os.path.join(dirpath, fn)
        try:
            b = open(p, 'rb').read()
        except Exception:
            continue
        found = [(lab, b.count(nb)) for lab, nb in pats if nb in b]
        if found:
            rel = os.path.relpath(p, DUMP)
            print(f'  {rel}  ({len(b):,} b)')
            for lab, c in found:
                print(f'      {lab} x{c}')
