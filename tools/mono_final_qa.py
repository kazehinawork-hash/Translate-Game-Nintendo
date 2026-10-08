"""QA CUOI (v2): kiem chung CA 13 file ngon ngu MONOPOLY."""
import html
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '01002C201BC40000'
SRC = r'E:\MONO_work\data.unity3d'
DST = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'Data', 'data.unity3d')
NS = '{http://schemas.ubisoft.com/oasis/2011/extractor}'

import UnityPy

TAG_RE = re.compile(r'<t\b(?:[^>"\']|"[^"]*"|\'[^\']*\')*?>')
ATTR_RE = re.compile(r'([A-Za-z_][\w:-]*)\s*=\s*"([^"]*)"')


def load_asset(raw):
    best = None
    for enc in ('utf-16-le', 'utf-16-be', 'utf-8'):
        for marker in ('<?xml', '<oasis'):
            i = raw.find(marker.encode(enc))
            if i >= 0 and (best is None or i < best[0]):
                best = (i, enc)
    if best is None:
        return None, None
    i, enc = best
    try:
        txt = raw[i:].decode(enc)
    except Exception:
        return None, None
    return txt.rstrip('\x00'), enc


def read_all(path):
    """-> {ten_file: {id: text}}"""
    env = UnityPy.load(path)
    n_obj = len(list(env.objects))
    out = {}
    for o in env.objects:
        if o.type.name != 'TextAsset':
            continue
        d = o.read()
        nm = getattr(d, 'm_Name', '')
        if not nm.startswith('oasis_'):
            continue
        txt, enc = load_asset(o.get_raw_data())
        if txt is None:
            continue
        ents = {}
        for m in TAG_RE.finditer(txt):
            at = dict(ATTR_RE.findall(m.group(0)))
            if 'id' in at and 'text' in at:
                ents[at['id']] = html.unescape(at['text'])
        if ents:
            out[nm] = ents
    return n_obj, out


print('=== DOC 2 BUNDLE ===')
n1, src = read_all(SRC)
n2, dst = read_all(DST)
print(f'  object: goc {n1:,} | thanh pham {n2:,}  -> {"KHOP" if n1 == n2 else "LECH!"}')
print(f'  file ngon ngu: goc {len(src)} | thanh pham {len(dst)}')
for k in sorted(src):
    print(f'    {k:<30} goc {len(src[k]):>5} muc | thanh pham {len(dst.get(k, {})):>5} muc')

TAG = re.compile(r'\{[^}]*\}|%[sdif]|<[^>]{1,30}>|\[\[[^\]]*\]\]')
FOREIGN = re.compile(r'[\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff00-\uffef'
                     r'\u1100-\u11ff\u3130-\u318f\uac00-\ud7ff\u3040-\u30ff'
                     r'\u0600-\u06ff\ufb50-\ufdff\ufe70-\ufeFF\u0400-\u04ff]')

print('\n=== KIEM TRA TUNG FILE ===')
en = dst['oasis_englishgb']
ref_tags = {i: sorted(TAG.findall(t)) for i, t in en.items()}
ref_nl = {i: t.count('\n') for i, t in en.items()}

bad = 0
for nm in sorted(dst):
    ents = dst[nm]
    ids_missing = [i for i in src.get(nm, {}) if i not in ents]
    ids_extra = [i for i in ents if i not in src.get(nm, {})]
    diff_from_en = [i for i, t in ents.items() if t != en.get(i)]
    tbad = [i for i, t in ents.items() if sorted(TAG.findall(t)) != ref_tags.get(i)]
    nlb = [i for i, t in ents.items() if t.count('\n') != ref_nl.get(i)]
    # chi bao ky tu la MOI sinh ra (ky tu da co san trong nguon cua chinh id do thi bo qua)
    fbad = [i for i, t in ents.items()
            if set(FOREIGN.findall(t)) - set(FOREIGN.findall(src.get('oasis_englishgb', {}).get(i, '')))]
    ebad = [i for i, t in ents.items() if not t.strip()]
    if fbad and nm == 'oasis_englishgb':
        print(f'    (ky tu la moi sinh: {len(fbad)} muc)')
        for i in fbad[:12]:
            print(f'      id {i}: {ents[i][:60]!r}')
    leak = [i for i, t in ents.items() if t == src.get(nm, {}).get(i) and nm != 'oasis_englishgb']
    flag = ''
    if ids_missing or ids_extra or diff_from_en or tbad or nlb or fbad or ebad:
        flag = '  <<< VAN DE'
        bad += 1
    print(f'  {nm:<30} id: {len(ents):>5} | lech tieng Viet: {len(diff_from_en):>4} | '
          f'tag:{len(tbad)} nl:{len(nlb)} la:{len(fbad)} rong:{len(ebad)} | '
          f'id thua:{len(ids_extra)} thieu:{len(ids_missing)}{flag}')

print('\n=== DOI CHIEU NGON NGU GOC vs BAN DICH (xac nhan id khop) ===')
for i in ('5', '6', '7', '3290'):
    print(f'  id {i}:')
    for nm in ('oasis_englishgb', 'oasis_german', 'oasis_japanese', 'oasis_spanish', 'oasis_russian'):
        if nm in src and nm in dst:
            print(f'    {nm:<24} goc={src[nm].get(i, "")[:26]!r:<30} -> VI={dst[nm].get(i, "")[:26]!r}')

print('\nKET QUA:', 'PASS' if bad == 0 else f'CO VAN DE o {bad} file')
