"""MONOPOLY: build mod tach biet cho tung phien ban (Base v1.0 hoac Update v1.6).

- Khi nguoi dung choi Base v1.0 (khong cai update):
    Bundle lay tu E:\MONO_work\data.unity3d (198.295 objects, 2.063 muc text)
    Ghi vao output/.../01002C201BC40000/romfs/Data/data.unity3d

- Khi nguoi dung choi Update v1.6:
    Bundle lay tu dump/01002C201BC40000/... (199.781 objects, 2.106 muc text)
    Ghi vao output/.../01002C201BC40800/romfs/Data/data.unity3d

Chay: python tools/mono_build_dual.py
"""
import html
import json
import os
import re
import struct
import sys
import xml.etree.ElementTree as ET
import UnityPy

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID_BASE = '01002C201BC40000'
TID_UPD = '01002C201BC40800'

vi_path = os.path.join(ROOT, 'games', f'{TID_BASE}_Monopoly', 'translations', 'mono_vi.json')
vi = json.load(open(vi_path, encoding='utf-8'))
print(f'Da nap {len(vi):,} ban dich tieng Viet.')

TAG_T = re.compile(r'<t\b(?:[^>"\']|"[^"]*"|\'[^\']*\')*?>')
TAG_L = re.compile(r'<l\b(?:[^>"\']|"[^"]*"|\'[^\']*\')*?/>')
ATTR_RE = re.compile(r'([A-Za-z_][\w:-]*)\s*=\s*"([^"]*)"')
NS = '{http://schemas.ubisoft.com/oasis/2011/extractor}'


def esc_attr(s):
    s = html.escape(s, quote=True)
    return (s.replace('\r\n', '&#xA;').replace('\n', '&#xA;')
             .replace('\r', '&#xD;').replace('\t', '&#x9;'))


def replace_tags(body, pattern, id2vi):
    out = []
    pos = 0
    n = 0
    for m in pattern.finditer(body):
        tag = m.group(0)
        attrs = ATTR_RE.findall(tag)
        d = dict(attrs)
        if 'id' not in d or 'text' not in d:
            continue
        v = id2vi.get(d['id'])
        if v is None:
            continue
        out.append(body[pos:m.start()])
        parts = [f'{k}="{esc_attr(v) if k == "text" else val}"' for k, val in attrs]
        closing = '/>' if tag.rstrip().endswith('/>') else '>'
        out.append('<t ' + ' '.join(parts) + closing if pattern is TAG_T
                   else '<l ' + ' '.join(parts) + closing)
        pos = m.end()
        n += 1
    out.append(body[pos:])
    return ''.join(out), n


def build_version(src_bundle, target_tid, label):
    print(f'\n======================================================')
    print(f'BAT DAU BUILD CHO: {label}')
    print(f'Nguon: {src_bundle} ({os.path.getsize(src_bundle):,} bytes)')
    print(f'Target TID: {target_tid}')
    print(f'======================================================')

    env = UnityPy.load(src_bundle)
    print(f'Tong objects trong bundle: {len(env.objects):,}')

    # 1. Trich xuat id2vi tu englishgb
    id2vi = {}
    for o in env.objects:
        if o.type.name != 'TextAsset':
            continue
        raw = o.get_raw_data()
        name_len = int.from_bytes(raw[:4], 'little')
        offset = 4 + name_len
        while offset % 4 != 0:
            offset += 1
        data_len = int.from_bytes(raw[offset:offset+4], 'little')
        name = raw[4:4+name_len].decode('utf-8', errors='ignore')
        if name != 'oasis_englishgb':
            continue
        data = raw[offset+4:offset+4+data_len]
        txt = (data[2:] if data.startswith(b'\xff\xfe') else data).decode('utf-16-le')
        root = ET.fromstring(txt)
        for e in list(root.find(f'{NS}translations')):
            id2vi[e.get('id')] = vi.get(e.get('text') or '', e.get('text') or '')

    print(f'Bang id->VI cho {label}: {len(id2vi):,} entries')

    # 2. Thay the trong tat ca 14 TextAsset Oasis
    total = 0
    for o in env.objects:
        if o.type.name != 'TextAsset':
            continue
        raw = o.get_raw_data()
        name_len = int.from_bytes(raw[:4], 'little')
        offset = 4 + name_len
        while offset % 4 != 0:
            offset += 1
        data_len = int.from_bytes(raw[offset:offset+4], 'little')
        name = raw[4:4+name_len].decode('utf-8', errors='ignore')
        if not name.startswith('oasis_'):
            continue

        data = raw[offset+4:offset+4+data_len]
        has_bom = data.startswith(b'\xff\xfe')
        txt = (data[2:] if has_bom else data).decode('utf-16-le')

        if name == 'oasis__global':
            body, n = replace_tags(txt, TAG_L, id2vi)
            tag_label = '<l> (global)'
        else:
            body, n = replace_tags(txt, TAG_T, id2vi)
            tag_label = '<t>'

        if n == 0:
            print(f'  [-] {name:<28} khong thay the duoc muc nao')
            continue

        new_data = (b'\xff\xfe' if has_bom else b'') + body.encode('utf-16-le')

        # Dong goi chuan TextAsset
        name_bytes = name.encode('utf-8')
        buf = struct.pack('<i', len(name_bytes)) + name_bytes
        while len(buf) % 4 != 0:
            buf += b'\x00'
        buf += struct.pack('<i', len(new_data)) + new_data
        while len(buf) % 4 != 0:
            buf += b'\x00'

        o.set_raw_data(buf)
        total += n
        print(f'  [+] {name:<28} thay {n:>5} muc  {tag_label}')

    print(f'Tong cong thay the {total:,} muc text.')

    # 3. Luu bundle
    bf = list(env.files.values())[0]
    print('Dang nen LZ4 va xuat bundle...')
    bundle_bytes = bf.save(packer='original')
    out_dir = os.path.join(ROOT, 'output', 'atmosphere', 'contents', target_tid, 'romfs', 'Data')
    os.makedirs(out_dir, exist_ok=True)
    dst_file = os.path.join(out_dir, 'data.unity3d')
    with open(dst_file, 'wb') as f:
        f.write(bundle_bytes)
    print(f'==> DA XUAT THANH CONG: {dst_file} ({os.path.getsize(dst_file):,} bytes)')


# 1. Build ban Base v1.0 tu E:\MONO_work\data.unity3d
SRC_BASE = r'E:\MONO_work\data.unity3d'
if os.path.exists(SRC_BASE):
    build_version(SRC_BASE, TID_BASE, 'BASE v1.0 (TitleID 01002C201BC40000)')
else:
    print(f'Khong tim thay {SRC_BASE}, bo qua build Base.')

# 2. Build ban Update v1.6 tu dump/01002C201BC40000/romfs/Data/data.unity3d
SRC_UPD = os.path.join(ROOT, 'dump', TID_BASE, 'romfs', 'Data', 'data.unity3d')
if os.path.exists(SRC_UPD):
    build_version(SRC_UPD, TID_UPD, 'UPDATE v1.6 (TitleID 01002C201BC40800)')
else:
    print(f'Khong tim thay {SRC_UPD}, bo qua build Update.')

print('\nBuild Dual Version Monopoly HOAN TAT MY MAN!')
