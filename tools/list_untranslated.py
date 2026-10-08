"""Liet ke DAY DU chuoi chua dich cua tung game (dung lai adapter cua qa_text.py).

Dung: python tools/list_untranslated.py [game ...]
Xuat ra games/_consistency/untranslated_<game>.json + in tom tat.
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import qa_text  # noqa: E402

OUTDIR = os.path.join(ROOT, 'games', '_consistency')
os.makedirs(OUTDIR, exist_ok=True)


def untranslated_of(src, built):
    out = {}
    for k, v in built.items():
        s = src.get(k)
        if s is None:
            continue
        if v == s and len(v) >= 8 and len(v.split()) >= 2:
            out[k] = s
    return out


def main():
    games = sys.argv[1:] or ['hogwarts', 'hades2', 'switchsports']
    grand = 0
    for game in games:
        if game not in qa_text.ADAPTERS:
            print(f'  (bo qua {game}: khong co adapter)')
            continue
        print(f'\n{"="*70}\n{game.upper()}\n{"="*70}')
        allun = {}
        for name, src, built in qa_text.ADAPTERS[game]():
            un = untranslated_of(src, built)
            allun[name] = un
            print(f'\n  --- {name}: nguon {len(src):,} | build {len(built):,} | CHUA DICH {len(un):,}')
            for k, v in sorted(un.items())[:15]:
                print(f'      {k[:50]:<50} {v[:78]!r}')
            if len(un) > 15:
                print(f'      ... con {len(un)-15} muc nua')
            grand += len(un)
        p = os.path.join(OUTDIR, f'untranslated_{game}.json')
        json.dump(allun, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'\n  -> {p}')
    print(f'\nTONG CHUA DICH: {grand:,}')


if __name__ == '__main__':
    raise SystemExit(main())
