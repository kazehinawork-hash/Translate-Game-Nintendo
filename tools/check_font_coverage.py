"""
check_font_coverage.py — Kiểm tra một font TTF có phủ HẾT các ký tự đang dùng
trong gói mod AVAFDICT (MAIN/SUB) hay không.

Cách dùng (chạy từ gốc dự án):
    python tools/check_font_coverage.py <font.ttf> <file1.bin> [<file2.bin> ...]

Ví dụ:
    python tools/check_font_coverage.py tools/fonts_hades2/Lato-Regular.ttf \
        output/atmosphere/contents/0100F7E00C70E000/romfs/Phoenix/Content/Localization/SWITCH/MAIN-enUS.bin \
        output/atmosphere/contents/0100F7E00C70E000/romfs/Phoenix/Content/Localization/SWITCH/SUB-enUS.bin

Kết quả PASS nghĩa là font không để lại ô vuông cho bất kỳ ký tự nào trong mod.
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))

from avaf_codec import unpack_avafdict          # noqa: E402
from fontTools.ttLib import TTFont              # noqa: E402

IGNORE = {0x0a, 0x0d, 0x09}  # newline / carriage return / tab: không phải glyph


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    font_path, bins = sys.argv[1], sys.argv[2:]
    cmap = TTFont(font_path).getBestCmap()

    cps = set()
    for b in bins:
        data = unpack_avafdict(open(b, 'rb').read())
        for v in data.values():
            cps.update(ord(c) for c in v)

    missing = sorted(c for c in cps if c not in cmap and c not in IGNORE)
    print(f'font      : {font_path} ({len(cmap)} glyph)')
    print(f'bin(s)    : {len(bins)} file')
    print(f'ky tu dung: {len(cps)}')
    print(f'thieu     : {len(missing)} {[hex(m) for m in missing[:20]]}')
    print('KET QUA   :', 'PASS - font phu het' if not missing else 'FAIL - thieu glyph')
    return 0 if not missing else 2


if __name__ == '__main__':
    raise SystemExit(main())
