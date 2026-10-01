import os
import sys
import struct
import ctypes
import nsz.nut.Keys as Keys
from nsz.Fs import Nsp

sys.stdout.reconfigure(encoding='utf-8')

Keys.load('input/prod.keys')
from find_rom import find_rom
nsp_path = sys.argv[1] if len(sys.argv) > 1 else str(find_rom('0100F7E00C70E000'))
nsp = Nsp.Nsp()
nsp.open(nsp_path, 'rb')

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

for f in nsp:
    if f._path == 'ee8fed561b6ace5cc38c13699a3e9664.nca':
        rom = f.sections[1]
        lvl5_off = 14237696
        pak_start = lvl5_off + 512 + 502874912
        pak_size = 2377069343
        idx_off = 2375799106
        
        rom.seek(pak_start + idx_off + 322190)
        dir_bytes = rom.read(pak_size - 204 - (idx_off + 322190))
        
        import re
        matches = list(re.finditer(rb'((MAIN|SUB)-[a-zA-Z]+\.bin)', dir_bytes))
        print(f'Found {len(matches)} bin entries in index:')
        
        for m in matches:
            fname = m.group(1).decode()
            pos = m.end()
            enc_idx = struct.unpack('<I', dir_bytes[pos+1:pos+5])[0]
            rom.seek(pak_start + idx_off + enc_idx)
            raw = rom.read(16)
            # Offset is uint64 at raw[2:10]
            pak_off = struct.unpack('<Q', raw[2:10])[0]
            
            # Decompress and check magic and text
            data = decompress_entry(rom, pak_start, pak_off)
            if data.startswith(b'A\x00V\x00A\x00F'):
                entry_count = struct.unpack('<Q', data[0x20:0x28])[0]
                off2 = struct.unpack('<Q', data[0x38:0x40])[0]
                k = struct.unpack('<III', data[0x48+1000*24 : 0x48+1000*24+12])
                v = struct.unpack('<III', data[0x48+1000*24+12 : 0x48+1000*24+24])
                key_str = data[off2+k[0]:off2+k[0]+k[2]].decode('utf-8', errors='ignore')
                val_str = data[off2+v[0]:off2+v[0]+v[2]].decode('utf-8', errors='ignore')
                print(f'{fname:15} | off=0x{pak_off:08x} | entries={entry_count:5} | len={len(data):8} | key={key_str[:20]:20} | val={val_str[:25]}')
            else:
                print(f'{fname:15} | off=0x{pak_off:08x} | NOT AVAFDICT (len={len(data)}, magic={data[:8]})')
        break
