"""extract_romfs_with_titlekeys.py — Boc file RomFS tu NSP **co titlekey** (bản update).

nsz chi giai ma duoc NCA khi biet titlekey; titlekey lay bang:
    nsz --titlekeys <file.nsp>      -> sinh ./titlekeys.txt
Tool nay doc input/titlekeys.txt, nap vao registry Titles cua nsz roi parse RomFS.

Dung:
    python tools/extract_romfs_with_titlekeys.py <nsp> [--list] [--get <romfs/path> <out>]
"""
import argparse
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from nsz.Fs import Nsp                      # noqa: E402
import nsz.nut.Keys as Keys                 # noqa: E402
import nsz.nut.Titles as Titles             # noqa: E402
from nsz.Fs.Nca import Nca                  # noqa: E402


def load_titlekeys():
    p = os.path.join(ROOT, 'input', 'titlekeys.txt')
    n = 0
    if not os.path.exists(p):
        return 0
    for line in open(p, encoding='utf-8'):
        line = line.strip()
        if not line or '|' not in line:
            continue
        parts = line.split('|')
        if len(parts) < 2:
            continue
        rights_id, key = parts[0].strip(), parts[1].strip()
        tid = rights_id[:16].upper()
        Titles.get(tid).key = key
        n += 1
    return n


def open_romfs(nsp_path):
    nsp = Nsp.Nsp()
    nsp.open(nsp_path, 'rb')
    best = None
    for f in nsp:
        try:
            nca = Nca()
            nca.open(file=f)
        except Exception:
            continue
        for fs in nca.sectionFilesystems:
            if fs.fsType == 3 and (best is None or fs.size > best[1].size):
                best = (nca, fs, f)
    if not best:
        raise SystemExit('Khong tim thay section RomFS')
    return best


def parse_romfs(fs):
    base = fs.ivfc.levels[5].offset
    fs.seek(base)
    hdr = fs.read(0x50)
    (hs, zero, dhO, dhS, dmO, dmS, fhO, fhS, fmO, fmS, dOff) = struct.unpack('<IIQQQQQQQQQ', hdr)
    if hs != 0x50 or dOff != 0x200:
        raise SystemExit(f'Header RomFS khong hop le (headerSize={hs:#x} dataOff={dOff:#x}) '
                         f'-> titlekey sai hoac chua giai ma duoc')
    fs.seek(base + dmO)
    dmeta = fs.read(dmS)
    fs.seek(base + fmO)
    fmeta = fs.read(fmS)
    dirs, p = [], 0
    while p < len(dmeta):
        parent, sibling, child, file, h, nlen = struct.unpack_from('<IIIIII', dmeta, p)
        dirs.append({'off': p, 'parent': parent, 'name': dmeta[p + 24:p + 24 + nlen].decode('utf-8', 'replace')})
        p = (p + 24 + nlen + 3) & ~3
    files, p = [], 0
    while p < len(fmeta):
        parent, sibling, off, size, h, nlen = struct.unpack_from('<IIQQII', fmeta, p)
        files.append({'off': p, 'parent': parent, 'offset': off, 'size': size,
                      'name': fmeta[p + 32:p + 32 + nlen].decode('utf-8', 'replace')})
        p = (p + 32 + nlen + 3) & ~3
    dbyoff = {d['off']: d for d in dirs}

    def path_of(d):
        parts, cur, g = [d['name']], d, 0
        while cur['off'] != 0 and cur['parent'] in dbyoff and g < 80:
            cur = dbyoff[cur['parent']]
            parts.append(cur['name'])
            g += 1
        return '/'.join(reversed(parts))

    out = []
    for fl in files:
        pd = dbyoff.get(fl['parent'])
        p = ((path_of(pd) if pd else '') + '/' + fl['name']).lstrip('/')
        out.append((p, fl['offset'], fl['size']))
    return base, dOff, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('nsp')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--get', nargs=2, metavar=('ROMFS_PATH', 'OUT'))
    ap.add_argument('--filter', default=None)
    a = ap.parse_args()

    n = load_titlekeys()
    print(f'# nap {n} titlekey tu input/titlekeys.txt', flush=True)
    Keys.load(os.path.join(ROOT, 'input', 'prod.keys'))

    nca, fs, f = open_romfs(a.nsp)
    print(f'# NCA {os.path.basename(str(f._path))} | RomFS {fs.size:,} byte', flush=True)
    base, dOff, files = parse_romfs(fs)
    print(f'# {len(files):,} file', flush=True)

    if a.list or a.filter:
        sel = [x for x in files if (a.filter is None or a.filter.lower() in x[0].lower())]
        for p, off, size in sel[:60]:
            print(f'{size:>14,}  {p}')
        print(f'# hien {min(len(sel),60)}/{len(sel)} file khop')
        return
    if a.get:
        want = a.get[0].replace('\\', '/').lstrip('/')
        for p, off, size in files:
            if p.lower() == want.lower():
                fs.seek(base + dOff + off)
                data = fs.read(size)
                open(a.get[1], 'wb').write(data)
                print(f'OK: {p} -> {a.get[1]} ({len(data):,} byte)')
                return
        raise SystemExit(f'Khong thay file: {want}')


if __name__ == '__main__':
    raise SystemExit(main())
