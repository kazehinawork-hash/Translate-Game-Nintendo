# Translate Game — Việt hóa game Nintendo Switch

Dự án bản địa hóa (localization) game Nintendo Switch sang **tiếng Việt**, đóng gói dưới dạng
**mod LayeredFS** cho Atmosphere CFW (không sửa file gốc của game — chỉ chồng file đè lên RomFS,
gỡ ra là về nguyên trạng).

Mục tiêu: một **quy trình dùng chung theo engine** (không phải một mớ script riêng lẻ từng game),
tự động hóa từ bóc tách → dịch → vá font → đóng gói → kiểm toán.

---

## Cấu trúc thư mục

```
Translate Game/
├─ AGENTS.md                 Quy tắc làm việc của dự án (đọc trước khi làm)
├─ README.md                 File này
├─ docs/
│   ├─ STATE.md              Trạng thái/tiến độ từng game            ← ĐỌC ĐẦU TIÊN
│   ├─ BAI-HOC.md            Bài học kinh nghiệm + checklist bàn giao ← BẮT BUỘC ĐỌC
│   └─ INSTALL-MOD.txt       Hướng dẫn cài mod vào thẻ nhớ / máy ảo
├─ glossary/                 Từ điển thuật ngữ (master.csv + <game>.csv)
├─ input/                    Khoá bóc ROM (prod.keys, titlekeys) — KHÔNG commit
├─ tools/                    Toàn bộ script dùng chung (bóc/dịch/build/QA) → xem tools/README.md
├─ games/                    Dữ liệu từng game (nguồn + bản dịch) — KHÔNG commit
│   └─ <TitleID>_<Tên>/
│       ├─ source/           Dữ liệu gốc bóc từ ROM (text gốc, font gốc…)
│       ├─ translations/     BẢN DỊCH TIẾNG VIỆT  ← SỬA Ở ĐÂY khi cần fix
│       ├─ font_edit/        (nếu có) font đã giải mã để vá — tái tạo được, KHÔNG commit
│       └─ README.md         Hướng dẫn + bài học riêng của game đó
└─ output/                   SẢN PHẨM: mod LayeredFS — copy vào thẻ nhớ
    └─ atmosphere/contents/<TitleID>/romfs/...
```

> **Repo GitHub chỉ chứa MÃ NGUỒN.** `.gitignore` chặn `output/`, `dump/`, `input/`,
> `games/*/{source,translations,font_edit}/` và ROM (`.nsp/.xci`) — sản phẩm và dữ liệu game
> không bao giờ được push.

---

## Các game trong dự án

| Game | TitleID | Engine | Trạng thái |
|---|---|---|---|
| Hogwarts Legacy | `0100F7E00C70E000` | Unreal Engine 4.27 | ✅ MAIN + SUB 100%, font VN, patch pak |
| Hades II | `0100A00019DE0000` | MonoGame (SJSON + SpriteFont XNB) | ✅ 100% |
| Nintendo Switch Sports | `0100D2F00D5C0000` | Nintendo EPD (MSBT/BFARC) | ✅ 100% |
| Ori and the Will of the Wisps | `01008DD013200000` | Unity IL2CPP | ✅ 100% |
| Ori and the Blind Forest DE | `010061D00DB74000` | Unity IL2CPP (BitmapFont) | ✅ 100% (font vá bằng atlas SDF) |
| Kirby and the Forgotten Land | `01004D300C5AE000` | Nintendo/HAL "basil" (MSBT/BFOTF) | ✅ 100% (ghép glyph từ chính font gốc) |
| It Takes Two | `010092A0172E4000` | Unreal Engine 4 | ✅ 100% (text trong pak) |
| MONOPOLY (2024) | `01002C201BC40000` | Unity IL2CPP (hệ "Oasis") | ✅ 100% (mod đặt ở cả base + update) |
| Unravel Two | `0100E5D00CC0C000` | Native Switch (Coldwood) | 🔄 đang làm (đang gỡ lỗi treo logo) |
| Super Mario Party Jamboree | `0100965017338000` | — | ⛔ đã bỏ (tool không đọc nổi RomFS) |

Chi tiết từng game (cấu trúc RomFS, định dạng text, cách build, việc còn lại): xem
`games/<TitleID>_<Tên>/README.md` và `docs/STATE.md`.

---

## Quy trình chuẩn (5 giai đoạn)

Toàn bộ quy trình được gói trong skill **`/dich`** (`.agents/skills/dich/SKILL.md`) — tự hành,
áp dụng cho mọi engine:

```
Giai đoạn 1  Nhận diện engine & khởi tạo   → bóc thử RomFS, xác định file rời vs UFS (pak), nạp glossary
Giai đoạn 2  Trích xuất & dịch đa luồng    → chia chunk + subagent song song, giữ 100% placeholder/tag
Giai đoạn 3  Vá font đồng bộ toàn diện     → thêm dấu tiếng Việt mà KHÔNG mất glyph icon
Giai đoạn 4  Đóng gói mod LayeredFS        → output/atmosphere/contents/<TitleID>/romfs/…
Giai đoạn 5  QA & bàn giao                 → CỔNG QA bắt buộc PASS rồi mới kết thúc
```

**Cổng QA bắt buộc trước khi bàn giao:**

```bash
python tools/qa_text.py --game <ten_game>     # phải in PASS
```

Cổng này đọc lại **thành phẩm đã build**, so với nguồn và bắt: thiếu/thừa key, chuỗi rỗng,
ký tự lạ (CJK/Hangul/Kana/Ả Rập/Nga), lệch tag & placeholder, mục `[error:…]`/`[KEY]`, sai `\n`,
mã điều khiển, và độ phủ font.

Chạy trọn quy trình cho 1 game (build → font → QA → glossary), dừng ngay nếu 1 bước lỗi:

```bash
python tools/pipeline.py <game>        # hoặc: python tools/pipeline.py all
```

---

## Bộ công cụ (`tools/`)

Bản đồ đầy đủ theo engine: **`tools/README.md`**. Vài nhóm chính:

- **Chung:** `qa_text.py` (cổng QA), `check_glossary.py`, `check_font_coverage.py`,
  `find_rom.py`, `archive_rom.py` (chuyển ROM ra khỏi OneDrive sau khi bóc), `report.py`, `pipeline.py`.
- **Unreal (Hogwarts, It Takes Two):** `ue_romfs_tool.py`, `avaf_codec.py`, `build_patch_pak.py`,
  `itt_uasset_tool/` (C# + UAssetAPI).
- **Unity (Ori, MONOPOLY):** `unity_text_tool.py`, `unity_bitmapfont.py`, codec `kit_*` (Unravel),
  `mono_*` (MONOPOLY).
- **Nintendo EPD / HAL (Switch Sports, Kirby):** `extract_msbt.py`, `build_mod.py`,
  `kirby_*` (font CFF/glyf, Filter.bin), `zs_util.py` (nén ZSTD khớp tham số gốc).
- **Supergiant (Hades II):** `hades2_sjson_helper.py`, `patch_hades2_xnb_font.py`.

> `tools/legacy/` = script **một lần** đã chạy xong (chứa nội dung dịch đã sinh ra file nguồn).
> Muốn sửa câu chữ thì sửa file trong `games/<TID>/translations/`, **không** sửa các file này.

---

## Cách dùng mod

1. Chép nguyên thư mục `output/atmosphere/` vào **gốc thẻ nhớ Switch** (gộp vào `atmosphere` có sẵn).
2. Trên máy ảo (Eden/yuzu): thêm `atmosphere/contents/<TitleID>` vào mục **Add-Ons** của game.
3. Một số game cần để **ngôn ngữ game = English** (ví dụ Ori, Kirby) để ra tiếng Việt — xem
   ghi chú trong `README.md` của game đó.

Chi tiết cài đặt: `docs/INSTALL-MOD.txt`.

> ⚠️ Nếu game có **bản update**, mod phải đặt ở **ID của bản update** (base `…000` → update `…800`).
> Ví dụ MONOPOLY: chép cả `01002C201BC40000/` **và** `01002C201BC40800/`.

---

## Khi bản dịch bị lỗi — sửa ở đâu?

1. Mở `games/<TitleID>_<Tên>/README.md` để biết file bản dịch + lệnh build tương ứng.
2. Sửa trực tiếp file JSON/SJSON/XML trong `games/<TitleID>_<Tên>/translations/`.
3. Chạy lại script build tương ứng trong `tools/`.
4. Chạy `python tools/qa_text.py --game <ten_game>` cho tới khi **PASS**.
5. Copy lại `output/atmosphere/...` vào thẻ nhớ (hoặc thư mục mod của máy ảo).

---

## Quy tắc bắt buộc

Xem `AGENTS.md`. Tóm tắt:

- **Ngữ cảnh là số 1** — dịch theo ngữ cảnh game thủ, văn phong tự nhiên, không word-by-word.
- **Giữ nguyên 100%** placeholder/control code: `{0}`, `%s`, `<i>…</i>`, `\n`, `[[…]]`, `{$…}`,
  `{!Icons…}`, mã nút bấm Switch…
- **Tôn trọng `glossary/`** — thuật ngữ thống nhất; phát hiện thuật ngữ mới thì cập nhật từ điển.
- **Không bao giờ thay hẳn font game** — phải giữ đủ glyph gốc (kể cả icon) rồi mới thêm dấu tiếng Việt.
- **Không tin script build, tin thành phẩm** — sau mỗi lần build phải mở lại file đã đóng gói để kiểm.

36 bài học xương máu + checklist bàn giao nằm ở **`docs/BAI-HOC.md`** (đọc trước khi build).
