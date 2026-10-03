"""Quet tat ca 12 part, luu moi record bang dich (dung cho Unravel Two)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

from kit_localize import HIST_KEEP, try_rec

PARTS = r'E:\UNR_work\parts'
OUT = r'E:\UNR_work\loc'
os.makedirs(OUT, exist_ok=True)

files = sorted(os.listdir(PARTS), key=lambda x: int(x.rsplit('.', 1)[-1]))
for f in files:
    tag = 'p' + f.rsplit('.', 1)[-1]
    data = open(os.path.join(PARTS, f), 'rb').read()
    off = 0
    hist = b''
    n = 0
    saved = 0
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
        n += 1
        if (b'<NEWLINE>' in out and b'<loca>' in out) or b'CREDITS_' in out or b'AFTER_CREDITS' in out:
            open(os.path.join(OUT, f'{tag}_{off:x}.bin'), 'wb').write(out)
            saved += 1
        hist = (hist + out)[-HIST_KEEP:]
        off += 4 + ln
    print(f'{f}: {n} record | {saved} record bang dich', flush=True)
print('XONG', flush=True)
