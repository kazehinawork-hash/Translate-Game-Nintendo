"""
extract_il2cpp.py — Bóc `main` (ExeFS) + `global-metadata.dat` (RomFS) từ NSP, phục vụ dựng
typetree IL2CPP (đọc trường MonoBehaviour theo TÊN thay vì theo offset).

Dùng:
    python tools/extract_il2cpp.py "<game.nsp>" <thu_muc_ra>
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
sys.path.insert(0, ROOT)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    nsp_path, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)

    import nsz.nut.Keys as Keys
    from nsz.Fs import Nsp
    from nsz.Fs.Nca import Nca
    from nsz.Fs.Pfs0 import Pfs0

    Keys.load(os.path.join(ROOT, 'input', 'prod.keys'))
    nsp = Nsp.Nsp(); nsp.open(nsp_path, 'rb')
    got = []
    for f in nsp:
        try:
            nca = Nca(); nca.open(file=f)
        except Exception:
            continue
        for fs in nca.sectionFilesystems:
            if not isinstance(fs, Pfs0):
                continue
            names = [getattr(pf, 'name', None) or getattr(pf, '_path', '') for pf in fs.files]
            if 'main' not in names:
                continue
            for pf in fs.files:
                nm = getattr(pf, 'name', None) or getattr(pf, '_path', '')
                if nm != 'main':
                    continue
                data = pf.read(pf.size) if hasattr(pf, 'size') else pf.read()
                dst = os.path.join(outdir, 'main')
                open(dst, 'wb').write(data)
                got.append(('main', len(data)))
            break
    for nm, sz in got:
        print(f'OK: {nm} -> {outdir} ({sz:,} bytes)')
    if not got:
        print('KHONG tim thay ExeFS main trong NSP nay')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
