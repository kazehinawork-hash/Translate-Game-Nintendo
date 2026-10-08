"""Gop 72 ban dich moi cua v1.6 vao mono_vi.json (theo chuoi tieng Anh)."""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, 'games', '01002C201BC40000_Monopoly', 'translations')

new = json.load(open(os.path.join(T, 'v16_new.json'), encoding='utf-8'))
vi_new = json.load(open(os.path.join(T, 'v16_vi.json'), encoding='utf-8'))
vi = json.load(open(os.path.join(T, 'mono_vi.json'), encoding='utf-8'))
print(f'truoc: {len(vi):,} khoa')

added = 0
for item in new:
    i, en = item['id'], item['en']
    v = vi_new.get(i)
    if v and en not in vi:
        vi[en] = v
        added += 1
json.dump(vi, open(os.path.join(T, 'mono_vi.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print(f'them {added} khoa -> {len(vi):,} khoa')
