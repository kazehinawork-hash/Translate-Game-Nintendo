"""Phan tich 'cung cau nguon -> dich nhieu kieu' cho ca 5 game, phan loai de sua."""
import collections
import json
import os
import sys

sys.path.insert(0, r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\tools')
sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
import qa_text as Q

for game in ('switchsports', 'hades2', 'hogwarts', 'ori', 'obf'):
    try:
        sets = Q.ADAPTERS[game]()
    except Exception as e:
        print(f'{game}: loi {type(e).__name__} {str(e)[:60]}')
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
    caseonly = real = 0
    big = []
    for s, vs in multi.items():
        norm = {v.lower() for v in vs}
        if len(norm) == 1:
            caseonly += 1
        else:
            real += 1
            big.append((s, vs))
    print(f'\n=== {game}: {len(groups):,} cau nguon | {len(multi)} dich nhieu kieu '
          f'(chi khac hoa/thuong: {caseonly} | KHAC NGHIA: {real}) ===')
    for s, vs in big[:6]:
        print(f'  EN {s[:50]!r}')
        for v in list(vs)[:3]:
            print(f'     -> {v[:55]!r}   [{ex.get((s, v), "")}]')
