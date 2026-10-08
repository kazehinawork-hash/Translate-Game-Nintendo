"""Quet tim 'UnityFS' trong NCA du lieu cua NSP update MONOPOLY va cat ra bundle."""
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
# nap titlekey (co the can cho NCA cua ban update)
try:
    import nsz.nut.Titles as Titles
    tp = os.path.join(ROOT, 'input', 'titlekeys.txt')
    if os.path.exists(tp):
        for line in open(tp, encoding='utf-8'):
            if '|' in line:
                a, b = line.strip().split('|')[:2]
                Titles.get(a[:16].upper()).key = b.strip()
except Exception as e:
    print('nap titlekey loi:', e)
UPD = r'E:\ROM_Backup\Monopoly\MONOPOLY 2024 [01002C201BC40800][v393216][US][Update v1.6].nsp'
OUT = r'E:\MONO_work\upd_carve.unity3d'
MAGIC = b'UnityFS\x00'

nsp = Nsp.Nsp()
nsp.open(UPD, 'rb')
found = False
for f in nsp:
    try:
        nca = Nca()
        nca.open(file=f)
    except Exception:
        continue
    for fs in nca.sectionFilesystems:
        if fs.fsType != 3:
            continue
        size = fs.size
        if size < 10_000_000:
            continue
        print(f'quet section ROMFS {size:,} byte...', flush=True)
        CH = 8 << 20
        off = 0
        prev_tail = b''
        while off < size:
            fs.seek(off)
            buf = fs.read(min(CH, size - off))
            if not buf:
                break
            data = prev_tail + buf
            base_off = off - len(prev_tail)
            i = data.find(MAGIC)
            while i >= 0:
                pos = base_off + i
                # doc header UnityFS de lay tong kich thuoc
                try:
                    p = data.find(MAGIC, i)
                    seg = data[p:p + 200] if p >= 0 else b''
                    e1 = seg.index(b'\x00', 7)
                    ver, = struct.unpack_from('>I', seg, e1 + 1)
                    e2 = seg.index(b'\x00', e1 + 5)
                    e3 = seg.index(b'\x00', e2 + 1)
                    hdr_size, = struct.unpack_from('>q', seg, e3 + 1)
                    print(f'  THAY UnityFS @ {pos:,} ({pos:#x}) | version={ver} | tong size={hdr_size:,}', flush=True)
                    if 100_000_000 < hdr_size < 2_000_000_000:
                        fs.seek(pos)
                        blob = fs.read(hdr_size)
                        open(OUT, 'wb').write(blob)
                        print(f'  -> da cat {len(blob):,} byte ra {OUT}', flush=True)
                        found = True
                except Exception as ex:
                    print(f'  UnityFS @ {pos:,} nhung doc header loi: {ex}', flush=True)
                i = data.find(MAGIC, i + 1)
                if found:
                    break
            prev_tail = data[-64:]
            off += len(buf)
            if found:
                break
        if found:
            break
    if found:
        break
print('KET QUA:', 'tim thay' if found else 'KHONG tim thay UnityFS')
