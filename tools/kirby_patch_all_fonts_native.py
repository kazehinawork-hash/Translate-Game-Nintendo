"""Kirby and the Forgotten Land: Vá TRIỆT ĐỂ toàn bộ 45 font ScalableFontBin.

- Với 11 font .bfotf: Giữ NGUYÊN cấu trúc CID-Keyed ('Adobe', 'Japan1', 3)
  + Thêm 97 glyph tiếng Việt vào các unused CID slots (từ font vi_only.ttf)
  + Gán PrivateDict chuẩn của FDArray[0]
  + Mã hóa XOR khớp magic 0x36F81A1E
  + Nén zstandard khớp định dạng .cmp

- Với 34 font .bfttf (gồm K15-LocalCharacter-M và các bộ CHI, KOR, TWN):
  + Giữ NGUYÊN cấu trúc TrueType (glyf/hmtx)
  + Thêm glyphs tiếng Việt duỗi phẳng qua DecomposingRecordingPen + TTGlyphPen
  + Cập nhật bảng glyf, hmtx, maxp và cmap Unicode
  + Mã hóa XOR khớp magic 0x36F81A1E
  + Nén zstandard khớp định dạng .cmp

Chạy: python tools/kirby_patch_all_fonts_native.py
"""
import io
import os
import struct
import sys
import zstandard
from fontTools.ttLib import TTFont
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '01004D300C5AE000'
SRC_DIR = os.path.join(ROOT, 'games', f'{TID}_Kirby', 'source', 'font', 'ScalableFontBin')
OUT_DIR = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'font', 'ScalableFontBin')
os.makedirs(OUT_DIR, exist_ok=True)

VI_FONT_PATH = os.path.join(ROOT, 'games', '_consistency', 'vi_only.ttf')
f_vi = TTFont(VI_FONT_PATH)
gs_vi = f_vi.getGlyphSet()
cm_vi = f_vi.getBestCmap()
upem_vi = f_vi['head'].unitsPerEm
print(f'Da nap vi_only.ttf: {len(cm_vi)} ky tu, upem={upem_vi}')

MAGIC_KIRBY = 0x36F81A1E
compressor = zstandard.ZstdCompressor(level=15)
decompressor = zstandard.ZstdDecompressor()


BASE_ASCII_MAP = {
    'A': 'A', 'Á': 'A', 'À': 'A', 'Ả': 'A', 'Ã': 'A', 'Ạ': 'A',
    'Ă': 'A', 'Ắ': 'A', 'Ằ': 'A', 'Ẳ': 'A', 'Ẵ': 'A', 'Ặ': 'A',
    'Â': 'A', 'Ấ': 'A', 'Ầ': 'A', 'Ẩ': 'A', 'Ẫ': 'A', 'Ậ': 'A',
    'a': 'a', 'á': 'a', 'à': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
    'ă': 'a', 'ắ': 'a', 'ằ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
    'â': 'a', 'ấ': 'a', 'ầ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
    'E': 'E', 'É': 'E', 'È': 'E', 'Ẻ': 'E', 'Ẽ': 'E', 'Ẹ': 'E',
    'Ê': 'E', 'Ế': 'E', 'Ề': 'E', 'Ể': 'E', 'Ễ': 'E', 'Ệ': 'E',
    'e': 'e', 'é': 'e', 'è': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
    'ê': 'e', 'ế': 'e', 'ề': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
    'I': 'I', 'Í': 'I', 'Ì': 'I', 'Ỉ': 'I', 'Ĩ': 'I', 'Ị': 'I',
    'i': 'i', 'í': 'i', 'ì': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
    'O': 'O', 'Ó': 'O', 'Ò': 'O', 'Ỏ': 'O', 'Õ': 'O', 'Ọ': 'O',
    'Ô': 'O', 'Ố': 'O', 'Ồ': 'O', 'Ổ': 'O', 'Ỗ': 'O', 'Ộ': 'O',
    'Ơ': 'O', 'Ớ': 'O', 'Ờ': 'O', 'Ở': 'O', 'Ỡ': 'O', 'Ợ': 'O',
    'o': 'o', 'ó': 'o', 'ò': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
    'ô': 'o', 'ố': 'o', 'ồ': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
    'ơ': 'o', 'ớ': 'o', 'ờ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
    'U': 'U', 'Ú': 'U', 'Ù': 'U', 'Ủ': 'U', 'Ũ': 'U', 'Ụ': 'U',
    'Ư': 'U', 'Ứ': 'U', 'Ừ': 'U', 'Ử': 'U', 'Ữ': 'U', 'Ự': 'U',
    'u': 'u', 'ú': 'u', 'ù': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
    'ư': 'u', 'ứ': 'u', 'ừ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
    'Y': 'Y', 'Ý': 'Y', 'Ỳ': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y', 'Ỵ': 'Y',
    'y': 'y', 'ý': 'y', 'ỳ': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
    'Đ': 'D', 'đ': 'd'
}


def patch_bfotf(fn):
    base = fn[:-10]
    otf_path = os.path.join(ROOT, 'games', f'{TID}_Kirby', 'font_edit', f'{base}.otf')
    if not os.path.exists(otf_path):
        return
    p_src = os.path.join(SRC_DIR, fn)
    raw = open(p_src, 'rb').read()
    d = decompressor.decompress(raw[4:])
    w8, = struct.unpack_from('>I', d, 8)
    key = w8 ^ 0x4F54544F  # OTTO
    body = b''.join(struct.pack('>I', struct.unpack_from('>I', d, i)[0] ^ key)
                    for i in range(8, len(d), 4))
    assert body[:4] == b'OTTO', f'{fn} fail decipher OTTO'

    f = TTFont(io.BytesIO(body))
    cm_src = f.getBestCmap()
    top = f['CFF '].cff.topDictIndex[0]
    cs = top.CharStrings
    priv = top.FDArray[0].Private
    hmtx_src = f['hmtx'].metrics

    # 1. Tận dụng Eth (0x00D0) có sẵn nét tuyệt đẹp của chính font để gán cho Đ (0x0110)
    if 0x00D0 in cm_src:
        cid_eth = cm_src[0x00D0]
        for sub in f['cmap'].tables:
            if sub.isUnicode():
                sub.cmap[0x0110] = cid_eth

    f_edit = TTFont(otf_path)
    cm_edit = f_edit.getBestCmap()
    gs_edit = f_edit.getGlyphSet()
    hmtx_edit = f_edit['hmtx'].metrics

    used_cids = set(f.getBestCmap().values())
    unused = [cid for cid in cs.keys() if cid not in used_cids and cid != '.notdef']

    added_codes = [c for c in sorted(cm_edit) if c not in f.getBestCmap() and c <= 0xFFFF]
    for idx, code in enumerate(added_codes):
        cid = unused[idx]
        gn = cm_edit[code]
        w_vi, lsb_vi = hmtx_edit[gn]
        ch = chr(code)
        base_ch = BASE_ASCII_MAP.get(ch)
        if base_ch and ord(base_ch) in cm_src:
            base_cid = cm_src[ord(base_ch)]
            target_w, _ = hmtx_src[base_cid]
            shift_x = (target_w - w_vi) / 2.0
        else:
            target_w = w_vi
            shift_x = 0.0

        pen = T2CharStringPen(target_w, cs)
        if abs(shift_x) > 0.1:
            gs_edit[gn].draw(TransformPen(pen, (1, 0, 0, 1, shift_x, 0)))
        else:
            gs_edit[gn].draw(pen)

        t2cs = pen.getCharString()
        t2cs.private = priv
        cs[cid] = t2cs
        f['hmtx'].metrics[cid] = (int(target_w), int(lsb_vi + shift_x))
        for sub in f['cmap'].tables:
            if sub.isUnicode():
                sub.cmap[code] = cid

    buf = io.BytesIO()
    f.save(buf)
    new_otf = buf.getvalue()

    pad_len = (4 - (len(new_otf) % 4)) % 4
    if pad_len:
        new_otf += b'\x00' * pad_len
    enc_words = [struct.pack('>I', struct.unpack_from('>I', new_otf, i)[0] ^ key)
                 for i in range(0, len(new_otf), 4)]
    hdr = struct.pack('>II', MAGIC_KIRBY, len(new_otf) ^ key)
    enc_data = hdr + b''.join(enc_words)
    cmp_data = len(enc_data).to_bytes(4, 'little') + compressor.compress(enc_data)

    p_out = os.path.join(OUT_DIR, fn)
    with open(p_out, 'wb') as out_f:
        out_f.write(cmp_data)
    print(f'  [+] {fn:<36} -> Added {len(added_codes):>2} CID glyphs (balanced metrics) -> {len(cmp_data):,} bytes')


def patch_bfttf(fn):
    p_src = os.path.join(SRC_DIR, fn)
    raw = open(p_src, 'rb').read()
    d = decompressor.decompress(raw[4:])
    w8, = struct.unpack_from('>I', d, 8)
    key = w8 ^ 0x00010000  # TTF
    body = b''.join(struct.pack('>I', struct.unpack_from('>I', d, i)[0] ^ key)
                    for i in range(8, len(d), 4))
    assert body[:4] == b'\x00\x01\x00\x00', f'{fn} fail decipher TTF'

    f = TTFont(io.BytesIO(body))
    upem_target = f['head'].unitsPerEm
    scale = upem_target / upem_vi

    cm = f.getBestCmap()
    glyf = f['glyf']
    hmtx = f['hmtx']
    order = list(f.getGlyphOrder())

    # Map Eth (0x00D0) -> Đ (0x0110) nếu có sẵn
    if 0x00D0 in cm:
        eth_gname = cm[0x00D0]
        for sub in f['cmap'].tables:
            if sub.isUnicode():
                sub.cmap[0x0110] = eth_gname

    added = 0
    for code, gname in sorted(cm_vi.items()):
        if code in f.getBestCmap():
            continue
        new_gname = f'uni{code:04X}'
        orig_w = gs_vi[gname].width * scale
        ch = chr(code)
        base_ch = BASE_ASCII_MAP.get(ch)
        if base_ch and ord(base_ch) in cm:
            base_gn = cm[ord(base_ch)]
            target_w = hmtx[base_gn][0]
            shift_x = (target_w - orig_w) / 2.0
        else:
            target_w = int(orig_w)
            shift_x = 0.0

        rec = DecomposingRecordingPen(gs_vi)
        gs_vi[gname].draw(TransformPen(rec, (scale, 0, 0, scale, shift_x, 0)))
        pen = TTGlyphPen(None)
        rec.replay(pen)
        g = pen.glyph()
        glyf[new_gname] = g
        hmtx[new_gname] = (int(target_w), int(shift_x))
        for sub in f['cmap'].tables:
            if sub.isUnicode():
                sub.cmap[code] = new_gname
        order.append(new_gname)
        added += 1

    glyf.glyphOrder = order
    f.setGlyphOrder(order)
    f['maxp'].numGlyphs = len(order)

    buf = io.BytesIO()
    f.save(buf)
    new_ttf = buf.getvalue()

    pad_len = (4 - (len(new_ttf) % 4)) % 4
    if pad_len:
        new_ttf += b'\x00' * pad_len
    enc_words = [struct.pack('>I', struct.unpack_from('>I', new_ttf, i)[0] ^ key)
                 for i in range(0, len(new_ttf), 4)]
    hdr = struct.pack('>II', MAGIC_KIRBY, len(new_ttf) ^ key)
    enc_data = hdr + b''.join(enc_words)
    cmp_data = len(enc_data).to_bytes(4, 'little') + compressor.compress(enc_data)

    p_out = os.path.join(OUT_DIR, fn)
    with open(p_out, 'wb') as out_f:
        out_f.write(cmp_data)
    print(f'  [+] {fn:<36} -> Added {added:>2} TTF glyphs (balanced metrics) -> {len(cmp_data):,} bytes')


print('=== BAT DAU VA 11 FONT BFOTF (CID-KEYED) ===')
for fn in sorted(os.listdir(SRC_DIR)):
    if fn.endswith('.bfotf.cmp'):
        patch_bfotf(fn)

print('\n=== BAT DAU VA 34 FONT BFTTF (TRUETYPE) ===')
for fn in sorted(os.listdir(SRC_DIR)):
    if fn.endswith('.bfttf.cmp'):
        patch_bfttf(fn)

print('\nHoan tat vá toan bo 45 font ScalableFontBin cho Kirby!')
