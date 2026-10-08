"""Soat TOAN BO font Kirby: file goc vs mod, xem file nao CHUA duoc va va co phu tieng Viet."""
import io
import json
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import zstandard
from fontTools.ttLib import TTFont

TID = '01004D300C5AE000'
G = os.path.join(ROOT, 'games', f'{TID}_Kirby')
SRCDIR = os.path.join(G, 'source', 'font', 'ScalableFontBin')
OUTDIR = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'font', 'ScalableFontBin')
MAGIC = 0x36F81A1E
CAND = (0x4F54544F, 0x00010000, 0x74746366)

vi = json.load(open(os.path.join(G, 'translations', 'kirby_vi.json'), encoding='utf-8'))
used = set()
for ents in vi.values():
    for v in ents.values():
        used |= set(str(v))
# bo ma dieu khien (tham so cua \x0e...)
import re
TAG = re.compile(r'\x0e[\s\S]{1,3}[\s\S]{0,2}')
used = {c for c in used if c.isprintable() and ord(c) >= 0x20}
need = sorted(ord(c) for c in used if 0x1E00 <= ord(c) <= 0x1EFF or 0xC0 <= ord(c) <= 0x3FF)


def load_font(b):
    """-> (label, TTFont) hoac (None, None)"""
    cands = []
    if b[:4] == b'\x28\xb5\x2f\xfd':
        cands.append(('zstd', b))
    elif len(b) > 8 and b[4:8] == b'\x28\xb5\x2f\xfd':
        try:
            cands.append(('zstd+4', zstandard.ZstdDecompressor().decompress(b[4:], max_output_size=128 << 20)))
        except Exception:
            pass
    cands.append(('raw', b))
    for label, d in cands:
        if len(d) > 12 and struct.unpack_from('>I', d, 0)[0] == MAGIC:
            w8, = struct.unpack_from('>I', d, 8)
            for expect in CAND:
                key = w8 ^ expect
                body = b''.join(struct.pack('>I', struct.unpack_from('>I', d, i)[0] ^ key)
                                for i in range(8, len(d), 4))
                if body[:4] == struct.pack('>I', expect):
                    try:
                        f = TTFont(io.BytesIO(body), lazy=True)
                        f.getBestCmap()
                        return f'{label}+xor', f
                    except Exception:
                        pass
        try:
            f = TTFont(io.BytesIO(d), lazy=True)
            f.getBestCmap()
            return label, f
        except Exception:
            pass
    return None, None


print(f'ky tu tieng Viet co dau can co: {len(need)}\n')
print(f'{"file":<44}{"goc":<30}{"mod":<30}')
for fn in sorted(os.listdir(SRCDIR)):
    pg = os.path.join(SRCDIR, fn)
    po = os.path.join(OUTDIR, fn)
    lg, fg = load_font(open(pg, 'rb').read())
    if fg is None:
        print(f'{fn[:42]:<44}{"khong doc duoc":<30}')
        continue
    cg = set(fg.getBestCmap())
    mg = len([c for c in need if c not in cg])
    fmtg = 'CFF' if 'CFF ' in fg else ('glyf' if 'glyf' in fg else '?')
    info_g = f'{fmtg} upem={fg["head"].unitsPerEm} cmap={len(cg):,} thieuVI={mg}'
    if os.path.exists(po):
        lm, fm = load_font(open(po, 'rb').read())
        if fm is not None:
            cm = set(fm.getBestCmap())
            mm = len([c for c in need if c not in cm])
            fmtm = 'CFF' if 'CFF ' in fm else ('glyf' if 'glyf' in fm else '?')
            info_m = f'{fmtm} upem={fm["head"].unitsPerEm} cmap={len(cm):,} thieuVI={mm}'
            lost = len([c for c in cg if c not in cm])
            info_m += f' mat={lost}'
        else:
            info_m = 'KHONG DOC DUOC'
    else:
        info_m = '*** KHONG CO TRONG MOD ***'
    print(f'{fn[:42]:<44}{info_g:<30}{info_m}')
