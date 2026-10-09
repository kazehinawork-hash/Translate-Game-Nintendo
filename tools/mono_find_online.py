"""Tim nhanh OnlineGame / Crossplay trong oasis__global va cac TextAsset khac (khong loc kieu ma hoa)."""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUMP = os.path.join(ROOT, 'dump', '01002C201BC40000', 'romfs', 'Data', 'data.unity3d')
import UnityPy

env = UnityPy.load(DUMP)
for o in env.objects:
    if o.type.name != 'TextAsset':
        continue
    d = o.read()
    nm = getattr(d, 'm_Name', '')
    raw = o.get_raw_data()
    if b'OnlineGame' not in raw and b'Crossplay' not in raw:
        continue
    print(f'=== {nm} ({len(raw):,} b) co OnlineGame/Crossplay ===')
    for enc in ('utf-16-le', 'utf-8'):
        try:
            j = raw.find(b'<' if enc == 'utf-8' else '<'.encode(enc))
            txt = raw[j:].decode(enc, errors='replace') if j >= 0 else raw.decode(enc, errors='replace')
        except Exception:
            continue
        hits = [m.start() for m in re.finditer(r'OnlineGame|Crossplay', txt)]
        if hits:
            print(f'  [{enc}] {len(hits)} lan')
            for h in hits[:6]:
                s = max(0, h - 120)
                seg = txt[s:h + 160].replace('\n', ' | ')
                print(f'      ...{seg}...')
            break
