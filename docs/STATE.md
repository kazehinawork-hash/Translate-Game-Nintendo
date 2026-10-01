# Trạng thái dự án bản địa hóa Game Nintendo Switch

## 1. Hogwarts Legacy (Nintendo Switch)
- **Title ID**: `0100F7E00C70E000` (Base) / `0100F7E00C70E800` (Update v1.0.5)
- **Engine**: Unreal Engine 4.27 (Custom Avalanche Software Build)
- **Định dạng Text**: AVAFDICT 2.0 (`MAIN-*.bin`, `SUB-*.bin`)
- **Tiến độ dịch thuật & Đóng gói Mod**:
  - Đã trích xuất hoàn chỉnh 17.737 entries giao diện (MAIN) và 35.431 dialogues hội thoại (SUB).
  - **MAIN (UI/Menu/HUD): HOÀN THÀNH 100% — 17.737/17.737 chuỗi tiếng Việt.**
    - Dịch từ nguồn tiếng Trung (`Source_ZH`), chia 29 chunk × 400 chuỗi và dịch song song bằng subagent.
    - QA: 0 ký tự Hán sót, 0 sai lệch placeholder/tag, 0 chuỗi rỗng; 681 chuỗi giữ nguyên là các nhãn hợp lệ (độ phân giải `1280x720`, `120 FPS`, tên phím `Enter/Tab`, `[error:...]`).
  - **SUB (hội thoại): HOÀN THÀNH 100% — 35.431/35.431 chuỗi tiếng Việt.**
    - Kho SUB gốc bóc lại từ NSP bằng `nsz` + Oodle (9 từ điển ngôn ngữ) → dùng bản tiếng Pháp (`SUB-koKR.bin`, 35.431 entries) làm nguồn dịch (NSP base không có tiếng Anh).
    - Gộp trùng còn **26.296 chuỗi duy nhất**, chia 53 chunk × 500 (một số chunk tách nhỏ 250 khi quá dài) và dịch song song bằng subagent.
    - QA: keys khớp 100%, 0 sai lệch placeholder/tag (`<i>`, `\n`, `[[ ]]`...), 0 chuỗi rỗng; 77 chuỗi giữ nguyên là thán từ (`Hmm.`, `Argh…`), tên bùa trong tag (`<i>Nox</i>.`) và tên người.
    - Truy vết nguồn: `working/0100F7E00C70E000_Hogwarts/extracted_json/hogwarts_dialogs_fr.json`, `dialogs_fr_unique.json`; bản dịch ở `working/.../split_tasks/sub_trans/sub_*.json`.
    - Đã chuẩn hóa nốt tên Pháp hóa còn sót (đối chiếu chéo bằng cột tiếng Tây Ban Nha song song): `Cheek→Deek` (234), `Pallow→Sallow` (28), `Bôbalais→Spintwitches` (12), `Campolard-en-Haut/Bas→Upper/Lower Hogsfield` (5).
  - **Kiểm toán tổng hợp cuối (MAIN + SUB):** keys khớp 100%, **0** ký tự lạ (CJK/Hàn/Nhật/Ả Rập), **0** sai lệch placeholder/tag, **0** chuỗi rỗng, **0** tên Pháp hóa sót. Font đã cài phủ **223/223** ký tự dùng trong mod.
  - **Font chữ (Giai đoạn 3): ĐÃ VÁ (font dự phòng).**
    - Cấu trúc RomFS: text/font nằm trong pak IoStore (`Phoenix/Content/Paks/pakchunk*-Switch.pak/.ucas/.utoc`), **không** có file rời.
    - File font rời duy nhất là `Engine/Content/SlateDebug/Fonts/LastResort.ttf` — chính là font UE dùng dự phòng khi thiếu glyph (đúng trường hợp dấu tiếng Việt).
    - Đã thay bằng **Lato Regular** (phủ đủ 224 ký tự dùng trong bản dịch, gồm toàn bộ dấu tiếng Việt) tại:
      `output/atmosphere/contents/0100F7E00C70E000/romfs/Engine/Content/SlateDebug/Fonts/LastResort.ttf`
    - Font gốc lưu tại `working/0100F7E00C70E000_Hogwarts/romfs_dump/LastResort.ttf` (backup).
  - ✅ **ĐÃ XỬ LÝ việc engine bỏ qua file rời:** kiểm tra `Manifest_NonUFSFiles_Switch.txt` xác nhận
    `Phoenix/Content/Localization/SWITCH/*.bin` là **UFS (nằm trong pakchunk0-Switch.pak)**, không phải file rời
    → file `.bin` đặt rời bị engine bỏ qua (đã test thực tế: không lên tiếng Việt).
  - **Giải pháp: patch pak UE4** — `Phoenix/Content/Paks/pakchunk0-Switch_p.pak` (33,8 MB), chứa bản dịch cho
    **cả 14 ngôn ngữ** của game (arAE deDE enUS esES esMX frFR itIT jaJP koKR plPL ptBR ruRU zhCN zhTW).
    Build bằng `tools/build_patch_pak.py` (dùng thư viện `repak`, pak version V11, mount point `../../../`).
  - 🐞 **BUG CHÍ MẠNG ĐÃ SỬA (nguyên nhân gốc):** file AVAFDICT của game dùng magic **UTF-16LE**
    (`41 00 56 00 41 00…`, 32 byte), nhưng `tools/avaf_codec.py` ghi magic **ASCII** (`41 56 41 46…`).
    Game không đọc được từ điển → hiển thị toàn bộ chuỗi dạng `[KEY]` (đã thấy trong game).
    Đã sửa codec; kiểm chứng: `pack_avafdict(unpack_avafdict(file_gốc)) == file_gốc` → **True**.
    (Trước khi sửa luôn False → mọi bản mod trước đây đều vô hiệu vì lý do này.)
  - Công cụ hỗ trợ: `tools/ue_romfs_tool.py` (liệt kê/trích file RomFS), đọc mục lục pak bằng `repak` (xem Phụ lục A của skill `/dich`).
  - Mod LayeredFS hiện tại:
    `output/atmosphere/contents/0100F7E00C70E000/romfs/`
    - `Phoenix/Content/Paks/pakchunk0-Switch_p.pak` (33,8 MB) — **phần chính, chứa text bản dịch**.
    - `Phoenix/Content/Localization/SWITCH/` — 5 `MAIN-*.bin` + 5 `SUB-*.bin` (giữ cho đầy đủ).
    - `Engine/Content/SlateDebug/Fonts/LastResort.ttf` — font tiếng Việt (file rời, LayeredFS ăn).

---

## 2. Hades II (Nintendo Switch)
- **Title ID**: `0100A00019DE0000`
- **Trạng thái**: Hoàn thành 100%, SpriteFont XNB sắc nét, mod hoàn chỉnh tại `output/atmosphere/contents/0100A00019DE0000/`.

---

## 3. Nintendo Switch Sports
- **Title ID**: `0100D2F00D5C0000`
- **Trạng thái**: Hoàn thành 100% (7 môn thể thao + font BCFNT). Mod tại `output/atmosphere/contents/0100D2F00D5C0000/`.

---

## 4. Hạ tầng repo & đóng gói
- **Git**: đã khởi tạo (`git init`) + commit đầu; `.gitignore` ẩn khoá (`prod.keys`, `titlekeys.txt`), ROM, cache và dữ liệu nặng.
- **Gói phát hành**: dùng trực tiếp thư mục `output/atmosphere/` — chép nguyên thư mục này vào gốc thẻ nhớ Switch (gộp vào `atmosphere` có sẵn). Gồm cả 3 mod: `0100F7E00C70E000`, `0100A00019DE0000`, `0100D2F00D5C0000`. Hướng dẫn cài: `docs/INSTALL-MOD.txt`.
- **Dọn dẹp**: 35 file rác thư mục gốc đã nén vào `scratch/archive_root_scrap.zip` và xoá khỏi gốc; đã xoá toàn bộ `__pycache__`.
- **Ghi chú**: giữ nguyên `working/` (~330 MB) theo yêu cầu.
