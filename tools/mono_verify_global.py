"""Xac minh oasis__global trong ca 2 ban mod: cac muc <l id= text=> da thanh tieng Viet chua."""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import UnityPy

TARGETS = {
    'v16 (ID update)': os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01002C201BC40800',
                                    'romfs', 'Data', 'data.unity3d'),
    'base (ID base)': os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01002C201BC40000',
                                   'romfs', 'Data', 'data.unity3d'),
}


def check(label, p):
    if not os.path.exists(p):
        print(f'  [{label}] khong co file')
        return
    env = UnityPy.load(p)
    for o in env.objects:
        if o.type.name != 'TextAsset':
            continue
        d = o.read()
        if getattr(d, 'm_Name', '') != 'oasis__global':
            continue
        raw = o.get_raw_data()
        j = raw.find(b'<')
        txt = raw[j:].decode('utf-16-le', errors='replace')
        ids = {}
        for t in re.findall(r'<l\b[^>]*/>', txt):
            m = re.search(r'id="(\d+)"', t)
            mt = re.search(r'text="([^"]*)"', t)
            if m and mt:
                ids[m.group(1)] = mt.group(1)
        nvi = sum(1 for v in ids.values() if any(ord(c) > 127 for c in v))
        print(f'  [{label}] {os.path.getsize(p):,} b | oasis__global: {len(ids)} muc | {nvi} muc co dau')
        for i in ('5', '6', '433', '434', '435', '436'):
            print(f'        id={i}: {ids.get(i, "(khong co)")[:44]!r}')
        # cung kiem tra file ngon ngu chinh
        for o2 in env.objects:
            if o2.type.name != 'TextAsset':
                continue
            d2 = o2.read()
            if getattr(d2, 'm_Name', '') != 'oasis_englishgb':
                continue
            raw2 = o2.get_raw_data()
            j2 = raw2.find(b'<')
            t2 = raw2[j2:].decode('utf-16-le', errors='replace')
            ts = {}
            for tag in re.findall(r'<t\b[^>]*/>', t2):
                m = re.search(r'id="(\d+)"', tag)
                mt = re.search(r'text="([^"]*)"', tag)
                if m and mt:
                    ts[m.group(1)] = mt.group(1)
            nvi2 = sum(1 for v in ts.values() if any(ord(c) > 127 for c in v))
            print(f'        oasis_englishgb: {len(ts)} muc | {nvi2} muc co dau')
            break
        break


for label, p in TARGETS.items():
    check(label, p)
    print()
