"""Rut thuat ngu tu kho chuoi It Takes Two -> tao glossary TRUOC khi dich (BH-22)."""
import collections
import csv
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
items = json.load(open(r'E:\ITT_work\strings.json', encoding='utf-8'))
print(f'{len(items):,} chuoi | {len({i["en"] for i in items}):,} duy nhat')

# 1. ten rieng / thuat ngu: cum viet hoa xuat hien nhieu lan
cnt = collections.Counter()
for i in items:
    for m in re.findall(r"\b[A-Z][a-z]{2,}(?: [A-Z][a-z]{2,}){0,2}\b", i['en']):
        cnt[m] += 1
# 2. cac tu khoa UI
ui = collections.Counter()
for i in items:
    if len(i['en']) < 40:
        for w in re.findall(r"\b[A-Z][A-Za-z']+\b", i['en']):
            ui[w] += 1

print('\n=== cum ten rieng xuat hien >= 6 lan ===')
rows = []
for t, c in cnt.most_common(400):
    if c < 6:
        break
    rows.append((t, c))
for t, c in rows[:40]:
    print(f'  {c:>5}  {t}')

# 3. ghi glossary nhap (de nguoi/agent dien ban dich)
gp = os.path.join(ROOT, 'glossary', 'ittakestwo.csv')
os.makedirs(os.path.dirname(gp), exist_ok=True)
KNOWN = {
    'May': 'May', 'Cody': 'Cody', 'Rose': 'Rose', 'Dr': 'Tiến sĩ', 'Hakim': 'Hakim',
    'Book of Love': 'Sách Tình Yêu', 'The Book': 'Cuốn Sách', 'Moon Baboon': 'Moon Baboon',
    'Mud': 'Bùn', 'Language': 'Ngôn ngữ', 'Host': 'Chủ phòng', 'Join': 'Tham gia',
    'Play Local Wireless': 'Chơi không dây nội bộ', 'Shown Controller': 'Hiện tay cầm',
}
with open(gp, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['source', 'target', 'category', 'note'])
    for t, c in rows:
        cat = 'ProperNoun' if t in KNOWN else 'Term'
        w.writerow([t, KNOWN.get(t, ''), cat, f'xuat hien {c} lan'])
print(f'\nda tao glossary nhap: {gp} ({len(rows)} dong, cot "target" de trong cho phan dich)')
