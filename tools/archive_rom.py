"""
archive_rom.py — Lưu trữ ROM (.nsp/.xci) ra khỏi OneDrive sau khi đã bóc xách xong.

QUY TẮC CỦA DỰ ÁN: ROM chỉ nằm trong `input/` trong lúc bóc dữ liệu. Xong việc thì
**chuyển ra `E:\\ROM_Backup`** để (a) không phình OneDrive, (b) vẫn còn để bóc lại khi cần.
`tools/find_rom.py` tự tìm ROM trong `input/` TRƯỚC, rồi tới `E:\\ROM_Backup` — nên chuyển đi
không làm hỏng quy trình.

⚠️ LƯU Ý QUAN TRỌNG (đã từng dính): file trong OneDrive là **reparse point** (Files On-Demand).
`Move-Item`/`mv` báo thành công nhưng OneDrive **nuốt mất** — file vẫn nằm nguyên chỗ cũ.
Vì vậy tool này dùng: **copy → xác minh SHA256 → mới xoá bản nguồn**.

Dùng:
    python tools/archive_rom.py --list                 # xem đang có ROM nào trong input/
    python tools/archive_rom.py                        # lưu trữ tất cả
    python tools/archive_rom.py --dry                  # chỉ in việc sẽ làm
    python tools/archive_rom.py --to "D:\\ROM_Backup"  # đổi nơi lưu
    python tools/archive_rom.py --game Ori             # chỉ lưu ROM có tên chứa "Ori"
"""
import argparse
import hashlib
import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT = os.path.join(ROOT, 'input')
DEFAULT_BACKUP = r'E:\ROM_Backup'
EXTS = ('.nsp', '.xci', '.nsz', '.xcz')

# Gợi ý tên thư mục theo TitleID (khớp cách đặt tên sẵn có trong ROM_Backup)
TITLE_DIR = {
    '0100F7E00C70E000': 'HogwartsLegacy',
    '0100F7E00C70E800': 'HogwartsLegacy',
    '0100A00019DE0000': 'Hades2',
    '0100A00019DE0800': 'Hades2',
    '0100D2F00D5C0000': 'SwitchSports',
    '01008DD013200000': 'Ori',
    '01008DD013200800': 'Ori',
    '010061D00DB74000': 'OriBlindForest',
    '010061D00DB74800': 'OriBlindForest',
    '0100965017338000': 'MarioPartyJamboree',
    '0100965017338800': 'MarioPartyJamboree',
    '0100E5D00CC0C000': 'UnravelTwo',
    '0100E5D00CC0C800': 'UnravelTwo',
    '01004D300C5AE000': 'Kirby',
    '01004D300C5AE800': 'Kirby',
}


def sha256(path, chunk=8 << 20):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def pick_dir(name, backup):
    for tid, folder in TITLE_DIR.items():
        if tid.lower() in name.lower():
            return os.path.join(backup, folder)
    return os.path.join(backup, 'Khac')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--to', default=DEFAULT_BACKUP, help=f'nơi lưu (mặc định {DEFAULT_BACKUP})')
    ap.add_argument('--game', default=None, help='chỉ xử lý file có tên chứa chuỗi này')
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--keep-source', action='store_true', help='chỉ copy, KHÔNG xoá bản trong input/')
    a = ap.parse_args()

    roms = [f for f in sorted(os.listdir(INPUT))
            if f.lower().endswith(EXTS) and (not a.game or a.game.lower() in f.lower())] \
        if os.path.isdir(INPUT) else []

    if not roms:
        print(f'input/ không có ROM nào{" khớp " + a.game if a.game else ""}.')
        return 0

    print(f'ROM trong input/: {len(roms)}')
    for f in roms:
        p = os.path.join(INPUT, f)
        print(f'   {os.path.getsize(p)/1024**3:6.2f} GB  {f}')
    if a.list:
        return 0

    ok = 0
    for f in roms:
        src = os.path.join(INPUT, f)
        dst_dir = pick_dir(f, a.to)
        dst = os.path.join(dst_dir, f)
        print(f'\n─ {f}\n   -> {dst}')
        if a.dry:
            continue
        os.makedirs(dst_dir, exist_ok=True)
        if os.path.exists(dst) and os.path.getsize(dst) == os.path.getsize(src) \
                and sha256(dst) == sha256(src):
            print('   bản sao đã có và khớp -> chỉ xoá bản trong input/')
        else:
            shutil.copy2(src, dst)
            if sha256(dst) != sha256(src):
                print('   ❌ SHA256 KHÔNG khớp -> giữ nguyên bản trong input/, dừng lại')
                return 1
            print('   ✅ copy + xác minh SHA256: OK')
        if not a.keep_source:
            os.remove(src)
            print('   đã xoá bản trong input/')
        ok += 1

    print(f'\n=== xong: {ok}/{len(roms)} ROM đã lưu vào {a.to}')
    if not a.keep_source and not a.dry:
        print('   (tools/find_rom.py vẫn tìm thấy ROM trong E:\\ROM_Backup khi cần bóc lại)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
