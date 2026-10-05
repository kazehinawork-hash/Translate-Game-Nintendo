# It Takes Two (Switch) — `010092A0172E4000`  ✅ HOÀN THÀNH

- **Engine**: **Unreal Engine 4** (Hazelight, codename "Nuts")
- **Mod**: `output/atmosphere/contents/010092A0172E4000/romfs/Nuts/Content/Paks/Nuts-Switch_p.pak` (491 KB)

## Cách chơi
Copy `atmosphere/` vào thẻ nhớ Switch. **Không cần vá font** — xem mục Font bên dưới.

## Đã làm (đủ 5 giai đoạn)

| Giai đoạn | Kết quả |
|---|---|
| 1. Engine + bóc | UE4; RomFS 5.691 file; text nằm **trong pak** (UFS) → phải đóng **patch pak** |
| 2. Trích + dịch | **2.650 chuỗi duy nhất** (2.859 vị trí; 293 file phụ đề + 2 StringTable) — 8 chunk, 4 subagent |
| 3. Font | **KHÔNG cần vá**: `LastResort.ttf` gốc có **388.232 glyph** và **đã đủ 100% ký tự tiếng Việt** dùng trong bản dịch |
| 4. Đóng gói | `Nuts-Switch_p.pak` — 590 entry (295 .uasset + .uexp), V11, mount `../../../` |
| 5. QA | QA bản dịch PASS (0 thiếu/0 rỗng/0 ký tự lạ/0 lệch xuống dòng) + **đọc lại asset từ pak thấy đúng chữ Việt** |

## Công cụ (mới)

| Tool | Việc |
|---|---|
| `tools/itt_uasset_tool/` (C# + UAssetAPI) | `tojson` / `fromjson` cho asset UE4 — **mấu chốt: chỉ định `ObjectVersion` thủ công** (asset cooked = unversioned) |
| `tools/itt_extract_strings.py` | Bóc chuỗi từ JSON asset (StringTable + `TextPropertyData.CultureInvariantString`) |
| `tools/itt_terms.py` | Rút thuật ngữ → `glossary/ittakestwo.csv` (**tạo TRƯỚC khi dịch** — BH-22) |
| `tools/itt_chunk.py`, `tools/itt_qa.py`, `tools/itt_patch_json.py`, `tools/build_itt_pak.py` | Chia chunk → QA/gộp → ghi JSON → đóng pak |

## Quy trình build lại

```bash
# 1) bóc asset text tu pak (can E:\ITT_work\Nuts-Switch.pak)
python tools/archive_rom.py                 # ROM o ROM_Backup\ItTakesTwo
# 2) dump JSON  (E:\ITT_work\uag_tool)
dotnet run -- tojson E:\ITT_work\assets E:\ITT_work\json 522
# 3) boc chuoi + dich + QA
python tools/itt_extract_strings.py ; python tools/itt_terms.py ; python tools/itt_chunk.py
python tools/itt_qa.py                      # -> translations/itt_vi.json
# 4) ghi nguoc: JSON -> asset -> pak
python tools/itt_patch_json.py
cd E:\ITT_work\uag_tool && dotnet run -- fromjson E:\ITT_work\json_vi E:\ITT_work\assets_vi 522
python tools/build_itt_pak.py
```

Sửa bản dịch: `games/010092A0172E4000_ItTakesTwo/translations/vi_{1..8}.json` (dạng `{"chuỗi EN": "bản dịch"}`)
hoặc `itt_vi.json` → chạy lại bước 4.

## Lưu ý kỹ thuật (bài học BH-23)

1. Text **không** nằm trong `.locres` → nằm trong **asset UE4 nhị phân** (StringTable + phụ đề).
2. Máy có **.NET 10** → dùng **UAssetAPI**, **không cần tự viết parser**.
3. Asset `cooked` = **unversioned** → `new UAsset(...)` thường ném lỗi; phải dùng constructor 6 tham số
   với **`ObjectVersion` = 522** (UE4.27).
4. CLI của UAssetGUI **không** đặt được `ObjectVersion` (gọi sai còn mở giao diện) → viết tool C# riêng.
5. **Luôn kiểm roundtrip** trước khi dịch (đọc → JSON → asset → đọc lại: byte y hệt).
6. **Kiểm đường dẫn trong pak sau khi đóng** — lần đầu tôi tính sai gốc nên pak chứa `../assets_vi/...`
   (kiểm chứng đã bắt được trước khi bàn giao).
