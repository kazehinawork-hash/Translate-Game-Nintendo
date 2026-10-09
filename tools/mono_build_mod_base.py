"""MONOPOLY: build mod tu bundle BASE v1.0 (de dung khi TAT ban update).

Vi sao: mod o ID base bi ban update v1.6 ghi de -> game van doc du lieu goc.
Neu game chay base v1.0 (tat update) ma mod lai la ban v1.6 -> lech phien ban -> treo splash.
=> Dung cap khop: game v1.0  <->  mod build tu bundle v1.0.

Ghi vao: output/atmosphere/contents/01002C201BC40000/romfs/Data/data.unity3d
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
TID = '01002C201BC40000'
vi = json.load(open(os.path.join(ROOT, 'games', f'{TID}_Monopoly', 'translations', 'mono_vi.json'),
                   encoding='utf-8'))
print(f'{len(vi):,} ban dich')

NS = '{http://schemas.ubisoft.com/oasis/2011/extractor}'
import UnityPy

SRC = r'E:\MONO_work\data.unity3d'          # <-- bundle BASE v1.0 (520.071.132 b)
OUT = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'Data')
assert os.path.exists(SRC), f'khong thay {SRC}'
print(f'nguon: {SRC} ({os.path.getsize(SRC):,} b)')

TAG_RE = re.compile(r'<t\b(?:[^>"\']|"[^"]*"|\'[^\']*\')*?>')
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
print(f'tim thay {len(assets)} TextAsset oasis_*')

id2vi = {}
srcfile = None
for o, nm, prefix, txt, tail, enc in assets:
    if nm != 'oasis_englishgb':
        continue
    root = ET.fromstring(txt)
    ents = {e.get('id'): (e.get('text') or '') for e in list(root.find(f'{NS}translations'))}
    for tid, en in ents.items():
        id2vi[tid] = vi.get(en, en)
    srcfile = (nm, len(ents))
print(f'nguon {srcfile[0]}: {srcfile[1]:,} id -> bang id->VI: {len(id2vi):,}')


def replace_by_id(body):
    out = []
    pos = 0
    n = 0
    for m in TAG_RE.finditer(body):
        tag = m.group(0)
        attrs = ATTR_RE.findall(tag)
        d = dict(attrs)
        v = id2vi.get(d.get('id')) if d.get('id') else None
        if v is None:
            continue
        out.append(body[pos:m.start()])
        parts = [f'{k}="{esc_attr(v) if k == "text" else val}"' for k, val in attrs]
        closing = '/>' if tag.rstrip().endswith('/>') else '>'
        out.append('<t ' + ' '.join(parts) + closing)
        pos = m.end()
        n += 1
    out.append(body[pos:])
    return ''.join(out), n


total = 0
for o, nm, prefix, txt, tail, enc in assets:
    body, n = replace_by_id(txt)
    if n == 0:
        print(f'  [-] {nm:<28} KHONG thay duoc muc nao (khong phai file dich?)')
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
    print(f'  [+] {nm:<28} thay {n:>5} muc')

print(f'\ntong thay {total} muc')
if total:
    env.save(pack='original', out_path=OUT)
    p = os.path.join(OUT, 'data.unity3d')
    print(f'da ghi bundle: {os.path.getsize(p):,} b ({os.path.getsize(p)/1e6:.1f} MB)')
