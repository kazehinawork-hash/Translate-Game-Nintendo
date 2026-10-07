"""Boc toan bo chuoi tu kho Oasis cua MONOPOLY + xem tat ca ngon ngu co san."""
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '01002C201BC40000'
G = os.path.join(ROOT, 'games', f'{TID}_Monopoly')
OAS = r'E:\MONO_work\oasis'
NS = '{http://schemas.ubisoft.com/oasis/2011/extractor}'


def load_root(p):
    raw = open(p, 'rb').read()
    txt = raw.decode('utf-16', 'replace')
    i = txt.find('<')
    return ET.fromstring(txt[i:])


items = []
for fn in sorted(os.listdir(OAS)):
    if not fn.startswith('oasis_') or fn == 'oasis__global.bin':
        continue
    p = os.path.join(OAS, fn)
    root = load_root(p)
    tr = root.find(f'{NS}translations')
    lang = tr.get('language') if tr is not None else '?'
    ents = list(tr) if tr is not None else []
    print(f'{fn:<32} lang={lang:<22} {len(ents)} muc')
    if 'englishgb' in fn.lower():
        for e in ents:
            items.append({'id': e.get('id'), 'en': e.get('text') or ''})

os.makedirs(os.path.join(G, 'translations'), exist_ok=True)
json.dump(items, open(os.path.join(G, 'translations', 'mono_en.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print(f'\nBOC DUOC {len(items):,} chuoi tieng Anh -> translations/mono_en.json')
lens = sorted(len(i['en']) for i in items)
print(f'  do dai: min {lens[0]} | trung vi {lens[len(lens)//2]} | max {lens[-1]}')
print('\nvi du:')
for i in items[:12]:
    print(f'  #{i["id"]:<6} {i["en"][:70]!r}')
