"""Boc bang dich TIENG ANH cua Unravel Two ra file nguon."""
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

from kit_localize import HIST_KEEP, try_rec

PART = r'E:\UNR_work\parts\Data.kit.0'
OUT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\games\0100E5D00CC0C000_UnravelTwo\source'
os.makedirs(OUT, exist_ok=True)

data = open(PART, 'rb').read()
off = 0
hist = b''
keeper = []
while off + 4 <= len(data):
    got = try_rec(data, off, hist)
    if not got:
        ok = False
        for d in range(1, 64):
            g = try_rec(data, off + d, hist)
            if g:
                off += d; got = g; ok = True; break
        if not ok:
            off += 64
            continue
    ln, out, kind = got
    if (b'<NEWLINE>' in out and b'<loca>' in out) or b'CREDITS_' in out or b'AFTER_CREDITS' in out:
        keeper.append((off, out))
    hist = (hist + out)[-HIST_KEEP:]
    off += 4 + ln

print(f'{len(keeper)} record bang dich trong part 0')
# ghep theo ngon ngu (nhan dien don gian)
def lang_of(b):
    scores = {
        'fr': sum(b.count(w) for w in (b' le ', b' vous ', b' des ', b' est ', b' les ')),
        'en': sum(b.count(w) for w in (b' the ', b' you ', b' and ', b' your ', b' with ')),
        'it': sum(b.count(w) for w in (b' il ', b' che ', b' per ', b' non ', b' una ')),
        'es': sum(b.count(w) for w in (b' el ', b' los ', b' que ', b' para ', b' con ')),
        'de': sum(b.count(w) for w in (b' der ', b' die ', b' und ', b' nicht ', b' Sie ')),
    }
    return max(scores, key=scores.get), max(scores.values())

by_lang = {}
for off, out in keeper:
    lg, sc = lang_of(out)
    by_lang.setdefault(lg, []).append((off, out, sc))

for lg, lst in sorted(by_lang.items()):
    tot = sum(len(o) for _, o, _ in lst)
    print(f'  {lg}: {len(lst)} record, {tot:,} byte')

if 'en' in by_lang:
    en = b''.join(o for _, o, _ in by_lang['en'])
    p = os.path.join(OUT, 'unravel_en_raw.txt')
    open(p, 'wb').write(en)
    print(f'\n>>> tieng Anh: {len(en):,} byte -> {p}')
    # tach khoa/gia tri: bang theo TUNG DONG, khoa = dong [A-Z0-9_]+, gia tri = cac dong sau do
    lines = en.split(b'\r\n')
    pairs = []
    cur_key = None
    cur_val = []
    for line in lines:
        if re.fullmatch(rb'[A-Z0-9_]{2,}', line.strip()):
            if cur_key is not None:
                pairs.append((cur_key, b'\r\n'.join(cur_val).strip()))
            cur_key = line.strip()
            cur_val = []
        elif cur_key is not None:
            cur_val.append(line)
    if cur_key is not None:
        pairs.append((cur_key, b'\r\n'.join(cur_val).strip()))
    pairs = [(k, v) for k, v in pairs if v]
    print(f'    -> {len(pairs)} cap KHOA/GIA TRI')
    for k, v in pairs[:6]:
        print(f'      {k.decode()} = {v[:80].decode("utf-8","replace")!r}')
    import json
    json.dump([{'key': k.decode(), 'en': v.decode('utf-8', 'replace')} for k, v in pairs],
              open(os.path.join(OUT, 'unravel_en.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('    da luu unravel_en.json')
