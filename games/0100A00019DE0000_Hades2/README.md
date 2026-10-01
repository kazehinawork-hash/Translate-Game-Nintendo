# Hades II (Switch) — `0100A00019DE0000`

- **Engine**: Supergiant (MonoGame)
- **Định dạng text**: SJSON (`Game/Text/en/*.en.sjson`)
- **Sản phẩm**: `output/atmosphere/contents/0100A00019DE0000/`

## Sửa bản dịch ở đâu

- Bản dịch tiếng Việt: `translations/Game/Text/en/*.en.sjson`
  (mỗi entry `Texts = [ { Id = "…", DisplayName = "…" } ]`)
- Khoá gốc tiếng Anh: `source/raw_text/en/*.sjson`
- Font gốc + script lặt vặt: `source/orig_font/`, `source/orig_scripts/`
- File lẻ trong `_misc/`: script/dữ liệu phụ trợ của quá trình dịch (không bắt buộc).

## Build lại (chạy từ gốc dự án)

```bash
python tools/build_hades2_mod.py        # đóng gói mod LayeredFS
python tools/patch_hades2_xnb_font.py   # vá font SpriteFont XNB (chuẩn V7)
```

## Kiểm tra

```bash
python tools/qa_hades2_mod.py
```
Script này đối soát: file SJSON parse OK, multiset thẻ `{…}` khớp nguồn,
`translations/` đồng bộ với `output/`, font XNB đủ glyph tiếng Việt, tỷ lệ DN đã dịch.

## Lưu ý

- HUD/UI runtime đọc tuần tự → khối HUD (`UI_PlayerHealth`, `HUD_TraitCount`…) phải đặt **đầu file** `HelpText.en.sjson`.
- Font XNB: ghi đè **toàn bộ** glyph tiếng Việt (kể cả chữ 1 dấu) để không bị lệch font.
