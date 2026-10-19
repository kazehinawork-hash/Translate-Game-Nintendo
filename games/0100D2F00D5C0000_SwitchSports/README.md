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
python tools/patch_sws_rstb.py                   # → System/Resource/ResourceSizeTable.Product.150.rsizetable.zs (BẮT BUỘC)
```

> ⚠️ **Sau MỖI lần build text/font phải chạy `patch_sws_rstb.py`** — bảng size ghi kích thước giải nén của
> từng resource; thay file mà không vá bảng ⇒ engine cấp phát thiếu ⇒ treo/crash (BH-49).
> Game này `.zs` **KHÔNG dùng từ điển** (khác TotK), và bảng size cũng nén thuần (frame `28 b5 2f fd a0 …`).

## Kiểm tra

- `python tools/qa_text.py --game switchsports` — cổng QA chuẩn (PASS).
- `python tools/qa_switchsports.py` — độ phủ glyph (font gốc vs mod) + soát bản dịch.
- `python tools/final_check_switchsports.py` — kiểm tra toàn vẹn font/text/đường dẫn.
- `python tools/fix_sws_escapes.py [--apply]` — chuẩn hoá **thẻ điều khiển** (thêm byte `\x00`/`\uffff` bị thiếu)
  và **thêm lại dấu ngắt dòng** theo bản gốc. Chạy khi dump RomFS mới để rà lệch với nguồn.
- `python tools/sws_fix_zs.py` — xác nhận tham số frame Zstd khớp bản gốc.

## Đối chiếu với RomFS gốc (khi user dump bản mới)

```bash
# so cấu trúc + nhãn: 250/250 file, 24.597 nhãn, 0 thiếu/0 rỗng
python tools/qa_text.py --game switchsports
```

- Cảnh báo `CONTROL_CODE_LECH` ở `PlayerTitle_gen_{EUde,EUfr,EUru,USes,…}` là **bình thường**: nguồn là bảng
  tên riêng theo ngôn ngữ, còn bản dịch dùng chung một bảng tiếng Việt. File tiếng Anh (`USen`, `EUen`) đã đúng.

## Lưu ý

- ⚠️ **KHÔNG dùng `tools/build_custom_font.py`** (thay font bằng TTF Nunito → mất 96% glyph, game báo
  *"Unable to start software"*). Font tiếng Việt phải **giữ nguyên 4 font VDL gốc (OTTO/CFF, CID-keyed,
  số glyph không đổi)** rồi **tiêm glyph vào các slot CFF còn trống** — xem **BH-47** trong `docs/BAI-HOC.md`.
- Chỉ ghi đè **font Latin** (`Font/Font.Nin_NX_NVN.bfarc.zs`); **không** tạo `Font_CNzh/KRko/TWzh` (font khu vực giữ nguyên).
- File SARC phải nén lại đúng chuẩn **ZSTD Nintendo** (`.zs`, `windowLog=21` khớp gốc — BH-27).
- Tên file đích trong mod phải khớp tuyệt đối: `Font/Font.Nin_NX_NVN.bfarc.zs`,
  `Font/Font_CNzh.Nin_NX_NVN.bfarc.zs`, `Font/Font_KRko.Nin_NX_NVN.bfarc.zs`,
  `Font/Font_TWzh.Nin_NX_NVN.bfarc.zs`, `Mals/USen.Product.150.sarc.zs`,
  **`System/Resource/ResourceSizeTable.Product.150.rsizetable.zs`** (bảng kích thước — chép thiếu là treo/crash).
- Mod hiện gồm **3 thư mục**: `Mals/` + `Font/` + `System/`. Ngôn ngữ trong game phải để **English**.
