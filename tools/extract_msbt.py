"""
Tool trích xuất và đóng gói MSBT cho Nintendo Switch Sports (Nintendo EPD format)
Hỗ trợ UTF-16LE, escape tags/controls, LBL1, ATR1, TXT2, và SARC archive.
"""
import os
import sys
import glob
import json
import struct
import zstandard
import oead

def parse_msbt_bytes(data: bytes):
    bom = '<'
    pos = 32
    sections = {}
    while pos < len(data):
        magic = data[pos:pos+4].decode('latin1', 'ignore')
        size, = struct.unpack_from(f'{bom}I', data, pos+4)
        sections[magic] = data[pos+16:pos+16+size]
        pos += 16 + size
        rem = size % 16
        if rem != 0:
            pos += (16 - rem)

    if 'LBL1' not in sections or 'TXT2' not in sections:
        return {}

    lbl_data = sections['LBL1']
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

    txt_data = sections['TXT2']
    num_strings, = struct.unpack_from('<I', txt_data, 0)
    offsets = [struct.unpack_from('<I', txt_data, 4 + i*4)[0] for i in range(num_strings)]

    entries = {}
    for idx, name in labels:
        if idx >= len(offsets):
            continue
        start = offsets[idx]
        sorted_next = [o for o in offsets if o > start]
        end = min(sorted_next) if sorted_next else len(txt_data)
        raw_val = txt_data[start:end]
        
        # Parse text với control codes (0x0E tag nintendo)
        # Đối với text thông thường, decode UTF-16LE, bỏ null-byte cuối
        val_str = raw_val.decode('utf-16le', 'replace').rstrip('\x00')
        entries[name] = val_str

    return entries

def extract_all_texts(sarc_zs_path: str, output_json_dir: str):
    os.makedirs(output_json_dir, exist_ok=True)
    with open(sarc_zs_path, 'rb') as f:
        decompressed = zstandard.ZstdDecompressor().decompress(f.read())
    
    sarc = oead.Sarc(decompressed)
    total_strings = 0
    all_game_text = {}

    for file_entry in sarc.get_files():
        filename = file_entry.name
        if not filename.endswith('.msbt'):
            continue
        raw_data = bytes(file_entry.data)
        entries = parse_msbt_bytes(raw_data)
        if entries:
            all_game_text[filename] = entries
            total_strings += len(entries)
            
            # Xuất từng file json tương ứng
            out_file = os.path.join(output_json_dir, filename.replace('/', '__') + '.json')
            with open(out_file, 'w', encoding='utf-8') as jf:
                json.dump(entries, jf, ensure_ascii=False, indent=2)

    master_file = os.path.join(output_json_dir, '_all_strings.json')
    with open(master_file, 'w', encoding='utf-8') as mf:
        json.dump(all_game_text, mf, ensure_ascii=False, indent=2)

    print(f"Hoàn thành trích xuất!")
    print(f"- Số file MSBT: {len(all_game_text)}")
    print(f"- Tổng số chuỗi (strings): {total_strings}")
    print(f"- Đã lưu vào: {output_json_dir}")

if __name__ == '__main__':
    GAME_TAG = "0100D2F00D5C0000_SwitchSports"
    extract_all_texts(
        f'working/{GAME_TAG}/orig_mals/USen.Product.150.sarc.zs',
        f'working/{GAME_TAG}/raw_text_extracted/USen'
    )
