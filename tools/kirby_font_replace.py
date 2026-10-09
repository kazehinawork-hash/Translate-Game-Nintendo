"""THAY HAN font cua Kirby bang font ngoai (Nunito) - day du dau tieng Viet.

Theo de xuat cua nguoi dung: khong can bat chuoc dinh dang font cua Nintendo,
chi can mot font DAY DU glyph. Game nap font qua FreeType nen TTF chuan la du.

- Ten font co -B/-Bold -> Nunito-Bold;  -UB/-Ultra/-ExtraBold/Black -> Nunito-Black
- Boc lai dung dinh dang container cua game:
      [u32 out_len][ zstd( [MAGIC][true_len ^ key][words ^ key] ) ]
  (key giu nguyen cua font goc; tham so zstd khop file goc)
"""
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import zstandard
from zs_util import compress_like

TID = '01004D300C5AE000'
FONTDIR = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'font', 'ScalableFontBin')
MAGIC = 0x36F81A1E
CAND = (0x4F54544F, 0x00010000, 0x74746366)

BOLD = open(os.path.join(ROOT, 'tools', 'Nunito-Bold.ttf'), 'rb').read()
BLACK = open(os.path.join(ROOT, 'tools', 'Nunito-Black.ttf'), 'rb').read()
print(f'Nunito-Bold {len(BOLD):,} b | Nunito-Black {len(BLACK):,} b')


def decomp_frame(b):
    """Doc frame zstd du content-size co hay khong."""
    raw = b[4:]
    d = zstandard.ZstdDecompressor()
    try:
        return d.decompress(raw, max_output_size=128 << 20)
    except zstandard.ZstdError:
        # frame khong ghi content size -> dung stream_reader
        with d.stream_reader(raw) as r:
            return r.read(128 << 20)


def get_key(data):
    """Lay key XOR cua font goc."""
    if struct.unpack_from('>I', data, 0)[0] != MAGIC:
        return None
    w8, = struct.unpack_from('>I', data, 8)
    for expect in CAND:
        key = w8 ^ expect
        body = b''.join(struct.pack('>I', struct.unpack_from('>I', data, i)[0] ^ key)
                        for i in range(8, len(data), 4))
        if body[:4] == struct.pack('>I', expect):
            return key
    return None


def wrap(font, key):
    t = font if len(font) % 4 == 0 else font + b'\x00' * (4 - len(font) % 4)
    words = [MAGIC, len(font) ^ key]
    for i in range(0, len(t), 4):
        words.append(struct.unpack_from('>I', t, i)[0] ^ key)
    return struct.pack(f'>{len(words)}I', *words)


BOLD_KEYS = ('-B.', '-B-CREDIT', '-B-ASCII', '-B-OLM', 'RodinNTLGPro-B.', 'RodinNTLGPro-B-',
             'LogoGBlack-Black', 'LogoJrBlack-Black', 'SeuratProN-EB', 'GigaMaru-ExtraBold',
             'LineG-Ultra', 'LogoG-Ultra', 'LogoMaru-Ultra', 'ComicReggaeStd-B', 'Ruby-')
n_ok = 0
for fn in sorted(os.listdir(FONTDIR)):
    if not fn.endswith('.cmp'):
        continue
    p = os.path.join(FONTDIR, fn)
    ob = open(p, 'rb').read()
    frame = ob[4:]
    raw = decomp_frame(frame)
    key = get_key(raw)
    if key is None:
        print(f'  [!] {fn}: khong lay duoc key'); continue
    is_black = ('Ultra' in fn or 'UB' in fn or 'Black' in fn or 'ExtraBold' in fn)
    repl = BLACK if is_black else BOLD
    blob = wrap(repl, key)
    # dung frame zstd CHUAN (co content size) thay vi bat chuoc frame cua Nintendo
    new_frame = zstandard.ZstdCompressor(level=15).compress(blob)
    open(p, 'wb').write(struct.pack('<I', len(blob)) + new_frame)
    n_ok += 1
    print(f'  [+] {fn[:42]:<44} -> {"Nunito-Black" if is_black else "Nunito-Bold"} ({len(repl):,} b)')
print(f'\n  da thay {n_ok} font')
