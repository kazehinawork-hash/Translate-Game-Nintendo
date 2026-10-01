import os
import sys
import struct
import nsz.nut.Keys as Keys
from nsz.Fs import Nsp

sys.stdout.reconfigure(encoding='utf-8')

Keys.load('input/prod.keys')
nsp_path = r'E:\ROM_Backup\HogwartsLegacy\Hogwarts Legacy [0100F7E00C70E000][USA][v0][eShop].nsp'
nsp = Nsp.Nsp()
nsp.open(nsp_path, 'rb')

for f in nsp:
    if f._path == 'ee8fed561b6ace5cc38c13699a3e9664.nca':
        rom = f.sections[1]
        lvl5_off = 14237696
        pak_start = lvl5_off + 512 + 502874912
        pak_size = 2377069343
        idx_off = 2375799106
        
        rom.seek(pak_start + idx_off + 322190)
        dir_bytes = rom.read(pak_size - 204 - (idx_off + 322190))
        
        # Let's list all files in dir_bytes containing .bin or Localization
        import re
        matches = re.finditer(rb'([A-Za-z0-9_\-\./\\]+\.bin)', dir_bytes)
        for m in matches:
            fname = m.group(1)
            pos = m.end()
            # Encoded entry offset is right after null terminator or length byte
            # Let's check bytes right after
            enc_idx = struct.unpack('<I', dir_bytes[pos+1:pos+5])[0]
            # Read entry header from encoded index
            rom.seek(pak_start + idx_off + enc_idx)
            entry_bytes = rom.read(48)
            offset = struct.unpack('<Q', entry_bytes[:8])[0]
            print(f'{fname.decode()}: enc_idx=0x{enc_idx:x}, pak_offset=0x{offset:x}')
        break
