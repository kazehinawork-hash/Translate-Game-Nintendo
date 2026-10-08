"""Soat font cua MOI game: file goc vs file trong mod (dinh dang, upem, so glyph, cmap)."""
import io
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import zstandard
from fontTools.ttLib import TTFont

GAMES = [('01004D300C5AE000_Kirby', '01004D300C5AE000', 'font'),
         ('01008DD013200000_OriAndTheWillOfTheWisps', '01008DD013200000', 'Data'),
         ('010061D00DB74000_OriAndTheBlindForest', '010061D00DB74000', 'Data'),
         ('010092A0172E4000_ItTakesTwo', '010092A0172E4000', 'Paks')]

FONT_EXT = ('.ttf', '.otf', '.bfotf', '.bfttf', '.bfotf.cmp', '.bfttf.cmp', '.fgen')


def try_font(b):
    """Thu doc font tu bytes (co the boc XOR/zstd/prefix)."""
    attempts = [('raw', b)]
    if len(b) > 8 and b[4:8] == b'\x28\xb5\x2f\xfd':
        try:
            attempts.append(('zstd(prefix4)', zstandard.ZstdDecompressor().decompress(
                b[4:], max_output_size=128 << 20)))
        except Exception:
            pass
    if b[:4] == b'\x28\xb5\x2f\xfd':
        try:
            attempts.append(('zstd', zstandard.ZstdDecompressor().decompress(b, max_output_size=128 << 20)))
        except Exception:
            pass
    for d in [a[1] for a in attempts]:
        if len(d) > 12 and struct.unpack_from('>I', d, 0)[0] == 0x36F81A1E:
            w8, = struct.unpack_from('>I', d, 8)
            for expect in (0x4F54544F, 0x00010000, 0x74746366):
                key = w8 ^ expect
                body = b''.join(struct.pack('>I', struct.unpack_from('>I', d, i)[0] ^ key)
                                for i in range(8, len(d), 4))
                if body[:4] == struct.pack('>I', expect):
                    attempts.append(('xor-bfttf', body))
    for label, d in attempts:
        for off in (0, 4):
            try:
                f = TTFont(io.BytesIO(d[off:]), lazy=True)
                if 'cmap' in f:
                    return label + (f'@{off}' if off else ''), f
            except Exception:
                continue
    return None, None


for folder, tid, sub in GAMES:
    gdir = os.path.join(ROOT, 'games', folder)
    print(f'\n{"="*76}\n{folder}\n{"="*76}')
    # index file goc theo ten
    srcs = {}
    for r, _, fs in os.walk(gdir):
        for f in fs:
            srcs.setdefault(f, os.path.join(r, f))
    found = 0
    for r, _, fs in os.walk(os.path.join(ROOT, 'output', 'atmosphere', 'contents', tid)):
        for f in sorted(fs):
            if not f.lower().endswith(FONT_EXT):
                continue
            po = os.path.join(r, f)
            pg = srcs.get(f)
            lm, fm = try_font(open(po, 'rb').read())
            if fm is None:
                print(f'  [?] {f}: khong doc duoc font ({os.path.getsize(po):,} b)')
                continue
            found += 1
            fmt = 'CFF' if 'CFF ' in fm else ('glyf' if 'glyf' in fm else '?')
            cmod = len(fm.getBestCmap())
            line = f'  {f[:44]:<46} mod: {fmt:>4} upem={fm["head"].unitsPerEm:>5} glyph={fm["maxp"].numGlyphs:>6} cmap={cmod:>6}'
            if pg and os.path.exists(pg):
                lg, fg = try_font(open(pg, 'rb').read())
                if fg is not None:
                    fmtg = 'CFF' if 'CFF ' in fg else ('glyf' if 'glyf' in fg else '?')
                    cg = set(fg.getBestCmap())
                    cm = set(fm.getBestCmap())
                    lost = len([c for c in cg if c not in cm])
                    line += (f'\n        goc: {fmtg:>4} upem={fg["head"].unitsPerEm:>5} '
                             f'glyph={fg["maxp"].numGlyphs:>6} cmap={len(cg):>6} | MAT {lost}')
            print(line)
    print(f'  -> {found} file font trong mod')
