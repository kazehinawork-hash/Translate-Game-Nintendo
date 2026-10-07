"""MONOPOLY: ghi ban dich vao XML Oasis (thay thuoc tinh text=) roi dong goi lai bundle."""
import html
import json
import os
import re
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '01002C201BC40000'
G = os.path.join(ROOT, 'games', f'{TID}_Monopoly')
vi = json.load(open(os.path.join(G, 'translations', 'mono_vi.json'), encoding='utf-8'))
print(f'{len(vi):,} ban dich')

import UnityPy

SRC = r'E:\MONO_work\data.unity3d'
OUT = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'Data')
os.makedirs(OUT, exist_ok=True)

env = UnityPy.load(SRC)
LANG_FILES = ['oasis_englishgb']          # co the them cac file ngon ngu khac

TEXT_ATTR = re.compile(rb'text="(.*?)"')


def esc_attr(s):
    """Escape gia tri thuoc tinh XML. QUAN TRONG: \\n phai la &#xA; (KHONG duoc ghi
    xuong dong THAT - XML chuan hoa thuoc tinh se bien no thanh dau cach => mat ngat dong)."""
    s = html.escape(s, quote=True)
    return (s.replace('\r\n', '&#xA;').replace('\n', '&#xA;')
             .replace('\r', '&#xD;').replace('\t', '&#x9;'))


def patch_asset(o):
    d = o.read()
    if getattr(d, 'm_Name', '') not in LANG_FILES:
        return 0
    raw = o.get_raw_data()
    j = raw.find(b'<')
    if j < 0:
        print('  khong thay the <'); return 0
    prefix = raw[:j]
    body = raw[j:].decode('utf-16-le')

    n = 0
    def sub(m):
        nonlocal n
        raw_txt = m.group(1).decode('utf-16-le') if isinstance(m.group(1), bytes) else m.group(1)
        en = html.unescape(raw_txt)
        if en in vi:
            n += 1
            return 'text="' + esc_attr(vi[en]) + '"'
        return m.group(0)

    body2 = re.sub(r'text="([^"]*)"', sub, body)
    data = prefix + body2.encode('utf-16-le')
    if n == 0:
        print('  khong thay muc nao')
        return 0

    # dong goi lai TextAsset: [int32 nameLen][name][align4][int32 dataLen][data]
    name = getattr(d, 'm_Name', '').encode('utf-8')
    buf = struct.pack('<i', len(name)) + name
    while len(buf) % 4:
        buf += b'\x00'
    buf += struct.pack('<i', len(data)) + data
    o.set_raw_data(buf)
    print(f'  {getattr(d,"m_Name","?"):<22} thay {n} muc | raw {len(raw):,} -> {len(buf):,}')
    return n


total = 0
for o in env.objects:
    if o.type.name == 'TextAsset':
        total += patch_asset(o)
print(f'tong thay {total} muc')

if total:
    env.save(pack='original', out_path=OUT)   # giu nguyen kieu nen cua bundle goc
    outfile = os.path.join(OUT, 'data.unity3d')
    print(f'da ghi bundle: {outfile} ({os.path.getsize(outfile)/1e6:.1f} MB)')
