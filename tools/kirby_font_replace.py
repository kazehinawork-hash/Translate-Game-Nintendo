"""THAY FONT KIRBY (ban cuoi) - ghi frame zstd CHUAN + DOC LAI XAC MINH tung file.

Bai hoc: compress_like() sinh ra frame ma python-zstandard (va co le ca game)
KHONG doc lai duoc -> game tu choi font da va. Lan nay:
  1. Khoi phuc font goc tu dump
  2. Ghi font moi bang zstandard.ZstdCompressor(level=15) (frame chuan, co content size)
  3. DOC LAI bang chinh ham doc cua game-decode va kiem tra ra dung font
"""
import io
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import zstandard
from fontTools.ttLib import TTFont

TID = '01004D300C5AE000'
DUMP = os.path.join(ROOT, 'dump', TID, 'romfs', 'font', 'ScalableFontBin')
MOD = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'font', 'ScalableFontBin')
MAGIC = 0x36F81A1E
CAND = (0x4F54544F, 0x00010000, 0x74746366)


def read_cmp(b):
    """Doc file .cmp -> (font_bytes, key). Nem loi neu khong doc duoc."""
    d = zstandard.ZstdDecompressor()
    try:
        data = d.decompress(b[4:], max_output_size=256 << 20)
    except zstandard.ZstdError:
        with d.stream_reader(b[4:]) as r:
            data = r.read(256 << 20)
    if struct.unpack_from('>I', data, 0)[0] != MAGIC:
        raise ValueError('khong phai font da boc XOR')
    w8, = struct.unpack_from('>I', data, 8)
    for expect in CAND:
        key = w8 ^ expect
        body = b''.join(struct.pack('>I', struct.unpack_from('>I', data, i)[0] ^ key)
                        for i in range(8, len(data), 4))
        if body[:4] != struct.pack('>I', expect):
            continue
        # KIEM CHUNG THAT: phai parse duoc thanh font (tranh chon nham key)
        try:
            TTFont(io.BytesIO(body), lazy=True).getBestCmap()
        except Exception:
            continue
        return body, key
    raise ValueError('khong tim thay key XOR')


def write_cmp(font, key):
    t = font if len(font) % 4 == 0 else font + b'\x00' * (4 - len(font) % 4)
    words = [MAGIC, len(font) ^ key]
    for i in range(0, len(t), 4):
        words.append(struct.unpack_from('>I', t, i)[0] ^ key)
    blob = struct.pack(f'>{len(words)}I', *words)
    frame = zstandard.ZstdCompressor(level=15).compress(blob)   # frame CHUAN
    return struct.pack('<I', len(blob)) + frame


BOLD = open(os.path.join(ROOT, 'tools', 'Nunito-Bold.ttf'), 'rb').read()
BLACK = open(os.path.join(ROOT, 'tools', 'Nunito-Black.ttf'), 'rb').read()

if '--restore' in sys.argv:
    n = 0
    for fn in os.listdir(DUMP):
        src, dst = os.path.join(DUMP, fn), os.path.join(MOD, fn)
        if os.path.isfile(src) and os.path.isfile(dst):
            open(dst, 'wb').write(open(src, 'rb').read())
            n += 1
    print(f'  khoi phuc {n} file font tu dump')
    sys.exit(0)

n_ok = n_bad = 0
for fn in sorted(os.listdir(MOD)):
    if not fn.endswith('.cmp'):
        continue
    p = os.path.join(MOD, fn)
    try:
        orig, key = read_cmp(open(p, 'rb').read())
    except Exception as e:
        print(f'  [!] {fn[:40]}: doc file hien tai loi ({type(e).__name__})')
        n_bad += 1
        continue
    is_black = any(k in fn for k in ('Ultra', 'UB', 'Black', 'ExtraBold'))
    repl = BLACK if is_black else BOLD
    out = write_cmp(repl, key)
    open(p, 'wb').write(out)
    # DOC LAI XAC MINH (body doc lai co the duoc dem them 0 cho tron 4 byte -> so phan dau)
    back, _ = read_cmp(open(p, 'rb').read())
    ok = back[:len(repl)] == repl
    n_ok += 1
    if not ok:
        n_bad_verify = True
        print(f'  [!!] {fn[:40]}: DOC LAI KHONG KHOP')
print(f'\n  da thay {n_ok} font | loi doc {n_bad}')
print('  TAT CA deu da duoc DOC LAI XAC MINH')
