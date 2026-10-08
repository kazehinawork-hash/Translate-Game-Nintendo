"""Do tim header RomFS trong NCA du lieu cua ban update MONOPOLY."""
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from nsz.Fs import Nsp                      # noqa: E402
import nsz.nut.Keys as Keys                 # noqa: E402
from nsz.Fs.Nca import Nca                  # noqa: E402

Keys.load(os.path.join(ROOT, 'input', 'prod.keys'))
UPD = r'E:\ROM_Backup\Monopoly\MONOPOLY 2024 [01002C201BC40800][v393216][US][Update v1.6].nsp'

nsp = Nsp.Nsp()
nsp.open(UPD, 'rb')
for f in nsp:
    try:
        nca = Nca()
        nca.open(file=f)
    except Exception:
        continue
    for fs in nca.sectionFilesystems:
        if fs.fsType != 3 or fs.size < 100_000_000:
            continue
        print(f'section ROMFS size={fs.size:,}')
        for attr in ('offset', 'start', 'base', 'off'):
            if hasattr(fs, attr):
                print(f'  fs.{attr} = {getattr(fs, attr)}')
        try:
            print(f'  ivfc levels: {[(l.offset, l.size) for l in fs.ivfc.levels]}')
        except Exception as e:
            print(f'  ivfc: {e}')
        # do: doc 0x50 byte o vai ung vien, in headerSize + dataOff
        cands = [0, 0x200, 0x10000, 0x100000, 0x200000, 0x200200, 0x1f0000, 0x1f8000]
        try:
            lv = fs.ivfc.levels
            cands += [lv[5].offset, lv[5].offset - 0x200, lv[4].offset]
        except Exception:
            pass
        for c in sorted(set(x for x in cands if x is not None and x >= 0)):
            try:
                fs.seek(c)
                b = fs.read(0x50)
                if len(b) < 0x50:
                    continue
                hs, zero, dhO, dhS, dmO, dmS, fhO, fhS, fmO, fmS, dOff = struct.unpack('<IIQQQQQQQQQ', b)
                good = (hs == 0x50 and dOff in (0x200,)) and dmO < fs.size and fmO < fs.size
                flag = '<<< CO THE LA HEADER ROMFS' if good else ''
                print(f'  @{c:#09x} headerSize={hs} dataOff={dOff:#x} dmO={dmO:#x} fmO={fmO:#x} {flag}')
            except Exception as e:
                print(f'  @{c:#09x} loi {type(e).__name__}')
