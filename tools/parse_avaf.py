import os
import sys
import struct

sys.stdout.reconfigure(encoding='utf-8')

def parse_avafdict(data):
    if not data.startswith(b'A\x00V\x00A\x00F'):
        print('Not AVAFDICT')
        return None
    # Header format
    # 0x00: b'AVAFDICT 2.0   \x00\x00' (32 bytes)
    # 0x20: entry_count (uint64)
    # 0x28: hdr_len (uint64)
    # 0x30: off1 (uint64)
    # 0x38: off2 (uint64) -> strings table offset
    # 0x40: off3 (uint64)
    entry_count, hdr_len, off1, off2, off3 = struct.unpack('<QQQQQ', data[0x20:0x48])
    print(f'AVAFDICT: entries={entry_count}, hdr_len={hdr_len}, off1={off1}, off2={off2}, off3={off3}')
    
    entries = {}
    table_offset = 0x48
    # Let's inspect entry table format
    # Each entry has key and value triton
    for i in range(entry_count):
        k_off, k_unk, k_len = struct.unpack('<III', data[table_offset + i*24 : table_offset + i*24 + 12])
        v_off, v_unk, v_len = struct.unpack('<III', data[table_offset + i*24 + 12 : table_offset + i*24 + 24])
        
        k_str = data[off2 + k_off : off2 + k_off + k_len].decode('utf-8', errors='replace')
        v_str = data[off2 + v_off : off2 + v_off + v_len].decode('utf-8', errors='replace')
        entries[k_str] = v_str
    return entries

for fname in ['MAIN-frFR.bin', 'SUB-deDE.bin', 'SUB-enUS.bin']:
    fp = os.path.join('working/0100F7E00C70E000_Hogwarts/raw_text/en-US', fname)
    if os.path.exists(fp):
        with open(fp, 'rb') as f:
            data = f.read()
        print(f'\nParsing {fname} ({len(data)} bytes):')
        res = parse_avafdict(data)
        if res:
            print(f'Total parsed items: {len(res)}')
            # print 3 samples
            for i, (k, v) in enumerate(list(res.items())[:3]):
                print(f'  [{i}] {k} -> {v[:50]}')
