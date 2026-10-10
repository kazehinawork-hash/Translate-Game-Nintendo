"""Rebuild Filter.bin hoan hao cho Kirby and the Forgotten Land.

Bao dam:
1. Moi font trong Filter.bin deu co DAY DU:
   - 100% ky tu ASCII printable (0x20 .. 0x7E) gom moi chu cai A-Z, a-z, 0-9, dau cau.
   - 100% ky tu tieng Viet (co dau, hoa, thuong) va ky tu dac biet tu kirby_vi.json.
2. Repeat count chuan xac theo phong cach cua HAL Engine (4 cho text font / 1 cho icon & sub font).
3. 100% mang ky tu duoc sap xep tang dan (chars.sort()) de thuat toan Binary Search khong bao gio loi.
4. Ghi vao tat ca cac thu muc ngon ngu trong mod.
"""
import json
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '01004D300C5AE000'
SRC_FILTER = os.path.join(ROOT, 'dump', TID, 'romfs', 'msg', 'Kirby15', 'US_English', 'Filter.bin')
VI_JSON = os.path.join(ROOT, 'games', f'{TID}_Kirby', 'translations', 'kirby_vi.json')
MOD_MSG_DIR = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'msg', 'Kirby15')


def parse_filter_bin(data):
    magic, ver, fsize, flag, rloc_off = struct.unpack_from('<4sIIII', data, 0)
    assert magic == b'XBIN', f'Invalid magic: {magic}'
    num_fonts, = struct.unpack_from('<I', data, 0x14)
    font_offsets = [struct.unpack_from('<I', data, 0x18 + i * 4)[0] for i in range(num_fonts)]
    fonts = []
    for off in font_offsets:
        name_off, char_count = struct.unpack_from('<II', data, off)
        slen, = struct.unpack_from('<I', data, name_off)
        name = data[name_off + 4: name_off + 4 + slen].decode('latin1')
        chars = [struct.unpack_from('<H', data, off + 8 + i * 2)[0] for i in range(char_count)]
        fonts.append({'name': name, 'chars': chars})
    return fonts


def build_filter_bin(fonts):
    num_fonts = len(fonts)
    cur_off = 0xa0
    font_offsets = []
    font_blocks = []
    for f in fonts:
        cur_off = (cur_off + 0x1f) & ~0x1f
        font_offsets.append(cur_off)
        char_data = b''.join(struct.pack('<H', c) for c in f['chars'])
        data_len = 8 + len(char_data)
        block = struct.pack('<II', 0, len(f['chars'])) + char_data
        font_blocks.append(block)
        cur_off += data_len

    name_offsets = {}
    string_blocks = []
    for f in fonts:
        name = f['name']
        if name not in name_offsets:
            name_offsets[name] = cur_off
            s_bytes = name.encode('latin1')
            s_len = len(s_bytes)
            # 4 byte len + s_bytes + 1 null + pad 4
            s_block = struct.pack('<I', s_len) + s_bytes + b'\x00'
            pad_len = (4 - (len(s_block) % 4)) % 4
            s_block += b'\x00' * pad_len
            string_blocks.append((cur_off, s_block))
            cur_off += len(s_block)

    rloc_off = (cur_off + 0x0f) & ~0x0f
    fsize = rloc_off - 1

    total_len = rloc_off + 12
    out = bytearray(total_len)
    struct.pack_into('<4sIIII', out, 0, b'XBIN', 0x41234, fsize, 0xfde9, rloc_off)
    struct.pack_into('<I', out, 0x14, num_fonts)
    for i, off in enumerate(font_offsets):
        struct.pack_into('<I', out, 0x18 + i * 4, off)

    for f, f_off in zip(fonts, font_offsets):
        n_off = name_offsets[f['name']]
        char_data = b''.join(struct.pack('<H', c) for c in f['chars'])
        block = struct.pack('<II', n_off, len(f['chars'])) + char_data
        out[f_off: f_off + len(block)] = block

    for s_off, s_block in string_blocks:
        out[s_off: s_off + len(s_block)] = s_block

    out[rloc_off: rloc_off + 12] = b'RLOC\x00\x00\x00\x00\x00\x00\x00\x00'
    return bytes(out)


def main():
    print('=== BUILIDING UNIVERSAL FILTER.BIN (FULL ASCII + FULL VIETNAMESE) ===')
    # 1. Thu thap toan bo ky tu can thiet tu kirby_vi.json
    vi = json.load(open(VI_JSON, encoding='utf-8'))
    used_chars = set()
    for ents in vi.values():
        for v in ents.values():
            used_chars |= set(str(v))

    # Bo sung toan bo ASCII printable (0x20..0x7E)
    full_target_chars = set()
    for code in range(0x20, 0x7F):
        full_target_chars.add(chr(code))
    for c in used_chars:
        if c.isprintable():
            full_target_chars.add(c)

    sorted_targets = sorted(full_target_chars)
    print(f'Tong cong tap ky tu can ho tro day du: {len(sorted_targets)} ky tu (ASCII + Tieng Viet).')

    # 2. Nap va phan tich Filter.bin goc tu US_English
    orig_data = open(SRC_FILTER, 'rb').read()
    fonts = parse_filter_bin(orig_data)
    print(f'Da nap {len(fonts)} fonts tu US_English Filter.bin goc.')

    # 3. Bo sung ky tu vao tung font
    for idx, f in enumerate(fonts):
        fname = f['name']
        chars = f['chars']
        if len(chars) == 0:
            continue

        count_A = chars.count(ord('A'))
        count_a = chars.count(ord('a'))
        repeat = 4 if (count_A == 4 or count_a == 4) else 1

        existing_set = set(chars)
        added_count = 0
        for ch in sorted_targets:
            code = ord(ch)
            if code not in existing_set:
                for _ in range(repeat):
                    chars.append(code)
                existing_set.add(code)
                added_count += 1

        # Sap xep tang dan cho Binary Search
        chars.sort()
        f['chars'] = chars
        print(f'  [+] #{idx:2d} {fname:<32}: them {added_count:3d} ky tu (repeat={repeat}) -> tong={len(chars):4d}')

    # 4. Build file Filter.bin moi
    new_filter_data = build_filter_bin(fonts)
    print(f'\nFilter.bin moi: {len(new_filter_data):,} bytes (goc: {len(orig_data):,} bytes)')

    # Kiem tra tinh hop le
    verify_fonts = parse_filter_bin(new_filter_data)
    for vf in verify_fonts:
        assert vf['chars'] == sorted(vf['chars']), f'Font {vf["name"]} khong duoc sort!'
    print('Xac minh: 100% font duoc sort dung thu tu binary search!')

    # 5. Ghi vao tat ca cac thu muc ngon ngu trong mod
    written_count = 0
    for root, dirs, files in os.walk(MOD_MSG_DIR):
        for d in dirs:
            target_filter = os.path.join(root, d, 'Filter.bin')
            with open(target_filter, 'wb') as out_f:
                out_f.write(new_filter_data)
            written_count += 1
    print(f'Da cap nhat Filter.bin vao {written_count} thu muc ngon ngu trong mod!')


if __name__ == '__main__':
    main()
