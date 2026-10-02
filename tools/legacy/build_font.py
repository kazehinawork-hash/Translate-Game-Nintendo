"""
Patch toàn bộ các font hiển thị trong Nintendo Switch Sports
- Thay thế tất cả các font render chính và font gaiji (VDL-LOGOG-BOLD, VDL-LOGOG-ULTRA, VDL-GigaJr...)
  bằng font đầy đủ ký tự tiếng Việt.
- Giữ lại nintendo_ext_003 để hiển thị các nút điều khiển Joy-Con.
"""
import os
import sys
import struct
import zstandard
import oead

TITLE_ID = "0100D2F00D5C0000"
BASE_FONT_SARC = "games/0100D2F00D5C0000_SwitchSports/source/orig_font/Font/Font.Nin_NX_NVN.bfarc.zs"
OUTPUT_FONT_DIR = f"output/atmosphere/contents/{TITLE_ID}/romfs/Font"
OUTPUT_FONT_FILE = f"{OUTPUT_FONT_DIR}/Font.Nin_NX_NVN.bfarc.zs"

def encrypt_bfttf(data: bytes) -> bytes:
    k = 2785117442
    header_magic = 0xD99B871A
    file_size = len(data)
    rem = len(data) % 4
    if rem != 0:
        data = data + b'\x00' * (4 - rem)
    out_words = [header_magic, file_size ^ k]
    for i in range(0, len(data), 4):
        w, = struct.unpack_from('>I', data, i)
        out_words.append(w ^ k)
    return struct.pack(f'>{len(out_words)}I', *out_words)

def build_font_mod():
    print(">>> Bắt đầu tạo bản mod Font tiếng Việt toàn diện...")
    with open(BASE_FONT_SARC, 'rb') as f:
        decompressed_sarc = zstandard.ZstdDecompressor().decompress(f.read())

    sarc = oead.Sarc(decompressed_sarc)
    sarc_writer = oead.SarcWriter.from_sarc(sarc)

    arial_bold_path = "C:/Windows/Fonts/arialbd.ttf"
    with open(arial_bold_path, 'rb') as f:
        bold_ttf = f.read()

    enc_bold = encrypt_bfttf(bold_ttf)

    # Thay thế TOÀN BỘ các font chữ mà bfcpx gọi tới
    target_fonts = [
        'scft/VDL-LOGOG-BOLD.bfotf',
        'scft/VDL-LOGOG-ULTRA.bfotf',
        'scft/VDL-GigaJr-ExtraBold-003_Gaiji.bfotf',
        'scft/VDL-GigaJr-Ultra-003_Gaiji.bfotf',
        'scft/DFP_GBZY7_CNzh.bfttf',
        'scft/DFPT_ZY5_TWzh.bfttf',
        'scft/AsiaKTITGD4-R_KRko.bfttf'
    ]

    for font_name in target_fonts:
        if font_name in sarc_writer.files:
            sarc_writer.files[font_name] = oead.Bytes(enc_bold)
            print(f" [+] Đã thay thế font: {font_name}")

    print(">>> Đóng gói SARC font...")
    new_sarc_bytes = sarc_writer.write()[1]

    print(">>> Nén Zstandard (.zs)...")
    cctx = zstandard.ZstdCompressor(level=16)
    compressed_sarc = cctx.compress(new_sarc_bytes)

    os.makedirs(OUTPUT_FONT_DIR, exist_ok=True)
    with open(OUTPUT_FONT_FILE, 'wb') as f:
        f.write(compressed_sarc)

    print(f"\n✅ ĐÃ HOÀN TẤT FONT TIẾNG VIỆT TOÀN DIỆN!")
    print(f"👉 File kết quả: {OUTPUT_FONT_FILE}")

if __name__ == '__main__':
    build_font_mod()
