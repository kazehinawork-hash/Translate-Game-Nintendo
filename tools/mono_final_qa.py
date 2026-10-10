"""QA CUOI MONOPOLY: kiem chung CA 2 ban mod theo dung cap phien ban.

- BASE  v1.0 : output/.../01002C201BC40000  <-> bundle goc v1.0 (E:\\MONO_work\\data.unity3d)
- UPDATE v1.6: output/.../01002C201BC40800  <-> dump v1.6 (dump/01002C201BC40000/romfs/Data/data.unity3d)

Chay tu goc du an: python tools/mono_final_qa.py
"""
import html
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'

import UnityPy

TAG_RE = re.compile(r'<t\b(?:[^>"\']|"[^"]*"|\'[^\']*\')*?>')
ATTR_RE = re.compile(r'([A-Za-z_][\w:-]*)\s*=\s*"([^"]*)"')
TAG = re.compile(r'\{[^}]*\}|%[sdif]|<[^>]{1,30}>|\[\[[^\]]*\]\]')
FOREIGN = re.compile(r'[\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff00-\uffef'
                     r'\u1100-\u11ff\u3130-\u318f\uac00-\ud7ff\u3040-\u30ff'
                     r'\u0600-\u06ff\ufb50-\ufdff\ufe70-\ufeFF\u0400-\u04ff]')

PAIRS = [
    ('BASE v1.0', os.path.join(ROOT, 'output', 'atmosphere', 'contents',
                               '01002C201BC40000', 'romfs', 'Data', 'data.unity3d'),
     r'E:\MONO_work\data.unity3d'),
    ('UPDATE v1.6', os.path.join(ROOT, 'output', 'atmosphere', 'contents',
                                 '01002C201BC40800', 'romfs', 'Data', 'data.unity3d'),
     os.path.join(ROOT, 'dump', '01002C201BC40000', 'romfs', 'Data', 'data.unity3d')),
]


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
        return raw[i:].decode(enc).rstrip('\x00')
    except Exception:
        return None


def read_all(path):
    """-> (so_object, {ten_file: {id: text}})"""
    env = UnityPy.load(path)
    n_obj = len(list(env.objects))
    out = {}
    for o in env.objects:
        if o.type.name != 'TextAsset':
            continue
        nm = getattr(o.read(), 'm_Name', '')
        if not nm.startswith('oasis_'):
            continue
        txt = load_asset(o.get_raw_data())
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


def check_pair(label, dst_path, src_path):
    print(f'\n{"=" * 62}\n=== {label} ===\n  goc   : {src_path}\n  mod   : {dst_path}\n{"=" * 62}')
    if not os.path.exists(src_path):
        print('  [!] KHONG TIM THAY bundle goc -> BO QUA cap nay.')
        return None
    if not os.path.exists(dst_path):
        print('  [!] KHONG TIM THAY mod -> BO QUA cap nay.')
        return None

    n_src, src = read_all(src_path)
    n_dst, dst = read_all(dst_path)
    print(f'  object: goc {n_src:,} | mod {n_dst:,}  -> {"KHOP" if n_src == n_dst else "LECH!"}')
    print(f'  file ngon ngu: goc {len(src)} | mod {len(dst)}')

    en = dst.get('oasis_englishgb', {})
    src_en = src.get('oasis_englishgb', {})
    ref_tags = {i: sorted(TAG.findall(t)) for i, t in en.items()}
    ref_nl = {i: t.count('\n') for i, t in en.items()}

    print('\n  --- Kiem tra tung file ---')
    bad = 0
    if n_src != n_dst:
        bad += 1
    if len(src) != len(dst):
        bad += 1
    for nm in sorted(dst):
        ents = dst[nm]
        ids_missing = [i for i in src.get(nm, {}) if i not in ents]
        ids_extra = [i for i in ents if i not in src.get(nm, {})]
        diff_from_en = [i for i, t in ents.items() if t != en.get(i)]
        tbad = [i for i, t in ents.items() if sorted(TAG.findall(t)) != ref_tags.get(i)]
        nlb = [i for i, t in ents.items() if t.count('\n') != ref_nl.get(i)]
        fbad = [i for i, t in ents.items()
                if set(FOREIGN.findall(t)) - set(FOREIGN.findall(src_en.get(i, '')))]
        ebad = [i for i, t in ents.items() if not t.strip()]
        flag = ''
        if ids_missing or ids_extra or diff_from_en or tbad or nlb or fbad or ebad:
            flag = '  <<< VAN DE'
            bad += 1
        print(f'    {nm:<28} id:{len(ents):>5} khac-EN:{len(diff_from_en):>4} | '
              f'tag:{len(tbad)} nl:{len(nlb)} la:{len(fbad)} rong:{len(ebad)} | '
              f'thua:{len(ids_extra)} thieu:{len(ids_missing)}{flag}')

    print('\n  --- Doi chieu id khop giua cac ngon ngu ---')
    for i in ('5', '6', '7'):
        if i in en:
            print(f'    id {i}: EN={src_en.get(i, "")[:24]!r} -> VI={en.get(i, "")[:24]!r}')

    print(f'\n  KET QUA {label}: ' + ('PASS' if bad == 0 else f'CO VAN DE ({bad} muc)'))
    return bad == 0


def main():
    results = {}
    for label, dst_path, src_path in PAIRS:
        results[label] = check_pair(label, dst_path, src_path)
    print(f'\n{"=" * 62}\n=== TONG KET ===')
    for label, ok in results.items():
        state = 'BO QUA' if ok is None else ('PASS' if ok else 'CO VAN DE')
        print(f'  {label:<12} {state}')


if __name__ == '__main__':
    main()
