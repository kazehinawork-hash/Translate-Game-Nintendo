"""Kiem tra bundle v1.6 trong ban dump: TextAsset oasis_* va so muc."""
import os
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUMP = os.path.join(ROOT, 'dump', '01002C201BC40000', 'romfs', 'Data', 'data.unity3d')
BASE = r'E:\MONO_work\data.unity3d'
NS = '{http://schemas.ubisoft.com/oasis/2011/extractor}'
import UnityPy


def load(p):
    env = UnityPy.load(p)
    n_obj = len(list(env.objects))
    out = {}
    for o in env.objects:
        if o.type.name != 'TextAsset':
            continue
        d = o.read()
        nm = getattr(d, 'm_Name', '')
        raw = o.get_raw_data()
        out[nm] = (raw, d)
    return n_obj, out


for label, p in (('BASE v1.0', BASE), ('DUMP v1.6', DUMP)):
    if not os.path.exists(p):
        print(f'{label}: khong co file {p}'); continue
    n, tas = load(p)
    print(f'\n=== {label} ({os.path.getsize(p):,} b) ===')
    print(f'  object: {n:,} | TextAsset: {len(tas)}')
    for nm in sorted(k for k in tas if k.startswith('oasis_')):
        raw, d = tas[nm]
        try:
            j = raw.find(b'<')
            txt = raw[j:].decode('utf-16-le') if j >= 0 else ''
            root = ET.fromstring(txt)
            tr = root.find(f'{NS}translations')
            ent = list(tr) if tr is not None else []
            print(f'    {nm:<30} {len(raw):>9,} b | {len(ent):>5} muc | lang={tr.get("language") if tr is not None else "-"}')
        except Exception as e:
            print(f'    {nm:<30} {len(raw):>9,} b | loi {type(e).__name__}')
