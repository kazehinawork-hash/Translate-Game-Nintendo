"""
Script đóng gói Mod LayeredFS cho The Legend of Zelda: Tears of the Kingdom (TotK).
Sử dụng Zstandard với dictionary nén zs.zsdic từ ZsDic.pack.zs.
Tự động inject JSON -> MSBT (TXT2) -> SARC -> Zstandard (.zs).
Xuất ra output/atmosphere/contents/0100F2C0115B6000/romfs/Mals/USen.Product.142.sarc.zs
"""
import os
import sys
import glob
import json
import struct
import zstandard as zstd
import oead

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

TITLE_ID = "0100F2C0115B6000"
GAME_DIR = f"games/{TITLE_ID}_ZeldaTotK"
ROMFS_DUMP = rf"E:\RomFS_Dump\{TITLE_ID}\romfs"
MALS_ORIG = os.path.join(ROMFS_DUMP, "Mals", "USen.Product.142.sarc.zs")
ZSDIC_PATH = os.path.join(ROMFS_DUMP, "Pack", "ZsDic.pack.zs")
TRANSLATIONS_DIR = f"{GAME_DIR}/translations"
OUTPUT_DIR = f"output/atmosphere/contents/{TITLE_ID}/romfs/Mals"
OUTPUT_FILES = [
    f"{OUTPUT_DIR}/USen.Product.142.sarc.zs",
    f"{OUTPUT_DIR}/USen.Product.143.sarc.zs"
]

def replace_msbt_txt2(orig_msbt: bytes, new_entries: dict) -> bytes:
    bom = '<'
    pos = 32
    sections = []
    while pos < len(orig_msbt):
        magic = orig_msbt[pos:pos+4].decode('latin1', 'ignore')
        size, = struct.unpack_from(f'{bom}I', orig_msbt, pos+4)
        sect_data = orig_msbt[pos+16:pos+16+size]
        sections.append((magic, sect_data))
        pos += 16 + size
        rem = size % 16
        if rem != 0:
            pos += (16 - rem)

    lbl_data = dict(sections)['LBL1']
    num_groups, = struct.unpack_from('<I', lbl_data, 0)
    labels = []
    for g in range(num_groups):
        item_count, offset = struct.unpack_from('<II', lbl_data, 4 + g * 8)
        cur = offset
        for _ in range(item_count):
            str_len = lbl_data[cur]
            name = lbl_data[cur+1:cur+1+str_len].decode('utf-8', 'ignore')
            idx, = struct.unpack_from('<I', lbl_data, cur+1+str_len)
            labels.append((idx, name))
            cur += 1 + str_len + 4
    labels.sort()

    ordered_texts = []
    for idx, name in labels:
        ordered_texts.append(new_entries.get(name, ''))

    num_strings = len(ordered_texts)
    offsets = []
    text_blob = bytearray()
    for t in ordered_texts:
        offsets.append(len(text_blob))
        text_blob.extend(t.encode('utf-16le') + b'\x00\x00')

    base_offset = 4 + num_strings * 4
    txt2_payload = bytearray(struct.pack('<I', num_strings))
    for off in offsets:
        txt2_payload.extend(struct.pack('<I', base_offset + off))
    txt2_payload.extend(text_blob)

    new_msbt = bytearray(orig_msbt[:32])
    new_sections_bytes = bytearray()
    for magic, sdata in sections:
        if magic == 'TXT2':
            payload = bytes(txt2_payload)
        else:
            payload = sdata
        size = len(payload)
        header = magic.encode('latin1') + struct.pack('<I', size) + b'\x00' * 8
        new_sections_bytes.extend(header)
        new_sections_bytes.extend(payload)
        rem = size % 16
        if rem != 0:
            new_sections_bytes.extend(b'\x00' * (16 - rem))

    total_size = 32 + len(new_sections_bytes)
    struct.pack_into('<I', new_msbt, 18, total_size)
    return bytes(new_msbt + new_sections_bytes)

def build_totk_mod():
    print(">>> [TotK Build] Đang tải ZsDic...")
    with open(ZSDIC_PATH, 'rb') as f:
        zsdic_sarc = oead.Sarc(zstd.ZstdDecompressor().decompress(f.read()))

    zs_dict_data = None
    for f_in in zsdic_sarc.get_files():
        if f_in.name == 'zs.zsdic':
            zs_dict_data = bytes(f_in.data)
            break

    if not zs_dict_data:
        raise RuntimeError("Không tìm thấy zs.zsdic trong ZsDic.pack.zs!")

    dict_obj = zstd.ZstdCompressionDict(zs_dict_data)
    dctx = zstd.ZstdDecompressor(dict_data=dict_obj)

    print(">>> [TotK Build] Đang giải nén Mals USen SARC...")
    with open(MALS_ORIG, 'rb') as f:
        decompressed_sarc = dctx.decompress(f.read())

    sarc = oead.Sarc(decompressed_sarc)
    sarc_writer = oead.SarcWriter.from_sarc(sarc)

    print(">>> [TotK Build] Quét các file json bản dịch...")
    trans_files = glob.glob(f"{TRANSLATIONS_DIR}/*.json")
    if not trans_files:
        print(f"Cảnh báo: Không có file dịch nào trong {TRANSLATIONS_DIR}")
        return

    injected_count = 0
    total_strings = 0

    for tf in trans_files:
        base_name = os.path.basename(tf).replace('.json', '')
        # Phục hồi path trong SARC: 'LayoutMsg__GameOver_00.msbt' -> 'LayoutMsg/GameOver_00.msbt'
        sarc_inner_name = base_name.replace('__', '/')
        
        orig_file = None
        for f in sarc.get_files():
            if f.name == sarc_inner_name:
                orig_file = f
                break

        if not orig_file:
            print(f"Bỏ qua (không có trong SARC gốc): {sarc_inner_name}")
            continue

        with open(tf, 'r', encoding='utf-8') as jf:
            trans_dict = json.load(jf)

        orig_msbt_bytes = bytes(orig_file.data)
        new_msbt_bytes = replace_msbt_txt2(orig_msbt_bytes, trans_dict)

        sarc_writer.files[sarc_inner_name] = oead.Bytes(new_msbt_bytes)
        injected_count += 1
        total_strings += len(trans_dict)
        print(f"  + Đã inject {sarc_inner_name} ({len(trans_dict)} strings)")

    print(">>> [TotK Build] Đang đóng gói lại SARC...")
    new_sarc_bytes = sarc_writer.write()[1]

    print(">>> [TotK Build] Đang nén Zstandard với từ điển zs.zsdic (khớp chuẩn windowLog=23 Nintendo)...")
    # File gốc dùng window_log=23 (WD=0x68), dict_id=1 (FHD=0x81).
    # Chuẩn hóa để decoder của Nintendo Switch không bị abort / crash Atmosphere.
    params = zstd.ZstdCompressionParameters.from_level(15, window_log=23)
    cctx = zstd.ZstdCompressor(compression_params=params, dict_data=dict_obj)
    raw_compressed = cctx.compress(new_sarc_bytes)

    # Patch frame header sang FHD=0x81, WD=0x68, DictID=0x01 nếu chưa có
    header_ba = bytearray(raw_compressed)
    if header_ba[4] == 0x80:
        header_ba[4] = 0x81
        header_ba.insert(6, 0x01)
    compressed_sarc = bytes(header_ba)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for out_path in OUTPUT_FILES:
        with open(out_path, 'wb') as out_f:
            out_f.write(compressed_sarc)
        print(f"- Đã xuất mod tại: {out_path}")

    print(f"=== BUILD MOD TOTK THÀNH CÔNG ===")
    print(f"- Số file MSBT đã inject: {injected_count}")
    print(f"- Tổng số chuỗi đã dịch: {total_strings}")
    print(f"- Kích thước mod: {len(compressed_sarc):,} bytes")

if __name__ == '__main__':
    build_totk_mod()
