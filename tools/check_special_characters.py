"""
check_special_characters.py — Soát lỗi ký tự đặc biệt trong file bản dịch.

Kiểm tra:
  1. Gõ nhầm escape sequence: `/n`, `/t` (phải là `\\n`, `\\t`).
  2. Ngoặc nhọn `{...}` không cân / placeholder bị phá.
  3. Ký tự lạ còn sót: CJK (Trung/Nhật), Hangul (Hàn), Arabic, Kana.
  4. Nếu có file nguồn: đối chiếu multiset placeholder và số dòng `\\n` giữa nguồn ↔ bản dịch.

Cách dùng (chạy từ gốc dự án):
    python tools/check_special_characters.py <file_dich.json> [file_nguon.json]

File phải là JSON mảng các object. Tự nhận field:
  - khoá     : `Key` hoặc `Id`
  - bản dịch : `Vietnamese` hoặc `VI`
  - nguồn    : `Source_ZH` / `Source_FR` / `Source_ES` / `Source` / `Source_EN`
"""
import collections
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

KEY_FIELDS = ('Key', 'Id')
VAL_FIELDS = ('Vietnamese', 'VI')
SRC_FIELDS = ('Source_ZH', 'Source_FR', 'Source_ES', 'Source_EN', 'Source')

TOK = re.compile(r'\{[^{}]*\}|%[0-9\$]*[sdif]|<(?:i|/i)>|<img[^>]*/>|\\n|\\t|\[\[|\]\]')
RANGES = {
    'CJK': [(0x3000, 0x303f), (0x3400, 0x4dbf), (0x4e00, 0x9fff), (0xf900, 0xfaff), (0xff00, 0xffef)],
    'Hangul': [(0x1100, 0x11ff), (0x3130, 0x318f), (0xac00, 0xd7ff)],
    'Kana': [(0x3040, 0x30ff)],
    'Arabic': [(0x0600, 0x06ff), (0x0750, 0x077f), (0xfb50, 0xfdff), (0xfe70, 0xfeff)],
}


def weird(v):
    out = set()
    for ch in v:
        o = ord(ch)
        for n, rs in RANGES.items():
            if any(a <= o <= b for a, b in rs):
                out.add(n)
    return out


def load(path):
    data = json.load(open(path, encoding='utf-8-sig'))
    if isinstance(data, dict):
        data = data.get('translations', list(data.values()))
    rows = []
    for it in data:
        if not isinstance(it, dict):
            continue
        k = next((it[f] for f in KEY_FIELDS if f in it), None)
        if k is None:
            continue
        v = next((it[f] for f in VAL_FIELDS if f in it), '')
        s = next((it[f] for f in SRC_FIELDS if f in it), None)
        rows.append((k, v or '', s))
    return rows


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    tr = load(sys.argv[1])
    src = {k: s for k, _, s in load(sys.argv[2])} if len(sys.argv) > 2 else {}
    print(f'file dich : {sys.argv[1]} ({len(tr)} muc)')
    if src:
        print(f'file nguon: {sys.argv[2]} ({len(src)} muc)')

    errs = []
    stats = collections.Counter()
    for k, v, s in tr:
        if re.search(r'(?<!\\)/[nt]\b', v):
            errs.append(f'{k}: go nham escape "/n" hoac "/t"')
        if v.count('{') != v.count('}'):
            errs.append(f'{k}: ngoac nhon khong can {{ }}')
        w = weird(v)
        if w:
            stats['ky_tu_la'] += 1
            errs.append(f'{k}: con ky tu la {sorted(w)}')
        if not v.strip():
            stats['rong'] += 1
            errs.append(f'{k}: chuoi rong')
        if src and s is not None:
            if collections.Counter(TOK.findall(s)) != collections.Counter(TOK.findall(v)):
                stats['lech_placeholder'] += 1
                errs.append(f'{k}: lech placeholder/tag so voi nguon')
            if s.count('\n') != v.count('\n'):
                stats['lech_xuong_dong'] += 1
                errs.append(f'{k}: lech so xuong dong ({s.count(chr(10))} vs {v.count(chr(10))})')

    if errs:
        print(f'\nLOI ({len(errs)}):')
        for e in errs[:40]:
            print('  [E]', e)
        if len(errs) > 40:
            print(f'  ... va {len(errs) - 40} loi nua')
        return 2
    print('\nOK - khong phat hien loi dac biet.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
