"""Tim trong bundle v1.6 cach luu cac muc dang 'Menu/OnlineGame/...' (key duong dan)
va kiem tra ban dich cua mod co cham toi chung khong.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUMP = os.path.join(ROOT, 'dump', '01002C201BC40000', 'romfs', 'Data', 'data.unity3d')
MOD = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01002C201BC40800', 'romfs', 'Data', 'data.unity3d')
import UnityPy

TARGETS = [b'Crossplay', b'OnlinePlay', b'Menu/OnlineGame', b'NO_TRANS']


def scan(path, label):
    print(f'\n=== {label}: {path} ({os.path.getsize(path):,} b) ===')
    if not os.path.exists(path):
        print('  khong co file')
        return
    env = UnityPy.load(path)
    for o in env.objects:
        if o.type.name != 'TextAsset':
            continue
        d = o.read()
        nm = getattr(d, 'm_Name', '')
        raw = o.get_raw_data()
        hits = [t.decode() for t in TARGETS if t in raw]
        if not hits:
            continue
        print(f'  {nm}: co {hits}')
        # tim cac tag <t ...> chua Crossplay / key
        j = raw.find(b'<')
        txt = raw[j:].decode('utf-16-le', errors='replace')
        for m in re.finditer(r'<t\b[^>]*>', txt):
            tag = m.group(0)
            if 'Crossplay' in tag or 'OnlinePlay' in tag or 'key=' in tag:
                print('      ' + tag[:220])
        # dong dau file (khai bao)
        for ln in txt.splitlines()[:6]:
            print('      | ' + ln[:160])


scan(DUMP, 'BUNDLE GOC v1.6')
scan(MOD, 'BAN MOD (v1.6)')
