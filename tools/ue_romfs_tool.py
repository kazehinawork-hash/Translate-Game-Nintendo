"""
ue_romfs_tool.py — Liệt kê / trích file RomFS từ NSP game Nintendo Switch (Unreal Engine),
không cần hactool. Dùng cho các game UE4.27 dùng IoStore (pakchunk*.pak/.ucas/.utoc).

Cách dùng (chạy từ gốc dự án):
    python tools/ue_romfs_tool.py list   "<duong/dan/game.nsp>"
    python tools/ue_romfs_tool.py extract "<duong/dan/game.nsp>" "<RomFS/path>" "<out_file>"

Ghi chú:
- Cần `nsz` (pip) + `input/prod.keys`.
- RomFS: IVFC level cuối cùng là gốc dữ liệu; header RomFS nằm tại offset level5,
  dataOff (thường 0x200), còn bảng metadata (dir/file) nằm ở CUỐI khu vực RomFS.
- File offset trong bảng file tính từ  (level5_offset + dataOff).
"""
import os
import sys
import struct
import binascii

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from nsz.Fs import Nsp                      # noqa: E402
import nsz.nut.Keys as Keys                 # noqa: E402
from nsz.Fs.Nca import Nca                  # noqa: E402


def _open_nca(nsp_path):
    Keys.load(os.path.join(ROOT, 'input', 'prod.keys'))
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
            if fs.fsType == 3 and (best is None or fs.size > best[1].size):  # ROMFS
                best = (nca, fs)
                best = (nca, fs, f)
    if not best:
        raise SystemExit('Khong tim thay section RomFS trong NSP nay.')
    return best[0], best[1], best[2]


def _read_meta(fs, base, off, size):
    fs.seek(base + off)
    return fs.read(size)


def _parse(fs):
    base = fs.ivfc.levels[5].offset
    fs.seek(base)
    hdr = fs.read(0x50)
    hs, zero, dhO, dhS, dmO, dmS, fhO, fhS, fmO, fmS, dOff = struct.unpack('<IIQQQQQQQQQ', hdr)
    dmeta = _read_meta(fs, base, dmO, dmS)
    fmeta = _read_meta(fs, base, fmO, fmS)

    dirs, p = [], 0
    while p < len(dmeta):
        parent, sibling, child, file, h, nlen = struct.unpack_from('<IIIIII', dmeta, p)
        dirs.append({'off': p, 'parent': parent, 'name': dmeta[p + 24:p + 24 + nlen].decode('utf-8', 'replace')})
        p += 24 + nlen
        p = (p + 3) & ~3
    files, p = [], 0
    while p < len(fmeta):
        parent, sibling, off, size, h, nlen = struct.unpack_from('<IIQQII', fmeta, p)
        files.append({'off': p, 'parent': parent, 'offset': off, 'size': size,
                      'name': fmeta[p + 32:p + 32 + nlen].decode('utf-8', 'replace')})
        p += 32 + nlen
        p = (p + 3) & ~3
    return base, dOff, dirs, files


def _path_of(d, dbyoff):
    parts, cur, g = [d['name']], d, 0
    while cur['off'] != 0 and cur['parent'] in dbyoff and g < 80:
        cur = dbyoff[cur['parent']]
        parts.append(cur['name'])
        g += 1
    return '/'.join(reversed(parts))


def _walk(fs):
    base, dOff, dirs, files = _parse(fs)
    dbyoff = {d['off']: d for d in dirs}
    out = []
    for fl in files:
        pd = dbyoff.get(fl['parent'])
        path = ((_path_of(pd, dbyoff) if pd else '') + '/' + fl['name']).lstrip('/')
        out.append((path, fl['offset'], fl['size']))
    return base, dOff, out


def cmd_list(nsp_path):
    nca, fs, f = _open_nca(nsp_path)
    base, dOff, files = _walk(fs)
    print(f'# {f._path}  | {len(files)} file (RomFS)')
    for path, off, size in files:
        print(f'{size:>14}  off={off:>12}  {path}')


def cmd_extract(nsp_path, romfs_path, out_file):
    nca, fs, f = _open_nca(nsp_path)
    base, dOff, files = _walk(fs)
    want = romfs_path.replace('\\', '/').lstrip('/')
    for path, off, size in files:
        if path.lower() == want.lower():
            fs.seek(base + dOff + off)
            data = fs.read(size)
            open(out_file, 'wb').write(data)
            print(f'OK: {path} -> {out_file} ({len(data)} bytes)')
            return
    raise SystemExit(f'Khong thay file: {romfs_path}')


def cmd_extract_dir(nsp_path, prefix, out_dir):
    """Trich TAT CA file trong RomFS co tien to `prefix` ra thu muc out_dir (giu cau truc)."""
    nca, fs, f = _open_nca(nsp_path)
    base, dOff, files = _walk(fs)
    want = prefix.replace('\\', '/').lstrip('/').lower()
    sel = [(p, o, s) for p, o, s in files if p.lower().startswith(want)]
    print(f'# {len(sel)} file khop "{prefix}"')
    for path, off, size in sel:
        out_path = os.path.join(out_dir, *path.split('/'))
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fs.seek(base + dOff + off)
        data = fs.read(size)
        with open(out_path, 'wb') as g:
            g.write(data)
    print(f'# da ghi {len(sel)} file vao {out_dir}')


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return
    cmd = sys.argv[1].lower()
    if cmd == 'list':
        cmd_list(sys.argv[2])
    elif cmd == 'extract':
        cmd_extract(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == 'extract-dir':
        cmd_extract_dir(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
