"""Va font Kirby DUNG CACH: giu nguyen dinh dang CFF + upem + toan bo glyph goc, chi them tieng Viet.

Dinh dang file .bfotf.cmp:
    [u32 uncompressed_size][zstd frame]
ben trong (zstd giai nen ra):
    [u32 magic 0x36F81A1E][u32 true_len ^ key][tung word 4 byte ^ key]  -> OTF/CFF

Khac ban cu (patch_font_kirby.py): ban cu THAY HAN font bang subset Arial -> mat 262-340 glyph
(BH-20) va doi ca dinh dang CFF->TTF + upem 1000->2048.
"""
import io
import json
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import zstandard
from fontTools.ttLib import TTFont
from rebuild_cff_font import rebuild
from zs_util import compress_like

TID = '01004D300C5AE000'
G = os.path.join(ROOT, 'games', f'{TID}_Kirby')
SRC = os.path.join(G, 'source', 'font', 'ScalableFontBin')
OUT = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'font', 'ScalableFontBin')
SUPPLY = r'C:\Windows\Fonts\ARIALUNI.TTF'
MAGIC = 0x36F81A1E
CAND = (0x4F54544F, 0x00010000, 0x74746366)


def decomp(b):
    return zstandard.ZstdDecompressor().decompress(b[4:], max_output_size=128 << 20)


def unwrap(data):
    """-> (otf_bytes, key)"""
    if struct.unpack_from('>I', data, 0)[0] != MAGIC:
        return None, None
    w8, = struct.unpack_from('>I', data, 8)
    for expect in CAND:
        key = w8 ^ expect
        body = b''.join(struct.pack('>I', struct.unpack_from('>I', data, i)[0] ^ key)
                        for i in range(8, len(data), 4))
        if body[:4] != struct.pack('>I', expect):
            continue
        try:
            TTFont(io.BytesIO(body), lazy=True).getBestCmap()
            return body, key
        except Exception:
            continue
    return None, None


def wrap(otf, key, true_len):
    t = otf if len(otf) % 4 == 0 else otf + b'\x00' * (4 - len(otf) % 4)
    words = [MAGIC, true_len ^ key]
    for i in range(0, len(t), 4):
        words.append(struct.unpack_from('>I', t, i)[0] ^ key)
    return struct.pack(f'>{len(words)}I', *words)


def main():
    vi = json.load(open(os.path.join(G, 'translations', 'kirby_vi.json'), encoding='utf-8'))
    used = set()
    for entries in vi.values():
        for v in entries.values():
            used |= set(str(v))
    used = sorted({ord(c) for c in used if c.isprintable()})
    print(f'ky tu tieng Viet can co: {len(used)}')

    os.makedirs(OUT, exist_ok=True)
    done = 0
    for fn in sorted(os.listdir(SRC)):
        if not fn.endswith('.bfotf.cmp'):
            continue
        ob = open(os.path.join(SRC, fn), 'rb').read()
        frame = ob[4:]
        raw = zstandard.ZstdDecompressor().decompress(frame, max_output_size=128 << 20)
        otf, key = unwrap(raw)
        if not otf:
            print(f'  [!] {fn}: khong giai ma duoc -> bo qua')
            continue
        f0 = TTFont(io.BytesIO(otf))
        cg = set(f0.getBestCmap())
        upem0 = f0['head'].unitsPerEm
        new_otf = rebuild(otf, SUPPLY, used)
        # goi lai + kiem chung
        blob = wrap(new_otf, key, len(new_otf))
        back, _ = unwrap(blob)
        if back != new_otf:
            print(f'  [!!] {fn}: goi lai KHONG khop -> bo qua')
            continue
        new_frame = compress_like(frame, blob)
        out = struct.pack('<I', len(blob)) + new_frame
        open(os.path.join(OUT, fn), 'wb').write(out)

        # doc lai thanh pham
        chk_raw = zstandard.ZstdDecompressor().decompress(out[4:], max_output_size=128 << 20)
        chk_otf, _ = unwrap(chk_raw)
        fm = TTFont(io.BytesIO(chk_otf))
        cm = set(fm.getBestCmap())
        lost = len([c for c in cg if c not in cm])
        miss = len([c for c in used if c not in cm])
        ok = ('CFF ' in fm) and fm['head'].unitsPerEm == upem0 and lost == 0 and miss == 0
        done += 1
        print(f'  [{"OK" if ok else "!!"}] {fn[:36]:<38} CFF={"CFF " in fm} '
              f'upem {upem0}->{fm["head"].unitsPerEm} | cmap {len(cg):,}->{len(cm):,} '
              f'| mat {lost} | thieu VI {miss} | {len(ob):,}->{len(out):,} b')
    print(f'\n{done} font da va (giu nguyen dinh dang + upem + glyph goc)')


if __name__ == '__main__':
    raise SystemExit(main())
