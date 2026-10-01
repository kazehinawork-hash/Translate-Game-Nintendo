# Translate Game — Việt hóa game Nintendo Switch

Dự án bản địa hóa (localization) game Nintendo Switch sang tiếng Việt, đóng gói dưới dạng
**mod LayeredFS** cho Atmosphere CFW.

## Cấu trúc thư mục

```
Translate Game/
├─ AGENTS.md                 Quy tắc làm việc của dự án
├─ docs/
│   ├─ STATE.md              Trạng thái/tiến độ từng game  ← ĐỌC ĐẦU TIÊN
│   └─ INSTALL-MOD.txt       Hướng dẫn cài mod vào thẻ nhớ
├─ glossary/                 Từ điển thuật ngữ (master + từng game)
├─ input/                    Khoá (prod.keys, titlekeys) — KHÔNG commit
├─ tools/                    Toàn bộ script dùng chung (bóc tách/dịch/build/QA)
├─ games/                    Dữ liệu từng game (nguồn + bản dịch) — KHÔNG commit
│   └─ <TitleID>_<Tên>/
│       ├─ source/           Dữ liệu gốc bóc tách từ ROM (text gốc, font gốc…)
│       ├─ translations/     BẢN DỊCH TIẾNG VIỆT  ← SỬA Ở ĐÂY khi cần fix
│       └─ README.md         Hướng dẫn riêng cho game đó
├─ output/                   SẢN PHẨM: mod LayeredFS — copy vào thẻ nhớ
│   └─ atmosphere/contents/<TitleID>/romfs/...
└─ archive/                  File cũ/không dùng nữa (có thể xoá bất cứ lúc nào)
```

> `games/` và `output/` bị `.gitignore` chặn — repo GitHub chỉ chứa mã nguồn.

## Các game trong dự án

| Game | TitleID | Trạng thái |
|---|---|---|
| Hogwarts Legacy | `0100F7E00C70E000` | MAIN + SUB 100%, font VN, patch pak |
| Hades II | `0100A00019DE0000` | 100% |
| Nintendo Switch Sports | `0100D2F00D5C0000` | 100% |

## Cách dùng mod

Chép nguyên thư mục `output/atmosphere/` vào **gốc thẻ nhớ Switch** (gộp vào `atmosphere` có sẵn).
Chi tiết: `docs/INSTALL-MOD.txt`.

## Khi bản dịch bị lỗi — sửa ở đâu?

1. Mở `games/<TitleID>_<Tên>/README.md` để biết file bản dịch và lệnh build tương ứng.
2. Sửa trực tiếp file JSON/SJSON trong `games/<TitleID>_<Tên>/translations/`.
3. Chạy lại script build tương ứng trong `tools/`.
4. QA rồi copy lại `output/atmosphere/...` vào thẻ nhớ.

## Quy tắc bắt buộc

Xem `AGENTS.md`. Tóm tắt: giữ nguyên 100% placeholder/control code (`{0}`, `%s`, `<i>…</i>`,
`\n`, `[[…]]`, mã nút Switch…), dịch theo ngữ cảnh (không word-by-word), tôn trọng `glossary/`.
