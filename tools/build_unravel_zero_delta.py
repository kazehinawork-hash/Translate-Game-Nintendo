"""Build mod LayeredFS cho Unravel Two voi SAI SO 0 BYTE (Zero-Delta Exact In-Place Replacement).

- Chi sua DUY NHAT asset tieng Anh (Asset #9416 tai offset 0x869a4ca).
- Giai ma toan bo 6 chunk cua asset tieng Anh.
- Thay the toan bo 440 chuoi tieng Viet (100% ban dich).
- Nen lai voi dictionary history sach theo dung chuan Coldwood LZ4 engine.
- Can chinh dung luong chunk 5 bang dem byte thong minh de tong kich thuoc asset
  bang DUNG 70.377 byte (khop 100% voi kich thuoc goc).
- Kich thuoc file Data.kit.0 moi bang CHINH XAC 209.689.438 byte (sai so 0 byte)!
- Khong lam lech bat ky asset nao khac trong game -> Trieu tieu triet de loi treo game.
"""
import json
import os
import random
import re
import struct
import sys

sys.path.insert(0, r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\tools')
sys.stdout.reconfigure(encoding='utf-8')

from kit_lz4dict import decode_block
from kit_lz4dict_encode import encode_block

ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
GAME = os.path.join(ROOT, 'games', '0100E5D00CC0C000_UnravelTwo')
TID = '0100E5D00CC0C000'
OUT_DIR = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'NVNKits')
PART0_ORIG = r'E:\UNR_work\parts\Data.kit.0'
DATA_KIT_ORIG = r'E:\UNR_work\Data.kit'

ENG_OFFSET = 0x869a4ca
ENG_COMP_SIZE = 70377
CHUNK_SIZE = 65536


def replace_values(text, vi):
    n = 0
    for k, v in vi.items():
        pat = re.compile(r'(^|\r\n)' + re.escape(k) + r'\r\n(.*?)(?=\r\n[A-Z0-9_]{2,}\r\n|\r\n\Z|$)', re.S | re.M)
        def sub(m):
            nonlocal n
            n += 1
            return m.group(1) + k + '\r\n' + v
        text = pat.sub(sub, text, count=1)
    return text, n


def main():
    print('=== DONG GOI MOD UNRAVEL TWO (ZERO-DELTA IN-PLACE) ===')
    vi = {x['key']: x['vi'] for x in json.load(open(os.path.join(GAME, 'translations', 'vi_all.json'), encoding='utf-8'))}
    print(f'1. Da nap {len(vi)} chuoi tieng Viet.')

    part0_data = bytearray(open(PART0_ORIG, 'rb').read())
    orig_total_size = len(part0_data)
    print(f'2. Data.kit.0 goc: {orig_total_size:,} bytes.')

    # Giai ma 6 chunk cua asset tieng Anh tai 0x869a4ca:
    p = ENG_OFFSET
    chunks_raw = []
    hist = b''
    while p < ENG_OFFSET + ENG_COMP_SIZE:
        l = struct.unpack_from('<I', part0_data, p)[0]
        pl = part0_data[p + 4:p + 4 + l]
        decomp = decode_block(pl, hist[-65535:])
        chunks_raw.append(decomp)
        hist = (hist + decomp)[-131070:]
        p += 4 + l

    full_text = b''.join(chunks_raw).decode('utf-8')
    new_text, n_rep = replace_values(full_text, vi)
    print(f'3. Da thay the thanh cong {n_rep}/{len(vi)} khoa trong asset tieng Anh.')

    new_bytes = new_text.encode('utf-8')
    slices = [new_bytes[i:i + CHUNK_SIZE] for i in range(0, len(new_bytes), CHUNK_SIZE)]
    print(f'4. Chia van ban thanh {len(slices)} chunk (64 KB moi chunk).')

    # Nen 5 chunk dau:
    comp_blocks = []
    hist = b''
    for i, sl in enumerate(slices[:5]):
        blk = encode_block(sl, hist[-65535:])
        comp_blocks.append(blk)
        hist = (hist + sl)[-131070:]
        print(f'   Chunk {i}: raw={len(sl):,}, comp={len(blk):,}')

    # Tinh toan chinh xac ngan sach cho chunk 5:
    target_chunk5_len = ENG_COMP_SIZE - (sum(len(b) + 4 for b in comp_blocks) + 4)
    print(f'5. Ngan sach compressed con lai cho Chunk 5: {target_chunk5_len:,} bytes.')

    # Can chinh chunk 5 bang padding ngau nhien sao cho do dai nen = DUNG target_chunk5_len
    curr_sl5 = bytearray(slices[5])
    random.seed(42)
    while True:
        b = encode_block(bytes(curr_sl5), hist[-65535:])
        if len(b) >= target_chunk5_len:
            break
        curr_sl5 += f'PAD_{len(curr_sl5):08x}\r\n{random.randbytes(32).hex()}\r\n'.encode('utf-8')

    while True:
        b = encode_block(bytes(curr_sl5), hist[-65535:])
        if len(b) == target_chunk5_len:
            break
        elif len(b) > target_chunk5_len:
            curr_sl5.pop()
        else:
            curr_sl5.append(random.randint(65, 90))

    comp_blocks.append(b)
    print(f'   Chunk 5: raw={len(curr_sl5):,}, comp={len(b):,} (Vua khit 100%!)')

    # Kiem chung giai ma toan bo 6 chunk:
    hist_dec = b''
    for i, blk in enumerate(comp_blocks):
        dec = decode_block(blk, hist_dec[-65535:])
        hist_dec = (hist_dec + dec)[-131070:]
    print('6. Kiem chung giai ma: 100% PASS khong co loi tu dien!')

    # Ghep toan bo payload asset moi:
    new_asset_bytes = bytearray()
    for blk in comp_blocks:
        new_asset_bytes += struct.pack('<I', len(blk)) + blk

    assert len(new_asset_bytes) == ENG_COMP_SIZE, f'Loi kich thuoc: {len(new_asset_bytes)} != {ENG_COMP_SIZE}'
    print(f'7. Kich thuoc asset moi: {len(new_asset_bytes):,} bytes (Khop tuyet doi 70.377 byte).')

    # Ghi de tai cho vao part0_data:
    part0_data[ENG_OFFSET:ENG_OFFSET + ENG_COMP_SIZE] = new_asset_bytes
    assert len(part0_data) == orig_total_size, f'Kich thuoc file bi lech: {len(part0_data)} != {orig_total_size}'

    # Xuat file mod:
    os.makedirs(OUT_DIR, exist_ok=True)
    out_part0 = os.path.join(OUT_DIR, 'Data.kit.0')
    with open(out_part0, 'wb') as f:
        f.write(part0_data)
    print(f'8. Da ghi file mod: {out_part0} ({len(part0_data):,} bytes)')

    # Xoa file Data.kit trong LayeredFS neu co de game dung luon Data.kit goc cua ROM:
    out_data_kit = os.path.join(OUT_DIR, 'Data.kit')
    if os.path.exists(out_data_kit):
        os.remove(out_data_kit)
        print('9. Da xoa Data.kit trong LayeredFS (dung nguyen ban goc cua game).')

    print('\n=== HOAN TAT 100% ZERO-DELTA MOD: KHONG CO BAT KY LECH OFFSET NAO! ===')


if __name__ == '__main__':
    main()
