"""Va font tieng Viet cho Kirby and the Forgotten Land.

Dinh dang (da giai ma):
  .bfotf.cmp = [u32 uncompressed_size][zstd frame]
  ben trong  = [u32 magic 0x36F81A1E][u32 size ^ key][tung word 4 byte ^ key]  -> OTF/TTF

Cach va: thay noi dung font bang SUBSET cua Arial Unicode MS = (cmap font goc U ky tu dung
trong ban dich), giu nguyen toan bo glyph goc + them tieng Viet (bai hoc BH-20).
"""
import io
import json
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
import zstandard
from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '01004D300C5AE000'
G = os.path.join(ROOT, 'games', f'{TID}_Kirby')
SRC = os.path.join(G, 'source', 'font', 'ScalableFontBin')
OUT = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'font', 'ScalableFontBin')
SUPPLY = r'C:\Windows\Fonts\ARIALUNI.TTF'
MAGIC = 0x36F81A1E
TMP = os.path.join(os.environ.get('TEMP', '.'), 'kirby_font_work')
os.makedirs(TMP, exist_ok=True)


def decomp(b):
    return zstandard.ZstdDecompressor().decompress(b[4:], max_output_size=64 << 20)


def comp(b):
    return struct.pack('<I', len(b)) + zstandard.ZstdCompressor(level=16).compress(b)


def unwrap(data):
    """Thu tung khoa ung vien; chon khoa cho ra FONT DOC DUOC (tranh kiem tra vong tron)."""
    w0, = struct.unpack_from('>I', data, 0)
    if w0 != MAGIC:
        return None, None
    body, = struct.unpack_from('>I', data, 8)
    for expect in (0x4F54544F, 0x00010000, 0x74746366):
        key = body ^ expect
        out = bytearray()
        for i in range(8, len(data), 4):
            w, = struct.unpack_from('>I', data, i)
            out += struct.pack('>I', w ^ key)
        if bytes(out[:4]) != struct.pack('>I', expect):
            continue
        try:
            TTFont(io.BytesIO(bytes(out)), lazy=True).getBestCmap()
            return bytes(out), key
        except Exception:
            continue
    return None, None


def wrap_and_check(ttf, key):
    """Goi lai roi DOC LAI bang chinh ham unwrap -> dam bao key dung."""
    if len(ttf) % 4:
        t = ttf + b'\x00' * (4 - len(ttf) % 4)
    else:
        t = ttf
    words = [MAGIC, len(t) ^ key]
    for i in range(0, len(t), 4):
        w, = struct.unpack_from('>I', t, i)
        words.append(w ^ key)
    blob = struct.pack(f'>{len(words)}I', *words)
    back, _ = unwrap(blob)
    return blob if back == t else None


def main():
    vi = json.load(open(os.path.join(G, 'translations', 'kirby_vi.json'), encoding='utf-8'))
    used = set()
    for entries in vi.values():
        for v in entries.values():
            used |= set(str(v))
    used = {c for c in used if c.isprintable()}
    print(f'ky tu dung trong ban dich: {len(used)}')

    os.makedirs(OUT, exist_ok=True)
    done = 0
    for fn in sorted(os.listdir(SRC)):
        if not fn.endswith('.bfotf.cmp'):
            continue
        data = decomp(open(os.path.join(SRC, fn), 'rb').read())
        otf, key = unwrap(data)
        if not otf:
            print(f'  bo qua {fn} (khong giai ma duoc)')
            continue
        try:
            f = TTFont(io.BytesIO(otf), lazy=True)
            orig = set(f.getBestCmap())
        except Exception as e:
            print(f'  bo qua {fn}: {type(e).__name__}')
            continue
        keep = sorted(orig | {ord(c) for c in used})
        opts = subset.Options(layout_features=[], notdef_outline=True, recalc_bounds=True,
                              glyph_names=False, legacy_kern=False, drop_tables=['DSIG'], hinting=False)
        sup = subset.load_font(SUPPLY, opts)
        s = subset.Subsetter(options=opts)
        s.populate(unicodes=keep)
        s.subset(sup)
        p = os.path.join(TMP, 'sub.ttf')
        subset.save_font(sup, p, opts)
        sub = open(p, 'rb').read()
        cm = set(TTFont(io.BytesIO(sub), lazy=True).getBestCmap())
        miss = [c for c in used if ord(c) not in cm and ord(c) < 0xE000]
        wrapped = wrap_and_check(sub, key)
        if wrapped is None:
            print(f'  !! {fn}: goi lai that bai, bo qua')
            continue
        open(os.path.join(OUT, fn), 'wb').write(comp(wrapped))
        done += 1
        # kiem chung doc lai
        back, _ = unwrap(decomp(open(os.path.join(OUT, fn), 'rb').read()))
        chk = set(TTFont(io.BytesIO(back), lazy=True).getBestCmap()) if back else set()
        print(f'  [+] {fn[:38]:<40} {len(orig):>6,} -> {len(cm):>6,} glyph | thieu chu dich {len(miss)} | doc lai {"OK" if chk == cm else "LOI"}')
    print(f'\n{done} font Latin da va -> {OUT}')


if __name__ == '__main__':
    main()
