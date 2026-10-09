"""Xac minh bundle Monopoly bang REGEX (khong dung XML parser - file goc co XML hong san o dong 2068)."""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TID = '01002C201BC40000'
P = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'Data', 'data.unity3d')

import UnityPy

TAG_RE = re.compile(r'<t\b(?:[^>"\']|"[^"]*"|\'[^\']*\')*?>')
ATTR_RE = re.compile(r'([A-Za-z_][\w:-]*)\s*=\s*"([^"]*)"')

env = UnityPy.load(P)
print(f'bundle: {os.path.getsize(P):,} b | object: {len(list(env.objects)):,}')
for o in env.objects:
    if o.type.name != 'TextAsset':
        continue
    d = o.read()
    nm = getattr(d, 'm_Name', '')
    if not nm.startswith('oasis_') or nm == 'oasis__global':
        continue
    raw = o.get_raw_data()
    j = raw.find(b'<')
    txt = raw[j:].decode('utf-16-le', errors='replace').rstrip('\x00')
    tot = 0
    vi = 0
    sample = []
    for m in TAG_RE.finditer(txt):
        attrs = dict(ATTR_RE.findall(m.group(0)))
        if 'id' not in attrs:
            continue
        tot += 1
        t = attrs.get('text', '')
        if any(ord(c) > 127 for c in t):
            vi += 1
            if len(sample) < 3:
                sample.append(f'#{attrs["id"]}={t[:28]}')
    flag = 'OK ' if vi > 1500 else 'LOI'
    print(f'  [{flag}] {nm:<28} {tot:>5} muc | {vi:>5} muc co dau | {" ".join(sample)}')
