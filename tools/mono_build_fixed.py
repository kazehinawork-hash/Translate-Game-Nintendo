"""MONOPOLY: build mod chuan xac, sua dut diem loi [NO_ID].

Nguyen nhan loi [NO_ID]:
  Ban build truoc pack sai header TextAsset (gap doi name + data_len) -> offset lech
  -> game khong doc duoc XML tu dien -> hien [NO_ID]Menu/...

Script nay:
  1. Trích dung byte data cua TextAsset tu offset [4 + name_len + pad + 4].
  2. Thay noi dung bang id tu mono_vi.json (13 file <t> va oasis__global <l>).
  3. Dong goi lai TextAsset voi byte header chuan xac 100% cua Unity.
  4. Ghi bundle da dong goi ra CA HAI Title ID (base 0000 va update 0800).
"""
import html
import json
import os
import re
import struct
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID_BASE = '01002C201BC40000'
TID_UPD = '01002C201BC40800'

SRC = os.path.join(ROOT, 'dump', TID_BASE, 'romfs', 'Data', 'data.unity3d')
assert os.path.exists(SRC), f'Khong tim thay dump tai: {SRC}'

OUT_DIRS = [
    os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID_BASE, 'romfs', 'Data'),
    os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID_UPD, 'romfs', 'Data'),
]

vi_path = os.path.join(ROOT, 'games', f'{TID_BASE}_Monopoly', 'translations', 'mono_vi.json')
vi = json.load(open(vi_path, encoding='utf-8'))
print(f'Da nap {len(vi):,} ban dich | Nguon dump v1.6: {SRC} ({os.path.getsize(SRC):,} bytes)')

import UnityPy

TAG_T = re.compile(r'<t\b(?:[^>"\']|"[^"]*"|\'[^\']*\')*?>')
TAG_L = re.compile(r'<l\b(?:[^>"\']|"[^"]*"|\'[^\']*\')*?/>')
ATTR_RE = re.compile(r'([A-Za-z_][\w:-]*)\s*=\s*"([^"]*)"')


def esc_attr(s):
    s = html.escape(s, quote=True)
    return (s.replace('\r\n', '&#xA;').replace('\n', '&#xA;')
             .replace('\r', '&#xD;').replace('\t', '&#x9;'))


env = UnityPy.load(SRC)

# 1. Trích xuất text từ oasis_englishgb để tạo id2vi
id2vi = {}
NS = '{http://schemas.ubisoft.com/oasis/2011/extractor}'

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
    if data.startswith(b'\xff\xfe'):
        txt = data[2:].decode('utf-16-le')
    else:
        txt = data.decode('utf-16-le')
    root = ET.fromstring(txt)
    for e in list(root.find(f'{NS}translations')):
        id2vi[e.get('id')] = vi.get(e.get('text') or '', e.get('text') or '')

print(f'Bang id->VI: {len(id2vi):,} entries')


def replace_tags(body, pattern):
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


# 2. Thay thế dữ liệu trong tất cả 14 TextAsset oasis_*
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
    if has_bom:
        txt = data[2:].decode('utf-16-le')
    else:
        txt = data.decode('utf-16-le')

    if name == 'oasis__global':
        body, n = replace_tags(txt, TAG_L)
        label = '<l> (global)'
    else:
        body, n = replace_tags(txt, TAG_T)
        label = '<t>'

    if n == 0:
        print(f'  [-] {name:<28} khong thay the duoc muc nao')
        continue

    new_data = (b'\xff\xfe' if has_bom else b'') + body.encode('utf-16-le')

    # Đóng gói chuẩn TextAsset
    name_bytes = name.encode('utf-8')
    buf = struct.pack('<i', len(name_bytes)) + name_bytes
    while len(buf) % 4 != 0:
        buf += b'\x00'
    buf += struct.pack('<i', len(new_data)) + new_data
    while len(buf) % 4 != 0:
        buf += b'\x00'

    o.set_raw_data(buf)
    total += n
    print(f'  [+] {name:<28} thay {n:>5} muc  {label}')

print(f'\nTong cong da thay the {total:,} muc text.')

# 3. Luu bundle truc tiep qua BundleFile.save(packer="original")
bf = list(env.files.values())[0]
print('Dang nen va xuat bundle (giu nguyen LZ4 cua file goc)...')
bundle_bytes = bf.save(packer='original')
print(f'Bundle thanh pham: {len(bundle_bytes):,} bytes ({len(bundle_bytes)/1e6:.1f} MB)')

for out_dir in OUT_DIRS:
    os.makedirs(out_dir, exist_ok=True)
    dst_file = os.path.join(out_dir, 'data.unity3d')
    with open(dst_file, 'wb') as f:
        f.write(bundle_bytes)
    print(f'Da ghi: {dst_file} ({os.path.getsize(dst_file):,} bytes)')

print('\nBuild mod Monopoly HOAN TAT!')
