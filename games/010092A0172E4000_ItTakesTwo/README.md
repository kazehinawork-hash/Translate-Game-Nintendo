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

## ⛔ ĐIỂM CHẶN → ✅ ĐÃ GIẢI QUYẾT (05/10)

Ban đầu tưởng phải tự viết parser UE4. Nhưng kiểm tra máy thấy **đã có .NET 10.0.400** →
dùng được **UAssetAPI** (thư viện chuẩn cho asset UE4).

**Công cụ đã dựng và CHẠY ĐƯỢC:** `tools/itt_uasset_tool/` (C# + NuGet UAssetAPI)

Cách đọc asset **unversioned (cooked)** — mấu chốt:
```csharp
// PHẢI chỉ định ObjectVersion thủ công (CLI của UAssetGUI không làm được việc này)
new UAsset(path, ObjectVersion.VER_UE4_AUTOMATIC_VERSION /* =522, UE4.27 */,
           ObjectVersionUE5.<first>, new List<CustomVersion>(), null, CustomSerializationFlags.None);
```
- `asset.SerializeJson()` → JSON (sửa chữ ở đây)
- `UAsset.DeserializeJson(...)` + `asset.Write(path)` → ghi lại
- **Đã kiểm chứng ROUNDTRIP**: gốc 618 byte → ghi lại 618 byte, JSON **giống hệt** → **không mất dữ liệu**
- Đọc thử `ST_UTG_MenuLabels` thấy đúng chữ (EULA + nhãn menu)

→ **Đường đi đã thông**, không cần tự viết parser nữa.

## Việc còn lại

1. Bóc **2 StringTable** (`ST_UTG_*`) + **588 file phụ đề** từ pak → dump JSON bằng công cụ trên.
2. **Tạo glossary TRƯỚC** (BH-22 — lần trước làm sau nên phải sửa lại) rồi mới dịch.
3. Dịch (chia chunk + subagent) → ghi JSON ngược lại thành asset.
4. Vá font: thay `LastResort.ttf` (file rời) — giữ đủ glyph gốc + thêm dấu (BH-20).
5. Đóng gói: **patch pak** `Nuts-Switch_p.pak` (text là UFS trong pak) + file rời cho font.
6. QA + bàn giao.

## Ghi chú

- ROM đã chuyển ra `E:\ROM_Backup\ItTakesTwo\` (4 file: base + update + 2 DLC, SHA256 xác minh).
- Bằng chứng text đọc được: `ST_UTG_MenuLabels.uexp` chứa EULA tiếng Anh + `2022 Hazelight Studios AB`.
- Thư mục tạm: `E:\ITT_work` (chứa `Nuts-Switch.pak` 6,39 GB + mẫu asset).
