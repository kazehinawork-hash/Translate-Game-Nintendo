"""Dem phan THUC SU dich duoc trong so 'chua dich' (loai credits, ten nguoi, chuoi chi co tag)."""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'games', '_consistency')

STRIP = re.compile(r'\{[^{}]*\}|<[^>]*>|\[[^\]]*\]|%[sdfiu]|\\[nt]|\$[\w.]+|\|plural\(|\|\w+\(|[\W\d_]+')
SKIP_FILE = re.compile(r'credits|credit', re.I)


def realwords(v):
    core = STRIP.sub(' ', v)
    return [w for w in core.split() if len(w) > 1]


for game in ('hogwarts', 'hades2', 'switchsports'):
    p = os.path.join(D, f'untranslated_{game}.json')
    if not os.path.exists(p):
        continue
    data = json.load(open(p, encoding='utf-8'))
    print(f'\n{"="*74}\n{game.upper()}\n{"="*74}')
    tot_real = tot_credits = tot_tag = 0
    for name, items in data.items():
        if not items:
            continue
        real, credits, tagonly = [], [], []
        for k, v in sorted(items.items()):
            if SKIP_FILE.search(k):
                credits.append((k, v))
            elif realwords(v):
                real.append((k, v))
            else:
                tagonly.append((k, v))
        tot_real += len(real)
        tot_credits += len(credits)
        tot_tag += len(tagonly)
        print(f'\n  --- {name}: {len(items)} muc')
        print(f'      ten nguoi/credits (BO QUA)     : {len(credits)}')
        print(f'      chi co tag/placeholder (BO QUA): {len(tagonly)}')
        print(f'      >>> THUC SU CO CHU DE DICH     : {len(real)}')
        for k, v in real[:25]:
            print(f'        {k[:46]:<46} {v[:66]!r}')
        if len(real) > 25:
            print(f'        ... con {len(real)-25} muc')
    print(f'\n  TONG {game}: dich duoc {tot_real} | credits {tot_credits} | chi-tag {tot_tag}')
