"""QA CUOI: doi chieu TUNG MUC giua bundle goc va bundle thanh pham MONOPOLY."""
import collections
import io
import json
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
NAME = 'oasis_englishgb'

import UnityPy


def read_entries(path, name=NAME):
    env = UnityPy.load(path)
    n_obj = len(list(env.objects))
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
        tr = root.find(f'{NS}translations')
        # lay ten ngon ngu + cac muc
        return n_obj, (tr.get('language') if tr is not None else '?'), \
               {e.get('id'): (e.get('text') or '') for e in list(tr)}, txt
    return n_obj, '?', {}, ''


print('=== 1. FILE & CAY THU MUC (chi MONOPOLY) ===')
print(f'  goc      : {os.path.getsize(SRC)/1e6:,.1f} MB  {SRC}')
print(f'  thanh pham: {os.path.getsize(DST)/1e6:,.1f} MB  {DST}')
MOD = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID)
for dp, dn, fn in os.walk(MOD):
    rel = os.path.relpath(dp, MOD)
    for f in fn:
        fp = os.path.join(dp, f)
        print(f'    romfs/{(os.path.join(rel, f)).replace(os.sep, "/"):<52} {os.path.getsize(fp)/1e6:>9,.1f} MB')
print(f'  -> duong dan LayeredFS: atmosphere/contents/{TID}/romfs/Data/data.unity3d')

print('\n=== 2. DOC 2 BUNDLE ===')
n1, lang1, src, txt1 = read_entries(SRC)
n2, lang2, dst, txt2 = read_entries(DST)
print(f'  goc      : {n1:,} object | lang={lang1} | {len(src):,} muc')
print(f'  thanh pham: {n2:,} object | lang={lang2} | {len(dst):,} muc')
assert n1 == n2, f'SO OBJECT LECH: {n1} vs {n2}'
print(f'  OK so object khop ({n1:,})')

print('\n=== 3. DOI CHIEU TUNG MUC ===')
only_src = [k for k in src if k not in dst]
only_dst = [k for k in dst if k not in src]
print(f'  chi co o goc: {len(only_src)} | chi co o thanh pham: {len(only_dst)}')

TAG = re.compile(r'\{[^}]*\}|%[sdif]|<[^>]{1,30}>|\[\[[^\]]*\]\]')
def tags(s):
    return sorted(TAG.findall(s or '')), (s or '').count('\n')

FOREIGN = re.compile(r'[\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff00-\uffef'
                     r'\u1100-\u11ff\u3130-\u318f\uac00-\ud7ff\u3040-\u30ff'
                     r'\u0600-\u06ff\ufb50-\ufdff\ufe70-\ufeFF\u0400-\u04ff]')
CTRL = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')

n_tr = 0
bad_tag = []
bad_nl = []
bad_ctrl = []
bad_foreign = []
empty = []
for k in sorted(src, key=lambda x: int(x)):
    a, b = src[k], dst.get(k, '')
    if a == b:
        continue
    n_tr += 1
    ta, na = tags(a)
    tb, nb = tags(b)
    if ta != tb:
        bad_tag.append((k, a, b))
    if na != nb:
        bad_nl.append((k, a, b))
    if CTRL.search(b):
        bad_ctrl.append((k, b))
    if FOREIGN.search(b):
        bad_foreign.append((k, b))
    if not b.strip():
        empty.append((k, a))

print(f'  so muc DA DICH (khac ban goc): {n_tr:,}')
print(f'  lech placeholder/tag : {len(bad_tag)}')
print(f'  lech xuong dong      : {len(bad_nl)}')
print(f'  ky tu dieu khien     : {len(bad_ctrl)}')
print(f'  ky tu ngoai (CJK...) : {len(bad_foreign)}')
print(f'  chuoi rong           : {len(empty)}')

for label, arr in (('TAG', bad_tag), ('NL', bad_nl), ('CTRL', bad_ctrl), ('FOREIGN', bad_foreign), ('EMPTY', empty)):
    for it in arr[:6]:
        print(f'    [{label}] #{it[0]}: {str(it[1])[:55]!r} -> {str(it[2])[:55]!r}')

print('\n=== 4. MAU 12 MUC DA DICH ===')
shown = 0
for k in sorted(src, key=lambda x: int(x)):
    if src[k] != dst.get(k, '') and shown < 12:
        shown += 1
        print(f'  #{k:<6} EN: {src[k][:52]!r}')
        print(f'  {"":<6} VI: {dst[k][:52]!r}')
print('\nKET QUA:', 'PASS' if not (bad_tag or bad_nl or bad_ctrl or empty or only_src or only_dst) else 'CO VAN DE')
