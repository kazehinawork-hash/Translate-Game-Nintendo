"""Script dong bo va patch bang offset Data.kit cho Unravel Two.

- Tinh toan lai toan bo 3.166 offset bi dich chuyen do ban dich tieng Viet lam phinh Data.kit.0 (+52.492 byte).
- Cap nhat compressed size moi cho 5 goi localization trong Data.kit.
- Xuat file Data.kit vao output/atmosphere/contents/0100E5D00CC0C000/romfs/NVNKits/.
"""
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG_KIT = r'E:\UNR_work\Data.kit'
OUT_DIR = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '0100E5D00CC0C000', 'romfs', 'NVNKits')
OUT_KIT = os.path.join(OUT_DIR, 'Data.kit')

DELTA = 52492  # So byte lech giua mod Data.kit.0 va goc

# 5 goi localization da sua
ENTRIES = [
    (9418, 0x865b1aa, 131655, 144419, 0x865b1aa),
    (9419, 0x867b3f1, 127193, 139246, 0x867e5cd),
    (9416, 0x869a4ca, 70377,  72829,  0x86a05bb),
    (9417, 0x86ab7b3, 129776, 141388, 0x86b2238),
    (9415, 0x86cb2a3, 138117, 151728, 0x86d4a84),
]
MAP_KNOWN = {e[1]: (e[4], e[3]) for e in ENTRIES}


def patch_kit():
    with open(ORIG_KIT, 'rb') as f:
        kit_bytes = bytearray(f.read())

    magic, v1, v2, v3, chunk_size, unk, num_entries, num_parts = struct.unpack_from('<4s7I', kit_bytes, 0)
    assert magic == b'kit!', 'Khong dung dinh dang file Data.kit'

    patched_known = 0
    shifted_tail = 0

    for i in range(num_entries):
        p = 32 + i * 56
        u64_16 = struct.unpack_from('<Q', kit_bytes, p + 16)[0]
        off = u64_16 >> 24
        part = u64_16 & 0xffffff

        if part == 0 and off > 0:
            if off in MAP_KNOWN:
                new_off, new_comp_sz = MAP_KNOWN[off]
                new_u64_16 = (new_off << 24) | part
                struct.pack_into('<Q', kit_bytes, p + 16, new_u64_16)
                u64_24 = struct.unpack_from('<Q', kit_bytes, p + 24)[0]
                new_u64_24 = (new_comp_sz << 8) | (u64_24 & 0xff)
                struct.pack_into('<Q', kit_bytes, p + 24, new_u64_24)
                patched_known += 1
            elif off >= 0x86ece28:
                new_off = off + DELTA
                new_u64_16 = (new_off << 24) | part
                struct.pack_into('<Q', kit_bytes, p + 16, new_u64_16)
                shifted_tail += 1

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_KIT, 'wb') as f:
        f.write(kit_bytes)

    print(f'Da va xong Data.kit: {patched_known} asset text duoc cap nhat kich thuoc, {shifted_tail} asset sau duoc cap nhat offset.')
    print(f'File da ghi: {OUT_KIT} ({len(kit_bytes):,} bytes)')


if __name__ == '__main__':
    patch_kit()
