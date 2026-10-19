# -*- coding: utf-8 -*-
"""
apply_totk_trt_style.py — Chuẩn hoá bản dịch TotK theo phong cách/ thuật ngữ của
patch tham chiếu "The Red Team" (TRT).

Nguyên tắc:
  1. Chuỗi NGẮN (tên riêng / nhãn UI, nguồn EN <= 45 ký tự, không có mã điều khiển):
     nhận NGUYÊN văn bản TRT -> thống nhất tên gọi + kiểu chữ Title Case.
  2. Chuỗi dài: chỉ thay THUẬT NGỮ nhiều từ (>= 2 từ, >= 8 ký tự) theo bảng
     đối chiếu ours -> TRT, và chỉ thay trong các đoạn VĂN BẢN (không đụng thẻ điều khiển).

Dùng:
    python tools/apply_totk_trt_style.py --trt "<...>/USen.Product.142.sarc.zs" [--dry]
"""
import os
import re
import sys
import json
import glob
import argparse
import zstandard
import oead

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from extract_msbt import parse_msbt_bytes          # noqa: E402
import totk_text                                    # noqa: E402

TITLE_ID = '0100F2C0115B6000'
ROMFS = os.path.join(r'E:\RomFS_Dump', TITLE_ID, 'romfs')
TRANS_DIR = os.path.join(ROOT, 'games', f'{TITLE_ID}_ZeldaTotK', 'translations')
CTRL = re.compile(r'[\x00-\x1f\ue000-\uf8ff\uffff]')


def load_dict():
    zd = oead.Sarc(zstandard.ZstdDecompressor().decompress(
        open(os.path.join(ROMFS, 'Pack', 'ZsDic.pack.zs'), 'rb').read()))
    d = next(bytes(f.data) for f in zd.get_files() if f.name == 'zs.zsdic')
    return zstandard.ZstdCompressionDict(d)


def parse_sarc(path, dctx):
    out = {}
    for f in oead.Sarc(dctx.decompress(open(path, 'rb').read())).get_files():
        if not f.name.endswith('.msbt'):
            continue
        for k, v in parse_msbt_bytes(bytes(f.data)).items():
            out[f'{f.name}:::{k}'] = v
    return out


def is_plain(s):
    return bool(s) and not CTRL.search(s)


def is_name_label(inner, label):
    """Nhãn 'tên riêng / tên gọi / nhãn UI' — nơi nên theo đúng phong cách TRT."""
    if inner.startswith('LocationMsg/') or inner.startswith('LayoutMsg/'):
        return True
    if label in ('Name', 'Title', 'Short'):
        return True
    return label.endswith(('_Name', '_Title'))


def hyphen_ok(en_s, trt_s):
    """Tính từ ghép TotK: EN có gạch nối thì bản dịch cũng phải có (chống nhãn lệch)."""
    return ('-' in en_s) == ('-' in trt_s)


PLACEHOLDER = re.compile(r'%[sd]|\{[^}]*\}')


def placeholder_ok(en_s, trt_s):
    return PLACEHOLDER.findall(en_s) == PLACEHOLDER.findall(trt_s)


def replace_in_text(text, term_map):
    if not term_map:
        return text
    parts = totk_text.split_parts(text)
    changed = False
    for i, (kind, seg) in enumerate(parts):
        if kind != 'text':
            continue
        for old, new in term_map:
            if old not in seg:
                continue
            res, n = [], 0
            idx = seg.find(old)
            while idx != -1:
                before = seg[idx - 1] if idx > 0 else ' '
                after = seg[idx + len(old)] if idx + len(old) < len(seg) else ' '
                if not before.isalnum() and not after.isalnum():
                    res.append(seg[n:idx])
                    res.append(new)
                    n = idx + len(old)
                idx = seg.find(old, idx + 1)
            if n:
                res.append(seg[n:])
                seg = ''.join(res)
                changed = True
        parts[i] = (kind, seg)
    return ''.join(t for _, t in parts) if changed else text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trt', required=True)
    ap.add_argument('--dry', action='store_true')
    args = ap.parse_args()

    dctx = zstandard.ZstdDecompressor(dict_data=load_dict())
    en = parse_sarc(os.path.join(ROMFS, 'Mals', 'USen.Product.142.sarc.zs'), dctx)
    trt = parse_sarc(args.trt, dctx)
    print(f'EN {len(en)} chuỗi | TRT {len(trt)} chuỗi')

    adopt, terms = {}, {}
    for k, e in en.items():
        inner, label = k.split(':::')[0], k.split(':::')[-1]
        if not is_name_label(inner, label):
            continue
        t = trt.get(k)
        if t is None or e == t or not is_plain(e) or not is_plain(t):
            continue
        e2 = e.replace('\n', ' ').strip()
        t2 = t.replace('\n', ' ').strip()
        if len(e2) > 45 or not hyphen_ok(e2, t2) or not placeholder_ok(e2, t2):
            continue
        adopt[k] = t

    # Bảng thuật ngữ ours -> TRT suy ra từ chính bản dịch hiện tại
    ours_now = {}
    for tf in glob.glob(os.path.join(TRANS_DIR, '*.json')):
        inner = os.path.basename(tf)[:-5].replace('__', '/')
        for lb, v in json.load(open(tf, encoding='utf-8')).items():
            ours_now[f'{inner}:::{lb}'] = v

    for k, t in adopt.items():
        o = ours_now.get(k)
        if o is None or o == t or not is_plain(o):
            continue
        o2, t2 = o.replace('\n', ' ').strip(), t.replace('\n', ' ').strip()
        if len(o2) > 34 or len(t2) > 34 or o2 == t2:
            continue
        if '-' in o2 or '-' in t2:
            continue                                  # tính từ ghép: chỉ dùng nội bộ
        if len(o2.split()) < 2 or len(o2) < 8:
            continue
        if re.search(r'[.!?…]$', o2) or re.search(r'[.!?…]$', t2):
            continue
        terms[o2] = t2
    term_map = sorted(terms.items(), key=lambda kv: -len(kv[0]))

    print(f'Nhận nguyên văn TRT (tên riêng/nhãn): {len(adopt)}')
    print(f'Bảng thuật ngữ thay trong câu: {len(term_map)}')
    for o, t in term_map[:12]:
        print(f'   {o!r} -> {t!r}')

    if args.dry:
        print('\n--- DRY RUN: 10 ví dụ ---')
        c = 0
        for tf in sorted(glob.glob(os.path.join(TRANS_DIR, '*.json'))):
            inner = os.path.basename(tf)[:-5].replace('__', '/')
            data = json.load(open(tf, encoding='utf-8'))
            for lb, v in data.items():
                key = f'{inner}:::{lb}'
                new = adopt.get(key, replace_in_text(v, term_map))
                if new != v and c < 10:
                    print(f'  [{inner} :: {lb}]\n    CŨ : {v[:90]!r}\n    MỚI: {new[:90]!r}')
                    c += 1
        return

    n_adopt = n_term = 0
    for tf in sorted(glob.glob(os.path.join(TRANS_DIR, '*.json'))):
        inner = os.path.basename(tf)[:-5].replace('__', '/')
        data = json.load(open(tf, encoding='utf-8'))
        out = {}
        for lb, v in data.items():
            key = f'{inner}:::{lb}'
            if key in adopt and (not v or is_plain(v)):
                out[lb] = adopt[key]
                if out[lb] != v:
                    n_adopt += 1
            else:
                nv = replace_in_text(v, term_map)
                if nv != v:
                    n_term += 1
                out[lb] = nv
        with open(tf + '.bak', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        with open(tf, 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
    print(f'\nĐã nhận tên riêng: {n_adopt} chuỗi | thay thuật ngữ trong câu: {n_term} chuỗi')


if __name__ == '__main__':
    main()
