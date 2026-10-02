"""
Script đóng gói Mod Atmosphere LayeredFS cho Hades II (Nintendo Switch).
Tự động xuất các file bản dịch và cấu hình font vào output/atmosphere/contents/0100A00019DE0000/romfs/
"""
import os
import sys
import shutil

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

TITLE_ID = "0100A00019DE0000"
# LƯU Ý: đường dẫn phải theo CẤU TRÚC MỚI (games/<TID>_<Tên>/translations).
# Trước đây script dùng "translations/<TID>_Hades2" (cấu trúc cũ) nên đã hỏng sau khi tái cấu trúc.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSLATIONS_DIR = os.path.join(ROOT, "games", f"{TITLE_ID}_Hades2", "translations")
OUTPUT_DIR = os.path.join(ROOT, "output", "atmosphere", "contents", TITLE_ID, "romfs")

def build_mod():
    print(">>> Bắt đầu đóng gói bản mod Hades II sang LayeredFS...")
    
    if not os.path.exists(TRANSLATIONS_DIR):
        print(f"Lỗi: Không tìm thấy thư mục bản dịch: {TRANSLATIONS_DIR}")
        return

    # Quét toàn bộ file trong translations/
    count = 0
    for root, dirs, files in os.walk(TRANSLATIONS_DIR):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, TRANSLATIONS_DIR)
            dst_path = os.path.join(OUTPUT_DIR, rel_path)

            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)
            count += 1
            print(f" [+] Đã đóng gói: {rel_path}")

    print(f"\n✅ ĐÃ HOÀN TẤT ĐÓNG GÓI MOD HADES II! ({count} file)")
    print(f"👉 Thư mục mod sẵn sàng: output/atmosphere/contents/{TITLE_ID}/")

if __name__ == '__main__':
    build_mod()
