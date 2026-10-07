# MONOPOLY (2024) (Switch) — `01002C201BC40000`

- **Engine**: **Unity IL2CPP** — nhà phát hành **Ubisoft** (có `Plugins/ubiservices.nro`)
- **Trạng thái**: ✅ **Đã dịch xong text + đóng gói mod** (font cần chơi thử để xác nhận)

## Cấu trúc RomFS (208 file, 1.016 MB)

| Đường dẫn | Nội dung |
|---|---|
| `Data/data.unity3d` | **520 MB** — bundle chính, **198.295 object** (MonoBehaviour 30.593) ← **text nằm ở đây** |
| `Data/Managed/Metadata/global-metadata.dat` | 24 MB — metadata IL2CPP |
| `Data/StreamingAssets/Audio/GeneratedSoundBanks/Switch/<LANG>/VO.bnk` | audio lồng tiếng theo **7 ngôn ngữ** |
| `Data/StreamingAssets/defaultKeyBindings.json`, `defaultboard.json` | cấu hình (không phải text hiển thị) |
| `Plugins/ubiservices.nro`, `cimgui.nro` | plugin |

## Kho text: hệ thống **"Oasis"** của Ubisoft

Text **không** nằm trong `.locres`/CSV rời mà trong các **TextAsset** bên trong `Data/data.unity3d`:

- `oasis_englishgb` — **2.063 chuỗi** tiếng Anh (nguồn dịch)
- `oasis_french`, `oasis_german`, `oasis_spanish`, `oasis_italian`, `oasis_dutch`, `oasis_polish`,
  `oasis_russian`, `oasis_japanese`, `oasis_korean`, `oasis_traditional_chinese`,
  `oasis_simplified_chinese`, `oasis_brazilianportuguese` — 12 bản ngôn ngữ khác
- `oasis__global` — **file master**: `<languages>` (14, `English` = `master="true"`), `<characters>`, `<teams>`, `<sections>`
- `credits` — danh sách ghi công (có markup `<H1>`, `<T>`, `<N>`)

### Định dạng

```xml
<?xml version="1.0" encoding="utf-16"?>
<oasis oasisVersion="5.1.7518498.0" toolVersion="2.0.0"
       xmlns="http://schemas.ubisoft.com/oasis/2011/extractor">
  <translations language="EnglishGB">
    <t id="2" text="Online"/>
    <t id="4" text="Credits"/>
    ...
```

⚠️ TextAsset có **tiền tố byte hỏng** trước thẻ `<` đầu tiên — parse phải bỏ phần trước `<` rồi mới `decode('utf-16')`.

## Đã làm

1. Bóc 2.063 chuỗi từ `oasis_englishgb` → `translations/mono_en.json`.
2. **Tạo glossary TRƯỚC** (BH-22) → `glossary/monopoly.csv` (47 thuật ngữ chuẩn Monopoly + 300 gợi ý).
3. Dịch **1.704 chuỗi duy nhất** bằng 3 subagent (`todo_*.json` → `vi_*.json`) → `mono_vi.json`.
4. Ghi lại vào XML (thay thuộc tính `text="…"`) → đóng gói lại TextAsset → bundle.
5. Kiểm chứng bundle mới: **1.932 mục hiện tiếng Việt** / 2.063 (phần còn lại là mục giữ nguyên hợp lệ:
   `Ubisoft Connect`, `OK`, `AI`, `{0}`, chuỗi charset…).

**Thành phẩm**: `output/atmosphere/contents/01002C201BC40000/romfs/Data/data.unity3d` (522 MB)

`Data/data.unity3d` là **file rời trong RomFS** → **LayeredFS thay trực tiếp, KHÔNG cần patch pak**.

## QA cuối (`tools/mono_final_qa.py`) — PASS

| Hạng mục | Kết quả |
|---|---|
| Số object trong bundle | 198.295 = 198.295 ✅ |
| Số mục | 2.063 = 2.063 ✅ |
| Key thiếu / thừa | 0 / 0 ✅ |
| Lệch placeholder & tag (`{0}`, `%s`, `<b>`, `&#xA;`…) | **0** ✅ |
| Lệch xuống dòng | **0** ✅ |
| Ký tự ngoài (CJK/Hangul/Kana/Nga/Ả Rập) | **0** ✅ |
| Ký tự điều khiển | **0** ✅ |
| Chuỗi rỗng | **0** ✅ |

**1.926 mục đã dịch** (khác bản gốc), phần còn lại là mục giữ nguyên hợp lệ (`Ubisoft Connect`, `OK`, `AI`, `{0}`, charset).

### 🐛 Lỗi đã tìm ra & sửa trong lần QA cuối

Nguồn lưu xuống dòng bằng **tham chiếu ký tự `&#xA;`** trong thuộc tính XML (KHÔNG phải ký tự xuống dòng thật):

```xml
<t id="201" text="Authentication failed. &#xA;Please try again."/>
```

Bản build đầu ghi **xuống dòng thật** → XML chuẩn hoá giá trị thuộc tính biến nó thành **dấu cách**
→ **mất ngắt dòng** ở **124 mục**. Đã sửa `esc_attr()` trong `mono_build_mod.py` để escape
`\n → &#xA;`, `\r → &#xD;`, `\t → &#x9;` — QA lại: **0 lệch**.

## Font (cần chơi thử)

80 font TTF đóng trong bundle. **74 font đã đủ ký tự tiếng Việt**.

6 font còn thiếu:

| Font | Glyph | Thiếu |
|---|---|---|
| `NotoSans-CondensedBold`, `aline_font`, `LiberationSans` | 871–2.793 | chỉ `┿` (ký hiệu tiền của chính game) |
| `PerfectDOSVGA437` | 256 | 93 (font kiểu DOS) |
| **`KabelBold`, `KabelMedium`** | 574–575 | **88 ký tự có dấu** ← đáng lo nhất |

`fontTools.merge` **lỗi** trên 2 font Kabel (`NotImplementedType … .cff`) → chưa ghép được.
Nếu chơi thử thấy ô vuông ở tiêu đề → cần xử lý riêng 2 font này.

## Công cụ

| Script | Việc |
|---|---|
| `tools/mono_extract.py` | Bóc chuỗi từ kho Oasis → `mono_en.json` |
| `tools/mono_glossary_chunk.py` | Tạo `glossary/monopoly.csv` + chia chunk |
| `tools/mono_qa_merge.py` | QA + gộp `vi_*.json` → `mono_vi.json` |
| `tools/mono_build_mod.py` | Ghi bản dịch vào XML + đóng gói bundle |
| `tools/mono_verify.py` | Đọc lại bundle thành phẩm để kiểm chứng |
| `tools/mono_final_qa.py` | **QA cuối**: đối chiếu TỪNG MỤC gốc ↔ thành phẩm |
| `tools/mono_font_check.py` | Kiểm độ phủ tiếng Việt của 80 font |
| `tools/mono_patch_font.py` | Ghép glyph tiếng Việt vào font thiếu |

## Ghi chú

- ROM ở `E:\ROM_Backup\Monopoly\`. Thư mục tạm: `E:\MONO_work`.
- 🐛 **BH-24**: file `inspect.py` trong thư mục script tạm **che module chuẩn `inspect`** → `import UnityPy` chạy nhầm.
- 🐛 `env.save()` phải có `pack='original'`, nếu không bundle xuất ra **không nén** (520 MB → 1,27 GB).
