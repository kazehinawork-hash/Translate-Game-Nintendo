# Nintendo Switch Sports (Switch) — `0100D2F00D5C0000`

- **Engine**: Nintendo EPD (first-party)
- **Định dạng text**: MSBT trong `Mals/*.sarc.zs` (nén ZSTD); font `Font/*.bfarc.zs`
- **Sản phẩm**: `output/atmosphere/contents/0100D2F00D5C0000/`

## Sửa bản dịch ở đâu

- Bản dịch tiếng Việt: `translations/*.msbt.json` (mỗi file ứng với 1 file MSBT gốc)
- Khoá gốc bóc tách: `source/raw_text_extracted/`
- Gói gốc: `source/orig_mals/` (SARC gốc) — font gốc: `source/orig_font/`

## Build lại (chạy từ gốc dự án)

```bash
python tools/build_custom_font.py      # → 4 file Font/*.bfarc.zs (font tiếng Việt)
python tools/build_mod.py              # → Mals/USen.Product.150.sarc.zs (text đã dịch)
```

## Kiểm tra

- Soát lại chuỗi nút bấm Switch và control code trong các file `translations/*.msbt.json`
  (script QA riêng của game chưa tách riêng — dùng `tools/audit_translation_style.py`).

## Lưu ý

- Font tiếng Việt dùng **Nunito Black/Bold** (`tools/Nunito-*.ttf`) — chuẩn typography thể thao Nintendo.
- File SARC phải nén lại đúng chuẩn **ZSTD Nintendo** (`.zs`).
- Tên file đích trong mod phải khớp tuyệt đối: `Font/Font.Nin_NX_NVN.bfarc.zs`,
  `Font/Font_CNzh.Nin_NX_NVN.bfarc.zs`, `Font/Font_KRko.Nin_NX_NVN.bfarc.zs`,
  `Font/Font_TWzh.Nin_NX_NVN.bfarc.zs`, `Mals/USen.Product.150.sarc.zs`.
