"""
fix_hades2_qa_bugs.py — Sửa lỗi do cổng QA phát hiện trong bản dịch Hades II.

 1. 14 chuỗi có dấu `}` THỪA ở cuối (vd: '{#Emph}bộ gõ}' -> '{#Emph}bộ gõ')
    Quy tắc: giá trị kết thúc bằng `}` và số `}` = số `{` + 1  ->  bỏ `}` cuối.
 2. 2 chuỗi lọt chữ Trung: '亲眼' -> 'tận mắt'; '在那里' -> 'ở đó'

Chạy: python tools/fix_hades2_qa_bugs.py   (rồi build lại bằng build_hades2_mod.py)
"""
import glob
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(ROOT, 'games', '0100A00019DE0000_Hades2', 'translations', 'Game', 'Text', 'en')

ID_RE = re.compile(r'\bId\s*=\s*"([^"]+)"')
DN_RE = re.compile(r'(DisplayName\s*=\s*)(?:"""(.*?)"""|"([^"]*)")', re.S)
ZH = {'亲眼': 'tận mắt', '在那里': 'ở đó'}


def fix_file(path):
    text = open(path, encoding='utf-8').read()
    ids = [(m.start(), m.group(1)) for m in ID_RE.finditer(text)]
    out = text
    n_brace = n_zh = 0
    # sửa từ cuối lên để không lệch vị trí
    for i in range(len(ids) - 1, -1, -1):
        pos, name = ids[i]
        end = ids[i + 1][0] if i + 1 < len(ids) else len(text)
        m = DN_RE.search(out, pos, end)
        if not m:
            continue
        val = m.group(2) if m.group(2) is not None else (m.group(3) or '')
        nv = val
        for zh, vi in ZH.items():
            if zh in nv:
                nv = nv.replace(zh, vi)
                n_zh += 1
        if nv.count('}') == nv.count('{') + 1:
            r = nv.rstrip()
            if r.endswith('}'):                      # dang 1: dau } thua O CUOI
                nv = r[:-1].rstrip()
                n_brace += 1
            else:                                     # dang 2: dau } thua O GIUA
                # '{#Emph}noi dung}' -> '{#Emph}noi dung'  (tag {#...} tu dong, } sau la thua)
                nv2 = re.sub(r'(\{#[A-Za-z0-9_]+\})([^{}]*?)\}', r'\1\2', nv, count=1)
                if nv2 != nv:
                    nv = nv2
                    n_brace += 1
        if nv != val:
            if m.group(2) is not None:
                new = m.group(1) + '"""' + nv + '"""'
            else:
                new = m.group(1) + '"' + nv + '"'
            out = out[:m.start()] + new + out[m.end():]
    if out != text:
        open(path, 'w', encoding='utf-8').write(out)
    return n_brace, n_zh


def main():
    tb = tz = 0
    for f in sorted(glob.glob(os.path.join(DIR, '*.sjson'))):
        b, z = fix_file(f)
        if b or z:
            print(f'  {os.path.basename(f)}: bo {b} dau }} thua, sua {z} chu Trung')
            tb += b
            tz += z
    print(f'TONG: {tb} dau ngoac thua, {tz} chu Trung')


if __name__ == '__main__':
    main()
