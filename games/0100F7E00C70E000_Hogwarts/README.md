# Hogwarts Legacy (Switch) — `0100F7E00C70E000`

- **Engine**: Unreal Engine 4.27 (Avalanche)
- **Định dạng text**: AVAFDICT 2.0 (`MAIN-*.bin` UI, `SUB-*.bin` hội thoại)
- **Sản phẩm**: `output/atmosphere/contents/0100F7E00C70E000/`

## Sửa bản dịch ở đâu

| Phần | File cần sửa | Ghi chú |
|---|---|---|
| Giao diện / menu / HUD | `translations/translated_*.json` | Mỗi phần tử `{"Key": …, "Vietnamese": …}` |
| Hội thoại | `translations/sub_trans/sub_*.json` | Mỗi phần tử `{"Id": …, "VI": …}`; `Id` trỏ vào `source/extracted_json/dialogs_fr_unique.json` |

Khoá gốc để tra cứu: `source/extracted_json/hogwarts_main_raw.json` (17.737 key UI),
`source/raw_text/sub_dump/SUB-koKR.bin` (35.431 hội thoại, nguồn tiếng Pháp).

## Build lại (chạy từ gốc dự án)

```bash
python tools/build_hogwarts_mod.py     # → MAIN-*.bin (UI)
python tools/build_hogwarts_sub.py     # → SUB-*.bin (hội thoại)
python tools/build_patch_pak.py        # → pakchunk0-Switch_p.pak (14 ngôn ngữ)
```

## Kiểm tra

```bash
python tools/check_font_coverage.py tools/fonts_hades2/Lato-Regular.ttf \
  output/atmosphere/contents/0100F7E00C70E000/romfs/Phoenix/Content/Localization/SWITCH/MAIN-enUS.bin \
  output/atmosphere/contents/0100F7E00C70E000/romfs/Phoenix/Content/Localization/SWITCH/SUB-enUS.bin
```

## Lưu ý kỹ thuật (đã từng dính lỗi — đừng lặp lại)

1. **Magic AVAFDICT phải là UTF-16LE** (`41 00 56 00 …`). Ghi ASCII → game hiện toàn bộ `[KEY]`.
   Luôn tự kiểm: `pack_avafdict(unpack_avafdict(file_gốc)) == file_gốc`.
2. Text nằm **trong `pakchunk0-Switch.pak`** (UFS) → file `.bin` đặt rời trong `romfs/` **không được đọc**;
   phải đóng gói **patch pak** `pakchunk0-Switch_p.pak`.
3. Game có **14 ngôn ngữ** — patch pak đã phủ hết nên console để ngôn ngữ nào cũng ra tiếng Việt.
4. Font: thay file rời `Engine/Content/SlateDebug/Fonts/LastResort.ttf` (font dự phòng của UE).
