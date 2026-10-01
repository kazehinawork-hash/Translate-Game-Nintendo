"""
fix_hogwarts_fr_names.py — Sửa các tên/thuật ngữ bị PHÁP HÓA còn sót trong bản dịch SUB.

Nguyên nhân: SUB dịch từ tiếng Pháp nên tên riêng bị giữ theo bản Pháp hóa
(Adélaïde Duchêne, Aile-Céleste, Pont-Désir...) trong khi MAIN (dịch từ tiếng Trung)
dùng tên gốc. Đối chiếu 2 nguồn (cột ES của game + MAIN) để xác định tên đúng.

Chạy: python tools/fix_hogwarts_fr_names.py
"""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TR = os.path.join(ROOT, 'games', '0100F7E00C70E000_Hogwarts', 'translations', 'sub_trans')

# (mau, thay the) — ap dung theo thu tu, dai truoc
RULES = [
    (r'Adélaïde\s+Duchêne', 'Adelaide Oakes'),
    (r'Aile-Céleste', 'Highwing'),
    (r'Bourg-Garenne', 'Brocburrow'),
    (r'Pont-Désir', 'Keenbridge'),
    (r'Évent\s+Spavin', 'Spavin'),
    (r'Flèches\s+d.Argent', 'Silver Arrow'),
    (r'Braise\s+Filante', 'Ember Dash'),
    (r'Créasorts?', 'Spellcraft'),
    (r'Fléreurs?', 'Kneazle'),
    (r'Lépouvantail', 'Bù Nhìn'),
    (r'Rubanvols?', 'Wind Wisp'),
    (r'Tressedifs?', 'Yew Weaver'),
    (r'Moremplis', 'Lethifold'),
    (r'Duchêne', 'Oakes'),
    (r'Adélaïde', 'Adelaide'),
    (r'Théophilus', 'Theophilus'),
    (r'Clémentine', 'Clementine'),
    (r'Lénora', 'Lenora'),
    (r'Hébrides', 'Hebrides'),
    (r'Pyrénées', 'Pyrenees'),
    (r'Béatrice', 'Beatrice'),
    (r'Pénélope', 'Penelope'),
    (r'Léandre', 'Leander'),
    (r'Fripé', 'Wrinky'),
    (r'Bardolf', 'Bardolph'),
    (r'Roland', 'Rowland'),
    (r'Vivets?', 'Snidget'),
    (r'Bubobulb', 'Bubotuber'),
    (r'Delamare', 'Affpuddle'),
    (r'Musard', 'Streeler'),
    (r'Grottaleau', 'Marunweem'),
    (r'Gransandwich', 'Barnsandwich'),
    (r'Chartier', 'Jarvey'),
    (r'Magyar', 'Rồng Đuôi Gai Hungary'),
    (r'Horglup', 'Horklump'),
    (r'Murlap', 'Murtlap'),
    (r'Violette', 'Violet'),
    (r'Noisette', 'Hazel'),
    (r'Mirabelle', 'Mirabel'),
    (r'Croup', 'Crup'),
    (r'Imperium', 'Imperius'),
    (r'Têtenbulle', 'Bubble-Head'),
    (r'Belvédère', 'Belvedere'),
    (r'Brume', 'Broom'),
    (r'Agnès', 'Agnes'),
    (r'Scribe', 'Scribner'),
    (r'mandragore', 'Mandrake'),
]
COMPILED = [(re.compile(p), r) for p, r in RULES]


def fix(s):
    out = s
    for rx, rep in COMPILED:
        out = rx.sub(rep, out)
    return out


def main():
    files = sorted(glob.glob(os.path.join(TR, 'sub_*.json')))
    total = changed = 0
    per_rule = {}
    for f in files:
        data = json.load(open(f, encoding='utf-8'))
        dirty = False
        for it in data:
            total += 1
            old = it['VI']
            new = fix(old)
            if new != old:
                for rx, _ in COMPILED:
                    if rx.search(old) and not rx.search(new):
                        per_rule[rx.pattern] = per_rule.get(rx.pattern, 0) + 1
                it['VI'] = new
                changed += 1
                dirty = True
        if dirty:
            json.dump(data, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'dong da sua: {changed}/{total}')
    for p, c in sorted(per_rule.items(), key=lambda x: -x[1]):
        print(f'   {c:4}  {p}')


if __name__ == '__main__':
    main()
