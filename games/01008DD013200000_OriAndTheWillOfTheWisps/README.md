# Ori and the Will of the Wisps (Switch) — `01008DD013200000`

- **Engine**: **Unity (IL2CPP)** — `Data/Managed/Metadata/global-metadata.dat`
- **Bản ROM**: `input/Ori and the Will of the Wisps[01008DD013200000][US][v0].nsp` (2,9 GB)
  + UPD `01008DD013200800` (1,4 GB)
- **Sản phẩm (dự kiến)**: `output/atmosphere/contents/01008DD013200000/romfs/Data/data_*.unity3d`

## Trạng thái: ✅ ĐÃ BUILD MOD (chờ test trong game)

| Giai đoạn | Trạng thái |
|---|---|
| 1. Nhận diện engine & RomFS | ✅ Xong — Unity IL2CPP |
| 2. Định vị & giải mã text | ✅ Xong |
| 2b. Phương pháp vá bundle | ✅ Đã chứng minh |
| 2c. Quét toàn bộ + dịch | ✅ **1.877 mục / 1.793 chuỗi duy nhất — dịch 100%, QA 0 lỗi** |
| 3. Vá font Unity | ✅ **Đã thay TTF nhúng của `Candara` bằng Lato (đủ dấu tiếng Việt)** |
| 4. Đóng gói LayeredFS | ✅ **103 bundle (102 text + 1 font), 870,7 MB** |

> ⚠️ **Bài học quan trọng (đã sửa trong tool):** sau tên `...TextMessageProvider` có thể là
> `[int32 cờ][int32 len][chuỗi]` **hoặc** `[int32 len][chuỗi]`; giá trị cờ không phải luôn = 1.
> Rule cũ chỉ nhận cờ = 1 nên **bỏ sót 298 mục hội thoại** (data_249: 68 → 151 mục).
> `parse_message` nay thử lần lượt `delta=4` rồi `delta=0`.

## Bản dịch để sửa

- **File duy nhất cần sửa:** `translations/ori_vi.json` — mảng `[{Id, EN, VI}]` (1.793 dòng).
- Sửa `VI` → chạy lại `python tools/build_ori_mod.py` + `python tools/patch_font_ori.py` là xong.
- (Các thư mục `translations/chunks/` và `chunks2/` chỉ là bản chia nhỏ lúc dịch, không cần đụng.)

## Build lại

```bash
# 1) Bóc bundle gốc ra thư mục ngoài OneDrive (ví dụ C:\...\ori_work\Data)
#    (lần sau chỉ cần chạy lại nếu xoá; bundle gốc lấy từ NSP bằng tools/ue_romfs_tool.py)
# 2) Dịch: games/<TID>/translations/vi_*.json  (đã xong)
# 3) Đóng gói:
python tools/build_ori_mod.py --src <thu_muc_bundle_goc>
python tools/patch_font_ori.py     # vá font (xem ghi chú bên dưới)
```

## Ghi chú font (đã kiểm chứng bằng dữ liệu thật)

Game chỉ có **7 Font asset**, tất cả đều là **font động** (`m_CharacterRects = 0` → atlas dựng lúc chạy
từ `m_FontData`), nên thay TTF nhúng là có hiệu lực ngay.

| Font | Vai trò | Xử lý | Kết quả |
|---|---|---|---|
| `Candara` | Font UI chính (atlas động, **0 icon**) | **Thay hẳn** bằng Lato | 120/120 dấu VI, chỉ mất 2 ký tự vô nghĩa (U+2206, U+25AF) |
| `ProFontWindows` | Font text (**0 icon**) | **Thay hẳn** bằng Lato | 0 thiếu |
| `keyboard` | 52 chữ + **18 glyph ICON (PUA) đang dùng** (~100 lần/bundle) | **Hợp nhất** (giữ icon + thêm dấu) | 0 thiếu, giữ đủ 18 icon |
| `moon-tools` | **100% glyph icon** (PUA) đang dùng | **Hợp nhất** | 0 thiếu, giữ đủ 33 icon |
| `Roboto-Thin/Bold/Light` | Font UI | **Giữ nguyên** | Đã phủ đủ tiếng Việt từ đầu (896 glyph) |

- Công cụ hợp nhất: `tools/merge_vi_font.py` — thêm glyph tiếng Việt từ Lato vào font gốc,
  tự scale `unitsPerEm` (keyboard 1000, moon-tools 1024, Lato 2048) và **giữ toàn bộ glyph cũ**.
- Đã kiểm chứng: mọi glyph tiếng Việt trong mod **đều có nét vẽ thật**; các glyph icon giữ nguyên
  (kể cả U+E000–E002 vốn **rỗng sẵn ở bản gốc** — mod giống hệt gốc, không hồi quy).
- ⚠️ **Không** thay hẳn `keyboard`/`moon-tools`: chúng chứa glyph icon đang được game dùng,
  thay cả font sẽ làm icon biến mất.

## Việc còn lại

1. **Test trong game** (chép `output/atmosphere/` vào thẻ nhớ, đặt ngôn ngữ **English**
   → vì tiếng Việt được ghi đè lên khe tiếng Anh).
2. Nếu còn ô vuông ở vài chỗ → xác định font tương ứng và vá nốt.

## Text nằm ở đâu (đã xác minh)

- RomFS: `Data/data_0..306.unity3d` = **307 AssetBundle** (~1,36 GB), **nén**.
- Trong bundle: các `MonoBehaviour` tên `TextMessageProvider`, mỗi cái chứa 1 đoạn hội thoại.
- Chuỗi lưu kiểu Unity: `[int32 độ_dài][UTF-8][pad cho tròn 4 byte]`.
- Mỗi đoạn có **20 ngôn ngữ**: **tiếng Anh là 1 chuỗi riêng**, ngay sau là mảng 19 ngôn ngữ
  (Ý, Đức, TBN, Nhật, Bồ, Trung giản, Nga, Trung phồn, Séc, Đan, Hà, Phần, Hung, Hàn, Na Uy,
  Ba Lan, TBN-Mỹ, Thụy Điển, Thổ). **Không có tiếng Việt.**
- ⇒ Hướng làm: **ghi tiếng Việt đè lên khe tiếng Anh** → chơi ở ngôn ngữ English sẽ ra tiếng Việt.

Ví dụ thật (object 2638, `data_18.unity3d`):
```
EN: Press [StructureInteraction] to #place the amulet#!
IT: Premi [StructureInteraction] per #collocare l'amuleto#!
DE: Drücke [StructureInteraction], um #das Amulett zu platzieren#!
... (19 ngôn ngữ)
```

## Phương pháp vá (đã chứng minh)

1. `ObjectReader.get_raw_data()` → tìm mảng chuỗi đa ngôn ngữ.
2. Thay blob chuỗi tiếng Anh bằng bản dịch tiếng Việt (blob mới vẫn **bội số 4 byte**) → splice byte.
3. `ObjectReader.set_raw_data(new)` → `env.save(pack=..., out_path=...)`.

Đã kiểm chứng trên `data_18.unity3d`: object count **giữ nguyên 35.242**, chuỗi tiếng Việt có mặt.
(bundle ghi ra không nén = 89,9 MB so với 52,6 MB gốc → cần nén LZ4 khi build thật.)

## Công cụ

```bash
python tools/ue_romfs_tool.py list   "<nsp>"                 # liệt kê RomFS
python tools/ue_romfs_tool.py extract "<nsp>" "Data/data_18.unity3d" out.unity3d
python tools/unity_text_tool.py scan  <bundle.unity3d> [--out list.json]   # beta
python tools/unity_text_tool.py patch <bundle.unity3d> <map.json> <out_dir> # beta
```

Cần: `pip install UnityPy`.

## Việc còn lại (thứ tự đề xuất)

1. **Typetree IL2CPP** để đọc/ghi MonoBehaviour theo tên field (thay vì dò offset thủ công):
   trích `main` (ExeFS) + `Data/Managed/Metadata/global-metadata.dat` →
   `UnityPy.helpers.TypeTreeGenerator.load_il2cpp(il2cpp, metadata)`.
2. Quét **toàn bộ 307 bundle** → xuất JSON khoá gốc (tiếng Anh) + tra cứu ngữ cảnh theo tên object.
3. Dịch EN→VI (chia chunk, subagent song song — theo `/dich` Giai đoạn 2).
4. **Font**: kiểm tra font atlas của game có đủ dấu tiếng Việt không; nếu thiếu phải vá
   Font asset / TMP (Unity) — chưa có tool, sẽ dựng mới.
5. Đóng gói `Data/data_*.unity3d` (nén LZ4) vào `output/atmosphere/contents/01008DD013200000/romfs/`.
