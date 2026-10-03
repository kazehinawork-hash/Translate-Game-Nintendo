# Unravel Two (Nintendo Switch) — bản địa hóa tiếng Việt

**Title ID**: `0100E5D00CC0C000` (Base) / `0100E5D00CC0C800` (Update v65536, tên file `CR-33`)

## 1. Tổng quan kỹ thuật

| Hạng mục | Kết quả |
|---|---|
| ROM | `input/Unravel Two[0100E5D00CC0C000][US][v0].nsp` (2,81 GB) + update 20,5 MB |
| Bóc RomFS | ✅ **Được** — `python tools/ue_romfs_tool.py list "<nsp>"` → **22 file** |
| Engine | **Native Switch (NVN)**, engine riêng của Coldwood — **không** phải Unity/UE |
| Dữ liệu game | `NVNKits/Data.kit` (1,5 MB — bản mục lục) + `NVNKits/Data.kit.0` … `.kit.11` (~2,3 GB) |
| Âm thanh/Video | `NVN/Sounds/…`, `NVN/V/*.mp4` |
| Font | `fonts/unravel.fgen` (thấy trong dữ liệu; định dạng riêng, **chưa** giải mã) |
| Kiểu mod | Các file `.kit*` là **file rời trong RomFS** → **LayeredFS thay trực tiếp được**, KHÔNG cần patch pak ✅ |

## 2. Định dạng archive `.kit` — ĐÃ GIẢI MÃ (mức cơ bản)

Kiểm chứng thực tế trên `Data.kit.0`:

```
Record = [u32 compressed_len][LZ4 block]  →  giải nén ra JSON (CRLF + tab)
```

Ví dụ record đầu của `Data.kit.0`:

```
f0 04 7b 0d 0a 09 22 76 61 72 69 61 62 6c 65 73 ...   (LZ4 token 0xf0 + 4 → 19 byte literal)
```

Giải nén bằng `lz4.block.decompress(payload, uncompressed_size=4096)` → ra JSON hợp lệ:

```json
{
  "variables": { "speed": { "default": 0 }, "ext_speed": { "default": 1 }, "land": ...
```

→ Trong `Data.kit.0`: **665 record**, 309 record giải nén OK ở lần quét đầu (một phần record
cần đúng kích thước giải nén / có thể dùng codec khác — **cần hoàn thiện**).

## 3. Khoá text đã tìm thấy

Vùng ~`0x1EFA000` trong `Data.kit.0` chứa **nhãn giao diện**:

```
... Selector · Suggest · Left · PS4 · SecondPlay · Options · Pause · Resume · Lost ·
Trials · AssistMode · Volume · XBoxOne · Switch ...
```

Ngay sau đó là **bảng offset u32 tăng dần** (`0x78, 0xB4, 0x106, 0x113, 0x130, 0x169, …`)
→ đây là **bảng chuỗi UI** (index → chuỗi). Đây chính là nguồn text cần dịch.

## 4. Việc còn lại (Giai đoạn 2 → 5)

1. **Hoàn thiện codec `.kit`** (`tools/kit_codec.py`): xác định ranh giới record + kích thước
   giải nén chính xác (một số record bị lệch khi quét tuần tự).
2. Bóc toàn bộ chuỗi UI/hội thoại ra `source/`, dịch sang `translations/`.
3. Giải mã + vá font `fonts/unravel.fgen` (kiểm tra có đủ dấu tiếng Việt chưa).
4. Đóng gói lại `.kit` (LZ4) → `output/atmosphere/contents/0100E5D00CC0C000/romfs/NVNKits/`.
5. QA bằng `python tools/qa_text.py --game unravel`.

## 5. Ghi chú

- NSP này **đã giải mã** (không vướng titlekey như Super Mario Party Jamboree — xem BH-19).
- File `.fgen` là font riêng của engine; cần RE riêng nếu font gốc thiếu dấu tiếng Việt.

## Cách build lại

```bash
python tools/ue_romfs_tool.py extract "<rom trong input hoặc E:\ROM_Backup>" "NVNKits/Data.kit.0" "E:\UNR_work\Data.kit.0"
python tools/kit_codec.py "E:\UNR_work\Data.kit.0"
```
