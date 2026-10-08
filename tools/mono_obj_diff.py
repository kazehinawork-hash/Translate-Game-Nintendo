"""So TUNG OBJECT giua bundle goc va bundle mod MONOPOLY: dem xem khac bao nhieu object."""
import hashlib
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = r'E:\MONO_work\data.unity3d'
DST = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01002C201BC40000', 'romfs', 'Data', 'data.unity3d')

import UnityPy


def load_map(path):
    env = UnityPy.load(path)
    m = {}
    for o in env.objects:
        try:
            m[o.path_id] = (o.type.name, o.get_raw_data())
        except Exception:
            m[o.path_id] = (o.type.name, None)
    return m


print('doc bundle goc...', flush=True)
g = load_map(SRC)
print(f'  {len(g):,} object', flush=True)
print('doc bundle mod...', flush=True)
m = load_map(DST)
print(f'  {len(m):,} object', flush=True)

only_g = sorted(set(g) - set(m))
only_m = sorted(set(m) - set(g))
print(f'\nchi o goc: {len(only_g)} | chi o mod: {len(only_m)}')

diff = []
for pid in g:
    if pid not in m:
        continue
    tg, dg = g[pid]
    tm, dm = m[pid]
    if tg != tm or dg != dm:
        diff.append(pid)
print(f'object KHAC noi dung: {len(diff):,} / {len(g):,}')
from collections import Counter
c = Counter(g[p][0] for p in diff)
print('  theo loai:', dict(c.most_common(8)))
print('  vi du path_id:', diff[:15])
