"""Thong nhat thuat ngu ban dich Kirby theo glossary + ghi glossary/kirby.csv."""
import csv
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
G = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby')
T = os.path.join(G, 'translations')

# --- 1. GLOSSARY chinh thuc ---
TERMS = [
    ('Mouthful Mode', 'Chế Độ Ngậm', 'Ability', 'Khả năng ngậm vật thể của Kirby'),
    ('Copy Ability', 'Năng lực Copy', 'Ability', 'Khả năng sao chép của Kirby'),
    ('Star Coin', 'Đồng Sao', 'Item', 'Tiền tệ trong game'),
    ('Rare Stone', 'Đá Hiếm', 'Item', 'Nguyên liệu nâng cấp'),
    ('Blueprint', 'Bản thiết kế', 'Item', 'Bản vẽ chế tạo'),
    ('Present Code', 'Mã Quà Tặng', 'Item', 'Mã để nhận quà'),
    ('Treasure Road', 'Con đường Kho báu', 'Mode', 'Màn thử thách'),
    ('Waddle Dee Town', 'Thị trấn Waddle Dee', 'Place', ''),
    ('Waddle Dee', 'Waddle Dee', 'Character', 'Giữ nguyên'),
    ('Waddle Dee-liveries', 'Waddle Dee-liveries', 'Place', 'Giữ nguyên (chơi chữ delivery)'),
    ('Wise Waddle Dee', 'Waddle Dee Thông Thái', 'Character', ''),
    ('Usher Waddle Dee', 'Waddle Dee Soát Vé', 'Character', ''),
    ('Tilt-and-Roll Kirby', 'Kirby Nghiêng & Lăn', 'Ability', ''),
    ('Colosseum', 'Đấu trường', 'Place', ''),
    ('Ultimate Cup', 'Cúp Tối Thượng', 'Item', ''),
    ('Beast Pack', 'Bầy Dã Thú', 'Faction', ''),
    ('Tropic Woods', 'Tropic Woods', 'Character', 'Giữ nguyên'),
    ('Meta Knight', 'Meta Knight', 'Character', 'Giữ nguyên'),
    ('King Dedede', 'King Dedede', 'Character', 'Giữ nguyên'),
    ('Elfilin', 'Elfilin', 'Character', 'Giữ nguyên'),
    ('Fecto Forgo', 'Fecto Forgo', 'Character', 'Giữ nguyên'),
    ('Morpho Knight', 'Morpho Knight', 'Character', 'Giữ nguyên'),
    ('Wondaria Remains', 'Tàn tích Wondaria', 'Place', ''),
    ('Lab Discovera', 'Viện Discovera', 'Place', ''),
    ('Natural Plains', 'Đồng bằng Tự nhiên', 'Place', ''),
    ('Winter Horns', 'Sừng Mùa Đông', 'Place', ''),
    ('Extra Hard', 'Siêu Khó', 'Difficulty', ''),
    ('Wild Mode', 'Chế độ Hoang Dã', 'Mode', ''),
    ('Spring-Breeze Mode', 'Chế độ Gió Xuân', 'Mode', ''),
    ('Maxim Tomato', 'Maxim Tomato', 'Item', 'Giữ nguyên'),
    ('Retry', 'Thử lại', 'UI', ''),
    ('Treasure', 'Kho Báu', 'UI', ''),
]
os.makedirs(os.path.join(ROOT, 'glossary'), exist_ok=True)
gp = os.path.join(ROOT, 'glossary', 'kirby.csv')
with open(gp, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['source', 'target', 'category', 'note'])
    for r in TERMS:
        w.writerow(r)
print(f'da ghi glossary/kirby.csv ({len(TERMS)} thuat ngu)')

# --- 2. Thong nhat trong ban dich ---
REPL = [
    ('Mouthful Mode', 'Chế Độ Ngậm'),
    ('Mouthful Modes', 'Chế Độ Ngậm'),
    ('Chế Độ Há Miệng', 'Chế Độ Ngậm'),
    ('Há Miệng', 'Ngậm'),
    ('Waddle Dee soát vé', 'Waddle Dee Soát Vé'),
    ('Waddle Dee thông thái', 'Waddle Dee Thông Thái'),
    ('Wondaria Hoang Tàn', 'Tàn tích Wondaria'),
    ('Chơi lại', 'Thử lại'),
]
n_change = 0
for p in [os.path.join(T, 'kirby_vi.json')] + [os.path.join(T, f'vi_{i:02d}.json') for i in range(1, 11)]:
    if not os.path.exists(p):
        continue
    d = json.load(open(p, encoding='utf-8'))
    ch = 0
    if isinstance(d, dict):
        for fn, entries in d.items():
            for k, v in list(entries.items()):
                nv = str(v)
                for a, b in REPL:
                    if a in nv and a != b:
                        nv = nv.replace(a, b)
                if nv != v:
                    entries[k] = nv
                    ch += 1
    else:
        for x in d:
            nv = str(x.get('vi', ''))
            for a, b in REPL:
                if a in nv and a != b:
                    nv = nv.replace(a, b)
            if nv != x.get('vi', ''):
                x['vi'] = nv
                ch += 1
    if ch:
        json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        n_change += ch
        print(f'  {os.path.basename(p)}: sua {ch} chuoi')
print(f'tong sua {n_change} chuoi')
