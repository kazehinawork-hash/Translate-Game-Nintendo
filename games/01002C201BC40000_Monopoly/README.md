# MONOPOLY (2024) (Switch) — `01002C201BC40000`

- **Engine**: **Unity IL2CPP** (giống Ori) — nhà phát hành **Ubisoft** (có `Plugins/ubiservices.nro`)
- **Trạng thái**: 🔄 **Giai đoạn 1** (đã nhận diện xong — xem "Điểm chặn")

## Cấu trúc RomFS (208 file, 1.016 MB)

| Đường dẫn | Nội dung |
|---|---|
| `Data/data.unity3d` | **520 MB** — bundle chính, **198.295 object** (MonoBehaviour 30.593) ← **text nằm ở đây** |
| `Data/Managed/Metadata/global-metadata.dat` | 24 MB — metadata IL2CPP (cần để dựng typetree) |
| `Data/StreamingAssets/Audio/GeneratedSoundBanks/Switch/<LANG>/VO.bnk` | audio lồng tiếng theo **7 ngôn ngữ** (English(US), French, German, Italian, Japanese, Spanish, Brasilian Portuguese) |
| `Data/StreamingAssets/defaultKeyBindings.json`, `defaultboard.json` | cấu hình (không phải text hiển thị) |
| `Plugins/ubiservices.nro`, `cimgui.nro` | plugin |

→ **Không có** thư mục `Localization` / `.locres` / bảng CSV — text nằm trong **asset Unity**.

## Kiểm kê object trong bundle (đã chạy)

```
198.295 object:  GameObject 56.795 · Transform 38.950 · MonoBehaviour 30.593
                 RectTransform 17.845 · CanvasRenderer 13.045 · Texture2D 1.661 · Canvas 281
```

## Việc còn lại

1. Dựng **typetree IL2CPP** (`python tools/extract_il2cpp.py <rom> E:\MONO_work` — như đã làm cho Ori)
   để đọc được các MonoBehaviour theo **tên trường** thay vì offset.
2. Tìm kho text thật trong `data.unity3d` (MonoBehaviour/UI Text) → bóc chuỗi.
3. **Tạo glossary TRƯỚC** (BH-22) → dịch (chunk + subagent).
4. Vá font (kiểm đủ glyph gốc — BH-20).
5. Đóng gói: bundle là **file rời** (`Data/data.unity3d`) → **LayeredFS thay trực tiếp**, không cần patch pak.
6. QA + bàn giao.

## Ghi chú

- ROM đã chuyển `E:\ROM_Backup\Monopoly\` (2 file, SHA256 xác minh).
- Bản base 1,12 GB + update v1.6 (682 MB) — **bản update có thể chứa thêm text/nội dung** (cần đối chiếu khi bóc).
- Thư mục tạm: `E:\MONO_work` (bundle + metadata đã bóc).
- 🐞 **Đã gặp và sửa lỗi công cụ**: file `inspect.py` trong thư mục script tạm **che module chuẩn `inspect`**
  → `import UnityPy` chạy nhầm script cũ, `fontTools` báo lỗi lạ. Xem **BH-24**.
