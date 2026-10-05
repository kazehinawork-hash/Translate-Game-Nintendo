"""Soat loi mod Switch Sports: (a) glyph bi mat, (b) ban dich (thieu file, lech key, lech the)."""
import io
import json
import os
import re
import struct
import sys
import zstandard
import oead
from fontTools.ttLib import TTFont

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
GAME = os.path.join(ROOT, 'games', '0100D2F00D5C0000_SwitchSports')
ORIG = os.path.join(GAME, 'source', 'orig_font', 'Font.Nin_NX_NVN.bfarc.zs')
MOD = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '0100D2F00D5C0000', 'romfs', 'Font', 'Font.Nin_NX_NVN.bfarc.zs')
K = 2785117442


def decrypt(d):
    out = bytearray()
    for i in range(8, len(d), 4):
        w, = struct.unpack_from('>I', d, i)
        out += struct.pack('>I', w ^ K)
    return bytes(out)


def cmap_of(sarc_path, name):
    s = oead.Sarc(zstandard.ZstdDecompressor().decompress(open(sarc_path, 'rb').read()))
    for f in s.get_files():
        if f.name == name:
            t = TTFont(io.BytesIO(decrypt(f.data)), lazy=True)
            return set(t.getBestCmap())
    return set()


print('=== (a) GLYPH BI MAT khi thay font ===')
a = cmap_of(ORIG, 'scft/VDL-LOGOG-BOLD.bfotf')
b = cmap_of(MOD, 'scft/VDL-LOGOG-BOLD.bfotf')
lost = sorted(a - b)
print(f'  goc {len(a):,} glyph | mod {len(b):,} | MAT {len(lost):,}')
ranges = [(0x20, 0x7E, 'ASCII'), (0xA0, 0x24F, 'Latin-1/Extended'),
          (0x300, 0x36F, 'dau kết hợp'), (0x1E00, 0x1EFF, 'Latin Extended Additional'),
          (0x2000, 0x206F, 'punctuation'), (0x2190, 0x21FF, 'mui tên'),
          (0x2460, 0x24FF, 'so trong vong'), (0x25A0, 0x25FF, 'hình khối'),
          (0x3000, 0x303F, 'CJK punct'), (0xFF00, 0xFFEF, 'FULLWIDTH/HALFWIDTH'),
          (0xE000, 0xF8FF, 'PUA icon')]
for lo, hi, nm in ranges:
    l = [c for c in lost if lo <= c <= hi]
    g = [c for c in a if lo <= c <= hi]
    if g:
        print(f'    {nm:<26} goc {len(g):>5} | mat {len(l):>5}')
vi_need = 'àáâãèéêìíòóôõùúýăđĩũơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ'
vi_set = {ord(c) for c in vi_need}
print(f'  ky tu tieng Viet can: {len(vi_set)} | goc co: {len(vi_set & a)} | mod thieu: {len(vi_set - b)}')

print('\n=== (b) BAN DICH ===')
src_dir = os.path.join(GAME, 'source', 'raw_text_extracted', 'USen')
tr_dir = os.path.join(GAME, 'translations')
srcs = {f for f in os.listdir(src_dir) if f.endswith('.json')}
trs = {f for f in os.listdir(tr_dir) if f.endswith('.json')}
print(f'  file goc {len(srcs)} | file dich {len(trs)}')
miss = sorted(srcs - trs)
print(f'  THIEU BAN DICH: {len(miss)} {miss}')
TAG = re.compile(r'\\u000e[0-9a-fA-F]{0,2}|<[^<>]{1,20}>')
bad_key = bad_tag = empty = extra = 0
for f in sorted(srcs & trs):
    s = json.load(open(os.path.join(src_dir, f), encoding='utf-8'))
    t = json.load(open(os.path.join(tr_dir, f), encoding='utf-8'))
    if set(s) != set(t):
        bad_key += 1
        if bad_key <= 3:
            print(f'    LECH KEY {f}: thieu {list(set(s)-set(t))[:3]} | thua {list(set(t)-set(s))[:3]}')
    for k in set(s) & set(t):
        if not t[k].strip():
            empty += 1
        if sorted(TAG.findall(s[k])) != sorted(TAG.findall(t[k])):
            bad_tag += 1
            if bad_tag <= 5:
                print(f'    LECH THE [{f}] {k}\n      goc={s[k][:70]!r}\n      dich={t[k][:70]!r}')
print(f'  lech key: {bad_key} | lech the/control: {bad_tag} | rong: {empty}')
