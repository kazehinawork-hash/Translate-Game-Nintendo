"""Sua lai glossary cho dung nghia:
- master.csv hien dang chua noi dung Switch Sports -> chuyen thanh switchsports.csv
- master.csv moi = CHI gom thuat ngu THAT SU DUNG CHUNG (xuat hien giong nhau o >=2 game)
- cap nhat GAME_GLOSSARY cho tung game
"""
import csv
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
GD = os.path.join(ROOT, 'glossary')
GAMES = ['hogwarts_legacy.csv', 'hades2.csv', 'ori.csv', 'ori_bf.csv', 'unravel.csv', 'kirby.csv']


def read(f):
    p = os.path.join(GD, f)
    out = []
    for r in csv.DictReader(open(p, encoding='utf-8-sig')):
        s = (r.get('source') or '').strip()
        t = (r.get('target') or '').strip()
        c = (r.get('category') or '').strip()
        n = (r.get('note') or '').strip()
        if s and t:
            out.append((s, t, c, n))
    return out


# 1. master cu -> switchsports.csv
old_master = read('master.csv')
with open(os.path.join(GD, 'switchsports.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['source', 'target', 'category', 'note'])
    for r in old_master:
        w.writerow(r)
print(f'master.csv -> switchsports.csv ({len(old_master)} thuat ngu, noi dung cua Switch Sports)')

# 2. tinh thuat ngu DUNG CHUNG (cung source -> cung target o >=2 game)
from collections import defaultdict
pairs = defaultdict(set)
where = defaultdict(list)
for g in GAMES:
    for s, t, c, n in read(g):
        pairs[(s.lower(), t.lower())].add(g)
        where[(s.lower(), t.lower())].append((s, t, c, n, g))
shared = []
for (sl, tl), gs in pairs.items():
    if len(gs) >= 2:
        s, t, c, n, g = where[(sl, tl)][0]
        shared.append((s, t, c, n, sorted(gs)))
shared.sort(key=lambda x: -len(x[4]))
print(f'\nthuat ngu xuat hien giong nhau o >=2 game: {len(shared)}')

# 3. ghi master.csv moi = dong thuan chung (co ghi ro game nao dung)
with open(os.path.join(GD, 'master.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['source', 'target', 'category', 'note'])
    for s, t, c, n, gs in shared:
        note = (n + ' | ' if n else '') + 'dung chung: ' + ', '.join(x.split('.')[0] for x in gs)
        w.writerow([s, t, c, note])
for s, t, c, n, gs in shared[:12]:
    print(f'  {s:<22} -> {t:<22} ({len(gs)} game: {", ".join(x.split(".")[0] for x in gs)})')
if not shared:
    print('  (khong co thuat ngu nao giong nhau giua cac game)')
print(f'\nmaster.csv moi: {len(shared)} thuat ngu THAT SU dung chung')
