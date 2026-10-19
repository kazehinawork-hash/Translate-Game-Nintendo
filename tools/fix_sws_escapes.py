# -*- coding: utf-8 -*-
"""
fix_sws_escapes.py — Chuẩn hoá mã điều khiển + dấu ngắt dòng cho bản dịch Switch Sports.

Vấn đề phát hiện khi đối chiếu với RomFS gốc:
  1. Thẻ điều khiển trong bản dịch bị THIẾU byte so với gốc:
        \\x0e\\x03\\x02\\x02        -> phải là  \\x0e\\x00\\x03\\x02\\x02
        \\x0e\\x03\\x02\\x01        -> phải là  \\x0e\\x00\\x03\\x02\\x01
        \\x0e\\x03\\x02            -> phải là  \\x0e\\x00\\x03\\x02\\uffff   (thiếu cả byte kết!)
  2. Một số chuỗi bị BỎ MẤT dấu xuống dòng so với nguồn (chữ tràn khung).

Dùng:
    python tools/fix_sws_escapes.py            # xem thử (dry run)
    python tools/fix_sws_escapes.py --apply
"""
import os
import sys
import json
import glob
import shutil
import argparse
import zstandard
import oead

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from extract_msbt import parse_msbt_bytes  # noqa: E402

TID = '0100D2F00D5C0000'
DUMP = os.path.join(r'E:\RomFS_Dump', TID, 'romfs')
GAME = os.path.join(ROOT, 'games', f'{TID}_SwitchSports')
TRANS = os.path.join(GAME, 'translations')
BACKUP = os.path.join(GAME, '_misc', 'backup_translations_before_escape_fix')

REPL = [
    ('\x0e\x03\x02\x02', '\x0e\x00\x03\x02\x02'),
    ('\x0e\x03\x02\x01', '\x0e\x00\x03\x02\x01'),
    ('\x0e\x03\x02', '\x0e\x00\x03\x02\uffff'),
]


def fix_tags(s):
    for a, b in REPL:
        s = s.replace(a, b)
    return s


def split_tags(s):
    parts, cur, i = [], '', 0
    while i < len(s):
        c = s[i]
        if ord(c) < 0x20 and c not in '\n\r\t':
            j = i
            while j < len(s) and ord(s[j]) < 0x20 and s[j] not in '\n\r\t':
                j += 1
            tag = s[i:j]
            if j < len(s) and s[j] == '\uffff':
                tag += '\uffff'
                j += 1
            if cur:
                parts.append(('t', cur))
                cur = ''
            parts.append(('g', tag))
            i = j
        else:
            cur += c
            i += 1
    if cur:
        parts.append(('t', cur))
    return parts


OPEN_TAGS = ('\x0e\x00\x03\x02\x00', '\x0e\x00\x03\x02\x01', '\x0e\x00\x03\x02\x02')
CLOSE_TAG = '\x0e\x00\x03\x02\uffff'


def balance_ok(s):
    opens = sum(s.count(t) for t in OPEN_TAGS)
    return opens == s.count(CLOSE_TAG)


def rebuild_from_skeleton(src, ours):
    """Giữ NGUYÊN thẻ của bản gốc, chỉ thay các đoạn văn bản bằng bản dịch.
    Chỉ dùng khi số đoạn văn bản 2 bên bằng nhau (an toàn tuyệt đối)."""
    ps, po = split_tags(src), split_tags(ours)
    ts = [v for k, v in ps if k == 't']
    to = [v for k, v in po if k == 't']
    if len(ts) != len(to) or len(ts) < 2:
        return None
    out, ti = [], 0
    for k, v in ps:
        if k == 'g':
            out.append(v)
        else:
            out.append(to[ti])
            ti += 1
    return ''.join(out)


def add_newlines(s, need):
    """Chèn `need` dấu \\n vào các đoạn văn bản, chia theo độ dài."""
    if need <= 0:
        return s
    parts = split_tags(s)
    texts = [i for i, (k, _) in enumerate(parts) if k == 't' and len(parts[i][1]) > 4]
    total = sum(len(parts[i][1]) for i in texts)
    if total == 0:
        return s
    left = need
    for idx in texts:
        if left <= 0:
            break
        seg = parts[idx][1]
        k = max(1, round(need * len(seg) / total))
        k = min(k, left, seg.count(' ') or 1)
        if k <= 0:
            continue
        # chèn vào gần giữa các khoảng trắng
        words = seg.split(' ')
        if len(words) < 2:
            continue
        step = max(2, len(words) // (k + 1))
        out = []
        for wi, w in enumerate(words):
            out.append(w)
            if wi and left > 0 and wi % step == 0 and wi < len(words) - 1:
                out[-1] += '\n'
                left -= 1
        parts[idx] = ('t', ' '.join(out))
    return ''.join(v for _, v in parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    plain = zstandard.ZstdDecompressor()
    src = os.path.join(DUMP, 'Mals', 'USen.Product.150.sarc.zs')
    if not os.path.exists(src):
        src = os.path.join(GAME, 'source', 'orig_mals', 'USen.Product.150.sarc.zs')
    orig = {f.name: bytes(f.data) for f in oead.Sarc(plain.decompress(open(src, 'rb').read())).get_files()}

    n_tag = n_nl = n_skel = 0
    bad_balance = 0
    per_file = {}
    for jf in sorted(glob.glob(os.path.join(TRANS, '*.json'))):
        inner = os.path.basename(jf)[:-5].replace('__', '/')
        if inner not in orig:
            continue
        data = json.load(open(jf, encoding='utf-8'))
        src_e = parse_msbt_bytes(orig[inner])
        out, changed = {}, False
        for k, v in data.items():
            s = src_e.get(k)
            nv = fix_tags(v)
            if nv != v:
                n_tag += 1
                changed = True
            if s:
                need = s.count('\n') - nv.count('\n')
                if need > 0:
                    nv = add_newlines(nv, need)
                    n_nl += 1
                    changed = True
                if not balance_ok(nv):
                    sk = rebuild_from_skeleton(s, nv)
                    if sk:
                        nv = sk
                        n_skel += 1
                        changed = True
            bal = sum(nv.count(t) for t in OPEN_TAGS) - nv.count(CLOSE_TAG)
            if bal != 0:
                bad_balance += 1
                per_file[inner] = per_file.get(inner, 0) + 1
            out[k] = nv
        if changed and args.apply:
            os.makedirs(BACKUP, exist_ok=True)
            shutil.copy2(jf, os.path.join(BACKUP, os.path.basename(jf)))
            json.dump(out, open(jf, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    print(f'Chuỗi sửa thẻ điều khiển : {n_tag}')
    print(f'Chuỗi thêm dấu ngắt dòng : {n_nl}')
    print(f'Chuỗi dựng lại theo khung thẻ gốc : {n_skel}')
    print(f'Chuỗi thẻ đóng/mở LỆCH CÂN BẰNG sau khi sửa: {bad_balance}')
    for f, c in sorted(per_file.items(), key=lambda x: -x[1])[:8]:
        print(f'   {c:5}  {f}')
    print('ĐÃ GHI' if args.apply else 'DRY RUN (chưa ghi) — thêm --apply để ghi')


if __name__ == '__main__':
    main()
