"""So RIENG cac TextAsset giua bundle goc va bundle mod MONOPOLY."""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = r'E:\MONO_work\data.unity3d'
DST = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01002C201BC40000', 'romfs', 'Data', 'data.unity3d')
import UnityPy


def texts(path):
    env = UnityPy.load(path)
    out = {}
    n_obj = 0
    for o in env.objects:
        n_obj += 1
        if o.type.name != 'TextAsset':
            continue
        d = o.read()
        out[getattr(d, 'm_Name', '?')] = o.get_raw_data()
    return n_obj, out


n1, t1 = texts(SRC)
n2, t2 = texts(DST)
print(f'object: goc {n1:,} | mod {n2:,}')
print(f'TextAsset: goc {len(t1)} | mod {len(t2)}')
only1 = sorted(set(t1) - set(t2))
only2 = sorted(set(t2) - set(t1))
diff = [k for k in t1 if k in t2 and t1[k] != t2[k]]
print(f'chi goc: {only1}')
print(f'chi mod: {only2}')
print(f'TextAsset KHAC noi dung: {len(diff)}')
for k in diff:
    print(f'   {k}  ({len(t1[k]):,} -> {len(t2[k]):,} byte)')
