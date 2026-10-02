# AGENTS.md — Quy tắc làm việc cho dự án "Translate Game" (Nintendo Switch)

Dự án bản địa hóa (Localization) game Nintendo Switch sang tiếng Việt.
AI là engine dịch ngữ cảnh cao cấp, tuân thủ nghiêm ngặt bộ quy tắc chống máy móc và chống mất ngữ cảnh từ "Translate Book".

---

## 0. CẤU TRÚC THƯ MỤC (bắt buộc tuân theo)

```
Translate Game/
├─ AGENTS.md  README.md
├─ docs/                  STATE.md (tiến độ), INSTALL-MOD.txt (hướng dẫn cài)
├─ glossary/              master.csv + <game>.csv
├─ input/                 prod.keys, titlekeys (KHÔNG commit)
├─ tools/                 toàn bộ script dùng chung
├─ games/                 dữ liệu từng game (KHÔNG commit — .gitignore chặn)
│   └─ <TitleID>_<Tên>/
│       ├─ source/        dữ liệu gốc bóc từ ROM (raw_text, extracted_json, font gốc…)
│       ├─ translations/  BẢN DỊCH TIẾNG VIỆT  ← sửa ở đây khi cần fix
│       └─ README.md      hướng dẫn riêng của game
└─ output/                SẢN PHẨM (mod LayeredFS) — copy vào thẻ nhớ, KHÔNG commit
    └─ atmosphere/contents/<TitleID>/romfs/...
```

- Game **mới** → tạo `games/<TitleID>_<Tên>/{source,translations}/` (mục 5).
- **Không** tạo lại `working/`, `translations/`, `scratch/`, `temp/` ở gốc.

---

## 1. Ngôn ngữ giao tiếp
- Trả lời bằng **tiếng Việt**.

---

## 2. 🧠 BỘ NHỚ PHIÊN & TRẠNG THÁI (Session Memory) — BẮT BUỘC
- **ĐẦU PHIÊN**:
  - Đọc `docs/STATE.md` — trạng thái game đang dịch, các file đã xong, việc đang làm, glossary đã thống nhất.
  - Đọc `docs/BAI-HOC.md` — **bài học kinh nghiệm & checklist bàn giao**. Bắt buộc: chạy
    `python tools/qa_text.py --game <ten_game>` và phải **PASS** trước khi báo xong.
- **CUỐI PHIÊN / KHI XONG MỘT GIAI ĐOẠN**:
  - Cập nhật `docs/STATE.md` (tiến độ từng môn thể thao, danh mục file).
  - Tự động chạy tool build mod kiểm tra tính toàn vẹn của file.

---

## 2.1. LỆNH ĐIỀU HÀNH TỰ ĐỘNG TOÀN DIỆN ĐA GAME: `/dich`
- Lệnh `/dich` là **Quy trình chuẩn hóa tự hành đa năng (Universal Engine-Agnostic Pipeline)** áp dụng cho **MỌI TỰA GAME NINTENDO SWITCH** (Nintendo EPD, Unity, Unreal Engine, Supergiant SJSON, Monogame, RPG Maker...):
  - **Tự động nhận diện Engine & Cấu trúc RomFS**: Tự bóc tách file text, tự phân loại font và logic đóng gói mod tương ứng.
  - **Tự động chạy hết quy trình khép kín (End-to-End Autonomous Loop)**: Rà soát file -> Dịch đa luồng (subagents) -> Vá font đồng bộ -> Đóng gói mod LayeredFS -> Chạy QA đối soát tag/control code -> Dọn dẹp file tạm.
  - **TUYỆT ĐỐI KHÔNG DỪNG LẠI HỎI "tiếp tục"**: Tự chủ động thực hiện liên tục không ngắt quãng cho đến khi toàn bộ gói mod hoàn tất 100% không lỗi.
  - Chi tiết quy chuẩn 5 giai đoạn: `.agents/skills/dich/SKILL.md`.

---

## 3. QUY TẮC BẢN DỊCH KHÔNG MÁY MÓC (Theo Translate Book)
1. **NGỮ CẢNH LÀ SỐ 1**:
   - Dịch theo ngữ cảnh game thủ Việt Nam, văn phong Nintendo vui tươi, sôi nổi, tự nhiên.
   - Tuyệt đối không dịch word-by-word (từng chữ một).
2. **GLOSSARY LÀ MỆNH LỆNH**:
   - Mọi bản dịch phải tuân thủ nghiêm ngặt theo `glossary/master.csv`.
   - Nếu phát hiện thuật ngữ mới, phải cập nhật vào `glossary/master.csv` trước khi áp dụng.
3. **BẢO TỒN NGUYÊN VẸN FORMAT / CONTROL CODES NINTENDO**:
   - Ký tự nút bấm Switch: `` (A), `` (B), `` (X), `` (Y), `` (ZR), `` (ZL), `` (Stick), `` (R), `` (L)...
   - Control tag đổi màu, căn dòng: `\u000e\u0000...`, `\n`, `%s`, `{0}`. Giữ nguyên 100%, không được làm đứt gãy thẻ.
4. **ĐỘ DÀI CHUỖI GIAO DIỆN (UI Length)**:
   - Các nút bấm, nhãn ngắn gọn, súc tích để tránh tràn khung (text overflow) trên màn hình Switch.

---

## 4. QUY TRÌNH PIPELINE TỰ ĐỘNG CHI TIẾT

### A. Dòng Game Nintendo First-Party (Nintendo Switch Sports...)
1. **Trích xuất (Extract)**:
   - Dump RomFS từ ROM `.nsp`/`.xci` bằng `tools/hactool` + `prod.keys`.
   - Giải nén gói ngôn ngữ `.sarc.zs` bằng `zstandard` và `oead`.
   - Trích xuất MSBT sang JSON bằng `tools/extract_msbt.py` vào `games/0100D2F00D5C0000_SwitchSports/source/raw_text_extracted/USen/`.
2. **Đối soát từ điển (Glossary Alignment)**:
   - Kiểm tra và đồng bộ từ khóa với `glossary/master.csv` trước khi dịch.
3. **Dịch thuật ngữ cảnh (Translate)**:
   - Dịch giữ nguyên mã phím Switch (``, ``...) và tag điều khiển (`\u000e...`).
   - Kiểm soát độ dài ký tự tránh tràn khung UI.
   - Lưu kết quả vào `games/<TitleID>_<Tên>/translations/`.
4. **Xử lý Font chữ (Font Patching)**:
   - Tạo bộ font hỗ trợ đầy đủ tiếng Việt bằng `tools/build_custom_font.py`.
   - Đóng gói font thành 4 file `.bfarc.zs` chuẩn Nintendo vào `output/atmosphere/contents/<TitleID>/romfs/Font/`.
5. **Đóng gói Mod LayeredFS (Pack Mod)**:
   - Chạy `python tools/build_mod.py` để inject text vào MSBT -> đóng gói SARC -> nén ZSTD `.zs`.
   - Xuất file hoàn chỉnh vào `output/atmosphere/contents/<TitleID>/romfs/Mals/`.

### B. Dòng Game Supergiant Games (Hades II...)
1. **Trích xuất & Cấu trúc Text**:
   - Định dạng văn bản SJSON (`Game/Text/en/*.en.sjson`).
   - Xử lý mảng `Texts = [ { Id = "...", DisplayName = "..." } ]` bằng `tools/hades2_sjson_helper.py`.
2. **Xử lý Font chữ XNB Version 6/7 (SpriteFont Patching)**:
   - Chạy `python tools/patch_hades2_xnb_font.py`.
   - **Quy chuẩn bắt buộc**:
     - Đồng bộ hóa 100% toàn bộ glyphs tiếng Việt (ghi đè cả ký tự 1 dấu có sẵn lẫn ký tự 2 dấu/dấu nặng) để triệt tiêu hiện tượng lệch font.
     - Khóa chuẩn Horizontal Bearing (`Crop.X = ch_bb[0] - base_bb[0]`) để tránh dính/chèn chữ.
     - Khóa chuẩn Stem Baseline (`Crop.Y = base_orig_bottom - (base_bb[3] - ch_bb[1])`) giữ thẳng hàng tăm tắp với chữ Latin.
3. **Đóng gói Mod LayeredFS & Quản lý HUD**:
   - Chạy `python tools/build_hades2_mod.py`.
   - Khối In-Game UI / HUD (`UI_PlayerHealth`, `UI_ManaText`, `HUD_TraitCount`...) trong `HelpText.en.sjson` luôn ưu tiên đặt ở đầu file để engine nạp ngay tức thì.
4. **Kiểm tra chất lượng tự động (QA Audit)**:
   - Chạy `python tools/qa_hades2_mod.py` và `python tools/check_special_characters.py`.
   - Đảm bảo 100% bảo tồn thẻ (`{$Keywords...}`, `{!Icons...}`, `{#...}`), không dịch biến, không lỗi escape sequence (`\"`, `\n`).

---

## 5. QUẢN LÝ DUNG LƯỢNG & ĐỒNG BỘ ONEDRIVE
- Không lưu file ROM gốc (`.nsp`, `.xci`) trực tiếp trong thư mục OneDrive để tránh phình dung lượng.
- Tự động dọn dẹp file tạm (`scratch_*`, `__pycache__`, `temp_*`, ảnh thử nghiệm) sau mỗi giai đoạn kiểm thử.
- Chỉ lưu giữ tài nguyên cần thiết: script (`tools/`), cấu hình, từ điển (`glossary/`),
  dữ liệu gốc bóc tách + bản dịch (`games/<TitleID>_<Tên>/{source,translations}`) và thành phẩm (`output/`).
- Khi làm game mới, tạo `games/<TitleID>_<Tên>/{source,translations}/` để quản lý độc lập.
