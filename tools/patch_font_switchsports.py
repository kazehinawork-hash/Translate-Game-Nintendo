"""Vá font Switch Sports - CACH CHAC AN.

Font goc (VDL-LOGOG / VDL-GigaJr) co 8.207 glyph; Nunito chi 938 -> mat fullwidth,
so trong vong, mui ten, hinh khoi => UI ty so khong hien.

Giai phap: dung ARIALUNI.TTF (Arial Unicode MS - 38.928 glyph) phu DU:
ASCII, dau cau, mui ten, hinh khoi, so fullwidth ０-９, so trong vong ①-⑳, va tieng Viet.

(Dung fontTools.Merger de hop nhat Nunito + ArialUni KHONG chay duoc, nen dung thang
 ArialUni - chap nhan doi style de dam bao hien thi dung.)
"""
import io
import os
import struct
import sys

import zstandard
import oead
from fontTools.ttLib import TTFont

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
GAME = os.path.join(ROOT, 'games', '0100D2F00D5C0000_SwitchSports')
BASE = os.path.join(GAME, 'source', 'orig_font', 'Font.Nin_NX_NVN.bfarc.zs')
OUTDIR = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '0100D2F00D5C0000', 'romfs', 'Font')
OUT = os.path.join(OUTDIR, 'Font.Nin_NX_NVN.bfarc.zs')
K = 2785117442
MAGIC = 0xD99B871A
FONT = r'C:\Windows\Fonts\ARIALUNI.TTF'

TARGET = ['scft/VDL-LOGOG-BOLD.bfotf', 'scft/VDL-LOGOG-ULTRA.bfotf',
          'scft/VDL-GigaJr-ExtraBold-003_Gaiji.bfotf', 'scft/VDL-GigaJr-Ultra-003_Gaiji.bfotf']


def wrap(b):
    if len(b) % 4:
        b += b'\x00' * (4 - len(b) % 4)
    words = [MAGIC, len(b) ^ K]
    for i in range(0, len(b), 4):
        w, = struct.unpack_from('>I', b, i)
        words.append(w ^ K)
    return struct.pack(f'>{len(words)}I', *words)


def unwrap(d):
    out = bytearray()
    for i in range(8, len(d), 4):
        w, = struct.unpack_from('>I', d, i)
        out += struct.pack('>I', w ^ K)
    return bytes(out)


def main():
    sarc = oead.Sarc(zstandard.ZstdDecompressor().decompress(open(BASE, 'rb').read()))
    files = {f.name: f.data for f in sarc.get_files()}
    ttf = open(FONT, 'rb').read()
    cm = set(TTFont(io.BytesIO(ttf), lazy=True).getBestCmap())
    need = list(range(0x20, 0x7F)) + list(range(0xFF10, 0xFF1A)) + \
           [0x2190, 0x2191, 0x2192, 0x2193, 0x25CF, 0x25A0, 0x2460] + \
           [ord(c) for c in 'àáâãèéêìíòóôõùúýăđĩũơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ']
    missing = [hex(c) for c in need if c not in cm]
    print(f'Arial Unicode MS: {len(cm):,} glyph | thieu {len(missing)} {missing[:8]}')
    if missing:
        print('  -> KHONG dung font nay')
        return

    # unicodes can giu = cmap font GOC + MOI ky tu dung trong ban dich (dung chuan nhat)
    orig = set()
    for name in TARGET:
        if name in files:
            orig |= set(TTFont(io.BytesIO(unwrap(files[name])), lazy=True).getBestCmap())
    import json
    trans = set()
    tdir = os.path.join(GAME, 'translations')
    if os.path.isdir(tdir):
        for fn in os.listdir(tdir):
            if fn.endswith('.json'):
                for v in json.load(open(os.path.join(tdir, fn), encoding='utf-8')).values():
                    trans |= {ord(c) for c in str(v)}
    keep = sorted(orig | trans | set(need))
    print(f'giu {len(keep):,} codepoint (cmap goc {len(orig):,} | ban dich {len(trans):,} | mau {len(need)})')

    from fontTools import subset
    opts = subset.Options(layout_features=[], notdef_outline=True, recalc_bounds=True,
                          glyph_names=False, legacy_kern=False, drop_tables=['DSIG'],
                          hinting=False, desubroutinize=False)
    font = subset.load_font(FONT, opts)
    s = subset.Subsetter(options=opts)
    s.populate(unicodes=keep)
    s.subset(font)
    out_ttf = os.path.join(os.environ.get('TEMP', '.'), 'ss_arial_subset.ttf')
    subset.save_font(font, out_ttf, opts)
    sub_bytes = open(out_ttf, 'rb').read()
    sub_cm = set(TTFont(io.BytesIO(sub_bytes), lazy=True).getBestCmap())
    lost = [hex(c) for c in keep if c not in sub_cm]
    print(f'subset: {len(sub_cm):,} glyph | {len(sub_bytes):,} byte | thieu so voi yeu cau: {len(lost)}')

    for name in TARGET:
        if name in files:
            files[name] = wrap(sub_bytes)
            print(f'  [+] thay {name}')

    w = oead.SarcWriter.from_sarc(sarc)
    for n, d in files.items():
        w.files[n] = oead.Bytes(d)
    ns = w.write()[1]
    comp = zstandard.ZstdCompressor(level=16).compress(ns)
    os.makedirs(OUTDIR, exist_ok=True)
    open(OUT, 'wb').write(comp)
    print(f'\nda ghi {OUT} ({len(comp):,} byte)')


if __name__ == '__main__':
    main()
