"""Chuan bi dich 173 chuoi chua dich cua Switch Sports.

- Che MOI doan ma dieu khien / glyph PUA / ky tu CJK-Hangul-Kana thành token [[n]].
- Xuat file cong viec cho subagent (chuoi da che) + bang khoi phuc token.
- Khi nhan ban dich: kiem tra tap token phai KHOP roi moi khoi phuc.

Dung:
    python tools/sws_prepare_untranslated.py            # tao file cong viec
    python tools/sws_apply_untranslated.py             # khoi phuc + ghi vao translations/
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = os.path.join(ROOT, 'games', '0100D2F0' + '0D5C0000_SwitchSports')
G = os.path.join(ROOT, 'games', '0100D2F00D5C0000_SwitchSports')
CONS = os.path.join(ROOT, 'games', '_consistency')
CH = 45


def is_special(c):
    o = ord(c)
    if o < 0x20 and c not in '\n\t':
        return True
    if 0xE000 <= o <= 0xF8FF:              # PUA (glyph icon)
        return True
    if o in (0xFFFE, 0xFFFF):
        return True
    if 0x2E80 <= o <= 0x9FFF:              # CJK
        return True
    if 0xAC00 <= o <= 0xD7FF:              # Hangul (chua gia tri offset)
        return True
    if 0x1100 <= o <= 0x11FF:
        return True
    return False


def mask(s):
    """-> (chuoi_da_che, [cac_doan_goc])"""
    out = []
    toks = []
    i = 0
    n = 1
    while i < len(s):
        if is_special(s[i]):
            j = i
            while j < len(s) and is_special(s[j]):
                j += 1
            toks.append(s[i:j])
            out.append(f'[[{n}]]')
            n += 1
            i = j
        else:
            out.append(s[i])
            i += 1
    return ''.join(out), toks


def main():
    d = json.load(open(os.path.join(CONS, 'untranslated_switchsports.json'), encoding='utf-8'))
    items = []
    for name, m in d.items():
        for k, v in sorted(m.items()):
            f = k.split('::', 1)[0]
            kk = k.split('::', 1)[1]
            masked, toks = mask(v)
            items.append(dict(file=f, key=kk, en=v, masked=masked, tokens=toks))

    simple = [it for it in items if not it['tokens']]
    coded = [it for it in items if it['tokens']]
    print(f'tong {len(items)} | KHONG ma dieu khien: {len(simple)} | CO ma dieu khien: {len(coded)}')

    json.dump(items, open(os.path.join(CONS, 'sws_work.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    # chunk cho subagent: mang cac chuoi DA CHE
    todo = os.path.join(G, 'translations', '_todo')
    os.makedirs(todo, exist_ok=True)
    vals = [it['masked'] for it in items]
    nch = 0
    for i in range(0, len(vals), CH):
        nch += 1
        part = vals[i:i + CH]
        json.dump(part, open(os.path.join(todo, f'un_{nch:02d}.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        print(f'  un_{nch:02d}.json: {len(part)} chuoi')
    print(f'\n-> {len(items)} muc, {nch} chunk tai {todo}')
    print('   cac muc co ma dieu khien thi token [[n]] phai duoc giu nguyen')


if __name__ == '__main__':
    raise SystemExit(main())
