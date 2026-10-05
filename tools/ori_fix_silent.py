"""Sua lai Silent Woods theo DA SO (Tinh Lang 18 > Im Lang 6) + cap nhat glossary."""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
G = os.path.join(ROOT, 'games', '01008DD013200000_OriAndTheWillOfTheWisps')
P = os.path.join(G, 'translations', 'ori_vi.json')
d = json.load(open(P, encoding='utf-8'))
k = 'VI' if 'VI' in (d[0] if d else {}) else 'vi'

n = 0
for x in d:
    v = str(x.get(k, ''))
    if 'Rừng Im Lặng' in v:
        x[k] = v.replace('Rừng Im Lặng', 'Rừng Tĩnh Lặng')
        n += 1
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'Silent Woods: doi {n} muc sang "Rừng Tĩnh Lặng" (da so)')

d2 = json.load(open(P, encoding='utf-8'))
for term, var in (('Spirit Light', 'Ánh Sáng Tinh Linh'), ('Silent Woods', 'Rừng Im Lặng'),
                  ('Mouldwood', 'Đáy Rừng Mốc'), ('Glades', 'Đồng Cỏ Suối Nguồn')):
    c = sum(1 for x in d2 if var.lower() in str(x.get(k, '')).lower())
    print(f'  con lai "{var}": {c}')

# cap nhat glossary
gp = os.path.join(ROOT, 'glossary', 'ori.csv')
lines = open(gp, encoding='utf-8').read().splitlines()
out = []
for l in lines:
    if l.startswith('Silent Woods,'):
        l = 'Silent Woods,Rừng Tĩnh Lặng,Place,'
    if l.startswith('Spirit Light,'):
        l = 'Spirit Light,Ánh Sáng Linh Hồn,Item,Kinh nghiệm/tiền tệ'
    out.append(l)
open(gp, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('da cap nhat glossary/ori.csv')
