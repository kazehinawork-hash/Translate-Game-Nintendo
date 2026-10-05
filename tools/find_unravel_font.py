"""Tim va phan tich font .fgen cua Unravel Two trong archive .kit."""
import os
import re
import struct
import sys

sys.path.insert(0, r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\tools')
sys.stdout.reconfigure(encoding='utf-8')
from kit_lz4dict import Lz4DictError, decode_block

HIST_KEEP = 262140
MAGICS = {b'OTTO': 'OTF (CFF)', b'\x00\x01\x00\x00': 'TTF (glyf)', b'ttcf': 'TTF collection',
          b'wOFF': 'WOFF', b'DDS ': 'DDS texture', b'KTX ': 'KTX texture',
          b'\x89PNG': 'PNG', b'BM': 'BMP'}


def run(part):
    data = open(part, 'rb').read()
    off = 0
    hist = b''
    n = 0
    hits = []
    while off + 4 <= len(data):
        ln = struct.unpack_from('<I', data, off)[0]
        if not (4 <= ln <= 40_000_000) or off + 4 + ln > len(data):
            done = False
            for d in range(1, 64):
                if off + d + 4 > len(data):
                    break
                ln2 = struct.unpack_from('<I', data, off + d)[0]
                if 4 <= ln2 <= 40_000_000 and off + d + 4 + ln2 <= len(data):
                    try:
                        o2 = decode_block(data[off + d + 4:off + d + 4 + ln2], hist[-HIST_KEEP:])
                    except Lz4DictError:
                        continue
                    off += d
                    hist = (hist + o2)[-HIST_KEEP:]
                    off += 4 + ln2
                    done = True
                    break
            if not done:
                off += 64
            continue
        pl = data[off + 4:off + 4 + ln]
        try:
            out = decode_block(pl, hist[-HIST_KEEP:])
        except Lz4DictError:
            out = pl if pl.lstrip()[:1] in (b'{', b'[') else None
        if out is None:
            off += 64
            continue
        n += 1
        if b'fgen' in out or b'font' in out.lower()[:2000] or b'Fonts/' in out:
            head = out[:16]
            mg = next((v for k, v in MAGICS.items() if head.startswith(k)), '')
            hits.append((off, ln, len(out), mg, out[:200].decode('utf-8', 'replace').replace('\r\n', ' ')))
        hist = (hist + out)[-HIST_KEEP:]
        off += 4 + ln
    return n, hits


for part in (r'E:\UNR_work\parts\Data.kit.0', r'E:\UNR_work\parts\Data.kit.1'):
    if not os.path.exists(part):
        print(f'{part}: khong co')
        continue
    n, hits = run(part)
    print(f'\n=== {os.path.basename(part)}: {n} record | {len(hits)} record lien quan font ===')
    for off, ln, ol, mg, sample in hits[:8]:
        print(f'  @{off:#x} nen={ln:,} -> {ol:,} byte | magic: {mg or "(khong ro)"}')
        print(f'     {sample[:150]}')
