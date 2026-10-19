# -*- coding: utf-8 -*-
"""
totk_make_event_batches.py — Sinh các batch dịch EventFlowMsg còn thiếu cho TotK.

Đọc kho text gốc (source/raw_text), trừ đi phần ĐÃ dịch (translations/*.json),
gom theo file, đóng gói thành các chunk (mặc định ~250 chuỗi/chunk) và CHE mã
điều khiển bằng token [[n]] (xem tools/totk_text.py).

Output: games/<TID>/source/ev_batches/batch_XXX.json  (key -> chuỗi đã che)
        games/<TID>/source/ev_batches/manifest.json
"""
import os, sys, json, glob, re, argparse
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import totk_text as T

GAME = os.path.join(ROOT, 'games', '0100F2C0115B6000_ZeldaTotK')
RAW = os.path.join(GAME, 'source', 'raw_text')
TR = os.path.join(GAME, 'translations')
OUTDIR = os.path.join(GAME, 'source', 'ev_batches')


def has_letters(s):
    return bool(re.search(r'[A-Za-z]', s))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--size', type=int, default=250, help='số chuỗi mỗi chunk')
    ap.add_argument('--prefix', default='EventFlowMsg__', help='tiền tố file cần dịch')
    a = ap.parse_args()

    applied = set()
    for f in glob.glob(os.path.join(TR, '*.json')):
        base = os.path.basename(f)
        try:
            d = json.load(open(f, encoding='utf-8'))
        except Exception:
            continue
        for k in d:
            applied.add(base + ':::' + k)

    # gom phần còn thiếu theo file
    by_file = {}
    for f in sorted(glob.glob(os.path.join(RAW, '*.json'))):
        base = os.path.basename(f)
        if not base.startswith(a.prefix):
            continue
        d = json.load(open(f, encoding='utf-8'))
        todo = {}
        for k, v in d.items():
            if not isinstance(v, str):
                continue
            if (base + ':::' + k) in applied:
                continue
            if not v.strip() or not has_letters(v):
                continue
            todo[base + ':::' + k] = v
        if todo:
            by_file[base] = todo

    # đóng gói chunk
    chunks = []
    cur = {}
    for base in sorted(by_file):
        items = by_file[base]
        if len(items) > a.size:
            # tách file lớn
            keys = sorted(items)
            for i in range(0, len(keys), a.size):
                part = {k: items[k] for k in keys[i:i + a.size]}
                chunks.append(part)
            continue
        if len(cur) + len(items) > a.size and cur:
            chunks.append(cur)
            cur = {}
        cur.update(items)
    if cur:
        chunks.append(cur)

    n_by_file = sum(len(v) for v in by_file.values())
    print(f'[debug] by_file total={n_by_file} chunks_total={sum(len(c) for c in chunks)}')

    if os.path.isdir(OUTDIR):
        for f in glob.glob(os.path.join(OUTDIR, 'batch_*.json')):
            os.remove(f)
    os.makedirs(OUTDIR, exist_ok=True)

    manifest = {}
    total = 0
    for i, ch in enumerate(chunks):
        masked = {}
        for k, v in ch.items():
            m, _ = T.mask(v)
            masked[k] = m
        path = os.path.join(OUTDIR, f'batch_{i+1:03d}.json')
        json.dump(masked, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        files = sorted({k.split(':::')[0] for k in ch})
        manifest[f'batch_{i+1:03d}.json'] = {'n': len(ch), 'files': len(files)}
        total += len(ch)

    json.dump(manifest, open(os.path.join(OUTDIR, 'manifest.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(f'Tổng chuỗi còn thiếu: {total} | số file: {len(by_file)} | số chunk: {len(chunks)}')
    print(f'-> {OUTDIR}')


if __name__ == '__main__':
    main()
