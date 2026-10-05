"""
check_glossary.py — Ép dùng từ điển + kiểm tra TÍNH NHẤT QUÁN thuật ngữ.

Hai việc:
  A. GLOSSARY: nếu câu NGUỒN có chứa thuật ngữ trong `glossary/*.csv` thì câu DỊCH phải chứa
     bản dịch tương ứng (so theo TỪ, không phân biệt hoa/thường). Lệch -> báo.
  B. NHẤT QUÁN: cùng một câu nguồn (hoặc cùng một chuỗi nguồn) mà dịch ra 2 kiểu khác nhau
     -> báo (đây chính là loại lỗi 'Kneazle' vs 'Fléreur').

Dùng:
    python tools/check_glossary.py --game hogwarts            # chỉ báo cáo
    python tools/check_glossary.py --game hogwarts --strict   # lệch glossary -> exit 1
    python tools/check_glossary.py --game hades2 --suggest 20 # gợi ý thuật ngữ còn thiếu

Cột trong glossary được nhận tự động (source/target, English/Vietnamese, Original/Vietnamese…).
"""
import argparse
import collections
import csv
import glob
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import qa_text as Q  # noqa: E402

SRC_COLS = ('source', 'english', 'original', 'term', 'key', 'en')
DST_COLS = ('target', 'vietnamese', 'vi', 'translation', 'value')
WORD = re.compile(r"[\w'’-]+", re.UNICODE)
# Glossary dùng CHUNG cho mọi game + glossary riêng của từng game.
# (Không áp glossary của game này sang game khác — gây dương tính giả.)
# LƯU Ý: `master.csv` hiện đang mang nội dung của Switch Sports (Mode/UI) → chỉ dùng cho
# game đó; Ori chưa có glossary riêng (dùng --suggest để gợi ý rồi tạo glossary/ori.csv).
GAME_GLOSSARY = {
    'hogwarts': ['master.csv', 'hogwarts_legacy.csv'],
    'hades2': ['master.csv', 'hades2.csv'],
    'ori': ['ori.csv'],
    'obf': ['ori_bf.csv'],
    'switchsports': ['master.csv'],
    'kirby': ['kirby.csv'],
}


def load_glossary(game):
    """Trả [(source, target, category, file)] đã chuẩn hoá cột — CHỈ lấy file của game này."""
    wanted = GAME_GLOSSARY.get(game, ['master.csv'])
    out = []
    for fn in wanted:
        f = os.path.join(ROOT, 'glossary', fn)
        if not os.path.exists(f):
            continue
        try:
            rows = list(csv.DictReader(open(f, encoding='utf-8-sig')))
        except Exception as e:
            print('  !', fn, e)
            continue
        if not rows:
            continue
        cols = {c.lower().strip(): c for c in rows[0].keys() if c}
        sc = next((cols[c] for c in SRC_COLS if c in cols), None)
        tc = next((cols[c] for c in DST_COLS if c in cols), None)
        cc = cols.get('category') or cols.get('context') or None
        if not sc or not tc:
            print('  !', fn, 'không nhận ra cột nguồn/đích:', list(cols))
            continue
        for r in rows:
            s, t = (r.get(sc) or '').strip(), (r.get(tc) or '').strip()
            if s and t:
                out.append((s, t, (r.get(cc) or '').strip() if cc else '', fn))
    return out


def build_index(gloss):
    """first-word (lower) -> [(source_words, source, target, exact_only)]."""
    idx = collections.defaultdict(list)
    for s, t, cat, f in gloss:
        w = [x.lower() for x in WORD.findall(s)]
        if not w:
            continue
        # Từ ĐƠN (vd "On", "Back", "Par") rất dễ khớp bừa giữa câu -> chỉ chấp nhận khớp CHÍNH XÁC.
        exact_only = len(w) == 1
        idx[w[0]].append((w, s, t, exact_only))
    return idx


def check_game(game, gloss_idx, verbose=False):
    missing = collections.defaultdict(list)
    inconsistent = collections.defaultdict(set)
    total_entries = 0
    n_terms = sum(len(v) for v in gloss_idx.values())

    for name, src, built in Q.ADAPTERS[game]():
        for k, v in built.items():
            total_entries += 1
            s = src.get(k)
            if s is None:
                continue
            inconsistent[s].add(v)
            toks = [x.lower() for x in WORD.findall(s)]
            for i, w in enumerate(toks):
                for words, gsrc, gtgt, exact_only in gloss_idx.get(w, ()):
                    if exact_only:
                        # từ đơn: chỉ tính khi CẢ CÂU đúng bằng thuật ngữ
                        if len(toks) != 1 or toks[0] != words[0]:
                            continue
                    elif toks[i:i + len(words)] != words:
                        continue
                    if gtgt.lower() not in v.lower():
                        missing[gsrc].append((k, s[:60], v[:70], gtgt))

    print(f'\n=== {game}: {total_entries} mục | glossary: {n_terms} thuật ngữ')
    if missing:
        print(f'  [LỆCH GLOSSARY] {len(missing)} thuật ngữ bị dịch thiếu/sai:')
        for g, items in sorted(missing.items(), key=lambda x: -len(x[1]))[:12]:
            k, s, v, t = items[0]
            print(f'    "{g}" -> phải có "{t}" | {len(items)} lần | vd [{k}] {v[:60]!r}')
    else:
        print('  [GLOSSARY] OK — không có vi phạm')

    multi = {s: vs for s, vs in inconsistent.items() if len(vs) > 1}
    real = {}
    case_only = {}
    for s, vs in multi.items():
        norm = {v.lower() for v in vs}
        (case_only if len(norm) == 1 else real)[s] = vs
    print(f'  [NHẤT QUÁN] {len(real)} câu nguồn dịch KHÁC NGHĨA + {len(case_only)} chỉ khác hoa/thường')
    for s, vs in list(real.items())[:5]:
        print(f'    NGUỒN: {s[:58]!r}')
        for v in list(vs)[:3]:
            print(f'        -> {v[:70]!r}')
    return sum(len(x) for x in missing.values()), len(real)


def suggest(game, n=20):
    """Gợi ý thuật ngữ nên thêm vào glossary: từ nguồn VIẾT HOA xuất hiện nhiều (kèm ví dụ dịch)."""
    cnt = collections.Counter()
    ex = {}
    for name, src, built in Q.ADAPTERS[game]():
        for k, v in built.items():
            s = src.get(k) or ''
            if not any(not c.isascii() for c in v):
                continue                       # chỉ lấy câu có bản dịch thật
            for w in set(re.findall(r'\b[A-Z][a-zA-Z]{3,}\b', s)):
                cnt[w] += 1
                ex.setdefault(w, (s.strip()[:60], v.strip()[:70]))
    print(f'\n=== GỢI Ý thuật ngữ cho {game} (từ nguồn viết hoa, nên đưa vào glossary/<game>.csv) ===')
    print(f'   {"số lần":>6}  {"thuật ngữ":22} ví dụ (nguồn -> dịch)')
    for w, c in cnt.most_common(n):
        s, v = ex[w]
        print(f'   {c:6}  {w:22} {s!r} -> {v!r}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', required=True, choices=sorted(Q.ADAPTERS))
    ap.add_argument('--strict', action='store_true', help='lệch glossary -> mã lỗi 1')
    ap.add_argument('--suggest', type=int, default=0, help='gợi ý N thuật ngữ nên thêm vào glossary')
    ap.add_argument('--verbose', action='store_true')
    a = ap.parse_args()

    gloss = load_glossary(a.game)
    print(f'glossary: {len(gloss)} mục (dùng cho {a.game}: {", ".join(GAME_GLOSSARY.get(a.game, []))})')
    n_missing, n_multi = check_game(a.game, build_index(gloss), verbose=a.verbose)
    if a.suggest:
        suggest(a.game, a.suggest)
    return 1 if (a.strict and n_missing) else 0


if __name__ == '__main__':
    raise SystemExit(main())
