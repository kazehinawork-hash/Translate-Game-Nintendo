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

## ⚠️ LỖI ĐÃ SỬA #3: 8 mục MAIN hiển thị `[error:...]` (kể cả menu)

Soát toàn bộ 6.697 mục vật phẩm (`*_desc`, `*_name`, các độ hiếm `_Common/_Rare/_Epic/_Legendary`)
phát hiện 8 mục hiển thị **`[error:...]`** ra màn hình. Lỗi **có sẵn trong nguồn gốc** (cột tiếng
Trung cũng lỗi y hệt) nhưng **vá được** nhờ các key anh em:

| Key | Giá trị lỗi | Đã vá thành | Căn cứ |
|---|---|---|---|
| `Category_Hair` | `[error:Menu_Hair]` | `Kiểu Tóc` | `Menu_Hairstyle` |
| `Category_Outfit` | `[error:Menu_Outfits]` | `Trang Phục` | `Menu_Outfit`, `Category_Gear` |
| `Category_Quests` | `[error:Menu_ActiveQuests]` | `Nhiệm Vụ Đang Thực Hiện` | `MENU_ACTIVEQUEST` |
| `Data_RefreshesIn` | `Làm mới sau [error:time]` | `Làm mới sau {time}` | `Data_ExpiresIn` dùng `{time}` |
| `FGC_Collect_AstronomyTower` | `... [error:%d] ...` | `Tìm {0} mẩu Kiến Thức` | các key `FGC_*` khác dùng `{0}` |
| `FGC_Demiguise_AstronomyTower` | `... [error:%d] ...` | `Tìm {0} tượng Khỉ Tàng Hình Demiguise` | như trên |
| `Hamlet_Halkirk_CO_BB` | `[error:Hamelt_Halkirk]` | `Bainburgh` | `FT_OL_HamletHalkirk_CO_BB` |
| `ZSI_01` | `[ZSI_01_01_DADASide_Title]` | `Bài tập của Giáo sư Hecat 1` | chính key được tham chiếu |

Công cụ: `tools/fix_hogwarts_main_errors.py`. Sau khi vá: **0 mục `[error:...]`, 0 mục `[KEY]`**.

**Kiểm tra vật phẩm (sau khi vá):** 6.697 mục — 0 rỗng, 0 ký tự Hán/Nhật/Hàn, **0 lệch tag/placeholder**
so với nguồn, **0 ký tự không có trong font** trong mod. Còn 31 mục là placeholder dev có sẵn trong
nguồn gốc (giữ nguyên cho khớp bản gốc): `FGC_Broom_Collect_000_desc` = `TBD`, 30 mục `Outfit_073…077`
= `Outfit 073`, và `LighthouseSubtask_UnknownState` = `???`.

## ⚠️ LỖI ĐÃ SỬA #2: tên riêng bị "Pháp hóa" còn sót trong SUB

SUB dịch **từ tiếng Pháp**, nên một số tên riêng/thuật ngữ bị giữ theo bản Pháp hóa, trong khi
MAIN (dịch từ tiếng Trung) dùng **tên gốc** → hai phần không khớp nhau.

Cách phát hiện: quét toàn bộ SUB, tìm từ vừa **có trong cột `Source_FR`** vừa **KHÔNG có trong cột
`Source_ES`** → ra danh sách 21 từ nghi vấn; đối chiếu tiếp với MAIN để chốt tên đúng.

Ví dụ điển hình (đã sửa bằng `tools/fix_hogwarts_fr_names.py`, 353 dòng):

| Bản Pháp (sai) | Tên gốc (đúng) | Bằng chứng |
|---|---|---|
| `Adélaïde Duchêne` | **Adelaide Oakes** | ES: "Adelaide Oakes"; MAIN: `AdelaideOakes` |
| `Aile-Céleste` | **Highwing** | ES + MAIN `Highwing` |
| `Pont-Désir` | **Keenbridge** | ES + MAIN `Hamlet_KeenBridge` |
| `Bourg-Garenne` | **Brocburrow** | ES + MAIN |
| `Fléreur` | **Kneazle** | ES "kneazle"; MAIN "Mèo Kneazle" |
| `Lépouvantail` | **Bù Nhìn** (Scarecrow) | ES "Scarecrow" |
| `Tressedif` | **Yew Weaver** | ES "Tejetejos"; MAIN `BroomYewWeaver` |
| `Rubanvol` | **Wind Wisp** | ES "Volutas de Viento"; MAIN `BroomWindWisp` |
| `Delamare` | **Affpuddle** | ES "Sir Affpuddle"; MAIN |
| `Grottaleau` | **Marunweem** | ES + MAIN |
| `Brode` | **Weft** | ES "Grimbald Weft"; MAIN `LORE_BellTowers_Skull` |
| `Roland` | **Rowland** | ES "Rowland"; MAIN `Rowland Oakes` |
| `Vivet` | **Snidget** | ES "snidget" |
| `Bubobulb` / `Murlap` / `Horglup` / `Moremplis` / `Croup` | **Bubotuber / Murtlap / Horklump / Lethifold / Crup** | ES |
| `Créasort` | **Spellcraft** | ES "magifórmula" |
| `Imperium` | **Imperius** | ES "Imperius" |
| `Têtenbulle` | **Bubble-Head** | ES "casco-burbuja" |
| `Magyar` | **Rồng Đuôi Gai Hungary** | ES "colacuerno" (Horntail) |

**Kết quả sau khi sửa:** quét lại → **0 từ Pháp hóa còn sót**; so với nguồn → SUB chỉ còn **73**
chuỗi giữ nguyên (đều là thán từ `Hmm.` / `Argh…` và tên bùa `<i>Nox</i>.`), MAIN còn 681 nhãn
độ phân giải/FPS hợp lệ và **0 ký tự Hán**.

## ⚠️ LỖI ĐÃ SỬA #1: phụ đề bị tiếng Pháp

`tools/build_hogwarts_sub.py` đọc bản dịch ở `source/split_tasks/sub_trans/` — **thư mục này
không tồn tại**; bản dịch thật nằm ở `translations/sub_trans/`. Kết quả: `glob` trả về 0 file
→ `id2vi` rỗng → **toàn bộ `SUB-*.bin` giữ nguyên tiếng Pháp** (2,6% tiếng Việt) mà **không báo lỗi**.

- Đã sửa đường dẫn sang `translations/` và thêm **cảnh báo khi thiếu bản dịch**.
- Build lại: **26.296/26.296 chuỗi phụ đề** dùng đúng bản dịch → `SUB-enUS.bin` nay **97,7% tiếng Việt**.
- Patch pak cũng được build lại (28 entry, đã verify SUB khớp bản mới).
- **Bài học**: script build phải in số lượng bản dịch đã nạp; nạp 0 file thì phải báo lỗi,
  không được im lặng đóng gói dữ liệu gốc.

## Lưu ý kỹ thuật (đã từng dính lỗi — đừng lặp lại)

1. **Magic AVAFDICT phải là UTF-16LE** (`41 00 56 00 …`). Ghi ASCII → game hiện toàn bộ `[KEY]`.
   Luôn tự kiểm: `pack_avafdict(unpack_avafdict(file_gốc)) == file_gốc`.
2. Text nằm **trong `pakchunk0-Switch.pak`** (UFS) → file `.bin` đặt rời trong `romfs/` **không được đọc**;
   phải đóng gói **patch pak** `pakchunk0-Switch_p.pak`.
3. Game có **14 ngôn ngữ** — patch pak đã phủ hết nên console để ngôn ngữ nào cũng ra tiếng Việt.
4. Font: thay file rời `Engine/Content/SlateDebug/Fonts/LastResort.ttf` (font dự phòng của UE).
