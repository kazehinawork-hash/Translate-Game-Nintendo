# Ori and the Will of the Wisps (Switch) — `01008DD013200000`

- **Engine**: **Unity (IL2CPP)** — `Data/Managed/Metadata/global-metadata.dat`
- **Bản ROM**: `input/Ori and the Will of the Wisps[01008DD013200000][US][v0].nsp` (2,9 GB)
  + UPD `01008DD013200800` (1,4 GB)
- **Sản phẩm (dự kiến)**: `output/atmosphere/contents/01008DD013200000/romfs/Data/data_*.unity3d`

## Trạng thái: 🚧 ĐANG DỰNG PIPELINE (engine mới — Unity lần đầu)

| Giai đoạn | Trạng thái |
|---|---|
| 1. Nhận diện engine & RomFS | ✅ Xong — Unity IL2CPP |
| 2. Định vị & giải mã text | ✅ Xong (đã hiểu định dạng) |
| 2b. Phương pháp vá bundle | ✅ Đã chứng minh chạy được |
| 2c. Quét toàn bộ + dịch | ⏳ Chưa |
| 3. Vá font Unity | ⏳ Chưa |
| 4. Đóng gói LayeredFS | ⏳ Chưa |

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
