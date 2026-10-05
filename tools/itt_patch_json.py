"""Ghi ban dich nguoc vao cac file JSON asset It Takes Two (theo dung duong dan da luu)."""
import json
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
G = os.path.join(ROOT, 'games', '010092A0172E4000_ItTakesTwo')
vi = json.load(open(os.path.join(G, 'translations', 'itt_vi.json'), encoding='utf-8'))
items = json.load(open(r'E:\ITT_work\strings.json', encoding='utf-8'))
print(f'{len(vi):,} ban dich | {len(items):,} vi tri can ghi')

SRC = r'E:\ITT_work\json'
DST = r'E:\ITT_work\json_vi'
if os.path.isdir(DST):
    shutil.rmtree(DST)
shutil.copytree(SRC, DST)
print(f'da copy JSON -> {DST}')

TOK = re.compile(r'([A-Za-z_$][A-Za-z0-9_$]*)|\[(\d+)\]')


def get_parent(obj, path):
    """Di theo path, tra ve (container, key_cuoi) de gan gia tri."""
    parts = [(m.group(1) if m.group(1) is not None else int(m.group(2))) for m in TOK.finditer(path)]
    cur = obj
    for p in parts[:-1]:
        cur = cur[p]
    return cur, parts[-1]


cache = {}
changed = failed = 0
for it in items:
    asset, path, en = it['asset'], it['path'], it['en']
    newv = vi.get(en)
    if newv is None:
        failed += 1
        continue
    full = os.path.join(DST, asset)
    if full not in cache:
        cache[full] = json.load(open(full, encoding='utf-8'))
    try:
        parent, key = get_parent(cache[full], path)
        parent[key] = newv
        changed += 1
    except Exception as e:
        failed += 1
        if failed <= 5:
            print(f'  LOI path {asset} {path}: {type(e).__name__}')

for full, doc in cache.items():
    json.dump(doc, open(full, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'da ghi {changed:,} cho vao {len(cache)} file JSON | loi {failed}')
