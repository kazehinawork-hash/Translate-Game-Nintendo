# -*- coding: utf-8 -*-
"""
patch_totk_rstb.py — Vá ResourceSizeTable (RSTB) cho mod TotK.

TotK dùng System/Resource/ResourceSizeTable.Product.<ver>[.Nin_NX_NVN].rsizetable.zs
để biết KÍCH THƯỚC GIẢI NÉN của từng resource. Thay Mals/*.sarc.zs hoặc Font/*.bfarc.zs
mà không cập nhật RSTB -> game treo/crash khi nạp (bão `Unmapped Read` trong Eden).

Định dạng RSTB (TotK):
  - .zs nén **KHÔNG dùng từ điển** (khác Mals/Font — hai loại này BẮT BUỘC có từ điển).
  - Giải nén ra magic "RESTBL", sau đó là bảng các cặp (u32 crc32, u32 size).
  - Khoá = crc32(đường dẫn resource KHÔNG có đuôi nén), vd "Mals/USen.Product.142.sarc".
  - size = kích thước GIẢI NÉN + ít dư (dùng +0x1000 cho an toàn).

Dùng:
    python tools/patch_totk_rstb.py [--romfs <thư mục romfs của mod>]
"""
import os
import sys
import struct
import zlib
import argparse
import zstandard as zstd
import oead

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TITLE_ID = '0100F2C0115B6000'
SRC_ROMFS = os.path.join(r'E:\RomFS_Dump', TITLE_ID, 'romfs')
DEFAULT_ROMFS = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TITLE_ID, 'romfs')
SLACK = 0x1000
RSTB_NAMES = [
    'ResourceSizeTable.Product.143.Nin_NX_NVN.rsizetable.zs',
    'ResourceSizeTable.Product.143.rsizetable.zs',
    'ResourceSizeTable.Product.142.Nin_NX_NVN.rsizetable.zs',
    'ResourceSizeTable.Product.142.rsizetable.zs',
]


def load_dict():
    zd = oead.Sarc(zstd.ZstdDecompressor().decompress(
        open(os.path.join(SRC_ROMFS, 'Pack', 'ZsDic.pack.zs'), 'rb').read()))
    return zstd.ZstdCompressionDict(next(bytes(f.data) for f in zd.get_files() if f.name == 'zs.zsdic'))


def write_rstb(romfs_dir, verbose=True):
    """Đọc Mals/Font trong `romfs_dir`, vá RSTB gốc 1.4.3 và ghi vào romfs_dir/System/Resource."""
    dd = load_dict()
    dctx = zstd.ZstdDecompressor(dict_data=dd)
    src = os.path.join(SRC_ROMFS, 'System', 'Resource',
                       'ResourceSizeTable.Product.143.Nin_NX_NVN.rsizetable.zs')
    data = bytearray(dctx.decompress(open(src, 'rb').read()))

    targets = {
        'Mals/USen.Product.142.sarc': os.path.join(romfs_dir, 'Mals', 'USen.Product.142.sarc.zs'),
        'Font/Font.Nin_NX_NVN.bfarc': os.path.join(romfs_dir, 'Font', 'Font.Nin_NX_NVN.bfarc.zs'),
    }
    for path, zs_file in targets.items():
        if not os.path.exists(zs_file):
            raise SystemExit(f'Thiếu file mod: {zs_file}')
        dl = len(dctx.decompress(open(zs_file, 'rb').read()))
        h = zlib.crc32(path.encode('utf-8')) & 0xFFFFFFFF
        pos = data.find(struct.pack('<I', h))
        if pos < 0:
            raise SystemExit(f'Không tìm thấy entry RSTB cho {path}')
        old = struct.unpack_from('<I', data, pos + 4)[0]
        struct.pack_into('<I', data, pos + 4, dl + SLACK)
        if verbose:
            print(f'  RSTB {path}: {old} -> {dl + SLACK} (giải nén thật {dl})')

    out = zstd.ZstdCompressor(level=15).compress(bytes(data))     # KHÔNG từ điển
    plain = zstd.ZstdDecompressor()
    assert len(plain.decompress(out)) == len(data), 'RSTB phải đọc được khi không có từ điển!'
    assert len(dctx.decompress(out)) == len(data), 'RSTB phải đọc được cả khi có từ điển!'

    dst = os.path.join(romfs_dir, 'System', 'Resource')
    os.makedirs(dst, exist_ok=True)
    for n in RSTB_NAMES:
        open(os.path.join(dst, n), 'wb').write(out)
    if verbose:
        print(f'  ghi {len(RSTB_NAMES)} tên RSTB ({len(out)} byte) vào {dst}')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--romfs', default=DEFAULT_ROMFS)
    args = ap.parse_args()
    write_rstb(args.romfs)


if __name__ == '__main__':
    main()
