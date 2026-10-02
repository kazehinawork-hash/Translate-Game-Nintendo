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
| 6. **FONT TIẾNG VIỆT** | ⛔ **CHƯA XONG — ĐÂY LÀ ĐIỂM CHẶN** |

## ⛔ Điểm chặn: FONT là BitmapFont (atlas), KHÔNG có sẵn dấu tiếng Việt

- Game **không dùng TTF động** như Will of the Wisps. Nó dùng **BitmapFont tự vẽ** (`BitmapFont` +
  `BitmapFontChar`, `MoonTextMeshRenderer`): mỗi font là một **bảng glyph nhị phân** trỏ vào một
  **texture atlas 2048×2048** (đã đóng gói, không còn chỗ trống rõ ràng).
- **8 BitmapFont** trong bundle: `candara`, `msPGothic`, `adobeHeitiStdR`, `nyala`, `sakkalMajalla`,
  `kozukaGothicPro`, `nanumBrush`, `icons`.
- **Kiểm tra thực tế:** `candara` chỉ có **25/74** ký tự tiếng Việt (`ă â đ ê ô á à ã é è í ì ĩ ó ò õ ú ù ũ ý`)
  — tức là có chữ **1 dấu** nhưng **THIẾU toàn bộ chữ 2 dấu/dấu nặng** (`ắ ầ ẩ ậ ệ ộ ớ ợ ự ỵ`…).
  `msPGothic` 27/74, các font khác 19–25/74 → **không font nào phủ đủ tiếng Việt**.
- **Hệ quả:** nếu chép mod vào máy ngay bây giờ, các chữ có dấu thanh sẽ **không hiển thị** (ô trống/rác).

## Việc cần làm để hoàn thành (kế hoạch đề xuất)

1. Dựng **typetree IL2CPP** (đã chạy được cho game này: `Assembly-CSharp` OK) — nhưng class `BitmapFont`
   **không có trong metadata theo tên đó**, cần dò tên/namespace thật (hoặc dùng `BitmapFontChar`).
   Công cụ đã có: `tools/extract_il2cpp.py` (bóc `main` + `global-metadata.dat`).
2. Đọc đúng trường của BitmapFont: **PPtr tới atlas Texture2D** + **mảng glyph** (mã ký tự, UV, offset, advance).
3. Vẽ ~74 glyph tiếng Việt (dùng font cùng kiểu, ví dụ Lato/Nunito) vào **vùng trống của atlas**
   (hoặc mở rộng atlas rồi cập nhật lại toàn bộ UV), ghi thêm entry glyph.
4. Kiểm chứng: `python tools/qa_text.py --game obf` + so **số glyph / kích thước atlas** trước–sau.

**Chưa xác nhận được gì trong game** — phần text đã sẵn sàng nhưng mod **CHƯA dùng được** cho tới khi vá font.

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
