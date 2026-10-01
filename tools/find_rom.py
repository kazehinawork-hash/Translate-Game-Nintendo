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
DEFAULT_DIRS = [ROOT / 'input', Path(os.environ.get('ROM_DIR', r'E:\ROM_Backup'))]
EXTS = ('.nsp', '.xci')


def _dirs(extra=()):
    out = list(DEFAULT_DIRS)
    for d in extra:
        out.append(Path(d))
    return [d for d in out if d.exists()]


def list_roms(extra_dirs=()):
    """Trả về list[(Path, size_bytes)] của mọi ROM tìm thấy."""
    found = {}
    for d in _dirs(extra_dirs):
        for p in d.rglob('*'):
            if p.is_file() and p.suffix.lower() in EXTS:
                found[p.resolve()] = p.stat().st_size
    return sorted(found.items(), key=lambda x: str(x[0]))


def find_rom(keyword=None, extra_dirs=(), prefer_base=True):
    """Tìm ROM khớp `keyword` (TitleID hoặc tên, không phân biệt hoa thường).

    prefer_base=True: ưu tiên bản gốc (v0) hơn bản Update.
    Trả về Path hoặc None.
    """
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
    roms = list_roms(extra)
    kw = args[0] if args else None
    if kw:
        roms = [(p, s) for p, s in roms if kw.lower() in p.name.lower()]
    if not roms:
        print('Khong tim thay ROM nao' + (f' khop "{kw}"' if kw else '') + '.')
        print('Thu muc da quet:', ', '.join(str(d) for d in _dirs(extra)))
        return 1
    for p, s in (roms if show_all else roms[:1]):
        print(f'{s/1024/1024:10.1f} MB  {p}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
