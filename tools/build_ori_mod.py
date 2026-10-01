"""
build_ori_mod.py — Đóng gói mod Việt hóa Ori and the Will of the Wisps (Switch).

Ghép bản dịch (games/<TID>/translations/vi_*.json) vào từng AssetBundle
(Data/data_*.unity3d) rồi xuất mod LayeredFS:

    output/atmosphere/contents/01008DD013200000/romfs/Data/data_*.unity3d

Cách dùng (chạy từ gốc dự án):
    python tools/build_ori_mod.py [--src <thu_muc_bundle_goc>]

Mặc định đọc bundle gốc đã bóc ở $ORI_BUNDLES (hoặc tham số --src).
"""
import argparse
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from unity_text_tool import patch_bundle  # noqa: E402

TITLE = '01008DD013200000'
G = os.path.join(ROOT, 'games', f'{TITLE}_OriAndTheWillOfTheWisps')
SRC_TEXT = os.path.join(G, 'source', 'ori_text_all.json')
UNIQ = os.path.join(G, 'source', 'ori_unique.json')
TR = os.path.join(G, 'translations')
OUT_DATA = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TITLE, 'romfs', 'Data')


def load_vi():
    uniq = json.load(open(UNIQ, encoding='utf-8'))
    unique, key2id = uniq['unique'], uniq['key2id']
    id2vi = {}
    for i in range(20):
        p = os.path.join(TR, f'vi_{i:03d}.json')
        if not os.path.exists(p):
            break
        for it in json.load(open(p, encoding='utf-8')):
            id2vi[it['Id']] = it['VI']
    vi_list = [id2vi.get(i, unique[i]) for i in range(len(unique))]
    return vi_list, key2id


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default=os.environ.get('ORI_BUNDLES',
                    r'C:\Users\Admin\AppData\Local\Temp\ori_work\Data'))
    ap.add_argument('--pack', default='original')
    args = ap.parse_args()

    vi_list, key2id = load_vi()
    entries = json.load(open(SRC_TEXT, encoding='utf-8'))
    by_bundle = {}
    for e in entries:
        key = f"{e['bundle']}:{e['path_id']}"
        vid = key2id.get(key)
        if vid is None:
            continue
        by_bundle.setdefault(e['bundle'], {})[str(e['path_id'])] = vi_list[vid]

    print(f'bundle can va: {len(by_bundle)} | tong muc: {sum(len(v) for v in by_bundle.values())}')
    ok = fail = 0
    for bn, mapping in sorted(by_bundle.items()):
        src = os.path.join(args.src, bn)
        if not os.path.exists(src):
            print('  thieu', bn); fail += 1; continue
        try:
            n = patch_bundle(src, mapping, OUT_DATA, pack=args.pack)
            ok += 1
            print(f'  {bn}: va {n}/{len(mapping)}', flush=True)
        except Exception as ex:
            print('  LOI', bn, ex); fail += 1
    print(f'xong: {ok} bundle OK, {fail} loi -> {OUT_DATA}')


if __name__ == '__main__':
    main()
