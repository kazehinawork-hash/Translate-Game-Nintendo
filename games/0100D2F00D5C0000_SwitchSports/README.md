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
python tools/patch_font_switchsports_native.py   # → Font/Font.Nin_NX_NVN.bfarc.zs (font GỐC + tiêm glyph tiếng Việt)
python tools/build_mod.py                        # → Mals/USen.Product.150.sarc.zs (text đã dịch)
```

## Kiểm tra

- `python tools/qa_switchsports.py` — độ phủ glyph (font gốc vs mod) + soát bản dịch.
- `python tools/final_check_switchsports.py` — kiểm tra toàn vẹn font/text/đường dẫn.
- `python tools/sws_fix_zs.py` — xác nhận tham số frame Zstd khớp bản gốc.

## Lưu ý

- ⚠️ **KHÔNG dùng `tools/build_custom_font.py`** (thay font bằng TTF Nunito → mất 96% glyph, game báo
  *"Unable to start software"*). Font tiếng Việt phải **giữ nguyên 4 font VDL gốc (OTTO/CFF, CID-keyed,
  số glyph không đổi)** rồi **tiêm glyph vào các slot CFF còn trống** — xem **BH-47** trong `docs/BAI-HOC.md`.
- Chỉ ghi đè **font Latin** (`Font/Font.Nin_NX_NVN.bfarc.zs`); **không** tạo `Font_CNzh/KRko/TWzh` (font khu vực giữ nguyên).
- File SARC phải nén lại đúng chuẩn **ZSTD Nintendo** (`.zs`, `windowLog=21` khớp gốc — BH-27).
- Tên file đích trong mod phải khớp tuyệt đối: `Font/Font.Nin_NX_NVN.bfarc.zs`,
  `Font/Font_CNzh.Nin_NX_NVN.bfarc.zs`, `Font/Font_KRko.Nin_NX_NVN.bfarc.zs`,
  `Font/Font_TWzh.Nin_NX_NVN.bfarc.zs`, `Mals/USen.Product.150.sarc.zs`.
