# Kirby and the Forgotten Land (Switch) — `01004D300C5AE000`

- **Engine**: Nintendo/HAL (engine "basil") — first-party, định dạng **MSBT** + **BFFNT/BFOTF**
- **Sản phẩm**: `output/atmosphere/contents/01004D300C5AE000/` (380 file, 18,2 MB)

## Cấu trúc RomFS

| Thư mục | Nội dung |
|---|---|
| `msg/Kirby15/<LANG>/*.msbt` | **kho text** — 13 ngôn ngữ × 42 file MSBT (+ `Kirby15.msbp`) |
| `font/ScalableFontBin/*.bfotf.cmp` | **11 font Latin** (VDL-LogoG, VDL-GigaMaru, FOT-Rodin…, NINP-VDL-LineG) |
| `font/ScalableFontBin/{CHI,KOR,TWN}-*` | font khu vực Hán/Hàn (giữ nguyên) |
| `basil/*.bin`, `fgd/Archive.dat`, `gfx/`, `snd/`, `lyt/`, `yaml/` | dữ liệu game |

## Định dạng (đã giải mã)

```
.cmp     = [u32 uncompressed_size][zstd frame]            (magic zstd 28 b5 2f fd)
.bfotf   = [u32 magic 0x36F81A1E][u32 ?][từng word 4 byte ^ key]  -> OTF/TTF
```

## Đã làm

| Bước | Kết quả |
|---|---|
| Bóc kho text | 547 file `msg/` (13 ngôn ngữ) → `source/msg/Kirby15/` |
| Dịch | **2.508 chuỗi** (41 file MSBT) sang tiếng Việt — 10 chunk, 5+2 subagent |
| QA bản dịch | PASS — 0 lệch key, 0 mã điều khiển sai, 0 chuỗi rỗng, 0 ký tự lạ |
| Vá font | 11 font Latin → thêm tiếng Việt (giữ glyph gốc), **đọc lại OK** |
| Đóng gói | 369 file MSBT ở **9 khe ngôn ngữ Latin** (giữ nguyên JP/CN/TW/KR) |
| Kiểm chứng | **15.975/15.975 chuỗi khớp** trên thành phẩm |

## Cách chơi

Copy `atmosphere/` vào thẻ nhớ, để **ngôn ngữ máy = một ngôn ngữ Latin** (English/Pháp/Đức/Ý/Tây Ban Nha/Hà Lan).
Các khe Nhật/Trung/Hàn **giữ nguyên** để người chơi khu vực đó không bị lỗi font.

## Build lại

```bash
python tools/kirby_extract.py        # bóc chuỗi từ source/msg/... -> translations/kirby_en.json
python tools/kirby_chunk.py          # chia chunk   (đã dịch: vi_01..vi_10.json)
python tools/qa_kirby.py             # QA + gộp -> translations/kirby_vi.json
python tools/build_kirby_mod.py      # đóng gói 369 MSBT -> output/.../romfs/msg/
python tools/patch_font_kirby.py     # vá 11 font -> output/.../romfs/font/ScalableFontBin/
python tools/final_check_kirby.py    # kiểm chứng thành phẩm (phải PASS)
```

Sửa bản dịch: `games/01004D300C5AE000_Kirby/translations/vi_XX.json` (hoặc `kirby_vi.json`) rồi chạy lại
`qa_kirby.py` → `build_kirby_mod.py`.

## Lưu ý kỹ thuật (bài học)

1. **`.bfotf` Kirby dùng magic `0x36F81A1E`** (Switch Sports là `0xD99B871A`) — khoá XOR **khác nhau từng file**.
2. ⚠️ **Không dò khoá bằng cách so 4 byte đầu** — kiểu đó *luôn* tự tạo ra "OTTO" (vòng tròn), phải
   **thử parse font** mới biết khoá đúng (xem BH-21).
3. MSBT coi `\0` cuối chuỗi là ký tự kết thúc → **không để bản dịch kết thúc bằng thẻ chứa `\0`**
   (4 chuỗi đã bị hụt 1 byte, đã sửa bằng cách thêm khoảng trắng sau thẻ).
4. Font gốc là **OTF (CFF)** → `fontTools.merge.Merger` không hợp CFF với TTF; cách chạy được là
   **thay bằng subset của Arial Unicode MS** (giữ cmap gốc ∪ ký tự dùng trong bản dịch) như BH-20.
