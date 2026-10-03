"""Tim record chua CAU VAN (kho text hien thi) tren ca 12 part, ca record nen lan khong nen."""
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import lz4.block

BIG = 32 << 20
# cau van: tu 3+ tu lien tiep, co chu cai, ket thuc bang dau cau (khong phai duong dan/scene)
SENT = re.compile(rb"(?<![A-Za-z/|_.])[A-Z][a-z']{1,15}(?:[ ][a-z']{1,15}){2,}[.!?]")


def lz4_once(pl):
    for size in (1 << 16, 1 << 20, BIG):
        try:
            return lz4.block.decompress(pl, uncompressed_size=size)
        except Exception as e:
            if 'insufficient' in str(e).lower() or 'space' in str(e).lower():
                continue
            return None
    return None


out_dir = r'E:\UNR_work\parts'
results = []
for f in sorted(os.listdir(out_dir), key=lambda x: int(x.rsplit('.', 1)[-1])):
    data = open(os.path.join(out_dir, f), 'rb').read()
    n = len(data)
    off = 0
    best = (0, None, None)
    tot = 0
    while off + 4 <= n:
        ln = struct.unpack_from('<I', data, off)[0]
        if not (8 <= ln <= 40_000_000) or off + 4 + ln > n:
            off += 4
            continue
        pl = data[off + 4:off + 4 + ln]
        r = lz4_once(pl)
        buf = r if r else pl
        sents = SENT.findall(buf)
        tot += len(sents)
        if len(sents) > best[0]:
            best = (len(sents), off, buf)
        off += 4 + ln
    print(f'{f}: {tot} cau | record nhieu nhat @{best[1] if best[1] is not None else 0:#x} co {best[0]} cau', flush=True)
    if best[0] >= 5 and best[2]:
        results.append((best[0], f, best[1], best[2]))
        print('   vi du:', [s.decode("utf-8", "replace")[:60] for s in SENT.findall(best[2])[:3]], flush=True)

results.sort(reverse=True)
if results:
    n_s, f, off, buf = results[0]
    os.makedirs(r'E:\UNR_work\textrec', exist_ok=True)
    p = rf'E:\UNR_work\textrec\{f}_{off:x}.bin'
    open(p, 'wb').write(buf)
    print(f'\n>>> record nhieu cau nhat: {f} @{off:#x} ({len(buf):,} byte) da luu {p}')
    print(buf[:600].decode('utf-8', 'replace'))
