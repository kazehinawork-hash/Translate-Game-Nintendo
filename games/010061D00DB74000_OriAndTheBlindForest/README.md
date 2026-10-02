# Ori and the Blind Forest: Definitive Edition (Switch) — `010061D00DB74000`

- **Title ID**: `010061D00DB74000` (Base) + `010061D00DB74800` (Update v131072)
- **Engine**: Unity **IL2CPP** (Unity 2018.4.1f1) — bundle `Data/data.unity3d` (**1,74 GB**) + ~130 `Data/sharedassets*.resource`
- **Định dạng text**: MonoBehaviour `*TextMessageProvider` (giống Will of the Wisps):
  `[tên][pad][int32 cờ][int32 len][CHUỖI TIẾNG ANH][mảng ngôn ngữ khác]`
- **Sản phẩm**: `output/atmosphere/contents/010061D00DB74000/romfs/Data/data.unity3d`

## Tiến độ

| Giai đoạn | Trạng thái |
|---|---|
| 1. Nhận diện engine & RomFS | ✅ Xong |
| 2. Trích xuất text | ✅ **679 mục** (656 khoá), tiếng Anh |
| 2b. Dịch EN→VI | ✅ **100%** (659 chuỗi duy nhất, 3 chunk) |
| 2c. QA tag/placeholder | ✅ **0 lệch** |
| 3. Vá bundle (text) | ✅ **679 object** → `data.unity3d` (1,74 GB) |
| 4. Đóng gói LayeredFS | ✅ `output/atmosphere/contents/010061D00DB74000/romfs/Data/` |
| 5. Cổng QA | ✅ **PASS** (`python tools/qa_text.py --game obf`) |
| 6. **FONT TIẾNG VIỆT** | ✅ **XONG** — 78 glyph sinh vào atlas + đổi mã ký tự (xem bên dưới) |

## ✅ FONT đã xử lý xong (BitmapFont / atlas SDF)

Game **không đọc file font** — nó vẽ chữ từ **bảng glyph nhị phân** + **texture atlas SDF**.
Định dạng đã giải mã (`tools/unity_bitmapfont.py`):

- Mỗi font = MonoBehaviour class `BitmapFont`: `[header][tên][block1: count + entry 48B][block2 …][float metric]`
- **Entry 48 byte** = `[int32 mã ký tự]` + 11 float:
  `f0,f1 = u0,u1` · `f2,f3 = v0,v1` (gốc dưới) · `f4 = độ lệch ngang` · `f5..f8 = quad lấy mẫu SDF`
- **Atlas** = Texture2D tên `<font>_0 distance map`, **Alpha8**, giá trị nằm ở **kênh alpha**
- `candara` = font Latin: **448 glyph** (94 ASCII + 354 Latin‑1/mở rộng), atlas **2048×1024**

**Cách vá (không đổi kích thước atlas → không phải dịch chuyển 448 entry cũ):**

1. Bản dịch cần **78 ký tự** chưa có (74 chữ Việt + `ƠơƯư` + `…`) — atlas đã kín chỗ nhưng chỉ 48% pixel có mực.
2. **Mượn ô của các glyph không dùng**: chọn ký tự font CÓ mà bản dịch KHÔNG dùng (`Ø Æ Ä Ö Ō Õ Å …`
   ở dải Latin‑1 mở rộng / Cyrillic / Greek) — **196 ô** đủ điều kiện.
3. Vẽ glyph tiếng Việt từ **Lato** ở `em = 110 px` (đo từ atlas: cap 77 px, x-height 58 px), làm mềm nhẹ
   cho giống dạng SDF, đặt vào **đúng ô** của glyph mượn.
4. **Đổi mã ký tự** trong entry 48 byte từ ký tự cũ → ký tự tiếng Việt.

Công cụ: `python tools/patch_font_obf.py` (vẽ font + vá text trong cùng lượt).

**Kiểm chứng:** đọc lại bundle → **0/74 ký tự tiếng Việt còn thiếu**; cắt ảnh atlas ra xem bằng mắt:
`ạ ắ ệ ợ ự Ứ Ờ Ư ơ` đủ dấu, không cắt, không méo. Text tiếng Anh của game chỉ dùng 2 ký tự phi-ASCII (`’`) nên
**không ô mượn nào ảnh hưởng tới chữ tiếng Anh**.

⚠️ Đánh đổi: 78 ký tự bị mượn ô (Ø Æ Ä Ö …) sẽ **không còn hiển thị đúng** — chúng không xuất hiện trong
bản dịch lẫn text tiếng Anh của game.

## Cách build lại

```bash
python tools/extract_il2cpp.py "input\<game>.nsp" E:\OBF_work     # bóc main + metadata (cho typetree)
# (data.unity3d đã bóc sẵn ở E:\OBF_work\data.unity3d)
# sửa bản dịch: games/010061D00DB74000_OriAndTheBlindForest/translations/obf_vi.json
python tools/qa_text.py --game obf
```

## Ghi chú kỹ thuật

- Khoá text = `path_id` của MonoBehaviour; bản dịch lưu ở `translations/obf_vi.json` (`{Id, EN, VI}`).
- Dấu `#...#` = cụm nhấn mạnh màu; `[Tên]` = mã nút bấm; `\n` là 2 ký tự — **bảo toàn 100%**.
- ROM của game: đã chuyển sang `E:\ROM_Backup\OriBlindForest\` (xem `docs/BAI-HOC.md` BH-16).
