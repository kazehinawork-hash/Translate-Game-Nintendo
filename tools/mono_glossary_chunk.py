"""Tao glossary MONOPOLY TRUOC khi dich (BH-22) + chia chunk."""
import collections
import csv
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '01002C201BC40000'
G = os.path.join(ROOT, 'games', f'{TID}_Monopoly')
T = os.path.join(G, 'translations')
items = json.load(open(os.path.join(T, 'mono_en.json'), encoding='utf-8'))

# 1. thuat ngu hay gap (cum viet hoa)
cnt = collections.Counter()
for i in items:
    for m in re.findall(r"\b[A-Z][a-z]{2,}(?: [A-Z][a-z]{2,}){0,2}\b", i['en']):
        cnt[m] += 1

# bang thuat ngu chuan cua Monopoly (giu ten dia danh My, dich phan chung)
GLOSS = [
    ('GO', 'XUẤT PHÁT', 'Board'), ('Jail', 'Nhà tù', 'Board'), ('Free Parking', 'Bãi đỗ xe miễn phí', 'Board'),
    ('Go To Jail', 'Vào nhà tù', 'Board'), ('Chance', 'Cơ hội', 'Board'), ('Community Chest', 'Khí vận', 'Board'),
    ('Rent', 'Tiền thuê', 'Board'), ('House', 'Nhà', 'Board'), ('Hotel', 'Khách sạn', 'Board'),
    ('Mortgage', 'Cầm cố', 'Board'), ('Unmortgage', 'Chuộc lại', 'Board'), ('Property', 'Tài sản', 'Board'),
    ('Boardwalk', 'Boardwalk', 'Place'), ('Park Place', 'Park Place', 'Place'),
    ('Baltic Avenue', 'Baltic Avenue', 'Place'), ('Mediterranean Avenue', 'Mediterranean Avenue', 'Place'),
    ('Play', 'Chơi', 'UI'), ('Online', 'Trực tuyến', 'UI'), ('Credits', 'Ghi công', 'UI'),
    ('News', 'Tin tức', 'UI'), ('Help And Options', 'Trợ giúp & Tuỳ chọn', 'UI'),
    ('Ubisoft Connect', 'Ubisoft Connect', 'UI'), ('Objectives', 'Mục tiêu', 'UI'), ('Exit', 'Thoát', 'UI'),
    ('Settings', 'Cài đặt', 'UI'), ('Back', 'Quay lại', 'UI'), ('Cancel', 'Huỷ', 'UI'),
    ('Confirm', 'Xác nhận', 'UI'), ('Continue', 'Tiếp tục', 'UI'), ('Start Game', 'Bắt đầu ván', 'UI'),
    ('Single Player', 'Chơi đơn', 'UI'), ('Multiplayer', 'Nhiều người chơi', 'UI'),
    ('Pause', 'Tạm dừng', 'UI'), ('Resume', 'Tiếp tục', 'UI'), ('Loading', 'Đang tải', 'UI'),
    ('Player', 'Người chơi', 'UI'), ('Token', 'Quân cờ', 'Board'), ('Dice', 'Xúc xắc', 'Board'),
    ('Trade', 'Giao dịch', 'UI'), ('Bankrupt', 'Phá sản', 'Board'), ('Auction', 'Đấu giá', 'UI'),
    ('Pass GO', 'Qua ô Xuất phát', 'Board'), ('Chance Card', 'Thẻ Cơ hội', 'Board'),
    ('Community Chest Card', 'Thẻ Khí vận', 'Board'), ('Utility', 'Tiện ích', 'Board'),
    ('Railroad', 'Đường sắt', 'Board'), ('Salary', 'Tiền lương', 'Board'),
]
gp = os.path.join(ROOT, 'glossary', 'monopoly.csv')
with open(gp, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['source', 'target', 'category', 'note'])
    for r in GLOSS:
        w.writerow(r)
    for t, c in cnt.most_common(300):
        if c >= 6 and not any(t == g[0] for g in GLOSS):
            w.writerow([t, '', 'Term', f'xuat hien {c} lan - dien ban dich'])
print(f'glossary/monopoly.csv: {len(GLOSS)} thuat ngu chuan + goi y ({gp})')

# 2. chia chunk
keys = [i['en'] for i in items]
uniq = sorted(set(keys))
print(f'{len(keys)} chuoi | {len(uniq)} duy nhat')
json.dump(uniq, open(os.path.join(T, 'uniq_en.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
CH = 350
n = 0
for i in range(0, len(uniq), CH):
    n += 1
    part = uniq[i:i + CH]
    json.dump(part, open(os.path.join(T, f'todo_{n}.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'  todo_{n}.json: {len(part)} chuoi | dai nhat {max(len(x) for x in part)}')
print(f'tong {n} chunk')
