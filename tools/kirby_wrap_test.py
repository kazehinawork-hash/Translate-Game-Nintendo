"""Test co lap ham goi/mo font Kirby."""
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
MAGIC = 0x36F81A1E


def unwrap(data):
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
        if bytes(out[:4]) in (b'OTTO', b'\x00\x01\x00\x00', b'ttcf'):
            return bytes(out), key
    return None, None


def wrap(ttf, key):
    t = ttf + (b'\x00' * (4 - len(ttf) % 4) if len(ttf) % 4 else b'')
    words = [MAGIC, len(t) ^ key]
    for i in range(0, len(t), 4):
        w, = struct.unpack_from('>I', t, i)
        words.append(w ^ key)
    return struct.pack(f'>{len(words)}I', *words)


# gia lap: font TTF gia 32 byte
fake_ttf = b'\x00\x01\x00\x00' + bytes(range(0, 28))
print('font gia:', len(fake_ttf), 'byte | dau', fake_ttf[:4].hex())
for key in (0, 0x49621806, 0xDEADBEEF):
    blob = wrap(fake_ttf, key)
    back, k2 = unwrap(blob)
    print(f'  key {key:#010x}: blob {len(blob)} | doc lai {len(back) if back else "None"} byte | khop {back == fake_ttf}')
    if back and back != fake_ttf:
        print(f'    lech: {back[:16].hex(" ")} vs {fake_ttf[:16].hex(" ")}')

# thu voi font OTTO gia
fake_otf = b'OTTO' + bytes(range(0, 28))
print('\nfont OTTO gia:')
for key in (0x49621806,):
    blob = wrap(fake_otf, key)
    back, k2 = unwrap(blob)
    print(f'  key {key:#010x}: doc lai {"OK" if back == fake_otf else "LECH"} | key doc duoc {k2:#010x}')
