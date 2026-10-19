# -*- coding: utf-8 -*-
"""
gen_totk_glossary.py — Sinh glossary/totk.csv từ các file đã dịch có tính thuật ngữ.
Nguồn: StaticMsg__Reference (khái niệm), LocationMsg__Location (địa danh).
"""
import os, sys, json, csv, re
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.path.join(ROOT, 'games', '0100F2C0115B6000_ZeldaTotK')
RAW = os.path.join(GAME, 'source', 'raw_text')
TR = os.path.join(GAME, 'translations')

SOURCES = [
    ('StaticMsg__Reference.msbt.json', 'khái niệm'),
    ('LocationMsg__Location.msbt.json', 'địa danh'),
    ('LocationMsg__Dungeon.msbt.json', 'địa danh'),
    ('ActorMsg__Boss.msbt.json', 'quái vật'),
    ('ActorMsg__CharaDirectory.msbt.json', 'nhân vật'),
]

rows = []
seen = set()
for fname, note in SOURCES:
    sp = os.path.join(RAW, fname)
    tp = os.path.join(TR, fname)
    if not (os.path.exists(sp) and os.path.exists(tp)):
        print('thiếu:', fname)
        continue
    src = json.load(open(sp, encoding='utf-8'))
    tr = json.load(open(tp, encoding='utf-8'))
    for k, en in src.items():
        vi = tr.get(k)
        if not isinstance(en, str) or not isinstance(vi, str):
            continue
        en = en.strip()
        vi = vi.strip()
        if not en or not vi or en == vi:
            continue
        if len(en) > 45 or len(vi) > 55:
            continue
        if any(c in en for c in '\x0e\x00\x01\x02\x03\x04\x05\n') or any(c in vi for c in '\x0e\x00\x01\x02\x03\x04\x05\n'):
            continue
        if not re.search(r'[A-Za-z]', en):
            continue
        # chỉ giữ mục DẠNG THUẬT NGỮ (không phải câu)
        if note == 'khái niệm' and (len(en) > 30 or len(en.split()) > 4 or any(p in en for p in '.!?:,;')):
            continue
        # chuẩn hoá khoá camel-case -> cụm từ
        key = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', ' ', en)
        key_low = key.lower()
        if key_low in seen:
            continue
        seen.add(key_low)
        rows.append((key, vi, note))

rows.sort(key=lambda r: (r[2], r[0]))
out = os.path.join(ROOT, 'glossary', 'totk.csv')
with open(out, 'w', encoding='utf-8', newline='') as fo:
    w = csv.writer(fo)
    w.writerow(['en', 'vi', 'phan_loai'])
    w.writerows(rows)
print(f'Đã ghi {len(rows)} thuật ngữ -> {out}')
for r in rows[:12]:
    print('  ', r)
