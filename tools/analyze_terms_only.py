"""Loc DUNG nhom can nhat quan: nguon ngan, dang TEN RIENG / THUAT NGU (khong phai cau)."""
import collections
import json
import os
import re
import sys

sys.path.insert(0, r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\tools')
sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
import qa_text as Q

CJK = re.compile(r'[\u3000-\u9fff]')
OUT = {}
for game in ('switchsports', 'hades2', 'hogwarts', 'ori', 'obf'):
    try:
        sets = Q.ADAPTERS[game]()
    except Exception:
        continue
    groups = collections.defaultdict(set)
    ex = {}
    for name, src, built in sets:
        for k, v in built.items():
            s = (src.get(k) or '').strip()
            if not s:
                continue
            groups[s].add(str(v).strip())
            ex.setdefault((s, str(v).strip()), k)
    multi = {s: vs for s, vs in groups.items() if len(vs) > 1}
    term = []
    for s, vs in multi.items():
        nw = len(s.split())
        is_name = s[:1].isupper() and nw <= 4 and len(s) <= 40
        if CJK.search(s):
            is_name = len(s) <= 8          # nguon Trung/Nhat: chuoi ngan = ten/thuat ngu
        if not is_name:
            continue
        if any(len(v) > 60 or '\n' in v for v in vs):
            continue
        if {v.lower() for v in vs}.__len__() == 1:
            continue                            # chi khac hoa/thuong -> xu ly rieng
        term.append((s, vs, ex.get((s, sorted(vs)[0]), '')))
    OUT[game] = term
    print(f'\n=== {game}: {len(term)} DUNG{"" } ten rieng / thuat ngu can nhat quan '
          f'(tong so nhieu kieu: {len(multi)}) ===')
    for s, vs, k in term[:14]:
        print(f'  EN {s[:44]!r}  [{k[:44]}]')
        for v in list(vs)[:3]:
            print(f'     -> {v[:52]!r}')

json.dump({g: [[s, list(vs), k] for s, vs, k in lst] for g, lst in OUT.items()},
          open(os.path.join(ROOT, 'tools', '_consistency_terms.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('\nda luu tools/_consistency_terms.json')
