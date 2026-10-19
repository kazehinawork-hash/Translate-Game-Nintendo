# -*- coding: utf-8 -*-
"""
build_totk_trt_mod.py — Port bản Việt hoá của "The Red Team" (TRT) sang game 1.4.3.

Vì sao cần: SARC của TRT dựng từ bản cũ nên
  - thiếu file `LayoutMsg/AppLoadingMessage_00.msbt` (game 1.4.3 có)
  - thiếu 140 nhãn ở 11 file mà 1.4.3 thêm
  - không có `ResourceSizeTable` cho Product.143 -> game 1.4.3 treo ở "Launching..."

Cách làm: lấy CẤU TRÚC file/nhãn từ Mals gốc 1.4.3, điền văn bản theo thứ tự ưu tiên
    1) bản dịch TRT   2) bản dịch của mình (cho nhãn mới 1.4.3)   3) nguyên bản EN
rồi đóng gói lại + vá RSTB 1.4.3 (Mals + Font).

Dùng:
    python tools/build_totk_trt_mod.py --trt "<...>/USen.Product.142.sarc.zs" [--out output/TRT143]
"""
import os
import re
import sys
import glob
import json
import shutil
import argparse
import zstandard as zstd
import oead

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from build_totk_mod import replace_msbt_txt2          # noqa: E402
from extract_msbt import parse_msbt_bytes             # noqa: E402
import totk_text                                       # noqa: E402
import patch_totk_rstb as rstb                         # noqa: E402

TITLE_ID = '0100F2C0115B6000'
ROMFS = os.path.join(r'E:\RomFS_Dump', TITLE_ID, 'romfs')
OURS = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TITLE_ID, 'romfs')


def load_dict():
    zd = oead.Sarc(zstd.ZstdDecompressor().decompress(
        open(os.path.join(ROMFS, 'Pack', 'ZsDic.pack.zs'), 'rb').read()))
    return zstd.ZstdCompressionDict(next(bytes(f.data) for f in zd.get_files() if f.name == 'zs.zsdic'))


def tags_of(s):
    return sorted(t for k, t in totk_text.split_parts(s) if k == 'tag')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--trt', required=True)
    ap.add_argument('--out', default=os.path.join(ROOT, 'output', 'TRT143'))
    args = ap.parse_args()

    dd = load_dict()
    dctx = zstd.ZstdDecompressor(dict_data=dd)

    base = oead.Sarc(dctx.decompress(open(os.path.join(ROMFS, 'Mals', 'USen.Product.142.sarc.zs'), 'rb').read()))
    trt = {f.name: bytes(f.data) for f in oead.Sarc(dctx.decompress(open(args.trt, 'rb').read())).get_files()}
    ours = {f.name: bytes(f.data) for f in oead.Sarc(
        dctx.decompress(open(os.path.join(OURS, 'Mals', 'USen.Product.142.sarc.zs'), 'rb').read())).get_files()}

    writer = oead.SarcWriter.from_sarc(base)
    stat = {'trt': 0, 'ours': 0, 'skip_tag': 0, 'en': 0, 'newfile': 0}

    for f in base.get_files():
        name = f.name
        if not name.endswith('.msbt'):
            continue
        en_entries = parse_msbt_bytes(bytes(f.data))
        trt_entries = parse_msbt_bytes(trt[name]) if name in trt else {}
        our_entries = parse_msbt_bytes(ours[name]) if name in ours else {}
        merged = {}
        for label, en_text in en_entries.items():
            t = trt_entries.get(label)
            if t is not None:
                if tags_of(t) == tags_of(en_text):
                    merged[label] = t
                    stat['trt'] += 1
                    continue
                stat['skip_tag'] += 1
            o = our_entries.get(label)
            if o:
                merged[label] = o
                stat['ours'] += 1
            else:
                merged[label] = en_text
                stat['en'] += 1
        writer.files[name] = oead.Bytes(replace_msbt_txt2(bytes(f.data), merged))

    if 'LayoutMsg/AppLoadingMessage_00.msbt' not in trt:
        print('  + file thiếu LayoutMsg/AppLoadingMessage_00.msbt: giữ bản 1.4.3 (của mình/EN)')

    sarc_bytes = writer.write()[1]
    params = zstd.ZstdCompressionParameters.from_level(15, window_log=23)
    comp = bytearray(zstd.ZstdCompressor(compression_params=params, dict_data=dd).compress(sarc_bytes))
    if comp[4] == 0x80:
        comp[4] = 0x81
        comp.insert(6, 0x01)

    out_romfs = os.path.join(args.out, 'atmosphere', 'contents', TITLE_ID, 'romfs')
    out_mals = os.path.join(out_romfs, 'Mals')
    out_font = os.path.join(out_romfs, 'Font')
    os.makedirs(out_mals, exist_ok=True)
    os.makedirs(out_font, exist_ok=True)
    open(os.path.join(out_mals, 'USen.Product.142.sarc.zs'), 'wb').write(bytes(comp))
    shutil.copy2(os.path.join(os.path.dirname(args.trt), '..', 'Font', 'Font.Nin_NX_NVN.bfarc.zs'),
                 os.path.join(out_font, 'Font.Nin_NX_NVN.bfarc.zs'))

    print('Nguồn chuỗi:', stat)
    print('Mals mới (giải nén):', len(sarc_bytes), '| đóng gói:', len(comp))
    print('Đã ghi:', args.out)
    rstb.write_rstb(out_romfs)


if __name__ == '__main__':
    main()
