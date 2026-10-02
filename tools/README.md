# BẢN ĐỒ CÔNG CỤ (`tools/`)

> Chạy mọi script **từ gốc dự án**. Quy trình đầy đủ: xem `docs/BAI-HOC.md`.
> **Cổng QA bắt buộc trước khi bàn giao:** `python tools/qa_text.py --game <game>` → phải PASS.

## 🚀 Chạy trọn quy trình (nên dùng cái này)

| Việc | Lệnh |
|---|---|
| Build + QA 1 game | `python tools/pipeline.py hogwarts` (hoặc `ori`, `hades2`, `switchsports`) |
| Cả 4 game | `python tools/pipeline.py all` |
| Xem các bước | `python tools/pipeline.py <game> --list` |
| Chỉ chạy 1 bước | `python tools/pipeline.py <game> --only qa` |
| Cổng QA | `python tools/qa_text.py --game <game> [--font <ttf>] [--leak] [--verbose]` |
| Từ điển + nhất quán | `python tools/check_glossary.py --game <game> [--strict] [--suggest 20]` |
| Báo cáo toàn dự án | `python tools/report.py` (hoặc `--md`, `--no-qa`) |

Pipeline **dừng ngay** nếu một bước lỗi và **không chạy QA** — chống lỗi "build dở rồi tưởng xong".

## 🧩 Công cụ dùng chung

| File | Việc |
|---|---|
| `qa_text.py` | **Cổng QA**: đọc lại thành phẩm, so nguồn — key, rỗng, ký tự lạ, tag/placeholder, `[error:]`/`[KEY]`, `\n`, font, soát rò rỉ |
| `check_font_coverage.py` | Font có phủ 100% ký tự dùng trong mod không |
| `check_special_characters.py` | Bắt `/n` gõ nhầm, `{}` lệch, CJK/Hangul/Kana/Ả Rập |
| `merge_vi_font.py` | Thêm dấu tiếng Việt vào font gốc **mà giữ nguyên glyph icon (PUA)** |
| `find_rom.py` | Tìm ROM theo TitleID trong `input/` và `E:\ROM_Backup` |
| `archive_rom.py` | **Chuyển ROM ra khỏi OneDrive** sau khi bóc xong (copy → xác minh SHA256 → xoá) — xem BH-16 |
| `audit_translation_style.py` | Soi văn phong/độ dài bản dịch |

## 🎮 Theo engine

| Engine / game | File | Việc |
|---|---|---|
| **Unreal** (Hogwarts) | `ue_romfs_tool.py` | Liệt kê/trích file RomFS từ NSP (không cần hactool) |
| | `avaf_codec.py` | Codec AVAFDICT 2.0 (**magic UTF-16LE!**) |
| | `parse_avaf.py`, `get_exact_bin_offsets.py`, `read_all_bins_accurate.py` | Đọc từ điển gốc |
| | `export_main_dict.py`, `export_dialog_dict.py` | Bóc text → JSON nguồn |
| | `build_hogwarts_mod.py` / `build_hogwarts_sub.py` / `build_patch_pak.py` | Build MAIN / SUB / patch pak |
| | `fix_hogwarts_main_errors.py` | Vá `[error:...]`/`[KEY]` bằng key anh em |
| | `fix_hogwarts_fr_names.py` | Sửa tên bị Pháp hóa (đối chiếu cột FR vs ES) |
| **Unity** (Ori) | `unity_text_tool.py` | Bóc & vá text bundle (`parse_message` linh hoạt, không hardcode magic) |
| | `build_ori_mod.py`, `patch_font_ori.py` | Build bundle / vá font TTF động (thay hẳn + hợp nhất giữ icon) |
| | `unity_bitmapfont.py` | **Giải mã BitmapFont (Ori and the Blind Forest)**: bảng glyph 48B + atlas SDF + cắt glyph ra ảnh kiểm chứng |
| | `patch_font_obf.py` | **Vá font Blind Forest**: sinh glyph tiếng Việt vào ô glyph không dùng + đổi mã ký tự, vá text cùng lượt |
| | `extract_il2cpp.py` | Bóc `main` (ExeFS) + `global-metadata.dat` để dựng typetree IL2CPP |
| **Supergiant** (Hades II) | `hades2_sjson_helper.py` | Đọc/ghi SJSON |
| | `build_hades2_mod.py`, `patch_hades2_xnb_font.py` | Build mod / vá SpriteFont XNB |
| | `harmonize_hades2_terms.py`, `qa_hades2_mod.py` | Đồng bộ thuật ngữ / QA riêng |
| | `fix_hades2_qa_bugs.py` | Vá lỗi ngoặc `}` thừa + chữ Trung lọt |
| | `extract_lootdata.py` | Bóc dữ liệu LootData |
| **Nintendo EPD** (Switch Sports) | `extract_msbt.py` | MSBT ⇄ JSON (UTF-16LE, LBL1/ATR1/TXT2, SARC) |
| | `build_mod.py`, `build_custom_font.py` | Build SARC.zs / font BFARC |

## 🗄️ `tools/legacy/` — script MỘT LẦN (đã chạy xong, không cần chạy lại)

40 script `translate_*.py`, `trans_part*.py`, `apply_*.py`… — chúng chứa **bản dịch đã sinh ra file nguồn**.
Muốn sửa câu chữ thì sửa **file bản dịch trong `games/<TID>/translations/`**, KHÔNG sửa các file này.
Còn `build_font.py` cũng nằm đây vì đường dẫn của nó đã hỏng (dùng `build_custom_font.py` thay thế).
