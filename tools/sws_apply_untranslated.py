"""Khoi phuc token [[n]] -> ma dieu khien goc, roi ghi vao translations/ cua Switch Sports."""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.join(ROOT, 'games', '0100D2F00D5C0000_SwitchSports')
T = os.path.join(G, 'translations')
TODO = os.path.join(T, '_todo')
CONS = os.path.join(ROOT, 'games', '_consistency')

TOKEN = re.compile(r'\[\[(\d+)\]\]')


def main():
    work = json.load(open(os.path.join(CONS, 'sws_work.json'), encoding='utf-8'))
    trans = {}
    for i in range(1, 10):
        p = os.path.join(TODO, f'vi_{i:02d}.json')
        if os.path.exists(p):
            d = json.load(open(p, encoding='utf-8'))
            trans.update(d)
            print(f'  nap vi_{i:02d}.json: {len(d)} muc')
    print(f'tong ban dich (da che): {len(trans):,}')

    ok = miss = badtok = 0
    per_file = {}
    problems = []
    for it in work:
        m = it['masked']
        vi_masked = trans.get(m)
        if vi_masked is None:
            miss += 1
            if miss <= 5:
                problems.append(f'[thieu ban dich] {it["file"]}::{it["key"]} = {m[:60]!r}')
            continue
        nums = [int(x) for x in TOKEN.findall(vi_masked)]
        want = list(range(1, len(it['tokens']) + 1))
        if sorted(nums) != want:
            badtok += 1
            if badtok <= 5:
                problems.append(f'[loi token] {it["file"]}::{it["key"]} can {want} co {sorted(nums)}')
            continue
        # khoi phuc
        out = TOKEN.sub(lambda mo: it['tokens'][int(mo.group(1)) - 1], vi_masked)
        per_file.setdefault(it['file'], {})[it['key']] = out
        ok += 1

    print(f'\nkhoi phuc OK: {ok} | thieu ban dich: {miss} | loi token: {badtok}')
    for p in problems:
        print('  ' + p)

    # ghi vao tung file json cua game (gop voi ban cu)
    nfile = 0
    for fname, items in per_file.items():
        p = os.path.join(T, fname + '.json')
        old = {}
        if os.path.exists(p):
            old = json.load(open(p, encoding='utf-8'))
        before = len(old)
        changed = 0
        for k, v in items.items():
            if old.get(k) != v:
                changed += 1
            old[k] = v
        json.dump(old, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        nfile += 1
        print(f'  {fname}.json: {before} -> {len(old)} muc (doi {changed})')
    print(f'\nda ghi {nfile} file')


if __name__ == '__main__':
    raise SystemExit(main())
