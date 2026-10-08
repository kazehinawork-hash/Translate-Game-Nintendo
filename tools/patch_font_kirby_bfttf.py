"""Va NOT cac bo font .bfttf cua Kirby (CHI-/KOR-/TWN- + K15-LocalCharacter).

11 font .bfotf (CFF) da va o buoc truoc. Nhung game con dung cac bo .bfttf (glyf):
  CHI-*.bfttf.cmp (upem 1024), KOR-*.bfttf.cmp (upem 1000), TWN-*.bfttf.cmp (upem 1024),
  K15-LocalCharacter-M.bfttf.cmp (upem 1024)
Mod cu KHONG co cac file nay -> game roi vao font thieu dau -> O VUONG.

Cach va: HOP NHAT (merge) font goc + glyph tieng Viet cua Arial Unicode,
giu nguyen toan bo glyph goc va dung upem cua font goc (merge_vn_font lo viec scale).
"""
import io
import json
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import zstandard
from fontTools.ttLib import TTFont
from merge_vi_font import merge_vn_font
from add_glyphs_glyf import add_glyphs_glyf
from zs_util import compress_like

TID = '01004D300C5AE000'
G = os.path.join(ROOT, 'games', f'{TID}_Kirby')
SRC = os.path.join(G, 'source', 'font', 'ScalableFontBin')
OUT = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'font', 'ScalableFontBin')
SUPPLY = r'C:\Windows\Fonts\ARIALUNI.TTF'
MAGIC = 0x36F81A1E
CAND = (0x4F54544F, 0x00010000, 0x74746366)


def decomp(b):
    return zstandard.ZstdDecompressor().decompress(b[4:], max_output_size=128 << 20)


def unwrap(data):
    if struct.unpack_from('>I', data, 0)[0] != MAGIC:
        return None, None
    w8, = struct.unpack_from('>I', data, 8)
    for expect in CAND:
        key = w8 ^ expect
        body = b''.join(struct.pack('>I', struct.unpack_from('>I', data, i)[0] ^ key)
                        for i in range(8, len(data), 4))
        if body[:4] != struct.pack('>I', expect):
            continue
        try:
            TTFont(io.BytesIO(body), lazy=True).getBestCmap()
            return body, key
        except Exception:
            continue
    return None, None


def wrap(font, key, true_len):
    t = font if len(font) % 4 == 0 else font + b'\x00' * (4 - len(font) % 4)
    words = [MAGIC, true_len ^ key]
    for i in range(0, len(t), 4):
        words.append(struct.unpack_from('>I', t, i)[0] ^ key)
    return struct.pack(f'>{len(words)}I', *words)


def vi_codepoints():
    vi = json.load(open(os.path.join(G, 'translations', 'kirby_vi.json'), encoding='utf-8'))
    used = set()
    for ents in vi.values():
        for v in ents.values():
            used |= set(str(v))
    # bo cac ky tu nam trong THAM SO ma dieu khien (\x0e... + payload) va ma dieu khien
    from extract_msbt import parse_msbt_bytes  # noqa: F401
    import re
    ctrl = re.compile(r'\x0e[\s\S]{0,3}[\s\S]{0,2}')
    out = set()
    for ents in vi.values():
        for v in ents.values():
            clean = ctrl.sub('', str(v))
            out |= {ord(c) for c in clean if c.isprintable() and ord(c) >= 0x20}
    return out


def main():
    need = sorted(vi_codepoints())
    print(f'ky tu tieng Viet can co: {len(need)}')
    # Dung THANG Arial Unicode lam font nguon: add_glyphs_glyf chi ve cac glyph can thiet
    # nen khong cham. (Cat gon font nguon lam fontTools DOI TEN glyph -> loi KeyError
    # khi duoi glyph ghep, vd KeyError: 'Ohorn'.)
    SMALL = SUPPLY

    files = [f for f in sorted(os.listdir(SRC)) if f.endswith('.bfttf.cmp')]
    print(f'co {len(files)} file .bfttf.cmp can va\n')
    os.makedirs(OUT, exist_ok=True)

    ok = fail = 0
    for fn in files:
        ob = open(os.path.join(SRC, fn), 'rb').read()
        frame = ob[4:]
        raw = zstandard.ZstdDecompressor().decompress(frame, max_output_size=128 << 20)
        font, key = unwrap(raw)
        if not font:
            print(f'  [!] {fn[:40]}: khong giai ma duoc'); fail += 1; continue
        f0 = TTFont(io.BytesIO(font))
        cg = set(f0.getBestCmap())
        upem0 = f0['head'].unitsPerEm
        fmt0 = 'CFF' if 'CFF ' in f0 else 'glyf'
        try:
            new = add_glyphs_glyf(font, SMALL, need)
        except Exception as e:
            if ok == 0 and fail == 0:
                import traceback
                print(f'  [!!] {fn}: {type(e).__name__}: {e}')
                traceback.print_exc()
            else:
                print(f'  [!!] {fn[:40]}: loi {type(e).__name__}: {str(e)[:50]}')
            fail += 1
            continue
        try:
            fm = TTFont(io.BytesIO(new))
            cm = set(fm.getBestCmap())
        except Exception as e:
            print(f'  [!!] {fn[:40]}: font moi khong doc duoc'); fail += 1; continue
        lost = [c for c in cg if c not in cm]
        # bo qua cac ky tu chi la THAM SO ma dieu khien (>= 0x3000, vd U+4DFF cua \x0e\x00\x03\x04)
        miss = [c for c in need if c not in cm and c < 0x3000]
        if lost or miss:
            print(f'  [!!] {fn[:40]}: mat {len(lost)} glyph goc, thieu {len(miss)} ky tu VI -> BO QUA')
            fail += 1
            continue
        blob = wrap(new, key, len(new))
        new_frame = compress_like(frame, blob)
        out = struct.pack('<I', len(blob)) + new_frame
        open(os.path.join(OUT, fn), 'wb').write(out)
        ok += 1
        print(f'  [+] {fn[:40]:<42} {fmt0} upem {upem0} | cmap {len(cg):,}->{len(cm):,} | '
              f'mat 0 | {len(ob):,}->{len(out):,} b')

    print(f'\n{ok} font .bfttf da va | loi/bo qua: {fail}')


if __name__ == '__main__':
    raise SystemExit(main())
