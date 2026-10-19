# -*- coding: utf-8 -*-
"""
patch_sws_rstb.py — Vá ResourceSizeTable cho Nintendo Switch Sports (0100D2F00D5C0000).

Game EPD nào cũng có bảng `System/Resource/ResourceSizeTable.Product.<ver>.rsizetable.zs` ghi
KÍCH THƯỚC GIẢI NÉN của từng resource. Thay `Mals/*.sarc.zs` / `Font/*.bfarc.zs` mà không cập nhật
bảng -> engine cấp phát thiếu -> treo/crash (xem BH-49 trong docs/BAI-HOC.md).

Khác TotK: file `.zs` của game này nén **KHÔNG dùng từ điển** (windowLog=21, single-segment),
và bảng size cũng vậy -> nén lại bằng zstd thuần.

Dùng: python tools/patch_sws_rstb.py
"""
import os
import sys
import struct
import zlib
import zstandard as zstd

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TID = '0100D2F00D5C0000'
DUMP = os.path.join(r'E:\RomFS_Dump', TID, 'romfs')
ROMFS = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs')
SRC_RSTB = os.path.join(DUMP, 'System', 'Resource', 'ResourceSizeTable.Product.150.rsizetable.zs')
DST_RSTB = os.path.join(ROMFS, 'System', 'Resource', 'ResourceSizeTable.Product.150.rsizetable.zs')
SLACK = 0x1000

TARGETS = {
    'Mals/USen.Product.150.sarc': os.path.join(ROMFS, 'Mals', 'USen.Product.150.sarc.zs'),
    'Font/Font.Nin_NX_NVN.bfarc': os.path.join(ROMFS, 'Font', 'Font.Nin_NX_NVN.bfarc.zs'),
}


def main():
    plain = zstd.ZstdDecompressor()
    data = bytearray(plain.decompress(open(SRC_RSTB, 'rb').read()))
    print(f'RSTB gốc: {os.path.getsize(SRC_RSTB):,} byte nén -> {len(data):,} byte | magic {data[:4]!r}')

    for path, zs_file in TARGETS.items():
        dl = len(plain.decompress(open(zs_file, 'rb').read()))
        h = zlib.crc32(path.encode('utf-8')) & 0xFFFFFFFF
        pos = data.find(struct.pack('<I', h))
        if pos < 0:
            raise SystemExit(f'Không thấy entry RSTB cho {path}')
        old = struct.unpack_from('<I', data, pos + 4)[0]
        struct.pack_into('<I', data, pos + 4, dl + SLACK)
        flag = 'OK' if old >= dl else '⚠ VƯỢT HẠN MỨC'
        print(f'  {path}: {old:,} -> {dl + SLACK:,} (giải nén thật {dl:,})  [{flag}]')

    out = zstd.ZstdCompressor(level=15).compress(bytes(data))
    assert len(plain.decompress(out)) == len(data), 'RSTB nén lại không đọc được!'
    os.makedirs(os.path.dirname(DST_RSTB), exist_ok=True)
    open(DST_RSTB, 'wb').write(out)
    print(f'  frame mới: {out[:8].hex(" ")} (gốc {open(SRC_RSTB, "rb").read(8).hex(" ")})')
    print(f'  ghi {DST_RSTB} ({len(out):,} byte)')


if __name__ == '__main__':
    main()
