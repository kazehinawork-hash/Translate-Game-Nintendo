"""MONOPOLY: build mod vá CA `oasis__global` (bang text cua ngon ngu master "English").

Khac ban cu: ban cu chi vá cac file `<translations>` (13 file ngon ngu) va BO QUA oasis__global.
Nhung oasis__global cung chua 2.106 muc `<l id= text=>` CUNG KHONG GIAN id -> do la bang text
cua ngon ngu master. Neu game dat ngon ngu "English" thi no doc o day -> van tieng Anh.

Script nay vá CA HAI dang the: `<t id= text=>` (13 file) va `<l id= text=>` (oasis__global).

Dung: python tools/mono_build_mod_all.py [base|v16]
"""
import html
import json
import os
import re
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '01002C201BC40000'
MODE = (sys.argv[1] if len(sys.argv) > 1 else 'v16').lower()

if MODE == 'base':
    SRC = r'E:\MONO_work\data.unity3d'
    OUTDIR = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'Data')
    print('=== BUILD TU BUNDLE BASE v1.0 -> ID base ===')
else:
    SRC = os.path.join(ROOT, 'dump', TID, 'romfs', 'Data', 'data.unity3d')
    OUTDIR = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01002C201BC40800', 'romfs', 'Data')
    print('=== BUILD TU BUNDLE v1.6 -> ID update ===')

vi = json.load(open(os.path.join(ROOT, 'games', f'{TID}_Monopoly', 'translations', 'mono_vi.json'),
                   encoding='utf-8'))
print(f'{len(vi):,} ban dich | nguon: {SRC} ({os.path.getsize(SRC):,} b)')

NS = '{http://schemas.ubisoft.com/oasis/2011/extractor}'
import UnityPy
import xml.etree.ElementTree as ET

TAG_T = re.compile(r'<t\b(?:[^>"\']|"[^"]*"|\'[^\']*\')*?>')
TAG_L = re.compile(r'<l\b(?:[^>"\']|"[^"]*"|\'[^\']*\')*?/>')
ATTR_RE = re.compile(r'([A-Za-z_][\w:-]*)\s*=\s*"([^"]*)"')


def esc_attr(s):
    s = html.escape(s, quote=True)
    return (s.replace('\r\n', '&#xA;').replace('\n', '&#xA;')
             .replace('\r', '&#xD;').replace('\t', '&#x9;'))


def load_asset(raw):
    best = None
    for enc in ('utf-16-le', 'utf-16-be', 'utf-8'):
        for marker in ('<?xml', '<oasis'):
            i = raw.find(marker.encode(enc))
            if i >= 0 and (best is None or i < best[0]):
                best = (i, enc)
    if best is None:
        return None
    i, enc = best
    try:
        txt = raw[i:].decode(enc)
    except Exception:
        return None
    txt = txt.rstrip('\x00')
    tail = raw[i + len(txt.encode(enc)):]
    return raw[:i], txt, tail, enc


env = UnityPy.load(SRC)
assets = []
for o in env.objects:
    if o.type.name != 'TextAsset':
        continue
    d = o.read()
    nm = getattr(d, 'm_Name', '')
    if not nm.startswith('oasis_'):
        continue
    got = load_asset(o.get_raw_data())
    if got is None:
        print(f'  [!] {nm}: khong tim thay XML')
        continue
    assets.append((o, nm, *got))

# bang id -> VI lay tu englishgb
id2vi = {}
for o, nm, prefix, txt, tail, enc in assets:
    if nm != 'oasis_englishgb':
        continue
    root = ET.fromstring(txt)
    for e in list(root.find(f'{NS}translations')):
        id2vi[e.get('id')] = vi.get(e.get('text') or '', e.get('text') or '')
print(f'bang id->VI: {len(id2vi):,}')


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


total = 0
for o, nm, prefix, txt, tail, enc in assets:
    if nm == 'oasis__global':
        body, n = replace_tags(txt, TAG_L)      # <l id= text=>
        label = '<l> (bang master)'
    else:
        body, n = replace_tags(txt, TAG_T)      # <t id= text=>
        label = '<t>'
    if n == 0:
        print(f'  [-] {nm:<28} khong thay duoc muc nao')
        continue
    data = prefix + body.encode('utf-16-le') + tail
    name = nm.encode('utf-8')
    buf = struct.pack('<i', len(name)) + name
    while len(buf) % 4:
        buf += b'\x00'
    buf += struct.pack('<i', len(data)) + data
    while len(buf) % 4:
        buf += b'\x00'
    o.set_raw_data(buf)
    total += n
    print(f'  [+] {nm:<28} thay {n:>5} muc  {label}')

print(f'\ntong thay {total} muc')
if total:
    env.save(pack='original', out_path=OUTDIR)
    p = os.path.join(OUTDIR, 'data.unity3d')
    print(f'da ghi: {p} ({os.path.getsize(p):,} b)')
