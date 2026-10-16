"""
find_rom.py — Tìm file ROM (.nsp / .xci) theo TitleID hoặc tên game.

Thứ tự tìm:
  1. `input/` (trong dự án)
  2. Thư mục `ROM_DIR` (biến môi trường), mặc định `E:\\ROM_Backup`
  3. Mọi thư mục thêm qua tham số `--dir`

Cách dùng:
    python tools/find_rom.py                      # liệt kê mọi ROM tìm thấy
    python tools/find_rom.py 01008DD013200000     # tìm theo TitleID
    python tools/find_rom.py ori                  # tìm theo tên game
    python tools/find_rom.py ori --all            # in tất cả kết quả (kể cả bản update)

Dùng như thư viện:
    from find_rom import find_rom, list_roms
    path = find_rom('01008DD013200000')           # -> Path hoặc None
"""
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DIRS = [Path(os.environ.get('ROMFS_DUMP_DIR', r'E:\RomFS_Dump')), ROOT / 'dump', ROOT / 'input', Path(os.environ.get('ROM_DIR', r'E:\ROM_Backup'))]
EXTS = ('.nsp', '.xci')


def _dirs(extra=()):
    out = list(DEFAULT_DIRS)
    for d in extra:
        out.append(Path(d))
    return [d for d in out if d.exists()]


def find_romfs_dump(keyword=None):
    """Tìm thư mục RomFS đã dump (ưu tiên hàng đầu cho workflow tự hành 100%).
    Quét trong:
      1. E:\\RomFS_Dump\\<TitleID>\\romfs hoặc E:\\RomFS_Dump\\<TitleID>
      2. dump/<TitleID>/romfs hoặc dump/<TitleID>/
      3. games/<TitleID>_*/source/romfs/
      4. input/romfs/
    """
    search_dirs = [
        Path(os.environ.get('ROMFS_DUMP_DIR', r'E:\RomFS_Dump')),
        ROOT / 'dump',
        ROOT / 'input',
        ROOT / 'games',
    ]
    for base in search_dirs:
        if not base.exists():
            continue
        # Kiểm tra direct romfs
        direct = base / 'romfs'
        if direct.is_dir() and (not keyword or keyword.lower() in str(direct).lower()):
            return direct
        for p in base.iterdir():
            if not p.is_dir():
                continue
            if keyword and keyword.lower() not in p.name.lower():
                continue
            if (p / 'romfs').is_dir():
                return p / 'romfs'
            if p.name.lower() == 'romfs':
                return p
            # games/.../source/romfs
            if (p / 'source' / 'romfs').is_dir():
                return p / 'source' / 'romfs'
            # direct game folder containing game assets
            if (p / 'Data').is_dir() or (p / 'resource').is_dir() or (p / 'Common').is_dir():
                return p
    return None


def list_roms(extra_dirs=()):
    """Trả về list[(Path, size_bytes)] của mọi ROM tìm thấy."""
    found = {}
    for d in _dirs(extra_dirs):
        for p in d.rglob('*'):
            if p.is_file() and p.suffix.lower() in EXTS:
                found[p.resolve()] = p.stat().st_size
    return sorted(found.items(), key=lambda x: str(x[0]))


def find_rom(keyword=None, extra_dirs=(), prefer_base=True):
    """Tìm RomFS dump (ưu tiên 1) hoặc file ROM khớp `keyword`.
    Trả về Path (thư mục RomFS hoặc file ROM) hoặc None.
    """
    # 1. ƯU TIÊN 1: Thư mục RomFS đã dump
    romfs = find_romfs_dump(keyword)
    if romfs:
        return romfs

    # 2. ƯU TIÊN 2: File ROM (.nsp/.xci)
    roms = list_roms(extra_dirs)
    if keyword:
        k = keyword.lower()
        roms = [(p, s) for p, s in roms if k in p.name.lower()]
    if not roms:
        return None
    if prefer_base and len(roms) > 1:
        def rank(item):
            n = item[0].name.lower()
            return (('update' in n or 'upd' in n or 'v0' not in n and '[v1' in n), str(item[0]))
        roms = sorted(roms, key=rank)
    return roms[0][0]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    extra = []
    if '--dir' in sys.argv:
        extra = sys.argv[sys.argv.index('--dir') + 1:]
    show_all = '--all' in sys.argv
    kw = args[0] if args else None
    romfs = find_romfs_dump(kw)
    if romfs:
        print(f'[RomFS Dump] {romfs}')
        if not show_all:
            return 0
    roms = list_roms(extra)
    if kw:
        roms = [(p, s) for p, s in roms if kw.lower() in p.name.lower()]
    if not roms and not romfs:
        print('Khong tim thay ROM hoac RomFS nao' + (f' khop "{kw}"' if kw else '') + '.')
        print('Thu muc da quet:', ', '.join(str(d) for d in _dirs(extra)))
        return 1
    for p, s in (roms if show_all else roms[:1]):
        print(f'{s/1024/1024:10.1f} MB  {p}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
