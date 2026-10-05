"""Chia kho chuoi It Takes Two thanh chunk de giao subagent dich."""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
G = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\games\010092A0172E4000_ItTakesTwo'
T = os.path.join(G, 'translations')
os.makedirs(T, exist_ok=True)
items = json.load(open(r'E:\ITT_work\strings.json', encoding='utf-8'))

# gop trung: dich 1 lan theo chuoi nguon, map nguoc lai
uniq = {}
for i in items:
    uniq.setdefault(i['en'], []).append(i['path'])
keys = sorted(uniq)                      # on dinh
print(f'{len(items):,} chuoi | {len(keys):,} duy nhat')
json.dump(keys, open(os.path.join(T, 'uniq_en.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

CH = 340
n = 0
for i in range(0, len(keys), CH):
    n += 1
    part = keys[i:i + CH]
    json.dump(part, open(os.path.join(T, f'todo_{n}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'  todo_{n}.json: {len(part)} chuoi | dai nhat {max(len(x) for x in part)}')
print(f'tong {n} chunk -> {T}')
