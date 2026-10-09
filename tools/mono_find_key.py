"""Tim khoa 'Menu/OnlineGame/OnlinePlay/Crossplay' trong bundle, ca UTF-16 lan UTF-8,
va liet ke moi TextAsset co chua 'oasis' / localization.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUNDLES = {
    'GOC v1.6': os.path.join(ROOT, 'dump', '01002C201BC40000', 'romfs', 'Data', 'data.unity3d'),
    'MOD v1.6': os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01002C201BC40800', 'romfs', 'Data', 'data.unity3d'),
}
import UnityPy

KEYS = ['Menu/OnlineGame/OnlinePlay/Crossplay', 'Menu/OnlineGame/Crossplay_Body', 'OnlineGame/OnlinePlay']
NEEDLES = []
for k in KEYS:
    NEEDLES.append((k + ' [utf16]', k.encode('utf-16-le')))
    NEEDLES.append((k + ' [utf8]', k.encode('utf-8')))

path = BUNDLES['GOC v1.6']
print(f'=== {path} ({os.path.getsize(path):,} b) ===')
env = UnityPy.load(path)
allnames = []
for o in env.objects:
    if o.type.name != 'TextAsset':
        continue
    d = o.read()
    nm = getattr(d, 'm_Name', '')
    raw = o.get_raw_data()
    allnames.append((nm, len(raw)))
    for label, nb in NEEDLES:
        if nb in raw:
            print(f'  {nm}: TIM THAY {label} (x{raw.count(nb)})')

print(f'\n  tong TextAsset: {len(allnames)}')
loc = [n for n, _ in allnames if any(s in n.lower() for s in ('oasis', 'loc', 'text', 'lang', 'string'))]
print('  cac TextAsset lien quan ban dich:')
for n, sz in sorted(allnames):
    if n in loc or n.startswith('oasis') or 'loc' in n.lower():
        print(f'    {n:<34} {sz:>10,} b')

# in cau truc file oasis__global (no khong co <translations>)
for o in env.objects:
    if o.type.name != 'TextAsset':
        continue
    d = o.read()
    if getattr(d, 'm_Name', '') != 'oasis__global':
        continue
    raw = o.get_raw_data()
    j = raw.find(b'<')
    txt = raw[j:].decode('utf-16-le', errors='replace')
    print(f'\n  --- oasis__global, 40 dong dau ---')
    for ln in txt.splitlines()[:40]:
        print('    | ' + ln[:150])
