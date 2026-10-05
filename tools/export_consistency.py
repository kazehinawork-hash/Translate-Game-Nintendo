"""Xuat danh sach 'ten rieng/thuat ngu dich nhieu kieu' rieng cho tung game (de sua)."""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
src = json.load(open(os.path.join(ROOT, 'tools', '_consistency_terms.json'), encoding='utf-8'))
out_dir = os.path.join(ROOT, 'games', '_consistency')
os.makedirs(out_dir, exist_ok=True)
for g, rows in src.items():
    items = [{'en': s, 'vi_variants': vs, 'vi_pho_bien': vs[0] if vs else '',
              'vi_vi_du': vs[1] if len(vs) > 1 else '', 'key_vi_du': k} for s, vs, k in rows]
    p = os.path.join(out_dir, f'{g}.json')
    json.dump(items, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{g}: {len(items)} muc -> games/_consistency/{g}.json')
