import os
import sys
import struct
import ctypes
import json
import nsz.nut.Keys as Keys
from nsz.Fs import Nsp

sys.stdout.reconfigure(encoding='utf-8')

exact_offsets = {
    'SUB-esMX': 0x33e2b7f0, # Arabic
    'SUB-frFR': 0x33f3d3b0, # German
    'SUB-jaJP': 0x341030c0, # Spanish
    'SUB-koKR': 0x341e2120, # French
    'SUB-plPL': 0x342ccc80, # Italian
    'SUB-ptBR': 0x343b2460, # Japanese
    'SUB-ruRU': 0x344955c0, # Korean
    'SUB-zhCN': 0x34596450, # Polish
    'SUB-zhTW': 0x34682240, # Brazilian Portuguese
}

dll_path = os.path.abspath('tools/oo2core_9_win64.dll')
oodle = ctypes.cdll.LoadLibrary(dll_path)
OodleLZ_Decompress = oodle.OodleLZ_Decompress
OodleLZ_Decompress.argtypes = [
    ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_size_t,
    ctypes.c_int, ctypes.c_int, ctypes.c_int,
    ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p,
    ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int
]
OodleLZ_Decompress.restype = ctypes.c_size_t

def decompress_entry(rom, pak_start, off):
    rom.seek(pak_start + off)
    head = rom.read(48)
    o, size, uncomp_size, comp_method = struct.unpack('<QQQI', head[:28])
    if comp_method == 0:
        return rom.read(size)
    bc = struct.unpack('<I', rom.read(4))[0]
    blocks = []
    for _ in range(bc):
        b_start, b_end = struct.unpack('<QQ', rom.read(16))
        blocks.append((b_start, b_end))
    rom.seek(pak_start + off)
    full_data = rom.read(blocks[-1][1] + 16)
    
    total_buf = ctypes.create_string_buffer(uncomp_size + 65536)
    out_ptr = ctypes.cast(total_buf, ctypes.c_void_p).value
    cur_offset = 0
    for i, (b_start, b_end) in enumerate(blocks):
        chunk = full_data[b_start:b_end]
        cur_uncomp = min(1048576, uncomp_size - cur_offset)
        res = OodleLZ_Decompress(chunk, len(chunk), ctypes.c_void_p(out_ptr + cur_offset), cur_uncomp, 1, 0, 0, None, 0, None, None, None, 0, 3)
        cur_offset += res
    return bytes(total_buf.raw[:uncomp_size])

def parse_avaf(data):
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

Keys.load('input/prod.keys')
from find_rom import find_rom
nsp_path = sys.argv[1] if len(sys.argv) > 1 else str(find_rom('0100F7E00C70E000'))
print('ROM:', nsp_path)
nsp = Nsp.Nsp()
nsp.open(nsp_path, 'rb')

for f in nsp:
    if f._path == 'ee8fed561b6ace5cc38c13699a3e9664.nca':
        rom = f.sections[1]
        lvl5_off = 14237696
        pak_start = lvl5_off + 512 + 502874912
        
        # We need French, German, Spanish or Italian to correlate
        # Let's extract SUB-koKR (French) and SUB-jaJP (Spanish)
        print('Extracting SUB-koKR (French dialogs)...')
        d_fr = decompress_entry(rom, pak_start, exact_offsets['SUB-koKR'])
        fr_dict = parse_avaf(d_fr)
        print(f'French dialog entries: {len(fr_dict)}')
        
        print('Extracting SUB-jaJP (Spanish dialogs)...')
        d_es = decompress_entry(rom, pak_start, exact_offsets['SUB-jaJP'])
        es_dict = parse_avaf(d_es)
        print(f'Spanish dialog entries: {len(es_dict)}')
        
        # Combine into dialogue json
        sub_list = []
        for k in fr_dict.keys():
            sub_list.append({
                "Key": k,
                "Source_FR": fr_dict[k],
                "Source_ES": es_dict.get(k, "")
            })
        
        out_sub_path = 'games/0100F7E00C70E000_Hogwarts/source/extracted_json/hogwarts_dialogs_raw.json'
        with open(out_sub_path, 'w', encoding='utf-8') as sf:
            json.dump(sub_list, sf, ensure_ascii=False, indent=2)
        print(f'Saved {len(sub_list)} dialogues to {out_sub_path}!')
        break
