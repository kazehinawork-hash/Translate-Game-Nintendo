"""
patch_font_obf.py — Vá font tiếng Việt cho Ori and the Blind Forest (BitmapFont / atlas SDF).

Cách làm (an toàn, không đổi kích thước atlas):
  1. Bản dịch cần N ký tự mà font `candara` chưa có (74 chữ Việt + '…').
  2. Chọn các glyph "nhường chỗ": ký tự nằm trong font nhưng BẢN DỊCH KHÔNG DÙNG
     (Latin-1 mở rộng: ä ë ö ü ï î û å ø æ ç ñ Ä Ë Ö Ü ... ) — giữ nguyên mọi thông số khác.
  3. Vẽ glyph tiếng Việt (từ Lato, cỡ em=110 như đo từ atlas) vào ĐÚNG ô của glyph nhường chỗ,
     làm mềm nhẹ cho giống dạng SDF.
  4. Ghi lại **mã ký tự** trong entry 48 byte: từ ký tự cũ -> ký tự tiếng Việt.
  -> Không phải mở rộng atlas, không phải dịch chuyển toạ độ của 448 entry cũ.

Dùng: python tools/patch_font_obf.py [--dry]
"""
import argparse
import json
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import numpy as np  # noqa: E402
from PIL import Image, ImageDraw, ImageFilter, ImageFont  # noqa: E402
from unity_bitmapfont import find_fonts, parse_glyphs, rect_px  # noqa: E402

W = r'E:\OBF_work'
BUNDLE = os.path.join(W, 'data.unity3d')
G = os.path.join(ROOT, 'games', '010061D00DB74000_OriAndTheBlindForest')
OUT = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '010061D00DB74000', 'romfs', 'Data')
TTF = os.path.join(ROOT, 'tools', 'fonts_hades2', 'Lato-Bold.ttf')
EM = 110


def render(ch):
    f = ImageFont.truetype(TTF, EM)
    img = Image.new('L', (EM * 2, EM * 2), 0)
    ImageDraw.Draw(img).text((EM * 0.5, EM * 0.5), ch, fill=255, font=f)
    a = np.array(img)
    ys, xs = np.nonzero(a > 8)
    if not len(xs):
        return None
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--font', default='candara')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()

    rows = json.load(open(os.path.join(G, 'translations', 'obf_vi.json'), encoding='utf-8'))
    needed = set()
    for r in rows:
        needed |= {ord(c) for c in r['VI']}
    print(f'bản dịch dùng {len(needed)} ký tự (kể cả ASCII)')

    fonts, env = find_fonts(BUNDLE)
    fobj = next((p, r) for p, n, r in fonts if n == a.font)
    pid, raw = fobj
    glyphs, blocks = parse_glyphs(raw)
    print(f'font {a.font!r}: {len(glyphs)} glyph, block {blocks}')

    A = None
    texobj = None
    for o in env.objects:
        if o.type.name == 'Texture2D':
            d = o.read()
            if str(getattr(d, 'm_Name', '')) == f'{a.font}_0 distance map':
                A = np.array(d.image)[:, :, 3].copy()
                texobj = (o, d)
                break
    H, Wd = A.shape
    print(f'atlas {Wd}x{H}')

    missing = sorted(c for c in needed if c not in glyphs and c > 127)
    print(f'ký tự cần thêm: {len(missing)} -> {"".join(chr(c) for c in missing)}')

    # glyph nhường chỗ: mọi ký tự font CÓ mà bản dịch KHÔNG dùng (Latin-1 mở rộng, Cyrillic,
    # Greek...) — tránh ASCII để không ảnh hưởng giao diện tiếng Anh.
    donors = [c for c in glyphs
              if c > 0x7F and c not in needed and chr(c).isalpha()]
    donors.sort(key=lambda c: (rect_px(glyphs[c], Wd, H)[1] - rect_px(glyphs[c], Wd, H)[0]) *
                              (rect_px(glyphs[c], Wd, H)[3] - rect_px(glyphs[c], Wd, H)[2]))
    print(f'glyph nhường chỗ khả dụng: {len(donors)} (>= {len(missing)}? {len(donors) >= len(missing)})')

    used_donors = set()
    changes = {}
    for ch in missing:
        g = render(chr(ch))
        if g is None:
            print(f'   ! không render được {chr(ch)!r}')
            continue
        gh, gw = g.shape
        want_upper = chr(ch).isupper()
        picked = None
        for c in donors:
            if c in used_donors:
                continue
            if chr(c).isupper() != want_upper:
                continue
            xa, xb, ya, yb = rect_px(glyphs[c], Wd, H)
            cw, chh = xb - xa, yb - ya
            if cw >= gw * 0.75 and chh >= gh * 0.75:
                picked = c
                break
        if picked is None:
            print(f'   ! hết chỗ cho {chr(ch)!r} (cần {gw}x{gh})')
            continue
        used_donors.add(picked)
        xa, xb, ya, yb = rect_px(glyphs[picked], Wd, H)
        cw, chh = xb - xa, yb - ya
        sc = min(cw / gw, chh / gh, 1.0)
        nw, nh = max(1, int(gw * sc)), max(1, int(gh * sc))
        gi = Image.fromarray(g).resize((nw, nh), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.6))
        patch = np.zeros((chh, cw), dtype=np.uint8)
        ox, oy = (cw - nw) // 2, (chh - nh) // 2
        patch[oy:oy + nh, ox:ox + nw] = np.array(gi)
        A[ya:yb, xa:xb] = patch
        changes[picked] = ch
        print(f'   {chr(ch)!r} (U+{ch:04X}) <- ô của {chr(picked)!r} (U+{picked:04X}) rect {cw}x{chh}')

    print(f'\nđã vẽ {len(changes)}/{len(missing)} glyph')
    if a.dry:
        return 0

    # ghi lại mã ký tự trong bảng glyph
    n_edit = 0
    new_raw = bytearray(raw)
    for base, cnt in blocks:
        for k in range(cnt):
            off = base + 4 + k * 48
            c = int.from_bytes(new_raw[off:off + 4], 'little')
            if c in changes:
                new_raw[off:off + 4] = int(changes[c]).to_bytes(4, 'little')
                n_edit += 1
    print(f'đã đổi mã ký tự cho {n_edit} entry')

    # ghi lại texture
    o, d = texobj
    img = d.image.convert('RGBA')
    arr = np.array(img)
    arr[:, :, 3] = A
    d.image = Image.fromarray(arr)
    d.save()
    print('đã cập nhật atlas texture')

    # ---- vá TEXT (bản dịch) trong cùng lượt, tránh ghi đè lẫn nhau ----
    from unity_text_tool import parse_message, _blob, _align4
    data = json.load(open(os.path.join(G, 'source', 'obf_text_all.json'), encoding='utf-8'))
    vi_by_en = {r['EN']: r['VI'] for r in rows}
    want = {str(dd['path_id']): vi_by_en.get(dd['english'], dd['english']) for dd in data}
    n_text = 0
    for o in env.objects:
        if o.type.name != 'MonoBehaviour':
            continue
        k = str(o.path_id)
        if k not in want:
            continue
        r2 = o.get_raw_data()
        m = parse_message(r2)
        if not m:
            continue
        _nm, off, ln, _en = m
        old = _align4(4 + ln)
        o.set_raw_data(r2[:off] + _blob(want[k]) + r2[off + old:])
        n_text += 1
    print(f'đã vá {n_text}/{len(want)} object text')

    # ghi lại font raw
    fo = next(x for x in env.objects if x.type.name == 'MonoBehaviour' and x.path_id == pid)
    fo.set_raw_data(bytes(new_raw))
    print('đã cập nhật bảng glyph')

    # lưu bundle ra output
    os.makedirs(OUT, exist_ok=True)
    env.save(pack='original', out_path=OUT)
    p = os.path.join(OUT, 'data.unity3d')
    print(f'đã lưu bundle: {p} ({os.path.getsize(p):,} bytes)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
