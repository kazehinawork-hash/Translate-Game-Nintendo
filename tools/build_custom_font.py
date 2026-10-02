"""
Script tạo font tiếng Việt mang phong cách thể thao, bo tròn (Rounded Bold)
giống 99% font gốc VDL-LogoG của Nintendo Switch Sports.
Sử dụng Nunito ExtraBold / Black (chuẩn typography thể thao Nintendo).
"""
import os
import sys
import struct
import shutil
import zstandard
import oead

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

TITLE_ID = "0100D2F00D5C0000"
GAME_TAG = "0100D2F00D5C0000_SwitchSports"
BASE_FONT_SARC = f"games/{GAME_TAG}/source/orig_font/Font.Nin_NX_NVN.bfarc.zs"
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

def build_custom_font_mod():
    print(">>> Bắt đầu tạo bản mod Font bo tròn thể thao giống font gốc...")
    with open(BASE_FONT_SARC, 'rb') as f:
        decompressed_sarc = zstandard.ZstdDecompressor().decompress(f.read())

    sarc = oead.Sarc(decompressed_sarc)
    sarc_writer = oead.SarcWriter.from_sarc(sarc)

    font_bold_path = "tools/Nunito-Bold.ttf"
    font_ultra_path = "tools/Nunito-Black.ttf"

    with open(font_bold_path, 'rb') as f:
        bold_ttf = f.read()
    with open(font_ultra_path, 'rb') as f:
        ultra_ttf = f.read()

    enc_bold = encrypt_bfttf(bold_ttf)
    enc_ultra = encrypt_bfttf(ultra_ttf)

    # Thay thế CHỈ các font LATIN của game (dùng cho tiếng Anh/Việt).
    # ⚠️ KHÔNG được thay 3 font chữ Hán/Hàn/Nhật (DFP_GBZY7_CNzh, DFPT_ZY5_TWzh,
    #    AsiaKTITGD4-R_KRko): mod chỉ dịch khe tiếng Anh, giữ nguyên 3 font khu vực đó
    #    để người chơi để tiếng Trung/Hàn/Nhật vẫn hiển thị đúng.
    target_fonts = {
        'scft/VDL-LOGOG-BOLD.bfotf': enc_bold,
        'scft/VDL-LOGOG-ULTRA.bfotf': enc_ultra,
        'scft/VDL-GigaJr-ExtraBold-003_Gaiji.bfotf': enc_bold,
        'scft/VDL-GigaJr-Ultra-003_Gaiji.bfotf': enc_ultra,
    }

    for font_name, enc_data in target_fonts.items():
        if font_name in sarc_writer.files:
            sarc_writer.files[font_name] = oead.Bytes(enc_data)
            print(f" [+] Đã cập nhật font phong cách Nintendo: {font_name}")

    print(">>> Đóng gói SARC font...")
    new_sarc_bytes = sarc_writer.write()[1]

    print(">>> Nén Zstandard (.zs)...")
    cctx = zstandard.ZstdCompressor(level=16)
    compressed_sarc = cctx.compress(new_sarc_bytes)

    os.makedirs(OUTPUT_FONT_DIR, exist_ok=True)
    with open(OUTPUT_FONT_FILE, 'wb') as f:
        f.write(compressed_sarc)

    # Dọn 3 file font khu vực (CNzh/KRko/TWzh) khỏi mod nếu có — KHÔNG ghi đè chúng.
    for extra in ['Font_CNzh.Nin_NX_NVN.bfarc.zs', 'Font_KRko.Nin_NX_NVN.bfarc.zs', 'Font_TWzh.Nin_NX_NVN.bfarc.zs']:
        p = os.path.join(OUTPUT_FONT_DIR, extra)
        if os.path.exists(p):
            os.remove(p)
            print(f" [-] Đã xoá khỏi mod (giữ nguyên font gốc của game): {extra}")

    print(f"\n✅ ĐÃ TẠO XONG FONT TIẾNG VIỆT PHONG CÁCH NINTENDO!")
    print(f"👉 File kết quả: {OUTPUT_FONT_FILE}")

if __name__ == '__main__':
    build_custom_font_mod()
