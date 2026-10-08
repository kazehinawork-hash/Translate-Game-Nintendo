"""Doi chieu ma dieu khien giua cac ngon ngu GOC (US_English / JP_Japanese / CN_Chinese)."""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from extract_msbt import parse_msbt_bytes

G = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'source', 'msg', 'Kirby15')
CTRL = re.compile(r'[\x00-\x1f\ue000-\uf8ff\ufffe\uffff]+')

KEYS = [('Cmn.msbt', 'DifficultySelectExplanationCasual'),
        ('MgameFood.msbt', 'DifficultyDetail_Easy'),
        ('Dialog.msbt', 'Text_Amiibo_NotAllowedOther')]

for fn, key in KEYS:
    print(f'\n===== {fn} :: {key} =====')
    for lang in ('US_English', 'JP_Japanese', 'CN_Chinese', 'EU_French'):
        p = os.path.join(G, lang, fn)
        if not os.path.exists(p):
            continue
        try:
            d = parse_msbt_bytes(open(p, 'rb').read())
        except Exception as e:
            print(f'  {lang}: loi {type(e).__name__}')
            continue
        v = d.get(key)
        if v is None:
            print(f'  {lang}: khong co key')
            continue
        # 40 ky tu quanh ma dieu khien dau tien
        i = CTRL.search(v)
        seg = v[max(0, i.start() - 6): i.end() + 12] if i else v[:30]
        print(f'  {lang:<12} {seg.encode("unicode_escape").decode()}')
