"""Dong goi lai font Kirby SAU KHI SUA BANG FONTFORGE.

Doc cac file .ttf/.otf trong games/<TID>_Kirby/font_edit/, ma hoa lai (XOR bang key
da luu trong <file>.key), nen bang frame zstd CHUAN, ghi vao mod.

Dung:
    python tools/kirby_font_reencrypt.py            # dong goi tat ca
    python tools/kirby_font_reencrypt.py --check     # chi kiem tra, khong ghi
"""
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import zstandard

TID = '01004D300C5AE000'
EDIT = os.path.join(ROOT, 'games', f'{TID}_Kirby', 'font_edit')
MOD = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'font', 'ScalableFontBin')
MAGIC = 0x36F81A1E


def wrap(font, key):
    t = font if len(font) % 4 == 0 else font + b'\x00' * (4 - len(font) % 4)
    words = [MAGIC, len(font) ^ key]
    for i in range(0, len(t), 4):
        words.append(struct.unpack_from('>I', t, i)[0] ^ key)
    blob = struct.pack(f'>{len(words)}I', *words)
    return struct.pack('<I', len(blob)) + zstandard.ZstdCompressor(level=15).compress(blob)


def unwrap(b):
    d = zstandard.ZstdDecompressor()
    try:
        data = d.decompress(b[4:], max_output_size=256 << 20)
    except zstandard.ZstdError:
        with d.stream_reader(b[4:]) as r:
            data = r.read(256 << 20)
    w8, = struct.unpack_from('>I', data, 8)
    for e in (0x4F54544F, 0x00010000, 0x74746366):
        k = w8 ^ e
        body = b''.join(struct.pack('>I', struct.unpack_from('>I', data, i)[0] ^ k)
                        for i in range(8, len(data), 4))
        if body[:4] == struct.pack('>I', e):
            return body
    return None


check = '--check' in sys.argv
n_ok = n_bad = 0
for fn in sorted(os.listdir(EDIT)):
    if not (fn.endswith('.ttf') or fn.endswith('.otf')):
        continue
    keyp = os.path.join(EDIT, fn + '.key')
    if not os.path.exists(keyp):
        print(f'  [!] {fn}: thieu file .key')
        n_bad += 1
        continue
    key = int(open(keyp).read().strip(), 16)
    font = open(os.path.join(EDIT, fn), 'rb').read()
    target = fn.replace('.otf', '.bfotf.cmp').replace('.ttf', '.bfttf.cmp')
    data = wrap(font, key)
    if not check:
        open(os.path.join(MOD, target), 'wb').write(data)
    # doc lai xac minh
    back = unwrap(open(os.path.join(MOD, target), 'rb').read()) if not check else font
    ok = back[:len(font)] == font
    if ok:
        n_ok += 1
    else:
        n_bad += 1
        print(f'  [!!] {fn}: doc lai KHONG khop')
print(f'\n  {"(kiem tra) " if check else ""}{n_ok} font dong goi OK | {n_bad} loi')
if not check:
    print('  -> mod da cap nhat, chep vao Eden de test')
