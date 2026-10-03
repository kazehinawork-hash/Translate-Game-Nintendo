"""Boc archive .kit Unravel Two - ban toi uu, tim record bang dich theo ngon ngu."""
import os
import re
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')

MAXOFF = 65535
HIST_KEEP = 262140  # giu dem lon hon cua so (tranh truot tu dien)


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit_lz4dict import Lz4DictError as Lz4Err, decode_block


def looks_json(b):
    s = b.lstrip()[:1]
    return s in (b'{', b'[') and b'"' in b[:200]


def try_rec(data, off, hist):
    if off + 4 > len(data):
        return None
    ln = struct.unpack_from('<I', data, off)[0]
    if not (4 <= ln <= 40_000_000) or off + 4 + ln > len(data):
        return None
    pl = data[off + 4:off + 4 + ln]
    try:
        return (ln, decode_block(pl, hist), 'lz4')
    except Lz4Err:
        pass
    if looks_json(pl):
        return (ln, pl, 'raw')
    return None


LANG_HINT = {
    'en': [b' the ', b' you ', b' and ', b' your ', b' with '],
    'fr': [b' le ', b' la ', b' vous ', b' des ', b' est '],
    'de': [b' der ', b' die ', b' und ', b' nicht ', b' Sie '],
    'es': [b' el ', b' los ', b' que ', b' para ', b' con '],
    'it': [b' il ', b' che ', b' per ', b' con ', b' non '],
    'ja': [],
    'ko': [],
    'ru': [],
    'pt': [b' que ', b' para ', b' com ', b' n\\xe3o ', b' uma '],
}


def guess_lang(b):
    best, score = None, 0
    for lang, words in LANG_HINT.items():
        c = sum(b.count(w) for w in words)
        if c > score:
            best, score = lang, c
    return best, score


if __name__ == '__main__':
    tag = sys.argv[1]
    part = sys.argv[2]
    outdir = r'E:\UNR_work\loc'
    os.makedirs(outdir, exist_ok=True)
    data = open(part, 'rb').read()
    off = 0
    hist = b''
    n = 0
    resync = 0
    saved = []
    while off + 4 <= len(data):
        got = try_rec(data, off, hist)
        if not got:
            ok = False
            for d in range(1, 64):
                g = try_rec(data, off + d, hist)
                if g:
                    off += d; resync += 1; got = g; ok = True; break
            if not ok:
                off += 64
                continue
        ln, out, kind = got
        n += 1
        # record bang dich?
        if (b'<NEWLINE>' in out and b'<loca>' in out) or b'CREDITS_' in out or b'AFTER_CREDITS' in out:
            lang, sc = guess_lang(out)
            kcount = out.count(b'\r\n\r\n')
            lang = lang or 'unknown'
            p = os.path.join(outdir, f'{tag}_{lang}_{off:x}.txt')
            open(p, 'wb').write(out)
            saved.append((lang, off, len(out), kcount, sc, p))
        hist = (hist + out)[-HIST_KEEP:]
        off += 4 + ln
    print(f'{tag}: {n} record ({resync} resync) | {len(saved)} record bang dich', flush=True)
    for lang, off, sz, kc, sc, p in saved:
        print(f'   [{lang}] @{off:#x} {sz:,} byte | ~{kc} muc | score {sc}', flush=True)
