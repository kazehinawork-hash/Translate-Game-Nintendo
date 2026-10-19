# -*- coding: utf-8 -*-
"""
totk_apply_batches.py — Nạp kết quả dịch từ các batch vào translations/<file>.json.

Đọc games/<TID>/translations/ev_batches/batch_*.json (kết quả subagent, đã che token [[n]]),
khôi phục mã điều khiển bằng danh sách thẻ của chuỗi GỐC, rồi hợp nhất:
    merged = <bản dịch tiếng Anh gốc của file>  (đảm bảo ĐỦ nhãn — tránh build xoá trắng)
    merged.update(<bản dịch đã có của file>)    (giữ công sức trước)
    merged.update(<kết quả batch mới>)

Báo lỗi rõ: JSON hỏng, key lạ, lệch token [[n]].
"""
import os, sys, json, glob, re, argparse
sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import totk_text as T

GAME = os.path.join(ROOT, 'games', '0100F2C0115B6000_ZeldaTotK')
RAW = os.path.join(GAME, 'source', 'raw_text')
TR = os.path.join(GAME, 'translations')
IN_BATCH = os.path.join(GAME, 'source', 'ev_batches')
OUT_BATCH = os.path.join(TR, 'ev_batches')
TOKEN = re.compile(r'\[\[(\d+)\]\]')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--verbose', action='store_true')
    a = ap.parse_args()

    out_files = sorted(glob.glob(os.path.join(OUT_BATCH, 'batch_*.json')))
    in_files = glob.glob(os.path.join(IN_BATCH, 'batch_*.json'))
    print(f'Batch nguồn: {len(in_files)} | Batch đã dịch: {len(out_files)}')
    if not out_files:
        print('Chưa có batch nào được dịch.')
        return

    src_cache = {}
    written = {}
    bad = []
    literal_fixed = []
    restored = 0

    for f in out_files:
        name = os.path.basename(f)
        ip = os.path.join(IN_BATCH, name)
        src = json.load(open(ip, encoding='utf-8')) if os.path.exists(ip) else None
        try:
            out = json.load(open(f, encoding='utf-8'))
        except Exception as e:
            bad.append((name, f'JSON hỏng: {e}'))
            continue
        if src is not None:
            miss = [k for k in src if k not in out]
            extra = [k for k in out if k not in src]
            if miss:
                bad.append((name, f'thiếu {len(miss)} nhãn'))
            if extra:
                bad.append((name, f'thừa {len(extra)} nhãn'))
        for k, vi in out.items():
            if ':::' not in k:
                bad.append((k, 'key sai định dạng'))
                continue
            base, label = k.split(':::', 1)
            if base not in src_cache:
                p = os.path.join(RAW, base)
                if not os.path.exists(p):
                    bad.append((k, 'file gốc không tồn tại'))
                    continue
                src_cache[base] = json.load(open(p, encoding='utf-8'))
            if label not in src_cache[base]:
                bad.append((k, 'nhãn không có trong nguồn'))
                continue
            orig = src_cache[base][label]
            if src is not None and k in src and sorted(TOKEN.findall(src[k])) != sorted(TOKEN.findall(vi or '')):
                bad.append((k, 'lệch token [[n]]'))
                continue
            _, tags = T.mask(orig)
            try:
                full = T.unmask(vi, tags)
            except Exception as e:
                bad.append((k, f'khôi phục lỗi: {e}'))
                continue
            # nguồn TotK không bao giờ có literal '\n' (2 ký tự) -> nếu model ghi literal thì sửa thành xuống dòng thật
            if '\\n' in full and '\\n' not in orig:
                full = full.replace('\\n', '\n')
                literal_fixed.append(k)
            written.setdefault(base, {})[label] = full
            restored += 1

    if bad:
        print(f'CẢNH BÁO: {len(bad)} vấn đề:')
        for x in bad[:25]:
            print('   ', x)

    n_files = 0
    for base, trans in written.items():
        outpath = os.path.join(TR, base)
        merged = dict(src_cache[base])
        if os.path.exists(outpath):
            try:
                merged.update(json.load(open(outpath, encoding='utf-8')))
            except Exception:
                pass
        merged.update(trans)
        json.dump(merged, open(outpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        n_files += 1

    print(f'Đã khôi phục {restored} chuỗi vào {n_files} file dịch.')
    if literal_fixed:
        print(f'(đã tự sửa literal "\\n" -> xuống dòng thật cho {len(literal_fixed)} chuỗi)')


if __name__ == '__main__':
    main()
