"""Kiem tra: doan canh bao dong kinh (epilepsy) co nam trong bang Oasis khong, va da dich chua."""
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = '{http://schemas.ubisoft.com/oasis/2011/extractor}'
import UnityPy

SRC = os.path.join(ROOT, 'dump', '01002C201BC40000', 'romfs', 'Data', 'data.unity3d')
DST = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01002C201BC40000', 'romfs', 'Data', 'data.unity3d')

WANT = ('epilep', 'READ BEFORE PLAYING', 'dizziness', 'implanted medical', 'Take regular breaks')


def get_entries(path, name='oasis_englishgb'):
    env = UnityPy.load(path)
    for o in env.objects:
        if o.type.name != 'TextAsset':
            continue
        d = o.read()
        if getattr(d, 'm_Name', '') != name:
            continue
        raw = o.get_raw_data()
        j = raw.find(b'<')
        txt = raw[j:].decode('utf-16-le')
        root = ET.fromstring(txt)
        return {e.get('id'): (e.get('text') or '') for e in list(root.find(f'{NS}translations'))}
    return {}


src = get_entries(SRC)
dst = get_entries(DST)
print(f'nguon v1.6: {len(src)} id | mod: {len(dst)} id\n')

for kw in WANT:
    hits = [(i, t) for i, t in src.items() if kw.lower() in t.lower()]
    print(f'--- "{kw}": {len(hits)} muc trong bang dich')
    for i, t in hits[:3]:
        print(f'    #{i}: EN = {t[:70]!r}')
        print(f'          VI = {dst.get(i, "(khong co)")[:70]!r}')

# kiem tra tong quat: bao nhieu muc trong mod da doi so voi goc
diff = [i for i in src if dst.get(i) != src[i]]
print(f'\ntong muc KHAC giua goc va mod: {len(diff)}/{len(src)}')
print('  (neu gan bang tong so muc => mod DA duoc nap dung; neu ~0 => chua nap mod)')
