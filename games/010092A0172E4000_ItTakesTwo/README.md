# It Takes Two (Switch) — `010092A0172E4000`

- **Engine**: **Unreal Engine 4** (Hazelight, codename "Nuts"; script AngelScript gọi là "Cake")
- **Sản phẩm**: chưa có — đang ở **Giai đoạn 1** (xem mục "Điểm chặn")

## Cấu trúc RomFS (đã bóc được — 5.691 file, 7,0 GB)

| Đường dẫn | Nội dung |
|---|---|
| `Nuts/Content/Paks/Nuts-Switch.pak` | **6,87 GB** — gần như toàn bộ dữ liệu game (191.641 entry) |
| `Nuts/Script/Cake/**/*.as` | ~5.700 script AngelScript — **file RỜI** (thay được bằng LayeredFS) |
| `Engine/Content/SlateDebug/Fonts/LastResort.ttf` | **font dự phòng UE** — file RỜI, thay được để có tiếng Việt |
| `Manifest_NonUFSFiles_Switch.txt` | danh sách file rời |
| `UE4CommandLine.txt` | |

## Vị trí TEXT (đã xác định)

| Loại | File (trong pak) |
|---|---|
| **Menu / UI** | `Nuts/Content/Untold/StringTables/ST_UTG_MenuLabels.uasset` + `.uexp` (đọc được, 5 KB, đã thấy EULA + nhãn menu) |
| **Phụ đề** | `Nuts/Content/Cinematics/Subtitles/Generated/*.uasset` + `.uexp` — **588 file**, struct `HazeSubtitleAsset` (Lines[] → Text FText) |
| **Bảng điều khiển** | `Nuts/Content/Untold/StringTables/ST_UTG_SwitchControllerLayouts.uasset/.uexp` |

⚠️ **Không có file `.locres`** của game (chỉ có của Engine) → text nằm trong **asset UE4 nhị phân**.

## ⛔ ĐIỂM CHẶN

Text nằm trong **asset UE4 nhị phân** (`.uasset` + `.uexp`), **không phải** từ điển dễ sửa như
`AVAFDICT` của Hogwarts. Muốn dịch phải:
1. **Đọc/ghi được asset UE4** (parse đúng cấu trúc export + FText + `StringTable`), hoặc
2. **Vá tại chỗ với độ dài bằng nhau** (tiếng Việt thường DÀI HƠN tiếng Anh → không khả thi cho phần lớn chuỗi), hoặc
3. Dùng công cụ chuyên dụng (UAssetAPI/.NET) — máy chưa có.

→ **Cần viết bộ parse `.uasset/.uexp`** (đây là việc lớn, tương tự việc giải mã định dạng `.kit`
của Unravel Two trước đây).

## Việc còn lại

1. Viết codec đọc/ghi `.uasset`+`.uexp` cho `ST_UTG_*` và `Subtitles/*`.
2. Bóc toàn bộ chuỗi (menu + phụ đề) → dịch (có glossary tạo TRƯỚC — BH-22).
3. Vá font: thay `LastResort.ttf` (file rời) — giữ đủ glyph gốc + thêm dấu tiếng Việt (BH-20).
4. Đóng gói: **patch pak** (`Nuts-Switch_p.pak`) vì text là UFS trong pak + file rời cho font/script.
5. QA + chuyển ROM (đã chuyển: `E:\ROM_Backup\ItTakesTwo\`).

## Ghi chú

- ROM đã chuyển ra `E:\ROM_Backup\ItTakesTwo\` (4 file: base + update + 2 DLC, SHA256 xác minh).
- Bằng chứng text đọc được: `ST_UTG_MenuLabels.uexp` chứa EULA tiếng Anh + `2022 Hazelight Studios AB`.
- Thư mục tạm: `E:\ITT_work` (chứa `Nuts-Switch.pak` 6,39 GB + mẫu asset).
