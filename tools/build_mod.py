"""
Build và đóng gói bản dịch tiếng Việt vào cấu trúc Mod LayeredFS của Nintendo Switch.
Tự động convert JSON -> MSBT -> SARC -> Zstandard (.zs)
Tạo thư mục: output/atmosphere/contents/<TitleID>/romfs/Mals/USen.Product.150.sarc.zs
"""
import os
import sys
import glob
import json
import struct
import zstandard
import oead

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

TITLE_ID = "0100D2F00D5C0000"
GAME_TAG = "0100D2F00D5C0000_SwitchSports"
ORIG_SARC_PATH = f"games/{GAME_TAG}/source/orig_mals/USen.Product.150.sarc.zs"
TRANSLATIONS_DIR = f"games/{GAME_TAG}/translations"
OUTPUT_DIR = f"output/atmosphere/contents/{TITLE_ID}/romfs/Mals"
OUTPUT_FILE = f"{OUTPUT_DIR}/USen.Product.150.sarc.zs"

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

def build_mod():
    print(">>> Bắt đầu đóng gói bản dịch tiếng Việt...")
    # 1. Đọc SARC gốc
    with open(ORIG_SARC_PATH, 'rb') as f:
        decompressed_sarc = zstandard.ZstdDecompressor().decompress(f.read())

    sarc = oead.Sarc(decompressed_sarc)
    sarc_writer = oead.SarcWriter.from_sarc(sarc)

    # 2. Quét các file json đã dịch
    translated_json_files = glob.glob(os.path.join(TRANSLATIONS_DIR, "*.json"))
    if not translated_json_files:
        print("Không tìm thấy file dịch nào trong:", TRANSLATIONS_DIR)
        return

    try:
        from tools.extract_msbt import parse_msbt_bytes
    except ImportError:
        from extract_msbt import parse_msbt_bytes

    count = 0
    for jf_path in translated_json_files:
        base_name = os.path.basename(jf_path).replace('.json', '')
        # khôi phục đường dẫn thật trong SARC: e.g. LayoutMsg__Cmn_ModeSelect.msbt -> LayoutMsg/Cmn_ModeSelect.msbt
        sarc_internal_name = base_name.replace('__', '/')
        
        orig_file = sarc.get_file(sarc_internal_name)
        if not orig_file:
            print(f"Cảnh báo: Không tìm thấy {sarc_internal_name} trong SARC gốc!")
            continue

        orig_msbt = bytes(orig_file.data)
        current_entries = parse_msbt_bytes(orig_msbt)

        with open(jf_path, 'r', encoding='utf-8') as f:
            new_translations = json.load(f)

        current_entries.update(new_translations)
        new_msbt = replace_msbt_txt2(orig_msbt, current_entries)

        # Ghi đè vào SARC
        sarc_writer.files[sarc_internal_name] = oead.Bytes(new_msbt)
        count += 1
        print(f" [+] Đã đóng gói: {sarc_internal_name} ({len(new_translations)} chuỗi)")

    # 3. Build SARC nhị phân
    print(f"\n>>> Tạo file SARC mới ({count} file đã được Việt hóa)...")
    new_sarc_data = sarc_writer.write()[1]

    # 4. Nén Zstandard
    print(">>> Nén Zstandard (.zs)...")
    cctx = zstandard.ZstdCompressor(level=16)
    compressed_data = cctx.compress(new_sarc_data)

    # 5. Lưu vào output Atmosphere
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'wb') as f:
        f.write(compressed_data)

    print(f"\n✅ ĐÃ HOÀN TẤT BẢN MOD!")
    print(f"👉 File kết quả: {OUTPUT_FILE}")
    print(f"Kích thước: {len(compressed_data):,} bytes")

if __name__ == '__main__':
    build_mod()
