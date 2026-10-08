"""Nen lai (chuan hoa frame zstd) cac file .zs trong mod Switch Sports theo tham so GOC."""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import zstandard
from zs_util import compress_like, frame_params

G = os.path.join(ROOT, 'games', '0100D2F00D5C0000_SwitchSports')
OUT = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '0100D2F00D5C0000')

PAIRS = [('orig_mals/USen.Product.150.sarc.zs', 'Mals/USen.Product.150.sarc.zs'),
         ('orig_font/Font.Nin_NX_NVN.bfarc.zs', 'Font/Font.Nin_NX_NVN.bfarc.zs')]

for rel_g, rel_o in PAIRS:
    pg = os.path.join(G, 'source', *rel_g.split('/'))
    po = os.path.join(OUT, 'romfs', *rel_o.split('/'))
    bg = open(pg, 'rb').read()
    bo = open(po, 'rb').read()
    raw = zstandard.ZstdDecompressor().decompress(bo)      # noi dung da sua
    pg_p, po_p = frame_params(bg), frame_params(bo)
    print(f'\n{rel_o}')
    print(f'  frame goc: windowLog={pg_p["window_log"]} checksum={pg_p["checksum"]}')
    print(f'  frame mod: windowLog={po_p["window_log"]} checksum={po_p["checksum"]}')
    new = compress_like(bg, raw)
    p = frame_params(new)
    print(f'  frame moi: windowLog={p["window_log"]} checksum={p["checksum"]} | {len(bo):,} -> {len(new):,} b')
    # kiem chung: giai nen lai phai ra dung noi dung
    assert zstandard.ZstdDecompressor().decompress(new) == raw, 'giai nen lai KHONG khop!'
    open(po, 'wb').write(new)
    print(f'  [ok] da ghi lai {po}')
    print(f'       12 byte dau moi: {new[:12].hex(" ")}  (goc: {bg[:12].hex(" ")})')
