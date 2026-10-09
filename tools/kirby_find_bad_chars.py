"""Tim va bao cac ky tu LA trong ban dich Kirby (Hangul, CJK, ky tu toan rong...)."""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'translations', 'kirby_vi.json')

BAD = re.compile(r'[\u1100-\u11FF\u3130-\u318F\uAC00-\uD7AF'
                 r'\u3000-\u303F\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF'
                 r'\uFF00-\uFFEF\u3040-\u30FF\u0600-\u06FF'
                 r'\u0400-\u04FF\u4DC0-\u4DFF]')

vi = json.load(open(P, encoding='utf-8'))
hits = []
for key, ents in vi.items():
    for lang, val in ents.items():
        for ch in str(val):
            if BAD.match(ch):
                hits.append((key, lang, str(val)))
                break

print(f'  so chuoi co ky tu la: {len(hits)}')
for key, lang, val in hits[:20]:
    m = BAD.search(val)
    i = m.start()
    print(f'  {key[:38]:<40} [{lang}]  …{val[max(0,i-25):i+25]}…  (ky tu U+{ord(val[i]):04X})')

if hits:
    print('\n  Cac ky tu la gap phai:', sorted({m.group(0) for _, _, s in hits for m in [BAD.search(s)] if m}))
    print(f'\n  file: {P}')
