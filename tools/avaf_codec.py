import os
import sys
import struct

sys.stdout.reconfigure(encoding='utf-8')

def pack_avafdict(entries_dict):
    """
    entries_dict: { key_str: val_str, ... }
    Format AVAFDICT 2.0:
    Header 72 bytes:
      0x00: b'AVAFDICT 2.0   \x00\x00' (32 bytes)
      0x20: entry_count (uint64)
      0x28: hdr_len (uint64) = 72 (0x48)
      0x30: off1 (uint64) = table_len = entry_count * 24
      0x38: off2 (uint64) = table_len + 72
      0x40: off3 (uint64) = total string bytes length
    Table:
      For each entry (24 bytes):
        k_off (uint32), k_unk (uint32=0), k_len (uint32)
        v_off (uint32), v_unk (uint32=0), v_len (uint32)
    Strings Pool:
      Concatenation of UTF-8 key and value bytes.
    """
    keys = list(entries_dict.keys())
    entry_count = len(keys)
    table_len = entry_count * 24
    hdr_len = 72
    off1 = table_len
    off2 = table_len + hdr_len
    
    table_bytes = bytearray()
    string_bytes = bytearray()
    cur_str_off = 0
    
    for k in keys:
        v = entries_dict[k]
        k_b = k.encode('utf-8')
        v_b = v.encode('utf-8')
        
        k_off = cur_str_off
        k_len = len(k_b)
        string_bytes.extend(k_b)
        cur_str_off += k_len
        
        v_off = cur_str_off
        v_len = len(v_b)
        string_bytes.extend(v_b)
        cur_str_off += v_len
        
        # 24 bytes entry
        table_bytes.extend(struct.pack('<IIIIII', k_off, 0, k_len, v_off, 0, v_len))
        
    off3 = len(string_bytes)
    
    # Pack header
    # LUU Y: file goc cua game dung magic UTF-16LE (32 byte), KHONG phai ASCII.
    # Ghi sai magic => game khong doc duoc tu dien => moi chu hien dang [KEY].
    header_magic = 'AVAFDICT 2.0   \x00'.encode('utf-16-le')
    header = bytearray(72)
    header[:len(header_magic)] = header_magic
    struct.pack_into('<QQQQQ', header, 0x20, entry_count, hdr_len, off1, off2, off3)
    
    return bytes(header + table_bytes + string_bytes)

def unpack_avafdict(data):
    entry_count, hdr_len, off1, off2, off3 = struct.unpack('<QQQQQ', data[0x20:0x48])
    entries = {}
    table_offset = 0x48
    for i in range(entry_count):
        k_off, k_unk, k_len = struct.unpack('<III', data[table_offset + i*24 : table_offset + i*24 + 12])
        v_off, v_unk, v_len = struct.unpack('<III', data[table_offset + i*24 + 12 : table_offset + i*24 + 24])
        k_str = data[off2 + k_off : off2 + k_off + k_len].decode('utf-8', errors='replace')
        v_str = data[off2 + v_off : off2 + v_off + v_len].decode('utf-8', errors='replace')
        entries[k_str] = v_str
    return entries

# Test roundtrip with sample
test_data = {
    "Accio_Spell": "Triệu Tập",
    "Lumos_Spell": "Phát Sáng",
    "AvadaKedavra_Spell": "Lời Nguyền Chết Chóc",
    "UI_PlayGame": "Bắt Đầu Trò Chơi",
    "UI_Settings": "Cài Đặt Hệ Thống"
}

packed = pack_avafdict(test_data)
unpacked = unpack_avafdict(packed)
assert test_data == unpacked, "Roundtrip failed!"
print(f"Packer verification successful! Packed {len(test_data)} entries into {len(packed)} bytes.")
