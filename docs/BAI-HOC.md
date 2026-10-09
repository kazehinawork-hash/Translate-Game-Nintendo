# BÀI HỌC KINH NGHIỆM — Dự án Việt hóa Game Nintendo Switch

> Tài liệu này ghi lại **tất cả lỗi đã từng xảy ra thật** trong dự án, nguyên nhân gốc, cách phát hiện
> và **quy tắc chống lặp**. Đọc trước khi build, và chạy `python tools/qa_text.py` trước khi bàn giao.
>
> Cập nhật lần cuối: sau khi hoàn thành 4 game (Switch Sports, Hades II, Hogwarts Legacy, Ori and the Will of the Wisps).

---

## PHẦN 1 — 12 BÀI HỌC XƯƠNG MÁU

### BH-01. Script build đọc SAI đường dẫn → đóng gói dữ liệu GỐC mà không báo lỗi ⚠️ NẶNG NHẤT

- **Triệu chứng (Hogwarts):** trong game phụ đề vẫn **100% tiếng Pháp**, dù bản dịch đã xong 26.296/26.296 chuỗi.
  Script vẫn in `SUB entries: 35431` trông rất bình thường.
- **Nguyên nhân gốc:** `build_hogwarts_sub.py` glob ở `source/split_tasks/sub_trans/` (**không tồn tại**)
  thay vì `translations/sub_trans/`. `glob` trả về **danh sách rỗng**, `id2vi` rỗng, và code có dạng
  `val = id2vi.get(id) or <ban_goc>` → **âm thầm rơi về tiếng Pháp**.
- **Cách phát hiện:** build xong phải **đọc lại file đã đóng gói** và đếm xem bao nhiêu chuỗi khác nguồn.
- **QUY TẮC CHỐNG LẶP:**
  1. **Mọi script build phải in số lượng input đã nạp** (`Ban dich: 26296/26296`).
  2. **Nạp 0 file / thiếu bản dịch → in CẢNH BÁO hoặc `raise`**, tuyệt đối không im lặng.
  3. **Không dùng `x or fallback` cho dữ liệu dịch** khi chưa kiểm tra `x` có tồn tại.
  4. Sau build, chạy `tools/qa_text.py` — nó so bản đã đóng gói với nguồn và **báo % đã dịch**.

### BH-02. Công cụ nén/đóng gói ghi SAI MAGIC → game hiện `[KEY]` toàn bộ

- **Triệu chứng (Hogwarts):** vào game mọi chuỗi hiện dạng `[MENU_INVERTCAMERACONTROLSX]`.
- **Nguyên nhân gốc:** `avaf_codec.py` ghi magic `AVAFDICT 2.0` bằng **ASCII**, nhưng file gốc của game
  dùng **UTF-16LE** (`41 00 56 00 41 00…`, 32 byte).
- **QUY TẮC CHỐNG LẶP:** với mọi codec (AVAFDICT, MSBT, SARC, SJSON, unity3d…), **luôn kiểm tra roundtrip**:
  `pack(unpack(file_goc)) == file_goc`. Không đạt → codec sai, không được build.

### BH-03. File rời trong `romfs/` bị engine bỏ qua (Unreal mount pak trước)

- **Triệu chứng (Hogwarts):** đã đặt `MAIN-*.bin` trong `romfs/.../Localization/SWITCH/` nhưng game **không đổi**.
- **Nguyên nhân gốc:** các file đó là **UFS (nằm trong `pakchunk0-Switch.pak`)**, không có trong
  `Manifest_NonUFSFiles_Switch.txt`. UE mount `.pak` **trước** RomFS → file rời vô hiệu.
- **QUY TẮC CHỐNG LẶP:** trước khi hứa "LayeredFS chạy được", **kiểm tra file đích có trong
  `Manifest_NonUFSFiles_<Platform>.txt` / `Manifest_DebugFiles_<Platform>.txt`** hay không.
  Không có → phải đóng **patch pak** (`pakchunkX-Switch_p.pak`).

### BH-04. Nhận diện text bằng "giá trị magic" cứng → SÓT hàng trăm mục

- **Triệu chứng (Ori):** dịch xong 1.579 mục tưởng là hết; thực tế **sót 298 mục hội thoại** (data_249: 68/151).
- **Nguyên nhân gốc:** sau tên `...TextMessageProvider` tôi chỉ chấp nhận cờ `= 1`, nhưng thực tế cờ có thể
  là `1`, `2`, hoặc **không có**.
- **QUY TẮC CHỐNG LẶP:**
  1. **Không hardcode giá trị "magic"** khi parse nhị phân — thử lần lượt các khả năng và xác thực kết quả
     (chuỗi in được + có chữ cái).
  2. Sau khi trích xuất phải chạy **"soát rò rỉ"**: quét toàn bộ file tìm chuỗi giống câu (≥3 từ) **không nằm
     trong tập đã trích** → nếu còn nhiều, pattern còn sai.

### BH-05. Regex chỉ phủ một phần dải ký tự → bỏ sót / báo nhầm

- **Đã từng dính:** regex chỉ CJK **bỏ sót Hangul** (`촉` lọt vào bản dịch MAIN).
  Lần khác: bộ ký tự tiếng Việt **thiếu dấu** → báo nhầm 225 chuỗi tiếng Việt thành "chưa rõ".
- **QUY TẮC CHỐNG LẶP:** khi quét "ký tự lạ" phải phủ **đủ** các dải:
  CJK `\u3000-\u303f,\u3400-\u4dbf,\u4e00-\u9fff,\uf900-\ufaff,\uff00-\uffef`,
  Hangul `\u1100-\u11ff,\u3130-\u318f,\uac00-\ud7ff`, Kana `\u3040-\u30ff`,
  Ả Rập `\u0600-\u06ff`, Cyrillic `\u0400-\u04ff`.
  Và bộ ký tự tiếng Việt phải đủ: `ă â đ ê ô ơ ư` + **tất cả** nguyên âm có dấu thanh.
  → Dùng `tools/qa_text.py` (đã có sẵn bộ ký tự đầy đủ) thay vì tự viết regex.

### BH-06. Dịch từ ngôn ngữ đã "bản địa hóa tên riêng" → tên sai (Pháp hóa)

- **Triệu chứng (Hogwarts):** game hiện `Adélaïde Duchêne`, `Aile-Céleste`, `Pont-Désir`, `Fléreur`,
  `Lépouvantail`, `Roland`, `Bubobulb`, `Murlap`… trong khi MAIN lại dùng tên gốc.
- **Nguyên nhân gốc:** SUB dịch **từ tiếng Pháp**; tiếng Pháp đã Việt hóa/Pháp hóa tên riêng
  (`Deek→Cheek`, `Sallow→Pallow`, `Spintwitches→Bôbalais`, `Hogsfield→Campolard`…).
- **QUY TẮC CHỐNG LẶP (đã kiểm chứng hiệu quả 100%):**
  1. **Tuyệt đối không đoán tên.** Dùng **cột ngôn ngữ song song** (ES) để tra ngược tên gốc.
  2. Thuật toán: tìm từ **có trong `Source_FR`** và **KHÔNG có trong `Source_ES`** → danh sách nghi vấn.
  3. Đối chiếu tiếp với **phần đã dịch từ ngôn ngữ khác** (MAIN dịch từ tiếng Trung) → chốt tên đúng.
  4. Công cụ: `tools/fix_hogwarts_fr_names.py` (bảng ánh xạ) — mẫu để viết cho game khác.

### BH-07. Lỗi hiển thị `[error:...]` / `[KEY]` có sẵn trong nguồn — vá được nhờ key anh em

- **Triệu chứng (Hogwarts):** menu hiện `[error:Menu_Hair]`, hoạt động hiện `Làm mới sau [error:time]`,
  nhiệm vụ hiện `[error:Hamelt_Halkirk]`, và 1 mục hiện `[ZSI_01_01_DADASide_Title]`.
- **Nguyên nhân:** key tham chiếu bị **gõ sai / thiếu** trong dữ liệu gốc (cột tiếng Trung cũng lỗi y hệt).
- **QUY TẮC CHỐNG LẶP:**
  1. Quét `\[error:` và `^\[[A-Za-z0-9_]+\]$` trên **toàn bộ** MAIN/SUB.
  2. **Suy giá trị đúng từ key anh em**: `Menu_Hairstyle`→"Kiểu Tóc", `Data_ExpiresIn` dùng `{time}`
     nên `Data_RefreshesIn` cũng phải `{time}`, các key `FGC_*` dùng `{0}` chứ không phải `%d`.
  3. Công cụ: `tools/fix_hogwarts_main_errors.py`.

### BH-08. Font: thay cả font → MẤT GLYPH ICON

- **Triệu chứng (Ori):** nếu thay hẳn `keyboard`/`moon-tools` bằng Lato thì các **icon** trong game biến mất.
- **Nguyên nhân:** 2 font đó chứa **glyph PUA (Private Use Area)** đang được game dùng thật (~100 lần/bundle).
- **QUY TẮC CHỐNG LẶP:**
  1. Trước khi thay font phải kiểm: số glyph, **số glyph PUA**, `unitsPerEm`, atlas tĩnh hay động.
  2. Font **có PUA đang dùng** → **HỢP NHẤT** (`tools/merge_vi_font.py`) chứ không thay hẳn.
  3. Phải kiểm **độ phủ ký tự của bản dịch** bằng `tools/check_font_coverage.py` → phải PASS.

### BH-09. Game không có slot tiếng Việt

- **Đã gặp (Ori):** mỗi chuỗi có 20 ngôn ngữ, **không có tiếng Việt**.
- **QUY TẮC:** ghi đè lên **slot tiếng Anh**, và **phải nói rõ với người dùng: đặt ngôn ngữ game = English**.
  (Hogwarts thì ngược lại: patch pak chứa **cả 14 ngôn ngữ** nên console để ngôn ngữ nào cũng ra tiếng Việt.)

### BH-10. Kiểm tra bằng "đọc lại thành phẩm", không tin script build

- **Đã gặp:** script in "thành công" nhưng thành phẩm sai (BH-01), hoặc mod cũ vô hiệu vì magic sai (BH-02).
- **QUY TẮC CHỐNG LẶP — bắt buộc sau MỖI lần build:**
  1. **Mở lại file đã đóng gói** bằng chính codec đọc.
  2. So **multiset tag/placeholder** với nguồn.
  3. Đếm **bao nhiêu chuỗi khác nguồn** (đã dịch) và **bao nhiêu giống nguồn** (chưa dịch).
  4. So **số object / số entry** với bản gốc (không được thay đổi).
  5. Kiểm **font phủ đủ ký tự**.
  → `python tools/qa_text.py` làm tất cả các việc trên.

### BH-11. Chia việc cho subagent quá lớn → lỗi/truncate

- **Đã gặp (Hogwarts):** chunk 500 dòng làm subagent lỗi/truncate.
- **QUY TẮC:** nhãn UI ngắn **300–400 chuỗi/chunk**; hội thoại dài **200–250 chuỗi/chunk**.
  Chunk nào lỗi lặp lại → **tách đôi/tư** rồi chạy lại. Gộp chuỗi trùng để tiết kiệm 20–40% công.

### BH-12. Môi trường & quy trình

- **PowerShell + chuỗi tiếng Việt trong `python -c "..."`** bị hỏng ký tự → **luôn viết script ra file** rồi chạy.
- **`\n` literal (2 ký tự) vs xuống dòng thật**: phải so **cả hai chiều** với nguồn (đã từng dính 47 mục).
- **Không xoá dữ liệu nặng khi chưa hỏi.** Dữ liệu game (`games/`) và thành phẩm (`output/`) **không commit**
  (`.gitignore`); chỉ commit **mã nguồn** (`tools/`, `docs/`, `glossary/`, skill).
- **Chỉ `git push` khi người dùng yêu cầu.**

### BH-13. Đường dẫn TƯƠNG ĐỐI cũ còn sót sau khi tái cấu trúc → script build chết

- **Triệu chứng (Hades II):** chạy `build_hades2_mod.py` báo *"Không tìm thấy thư mục bản dịch:
  translations/0100A00019DE0000_Hades2"* — thư mục đó **không còn tồn tại** từ khi chuyển sang
  `games/<TID>/translations/`. Tương tự `build_font.py` trỏ vào `orig_font/Font/…` (không có).
- **Hậu quả:** mod Hades II **không thể build lại**; muốn sửa bản dịch cũng chịu.
- **QUY TẮC CHỐNG LẶP:**
  1. Mọi script build phải dựng đường dẫn từ **gốc dự án**:
     `ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))` rồi ghép `ROOT`.
  2. Sau khi tái cấu trúc thư mục → **rà soát lại toàn bộ đường dẫn**:
     `grep -n "['\"](translations|working|output|games|source)/" tools/*.py`
  3. `tools/pipeline.py` sẽ chạy thử từng bước nên lỗi kiểu này lộ ra ngay.

### BH-14. Cổng QA phải được HIỆU CHỈNH để không "kêu oan"

- **Đã gặp khi mới làm `qa_text.py`:** báo FAIL 15.000 lỗi giả ở Switch Sports vì coi **mã điều khiển
  Nintendo** (`\u000e…`, glyph icon `\ue0ab`) là "ký tự lạ"; báo sai cả khi `|plural(one=nội dung,
  other=…)` được dịch (regex bắt cả phần nội dung).
- **QUY TẮC:**
  1. Ký tự/tag chỉ bị coi là lỗi khi **LÀ MỚI so với nguồn** (so multiset với nguồn, không so tuyệt đối).
  2. Regex bắt placeholder phải bắt **phần đánh dấu**, không bắt nội dung bên trong.
  3. Phân mức: **LỖI** (chặn bàn giao) vs **CẢNH BÁO** (cần xem, không chặn).
     Hiện CẢNH BÁO gồm: khác số dòng, khác mã điều khiển/ngắt dòng, thừa key, rỗng-cả-nguồn.
  4. Trước khi tin cổng QA, phải **mở 1-2 ca cụ thể ra xem tận mắt** (như đã làm với Switch Sports:
     kiểm tra thấy khác biệt chỉ là ngắt dòng, không phải icon → mới hạ xuống cảnh báo).

### BH-15. Thay font KHU VỰC (Trung/Hàn/Nhật) → người chơi ngôn ngữ đó MẤT CHỮ

- **Triệu chứng (Switch Sports):** 4 file font trong mod **giống hệt nhau** (cùng MD5) và chỉ **139 KB**,
  trong khi font gốc là **4 file khác nhau, 10–13 MB**. Tức là đã thay cả font Hán/Hàn bằng font Latin.
- **Hậu quả:** ai để console ở tiếng Trung/Hàn/Nhật sẽ thấy ô vuông (mất glyph).
- **Nguyên nhân:** `build_custom_font.py` đưa cả 3 glyph font CJK (`DFP_GBZY7_CNzh`, `DFPT_ZY5_TWzh`,
  `AsiaKTITGD4-R_KRko`) vào danh sách thay thế, rồi **copy đè** sang `Font_CNzh/KRko/TWzh`.
- **Cách kiểm chứng (đã làm):** giải mã BFTTF gốc (XOR key `2785117442`, magic `0xD99B871A`) rồi so
  bảng mã: font Latin gốc có **0 glyph PUA**, font Hàn **964 PUA**, font Trung **127 PUA**
  → icon nằm ở font khu vực, KHÔNG phải font Latin.
- **QUY TẮC CHỐNG LẶP:**
  1. Mod chỉ dịch **một khe ngôn ngữ** thì **chỉ thay font của khe đó**; các font khu vực khác giữ nguyên.
  2. Kiểm tra "mod có thay font nào" bằng cách so **MD5 + kích thước** với bản gốc — trùng nhau hàng loạt là dấu hiệu sai.
  3. Trước khi thay font, đếm **glyph PUA** của font gốc: nếu font gốc CÓ PUA thì phải **hợp nhất**
     (`tools/merge_vi_font.py`), không được thay hẳn.

### BH-16. `move` trên file OneDrive báo THÀNH CÔNG nhưng KHÔNG chuyển gì

- **Triệu chứng:** chuyển ROM từ `input/` (trong OneDrive) sang `E:\ROM_Backup` bằng `Move-Item` →
  không báo lỗi, SHA256 "khớp", nhưng **file vẫn nằm nguyên trong `input/`** và thư mục đích **rỗng**.
- **Nguyên nhân:** file trong OneDrive là **reparse point** (Files On-Demand) — thao tác move bị
  sync engine của OneDrive nuốt.
- **QUY TẮC CHỐNG LẶP:**
  1. Với file trong OneDrive, **không dùng `move`** — dùng **copy → xác minh SHA256 → mới xoá** bản nguồn.
  2. Luôn kiểm chứng lại bằng lệnh **độc lập** (`cmd /c dir /a`) sau khi thao tác, đừng tin mỗi exit code.
  3. Công cụ có sẵn: `python tools/archive_rom.py` (làm đúng quy trình trên, tự chọn thư mục theo TitleID).
- **Quy tắc dự án kèm theo:** ROM chỉ nằm trong `input/` trong lúc bóc dữ liệu; **bóc xong phải chuyển
  ra `E:\ROM_Backup\<Tên game>\`**. `tools/find_rom.py` tìm cả 2 nơi nên vẫn bóc lại được khi cần.

### BH-18. Vá font BITMAP (bảng glyph + atlas SDF) — cách làm đã kiểm chứng

Áp dụng cho Ori and the Blind Forest (Moon Studios `BitmapFont`). **Đã làm xong và kiểm chứng bằng ảnh.**

- **Phát hiện chìa khoá:** atlas **không** tham chiếu từ font (không có PPtr nào — đã kiểm tra toàn bộ file);
  engine ghép **theo TÊN**: Texture2D `<tên font>_0 distance map` (ví dụ `candara_0 distance map`).
  Các Material "Font Material" có `_MainTex = null` → gán lúc chạy.
- **Định dạng bảng glyph:** `[header][tên][block: int32 count + count×entry 48B][float metric]`,
  entry = `[int32 mã ký tự]` + 11 float: `f0,f1 = u0,u1`, `f2,f3 = v0,v1` (**gốc dưới → phải lật**),
  `f4 = độ lệch ngang`, `f5..f8 = quad lấy mẫu SDF`.
- **Atlas là ảnh Alpha8**: khi decode ra RGBA thì **giá trị nằm ở kênh ALPHA** (đọc kênh L sẽ ra toàn 0 — đã dính).
- **Cách vá an toàn (khuyên dùng, không phải mở rộng atlas):**
  1. Xác định ký tự cần thêm = (ký tự bản dịch dùng) − (ký tự font có).
  2. **Mượn ô của glyph không dùng** (chọn ký tự font CÓ mà bản dịch KHÔNG dùng, cùng kiểu hoa/thường, ô đủ lớn)
     → không phải đổi kích thước atlas, **không phải dịch chuyển toàn bộ entry cũ**.
  3. Vẽ glyph mới (từ TTF, cỡ em đo từ atlas: cap-height/x-height) vào đúng ô đó, làm mềm nhẹ cho giống SDF.
  4. **Đổi mã ký tự** trong entry sang ký tự mới.
- **Kiểm chứng bắt buộc:** cắt vùng ô ra **ảnh** rồi **xem bằng mắt** (đã dùng cho cả lúc giải mã lẫn lúc sinh glyph);
  và kiểm tra ký tự bị mượn ô **không xuất hiện trong text game** (ở Blind Forest: text tiếng Anh chỉ có `’`).

### BH-17. Kiểm tra ĐỘ PHỦ FONT ngay từ Giai đoạn 1 (đừng đợi dịch xong mới phát hiện)

- **Đã gặp (Ori and the Blind Forest DE):** dịch xong 100% (659 chuỗi) mới phát hiện game dùng
  **BitmapFont** (bảng glyph nhị phân + **texture atlas 2048×2048**), và font `candara` chỉ có
  **25/74** ký tự tiếng Việt — thiếu toàn bộ chữ **2 dấu/dấu nặng** (`ắ ầ ậ ệ ộ ớ ợ ự ỵ`…).
  Vá font kiểu này phải **vẽ thêm glyph vào atlas** → chi phí lớn, không như thay file `.ttf`.
- **Hậu quả:** bản dịch xong nhưng **mod chưa dùng được**; nếu chép vào máy sẽ thấy ô trống ở chữ có dấu.
- **QUY TẮC CHỐNG LẶP:**
  1. Ở **Giai đoạn 1**, sau khi nhận diện engine, **kiểm tra ngay font**: loại font (TTF động / BitmapFont /
     SpriteFont / BFARC), số glyph, **có dấu tiếng Việt chưa**, có glyph **PUA (icon)** không.
  2. Nếu font thiếu dấu → **đánh giá chi phí vá TRƯỚC khi dịch** và báo người dùng biết đây là phần nặng.
  3. Thứ tự ưu tiên vá font: (a) thay `.ttf` rời → (b) **hợp nhất** giữ icon → (c) vẽ thêm glyph vào atlas
     (nặng nhất, chỉ làm khi (a)/(b) bất khả thi).
  4. Với font bitmap: tìm **atlas texture** + **bảng glyph** qua typetree IL2CPP
     (`tools/extract_il2cpp.py` bóc `main` + `global-metadata.dat`), rồi mới tính chuyện vẽ thêm.

### BH-19. Game MỚI có thể vượt khả năng bộ tool — kiểm tra "bóc được RomFS chưa" NGAY

**Ca thật: Super Mario Party Jamboree (10/2024) — dự án quyết định BỎ, không dịch.**

- **Đã tìm ra:** NCA3, SDK 17.5.4, Master Key Revision 0x11; **titlekey nằm dạng THÔ ngay trong ticket**
  của NSP (`tik[0x180:0x190]` = titlekey, KHÔNG mã hoá bằng titlekek — ticket loại "không ký").
  hactool với `--titlekey=` đó **giải mã NCA thành công** (hết "section corrupted") → **keys của người dùng đủ dùng**.
- **Chặn thật:** **không tool nào đọc được bảng RomFS** của game này:
  `hactool` → *"Failed to read RomFS directory cache!"*; `nsz` → lỗi đọc section; `ue_romfs_tool` → 0 file.
  (RomFS có offset metadata **vượt 4 GB** — bộ tool hiện tại chưa xử lý được.)
- **BÀI HỌC 1 (quy trình):** ở **Giai đoạn 1**, sau khi có ROM phải chạy thử
  `python tools/ue_romfs_tool.py list "<rom>"` — **nếu ra 0 file thì DỪNG và báo ngay**, đừng đi tiếp.
  Kiểm tra này mất 1 giây nhưng tiết kiệm rất nhiều thời gian.
- **BÀI HỌC 2 (kỹ thuật):** offset trong bảng **PFS0 của NSP là TƯƠNG ĐỐI** — phải cộng
  `0x10 + count*0x18 + strtab_size` mới ra vị trí thật của NCA (tôi từng trích sai vì tưởng tuyệt đối).
- **BÀI HỌC 3 (kỹ thuật):** NSP có nhiều loại ticket; **ticket không ký lưu titlekey dạng thô** —
  khi đó `titlekek` trong `prod.keys` **không dùng để giải mã titlekey** được (thử cả 22 khoá đều sai là dấu hiệu).
- **Hướng xử lý khi gặp lại:** (1) xin **NSP đã giải mã (decrypted)** của game → chạy thẳng;
  (2) hoặc tự viết module giải mã NCA + đọc RomFS (titlekey đã biết thì làm được, nhưng là việc lớn).

### BH-20. THAY HẲN font game = mất hàng nghìn glyph → UI (tỷ số) không hiện

**Ca thật: Nintendo Switch Sports — UI tỷ số không hiển thị (người dùng báo 03/10).**

- **Nguyên nhân gốc:** `tools/build_custom_font.py` **thay hẳn** 4 font Latin của Nintendo
  (`scft/VDL-LOGOG-BOLD.bfotf`, `VDL-LOGOG-ULTRA`, `VDL-GigaJr-ExtraBold-003_Gaiji`, `VDL-GigaJr-Ultra`)
  bằng **Nunito** (TTF 132 KB), làm **mất 7.888 / 8.207 glyph (96%)**:
  - font gốc: **8.207 glyph** (OTTO/CFF), phủ U+0000–U+FFE8
  - font mod: **938 glyph** (TTF/glyf)
  - mất trọn các nhóm: **fullwidth/halfwidth 164/164**, **số trong vòng 76/76**,
    mũi tên 13/13, hình khối 20/20, CJK punctuation 27/27
  → UI tỷ số (dùng glyph số/ký hiệu đặc biệt) **không còn gì để vẽ**.
- **BÀI HỌC 1:** **Không bao giờ thay hẳn font game.** Phải **hợp nhất** (giữ toàn bộ glyph gốc + thêm
  glyph tiếng Việt) — đúng như BH-8 đã ghi, nhưng lần này bị vi phạm.
- **BÀI HỌC 2 (cách kiểm tra BẮT BUỘC trước khi chốt font):** đếm và **so sánh số glyph** giữa
  font gốc và font trong mod; **liệt kê glyph bị mất theo nhóm**. Nếu mất > 0 ở nhóm UI
  (số, mũi tên, hình khối, fullwidth) → **KHÔNG được chốt**.
- **BÀI HỌC 3 (kỹ thuật):** `.bfotf` của Nintendo = **OTF bọc XOR** (magic `D99B871A`,
  key `2785117442`, XOR từng word 4 byte) → **giải mã/đóng gói đối xứng**.
  Font gốc là **OTTO/CFF**, Nunito là **TTF/glyf** → `fontTools.merge.Merger` **KHÔNG hợp được**
  hai loại khác nhau; muốn hợp nhất phải chuyển CFF→glyf trước (`Cu2QuPen` + `TTGlyphPen`,
  rồi cập nhật `glyphOrder` + `hmtx` cho glyph mới).
- **BÀI HỌC 4 (cách làm ĐÚNG — đã áp dụng và PASS):** dùng một font có độ phủ rộng
  (**Arial Unicode MS** — 38.928 glyph, có fullwidth/circled/arrows/shapes + tiếng Việt),
  rồi **subset** lại với danh sách = *cmap font gốc* ∪ *mọi ký tự THỰC DÙNG trong bản dịch*.
  ⚠️ Nếu chỉ lấy theo cmap gốc sẽ **thiếu ký tự** — lần đầu làm vậy nên sót **16 ký tự HOA
  tiếng Việt** (`Ơ Ư Ả Ấ Ậ Ắ Ề Ể Ồ Ổ Ộ Ớ Ờ Ở Ợ Ủ`) mà bản dịch lại có dùng.
  Kết quả sau khi sửa: font mod **8.334 glyph** (gốc 8.207), SARC **7,03 MB** (gốc 10,08 MB).
- **Trạng thái:** ✅ **ĐÃ SỬA XONG** — tool `tools/patch_font_switchsports.py`; soát lỗi: `tools/qa_switchsports.py`.

### BH-21. Nintendo First-Party (Kirby): `.cmp` = zstd, `.bfotf` = OTF bọc XOR — và bẫy "dò khoá vòng tròn"

**Ca thật: Kirby and the Forgotten Land (05/10).**

- **`.cmp`** = `[u32 uncompressed_size][zstd frame]` (magic zstd `28 b5 2f fd`).
- **`.bfotf`** (bên trong `.cmp`) = `[u32 magic][u32 ?][từng word 4 byte ^ key] → OTF`.
  Kirby dùng magic **`0x36F81A1E`** (Switch Sports dùng `0xD99B871A`) → **magic khác nhau theo game**.
- 🐞 **BẪY NẶNG (đã dính và sửa):** dò khoá bằng cách "thử XOR rồi xem 4 byte đầu có ra `OTTO` không"
  là **vòng tròn** — vì khoá được suy ra từ chính 4 byte đó, nên nhánh `OTTO` **luôn** cho ra `OTTO`
  kể cả khi font thật là **TTF** (`00 01 00 00`). Kết quả: gói lại font bằng **sai khoá** → file hỏng,
  game không đọc được (`KeyError: 'cmap'`, số bảng trong header vô lý ~20.000).
  **Cách đúng:** với mỗi khoá ứng viên, **thử parse font** (`TTFont(...).getBestCmap()`) — khoá nào
  cho ra font đọc được mới là khoá đúng. Sau khi gói **phải đọc lại** để xác nhận.
- **MSBT:** `\0` ở cuối chuỗi bị coi là ký tự kết thúc → nếu bản dịch **kết thúc bằng thẻ điều khiển
  chứa `\0`** thì byte cuối bị mất (game đọc thẻ cụt). Cách sửa: thêm khoảng trắng sau thẻ cuối.
- **Cấu trúc chuẩn first-party:** text ở `msg/<GameTag>/<LANG>/*.msbt` (13 ngôn ngữ), font ở
  `font/ScalableFontBin/*` — **chỉ vá các khe Latin**, giữ nguyên JP/CN/TW/KR để không phá font khu vực.
- **Font gốc là OTF (CFF)** → `Merger` không hợp được với TTF; dùng cách của BH-20 (subset Arial Unicode MS)
  → Kirby: 11 font Latin, mỗi font giữ ~8.049 glyph (gốc 8.207, phần "mất" là ký tự điều khiển 0x00–0x1D,
  không phải glyph hiển thị).

### BH-22. Glossary: phải nạp + tạo **TRƯỚC** khi dịch, và đừng "thống nhất máy móc" theo ngữ cảnh

**Ca thật: Kirby and the Forgotten Land (05/10).**

- 🐞 **Lỗi quy trình:** bỏ qua bước 3 Giai đoạn 1 (nạp `glossary/master.csv`) và **không tạo glossary
  cho game mới** → dịch xong 2.508 chuỗi mới phát hiện **7 câu nguồn bị dịch 2 kiểu** và thuật ngữ
  chính (`Mouthful Mode`) tồn tại **2 cách** ("giữ tiếng Anh" vs "Chế Độ Há Miệng").
  → **Bắt buộc:** trước khi giao subagent, tạo `glossary/<game>.csv` + đưa danh sách thuật ngữ vào
  prompt của subagent. Sau khi dịch, chạy kiểm tra **cùng câu nguồn → cùng bản dịch**.
- ⚠️ **Bẫy ngược lại — KHÔNG thống nhất máy móc:** khi thấy cùng câu nguồn dịch 2 kiểu, phải **xem
  ngữ cảnh từng chỗ**. Ví dụ thật:
  - `Listen` — nút thường = "Nghe", nhưng `Btn_Continue` (ý "nghe tiếp") = "Nghe tiếp".
  - `Look` — hướng dẫn = "Nhìn", nhưng `Figure.$View` (ngắm tượng) = "Ngắm".
  - `Fish` — tên loài = "Cá", hướng dẫn câu cá = "Câu cá".
  Thống nhất máy móc 3 chỗ này **làm hỏng** bản dịch; phải ghi **ngoại lệ theo key** vào glossary.
- **Cách kiểm tra dùng được:** `tools/kirby_glossary_check.py` + `tools/kirby_terms.py` — gom
  `en → {các bản dịch}` và liệt kê câu nguồn có >1 bản dịch, kèm **ngữ cảnh (file/key)** để phán đoán.
- **QA đúng cách:** lệch **số lượng `\n`** là **cảnh báo** (xuống dòng lại cho tiếng Việt), không phải
  lỗi; chỉ lệch **các mã điều khiển khác** mới tính là lỗi. (Bản QA đầu của Kirby báo nhầm 7 lỗi vì
  tính cả `\n` và cả ký tự PUA nằm trong thẻ.)

### BH-23. Asset UE4 nhị phân (It Takes Two): máy có .NET thì dùng UAssetAPI, đừng tự viết parser

**Ca thật: It Takes Two (05/10). Engine Unreal Engine 4 (Hazelight, codename "Nuts").**

- **Text không nằm trong `.locres`** (chỉ có locres của Engine) → nằm trong **asset UE4 nhị phân**:
  `Nuts/Content/Untold/StringTables/ST_UTG_*.uasset` (menu/UI) và
  `Nuts/Content/Cinematics/Subtitles/Generated/*.uasset` (588 file phụ đề, struct `HazeSubtitleAsset`).
  Tất cả **trong pak** (UFS) → vẫn là mod LayeredFS nhưng phải đóng **patch pak**.
- ⚠️ **BÀI HỌC 1 — KIỂM TRA `.NET` TRƯỚC KHI ĐỊNH TỰ VIẾT PARSER.** Máy đã có **.NET 10.0.400** nên
  dùng được **UAssetAPI** (thư viện chuẩn đọc/ghi asset UE4 4.13→5.7). Tự viết parser là **không cần thiết**.
- 🐞 **BÀI HỌC 2 — asset `cooked` là UNVERSIONED → PHẢI chỉ định `ObjectVersion` thủ công.**
  `new UAsset(path, EngineVersion.VER_UE4_27)` ném lỗi
  *"Cannot begin serialization of an unversioned asset before an object version is manually specified"*.
  Cách đúng (constructor 6 tham số):
  ```csharp
  new UAsset(path, ObjectVersion.VER_UE4_AUTOMATIC_VERSION /* =522, UE4.27 */,
             ObjectVersionUE5.<đầu tiên>, new List<CustomVersion>(), null, CustomSerializationFlags.None)
  ```
  Đối chiếu số: **UE4.27 = ObjectVersion 522**, 4.26 = 521? (tra bảng enum theo **giá trị**, tên enum
  không chứa "4_27" như dễ đoán — phải dò theo số).
- ⚠️ **BÀI HỌC 3 — CLI của UAssetGUI KHÔNG đặt được ObjectVersion** (`tojson <in> <out> <ver>` thiếu
  tham số này) → thất bại và **mở giao diện**; gọi sai tham số cũng mở GUI (dễ tưởng lỗi khác).
  Muốn dùng thì viết công cụ C# nhỏ gọi thẳng UAssetAPI (xem `tools/itt_uasset_tool/`).
- ✅ **BẮT BUỘC kiểm `roundtrip`** trước khi dịch: đọc → `SerializeJson` → `DeserializeJson` → `Write`
  → đọc lại. Đã kiểm: 618 byte → 618 byte, JSON giống hệt → mới tin được.

### BH-24. 🐞 ĐỪNG đặt tên script tạm trùng module chuẩn Python — nó CHE mất module thật

**Ca thật: MONOPOLY (05/10).** Trong thư mục scratchpad có file **`inspect.py`** (script tạm tôi tạo ở lượt trước).
Vì Python đặt **thư mục chứa script lên đầu `sys.path`**, mọi `import inspect` (thư viện chuẩn) đều lấy file đó →
hậu quả:
- `import UnityPy` (bên trong nó import `inspect`) → **chạy nhầm script cũ**, in ra output của việc khác hoàn toàn
  (mất gần 10 phút mới hiểu vì tưởng "output bị lặp").
- `fontTools` báo lỗi khó hiểu: `AttributeError: module 'inspect' has no attribute 'signature'`.

**Quy tắc:**
1. KHÔNG đặt tên script tạm trùng module chuẩn: `inspect.py`, `json.py`, `os.py`, `sys.py`, `re.py`, `time.py`,
   `random.py`, `copy.py`, `io.py`, `struct.py`, `collections.py`, `types.py`, `test.py`, `code.py`, `string.py`.
2. Nếu triệu chứng là "output lạ / lặp lại / module thiếu thuộc tính kỳ lạ" → **kiểm tra ngay** có file trùng tên
   module trong thư mục script hay không:
   ```powershell
   Get-ChildItem <thu_muc_script> -Filter *.py | Where-Object { $_.BaseName -in @('inspect','json','os','sys','re','time','random','copy','io','struct','collections') }
   ```
3. Chạy script tạm từ thư mục **sạch** (hoặc `python -P` / đặt `PYTHONSAFEPATH=1`) cũng phòng được.

---

### BH-25. 🐞 XML: xuống dòng trong THUỘC TÍNH phải là `&#xA;` — KHÔNG được ghi ký tự xuống dòng thật

**Ca thật: MONOPOLY (07/10).** Kho text Oasis lưu chuỗi trong **thuộc tính** XML:

```xml
<t id="201" text="Authentication failed. &#xA;Please try again."/>
```

Bản build đầu ghi **ký tự xuống dòng thật** vào thuộc tính. Chuẩn XML **bắt buộc chuẩn hoá giá trị
thuộc tính** (attribute-value normalization): mọi `\n`, `\r`, `\t` **thật** trong thuộc tính **bị biến
thành dấu cách** khi parser đọc. Hậu quả: **124 mục mất ngắt dòng**, game hiện một dòng dài
(`Authentication failed.  Please try again.` — thậm chí 2 dấu cách).

Chỉ phát hiện được khi QA **đọc lại thành phẩm** và **đếm số `\n`** so với nguồn; script build không báo gì.

**Quy tắc:**
1. Ghi text vào **thuộc tính** XML → luôn escape `\n → &#xA;`, `\r → &#xD;`, `\t → &#x9;`.
2. Đọc ra thì `html.unescape()` đã trả về ký tự thật — so sánh bình thường.
3. QA **bắt buộc** đếm số `\n` nguồn ↔ thành phẩm, không chỉ so tag/placeholder.

---

### BH-26. UnityPy: `env.save()` phải có `pack='original'` — và cách vá TextAsset ở mức RAW

**Ca thật: MONOPOLY (07/10).** Bundle `data.unity3d` gốc **520 MB** (có nén). Gọi `env.file.save()`
không tham số → ghi ra **1,27 GB** (mất nén):

```python
env.save(pack='original', out_path=<thu_muc_ra>)   # giữ nguyên kiểu nén của bundle gốc
```

**Cấu trúc RAW của một `TextAsset`** (để vá ở mức byte thay vì re-serialize cả object):

```
[int32 nameLen][name (UTF-8)][đệm 0 cho tròn 4][int32 dataLen][data]
```

→ Dựng lại đúng chuỗi này rồi `obj.set_raw_data(buf)`.

⚠️ TextAsset Unity có thể có **tiền tố byte lạ trước nội dung thật** (MONOPOLY: vài byte BOM hỏng trước
thẻ `<`). Khi parse phải **bỏ mọi thứ trước `<` đầu tiên** rồi mới `decode('utf-16')`.

**BẮT BUỘC đệm cuối cho tròn 4 byte** — Unity căn chỉnh từng trường theo 4 byte. Thiếu đệm → đọc lại báo
`ValueError: Expected to read N bytes, but only read N+2`:

```python
buf = struct.pack('<i', len(name)) + name
while len(buf) % 4: buf += b'\x00'          # đệm sau tên
buf += struct.pack('<i', len(data)) + data
while len(buf) % 4: buf += b'\x00'          # đệm cuối object
o.set_raw_data(buf)
```

**Vá nhiều file ngôn ngữ: thay theo `ID`, không theo chuỗi.** MONOPOLY có 13 file ngôn ngữ cùng bộ
**id** (id 5 = `Play`/`Spielen`/`プレイ`/`Jugar`/`Играть`). Nếu khớp theo chuỗi thì chỉ được ~100 mục
(trùng tên riêng); khớp theo **id** được đủ 2.063/file. Và **đừng dùng XML parser** cho các file dịch:
một số file có **NUL ở cuối** hoặc **XML hỏng sẵn** — dùng regex `<t ... id=".." text="..">` là đủ.

Sau build **phải mở lại thành phẩm** và so **số object** (198.295) + **số mục** (2.063) với bản gốc.

---

### BH-27. 🚨 NÉN LẠI `.zs` / `.cmp` → PHẢI KHỚP THAM SỐ FRAME CỦA FILE GỐC (windowLog)

**Ca thật: Nintendo Switch Sports (07/10).** File gốc `.zs` của Nintendo dùng **windowLog = 21**
(byte window descriptor `0x58`). Tool build dùng `zstandard.ZstdCompressor(level=16)` mặc định →
ra **windowLog = 22** (`0x60`). Decoder của game **từ chối frame** → vào game **báo lỗi software**
(hoặc không hiện tiếng Việt). Đây là **nguyên nhân crash**, không phải lỗi văn bản.

**Quy tắc:** mọi lần nén lại file của Nintendo phải **đọc tham số từ chính file gốc** rồi nén lại y hệt:

```python
from zs_util import compress_like          # tools/zs_util.py
new_zs = compress_like(open(file_goc, 'rb').read(), du_lieu_moi)
```

Kèm theo — **`.cmp` của Kirby có thêm 4 byte kích thước ở đầu**: `[u32 uncompressed_size][zstd frame]`;
`.zs` của Switch Sports thì **không** có tiền tố. Phải nhận đúng định dạng trước khi so tham số.

**Dấu hiệu nhận biết:** game chạy được với mod file rời/`.pak`/`.msbt` nhưng **crash** ở game có `.zs`/`.cmp`.

---

### BH-28. Vá font CFF/OTF: ĐỪNG thay bằng TTF — phải GIỮ định dạng + unitsPerEm

**Ca thật: Kirby and the Forgotten Land (07/10).** Font gốc là **OTF/CFF, unitsPerEm = 1000,
8.207–9.804 glyph**. Tool cũ (`patch_font_kirby.py`) **thay hẳn** bằng subset Arial Unicode →
**TTF/glyf, unitsPerEm = 2048**, và **mất 262–340 glyph gốc** (đúng lỗi BH-20) → **ô vuông trong game**.

**Kiểm tra bắt buộc sau khi vá font** (chỉ 2 dòng, phát hiện ngay):
```python
print('CFF ' in f, f['head'].unitsPerEm, len(f.getBestCmap()))   # phải giống HỆT font gốc
```

**Cách vá đúng** — `tools/rebuild_cff_font.py` (đã kiểm chứng 11/11 font Kirby):
- Dựng lại CFF bằng `FontBuilder`, **vẽ lại toàn bộ glyph gốc** qua `T2CharStringPen` → **0 glyph mất**
- Thêm glyph tiếng Việt từ font nguồn, **scale về đúng unitsPerEm của font đích**
- Chép lại `GPOS/GSUB/GDEF/VORG/BASE` nếu có
- ⚠️ **KHÔNG chép `vhea`/`vmtx`**: trong fontTools chúng **dùng chung metrics với `hmtx`**
  → chép vào sẽ làm `hmtx` hỏng khi đã thêm glyph mới (`KeyError` lúc compile).
- ⚠️ `fontTools.merge.Merger` **không ghép được** `glyf` (TTF) với `CFF ` (OTF) — lỗi
  `NotImplementedType ... has no attribute 'cff'`. Phải tự dựng lại như trên.
- ⚠️ `cffLib.CharStrings` **không cho thêm glyph mới** (`__setitem__` chỉ để GHI ĐÈ) → phải dựng lại CFF.

**Lưu ý khi gom "ký tự cần có" trong bản dịch:** các **tham số mã điều khiển** (vd `䷿Ｏ` sau
`\x0e\x00\x03\x04`) bị tính nhầm thành ký tự văn bản → sinh yêu cầu glyph không cần thiết.
Phải **bỏ các run mã điều khiển** trước khi gom ký tự.

---

### BH-29. 🚨 MỘT GAME CÓ THỂ CÓ **NHIỀU BỘ FONT** — phải vá HẾT; `TTGlyphPen` KHÔNG tự duỗi glyph ghép

**Ca thật: Kirby (08/10).** Sau khi vá xong **11 font `.bfotf` (CFF)** và kiểm chứng bằng `fontTools`
(đủ glyph, đúng upem), **game VẪN ô vuông**. Nguyên nhân: thư mục `font/ScalableFontBin` còn **34 font
`.bfttf` (glyf)** mà mod **không có**:

| Bộ | File | upem | cmap |
|---|---|---|---|
| `FOT-*.bfotf`, `VDL-*.bfotf` | 11 | 1000 | 8.2k–9.8k (CFF) |
| `CHI-*.bfttf` | 11 | 1024 | 7.6k |
| `KOR-*.bfttf` | 11 | 1000 | 18.3k |
| `TWN-*.bfttf` | 11 | 1024 | 14.6k |
| `K15-LocalCharacter-M.bfttf` | 1 | 1024 | **219** ← font "ký tự bản địa" |

**Quy tắc:** sau khi vá font, **liệt kê HẾT file font trong thư mục** và vá **tất cả**, đừng cho rằng
bộ đầu tiên là bộ game dùng. Kiểm bằng: `Get-ChildItem <font_dir> -Recurse -Include *.bfotf*,*.bfttf*`.

**Bẫy phụ — `TTGlyphPen(glyphSet)` KHÔNG duỗi glyph ghép.** Glyph tiếng Việt của Arial là glyph **ghép**
(tham chiếu `acute`/`breve`/`tilde`/`circumflex`). `TTGlyphPen(gs)` **giữ nguyên dạng ghép** → khi
`font.save()` sẽ chết vì font đích không có các tên thành phần đó:

```
KeyError: 'acute'   (hoặc 'breve' / 'tilde' / 'circumflex')
```

Cách đúng — duỗi hẳn thành glyph đơn:

```python
from fontTools.pens.recordingPen import DecomposingRecordingPen
rec = DecomposingRecordingPen(sup_gs)
sup_gs[sup_cmap[cp]].draw(TransformPen(rec, (scale, 0, 0, scale, 0, 0)))
pen = TTGlyphPen(None)
rec.replay(pen)
g = pen.glyph()          # <- glyph DON, khong con component
```

**Kiểm chứng font bằng PIXEL, đừng chỉ tin `getBestCmap()`:** `getBestCmap()` báo "có glyph" nhưng
FreeType/game vẫn có thể vẽ `.notdef`. Cách kiểm chắc chắn — render ký tự cần và **so với `.notdef`**
(ký tự PUA chắc chắn không có):

```python
ink('ạ') != ink('\ue123')   # phải khác nhau thì mới thật sự có glyph
```

---

### BH-30. 🔎 Kirby: font KHÔNG phải TTF chuẩn — có **XBIN config theo vùng** điều khiển bảng ký tự

**Ca thật: Kirby (08/10) — CHƯA XONG.** Sau khi vá đủ **45 file** trong `font/ScalableFontBin/`
(11 `.bfotf` CFF + 34 `.bfttf` glyf, mỗi file giữ nguyên toàn bộ glyph gốc + upem) thì **game VẪN ô vuông**.
Đào sâu RomFS thật mới thấy bức tranh đầy đủ:

```
font/
├─ ScalableFontBin/          45 file: .bfotf (CFF) + .bfttf (glyf)   <- đã vá
└─ Region/
   ├─ STD/  CHI/  KOR/  TWN/
   │   ├─ <TÊN_FONT>.bin          <- XBIN: magic 'XBIN' + version 4.12 + khối YAML
   │   ├─ <TÊN_FONT>-ASCII.bin    <- biến thể CHỈ ASCII
   │   └─ Ext-*.bffnt.cmp         <- font BITMAP (.bffnt) cho ký tự mở rộng
```

**Ba phát hiện quan trọng:**

1. **`.bfttf` KHÔNG phải TTF chuẩn.** Kiểm tra bảng: file gốc **không có** `maxp`, `post`… —
   đây là định dạng **rút gọn riêng của Nintendo**. Khi vá bằng fontTools rồi `font.save()`,
   fontTools **tự thêm lại** các bảng chuẩn (`maxp`, `post`, `name`, `OS/2`) và sắp xếp lại
   → **đổi cấu trúc font** → rất dễ bị loader của game từ chối (rồi rơi về font gốc → ô vuông).

2. **`font/Region/<VÙNG>/*.bin` là XBIN chứa YAML** — gần như chắc chắn là **cấu hình font**
   (font nào, cỡ nào, **bảng ký tự nào được phép**). Có cả biến thể `-ASCII`
   → nghi vấn lớn: vùng EU/US chỉ cho phép **ASCII** → ký tự có dấu **không bao giờ được hỏi**
   tới font scalable → rơi xuống `Ext-*.bffnt` (bitmap) → **ô vuông**.

3. **`Ext-*.bffnt.cmp` là font BITMAP** (`bffnt`) — không phải TTF. Muốn vá phải dùng cách của BH-18
   (mượn ô glyph trống + sinh glyph vào atlas), không dùng fontTools.

**Quy tắc rút ra:**
- Với game Nintendo first-party, **đừng giả định font là TTF/OTF chuẩn**. Kiểm **DANH SÁCH BẢNG** của file gốc
  trước: `sorted(TTFont(bytes).keys())`; thiếu `maxp`/`post` ⇒ định dạng rút gọn,
  **mọi `save()` của fontTools sẽ phá cấu trúc**.
- **Luôn liệt kê TOÀN BỘ thư mục `font/` (kể cả `Region/`)** bằng danh sách RomFS thật, không chỉ thư mục font chính.
- Kiểm chứng font phải bằng **render pixel** (so với `.notdef`), không chỉ `getBestCmap()`.

**Hướng sửa tiếp (chưa làm):** giải mã XBIN (`XBIN` + `4.12` + YAML) của `font/Region/<VÙNG>/*.bin`
để xem bảng ký tự bị giới hạn thế nào; nếu đúng là ASCII-only thì mở rộng bảng ký tự trong config,
hoặc vá `Ext-*.bffnt` (bitmap) theo BH-18.

---

### BH-31. 🚨 GAME CÓ **BỘ LỌC KÝ TỰ THEO NGÔN NGỮ** — chặn TRƯỚC cả font

**Ca thật: Kirby (09/10).** Vá font xong (đủ glyph, upem đúng) mà chữ có dấu **vẫn ô vuông**.
Thủ phạm là `msg/Kirby15/<NGÔN_NGỮ>/Filter.bin`:
- Là **XBIN** chứa **DANH SÁCH KÝ TỰ dạng UTF-16LE** (không phải dải, không phải bitmap).
- **Kích thước tỉ lệ với bộ chữ của ngôn ngữ**: English 6.172 b · French 6.396 · JP 21.828 · CN 31.064.
- Tiếng Anh = **chỉ A–Z a–z 0–9 và vài ký hiệu** → mọi ký tự có dấu bị **lọc bỏ trước khi tới font**
  → game vẽ ô vuông, **bất kể font có glyph hay không**.

**Bằng chứng quyết định:** thay tạm `Filter.bin` của tiếng Pháp cho tiếng Anh →
chữ **1 dấu** (`ô ơ ú à`) **hiện được ngay**; chữ **2 dấu** (`ằ ố ớ ợ`) vẫn vuông vì khối
`U+1EA0–0x1EFF` chưa có trong danh sách của tiếng Pháp.

**Cách vá:** danh sách **font** trong Filter giống hệt nhau ở mọi ngôn ngữ (31 font) → lấy Filter của
ngôn ngữ có bộ chữ lớn (JP) làm nền, rồi **thay các ô Kana/Kanji (không dùng) bằng ký tự cần thêm**
(`tools/kirby_filter_patch.py`). Chỉ sửa trong các **đoạn chuỗi dài ≥ 8 mã liên tiếp khác 0** để
không đụng vào offset/number của XBIN.

---

### BH-32. `.bfotf`/`.bfttf` = TTF/OTF **+ XOR** — nhưng game VẪN từ chối font ngoài

- Theo [hadashisora/NintyFont](https://github.com/hadashisora/NintyFont): *"BFTTF/BFOTF — a simple
  XOR encryption on top of normal TTF/OTF fonts."* → về nguyên tắc thay font khác được.
- **Thực tế Kirby:** thay cả 45 font bằng **Nunito** (phủ đủ tiếng Việt, frame zstd đã chuẩn, đọc lại
  xác minh PASS) → game **treo ngay ở màn hình `Launching...`**.
  ⇒ Game **kén định dạng font gốc của Nintendo**, không nhận TTF/OTF ngoài.
- Vậy hướng đúng vẫn là **thêm glyph vào chính font gốc** (giữ nguyên cấu trúc bảng).

---

### BH-33. 🚨 NÉN LẠI FILE FONT → PHẢI **MỞ LẠI ĐỌC** để xác minh (không chỉ kiểm lúc nạp)

**Ca thật: Kirby (09/10) — nguyên nhân gốc của cả một chuỗi thất bại.**
`compress_like()` (dùng chung cho `.zs`/`.cmp`) sinh ra frame zstd mà **python-zstandard không đọc
lại được** (`error determining content size from frame header`). Frame **gốc của Nintendo thì đọc OK**.

⇒ Mọi lần vá font trước đó đều **vô hiệu trong im lặng**: file ghi ra không giải nén được → game bỏ
qua → quay về font gốc → ô vuông. Script build **không hề báo lỗi**.

**Quy tắc:** sau khi ghi file nén, **bắt buộc**:
```python
new = compress_like(orig, data)
assert zstandard.ZstdDecompressor().decompress(new[...]) == data   # đọc lại phải ra đúng dữ liệu
```
Với Kirby nên dùng **frame zstd chuẩn** (`ZstdCompressor(level=15).compress`) thay vì bắt chước frame gốc.

---

### BH-34. Font Nintendo có bảng bị **cắt ngắn** (`vmtx`) → fontTools không load nổi

`.bfttf` của Kirby khai `maxp` ~7.755 glyph nhưng bảng `vmtx` chỉ có **3.077 byte** (cần 31.020) →
fontTools báo `TTLibError: not enough 'vmtx' table data`.

**Cách xử lý:** `vmtx`/`vhea` là đo bảng **chiều dọc**, không dùng cho chữ Latin →
**bỏ 2 tag này khỏi bảng mục lục sfnt** (giữ nguyên dữ liệu, thành mồ côi) rồi mới cho fontTools đọc:
```python
recs = [(t,c,o,l) for (t,c,o,l) in read_records(data) if t not in {'vmtx','vhea'}]
# ghi lại header + recs + phần dữ liệu còn lại
```

---

### BH-35. 🚨 FONT KIRBY = CFF **KIỂU CID** (`Adobe-Japan1-3`) + bị cắt `Private` → KHÔNG công cụ nào tự ghi được

Đây là **chốt chặn cuối cùng** của Kirby. Đã xác minh bằng cách mổ trực tiếp file:

| Phát hiện | Chi tiết |
|---|---|
| Kiểu font | `.bfotf` = **OTTO/CFF keyed by CID**; charset = `['.notdef','cid00001','cid00002',…]`; `ROS = ('Adobe','Japan1',3)` |
| Bị cắt | `topDict.Private = None` (và `FDArray[0]` cũng vậy) → ghi charstring mới là **`AttributeError: 'NoneType' has no attribute 'nominalWidthX'`** |
| Tên glyph | **Bắt buộc** dạng `cidNNNNN` — đặt `uniXXXX` là `KeyError` |
| fontTools | Không ghi nổi: `cs[...] = charstring`, `charStringsIndex.append()`, tự tạo `Private`, `fontTools.merge` — **tất cả đều sập** ở bước save/compile |
| `.bfttf` | **Thiếu hẳn bảng `head`** → không phải font độc lập, `TTFont` báo `KeyError: 'head'`, FontForge báo `Open failed` |
| FontForge (script) | Crash (`0xC0000005`) khi `mergeFonts` vào font CID này |

**Kết luận:** không nên vá font Kirby bằng script. Muốn xong thì phải làm **thủ công trên giao diện FontForge**
(mở `.otf` → `Element ▸ Merge Fonts` → chọn `games/_consistency/vi_only.ttf` → `File ▸ Generate Fonts`),
vì GUI hiển thị lỗi và xử lý được font CID, còn chạy script thì crash.

**Đã chuẩn bị sẵn cho việc thủ công:**
- `games/01004D300C5AE000_Kirby/font_edit/` — 45 font đã **giải mã** thành `.otf`/`.ttf` (+ file `.key`)
- `games/_consistency/vi_only.ttf` — font **nhỏ 215 glyph**, đúng 214 ký tự tiếng Việt cần thêm
- `tools/kirby_font_decrypt.py` — giải mã font gốc ra file thường
- `tools/kirby_font_reencrypt.py` — mã hoá lại + **đọc lại xác minh** sau khi sửa





| Game | Lỗi đã gặp | Nguyên nhân | Trạng thái |
|---|---|---|---|
| Hogwarts | Toàn bộ chuỗi hiện `[KEY]` | magic AVAFDICT ghi ASCII thay vì UTF-16LE | ✅ đã sửa |
| Hogwarts | File rời không có tác dụng | UFS nằm trong pak, UE mount pak trước | ✅ patch pak |
| Hogwarts | Phụ đề 100% tiếng Pháp | script build đọc sai đường dẫn, nạp 0 file | ✅ đã sửa |
| Hogwarts | Tên riêng Pháp hóa (353 dòng) | dịch từ tiếng Pháp | ✅ đã sửa |
| Hogwarts | 8 mục `[error:...]`/`[KEY]` | key tham chiếu sai có sẵn trong nguồn | ✅ đã vá |
| Hogwarts | Dấu cách trước dấu câu | lỗi dịch | ✅ đã vá |
| Ori | Sót 298 mục hội thoại | cờ trong `TextMessageProvider` không phải luôn = 1 | ✅ đã sửa |
| Ori | 2 font thiếu dấu tiếng Việt | chưa kiểm độ phủ | ✅ đã vá (thay + hợp nhất) |
| Hades II | `\n` literal / thiếu xuống dòng | không so với nguồn | ✅ đã sửa |
| Hades II | 14 chuỗi có `}` thừa, 2 chuỗi lọt chữ Trung | lỗi dịch | ✅ vá (cổng QA phát hiện) |
| Hades II | `build_hades2_mod.py` **không build lại được** | đường dẫn tương đối cũ sau tái cấu trúc | ✅ đã sửa (BH-13) |
| Switch Sports | 1.791 chuỗi **mất dấu ngắt dòng** so với bản gốc | lỗi dịch (đã kiểm chứng: chỉ là ngắt dòng, không phải icon) | ⚠️ **CẦN XEM TRONG GAME** — nếu chữ tràn khung thì phải thêm lại ngắt dòng |
| Switch Sports | **Thay cả font Trung/Hàn/Nhật** bằng font tiếng Việt | `build_custom_font.py` copy đè 3 file font khu vực | ✅ đã sửa (BH-15) — nay chỉ vá font Latin |
| Switch Sports | Font BFARC thiếu glyph | chưa kiểm độ phủ | ✅ đã vá |
| Ori Blind Forest DE | Font là **BitmapFont + atlas SDF**, thiếu 78 ký tự VI | game không đọc TTF; atlas kín chỗ | ✅ **đã vá** (mượn ô glyph không dùng + sinh glyph, xem BH-18) |
| MONOPOLY | **124 mục mất ngắt dòng** (game hiện 1 dòng dài) | ghi `\n` thật vào thuộc tính XML → bị chuẩn hoá thành dấu cách | ✅ đã sửa (BH-25) |
| MONOPOLY | Bundle 520 MB → **1,27 GB** khi build | `env.save()` thiếu `pack='original'` | ✅ đã sửa (BH-26) |
| MONOPOLY | 2 font **KabelBold/KabelMedium** (OTF/CFF) thiếu 88 dấu | `fontTools.merge` không ghép được glyf (Arial) ↔ CFF (Kabel) | ⚠️ **CHƯA VÁ** — cần chơi thử để biết có dùng tới không |
| Switch Sports | **Vào game báo lỗi software** (crash) | `.zs` nén lại bằng windowLog 22 trong khi gốc là 21 → decoder game từ chối frame | ✅ **đã sửa** (BH-27) — nén khớp tham số gốc |
| Switch Sports | Còn 173 chuỗi UI chưa dịch | các key có trong json nhưng value vẫn là tiếng Anh | ✅ **đã dịch** (còn 21 mục giữ nguyên có chủ đích: nhãn golf) |
| Kirby | **Ô vuông khi hiển thị** | thay hẳn font CFF/upem1000 bằng TTF/upem2048 → mất 262–340 glyph | ✅ **đã sửa** (BH-28) — dựng lại CFF giữ đủ glyph |
| Kirby | **Vẫn ô vuông sau khi vá `.bfotf`** | game còn dùng 34 font `.bfttf` (CHI/KOR/TWN/K15) mà mod KHÔNG có | ✅ đã bổ sung đủ 45 file (BH-29) |
| Kirby | **Vẫn ô vuông sau khi vá đủ 45 font** | `.bfttf` là định dạng rút gọn của Nintendo (không có `maxp`) → fontTools `save()` đổi cấu trúc; thêm nữa `font/Region/<VÙNG>/*.bin` (XBIN/YAML) quy định bảng ký tự được phép, `Ext-*.bffnt` là font BITMAP | ⚠️ **CHƯA XONG** — xem BH-30 |
| Unravel Two | **Treo ở logo Nintendo Switch** | `Data.kit.0` trong mod **lớn hơn gốc 1.460.324 byte** (repack LZ4 literal-only) | ⚠️ **CHƯA VÁ** — cần encoder LZ4-có-từ-điển để giữ đúng kích thước file |
| Ori WotW / It Takes Two | Ô vuông | font nằm **trong bundle Unity / pak**, mod không có file font rời | ⏳ cần vá font trong bundle/pak |

---

## PHẦN 3 — CHECKLIST BẮT BUỘC TRƯỚC KHI BÀN GIAO (Definition of Done)

Chạy **theo thứ tự**, tất cả phải đạt:

```bash
# 1) Đối chiếu codec (nếu có codec nén/đóng gói)
python -c "from tools.avaf_codec import *; d=open('<file_goc>','rb').read(); print('roundtrip:', pack_avafdict(unpack_avafdict(d))==d)"

# 2) QA tổng hợp (bản dịch theo từng game)
python tools/qa_text.py --game hogwarts     # hoặc ori / hades2 / switchsports

# 3) Độ phủ font
python tools/check_font_coverage.py <font.ttf> <file_MAIN.bin> <file_SUB.bin>

# 4) Ký tự đặc biệt / placeholder
python tools/check_special_characters.py <thu_muc_ban_dich>
```

**Mười điều phải trả lời được "CÓ" trước khi nói xong:**

1. Số entry trong mod **khớp 100%** với bản gốc?
2. **0 chuỗi rỗng**?
3. **0 ký tự** CJK/Hangul/Kana/Ả Rập/Nga trong bản dịch?
4. **0 sai lệch** tag/placeholder so với nguồn (`{0}`, `%d`, `<img …/>`, `\n`, `|plural(...)`)?
5. **0 mục `[error:`** và **0 mục `[KEY]`** còn lại?
6. **0 tên riêng bị bản địa hóa sai** (đã đối chiếu cột ngôn ngữ song song)?
7. Font **phủ 100%** ký tự dùng trong mod (và **không mất glyph icon**)?
8. Đã **mở lại thành phẩm** bằng codec đọc và xác nhận nội dung?
9. Số object/số entry **không đổi** so với bản gốc (không hỏng cấu trúc)?
10. Có hướng dẫn người dùng **chọn ngôn ngữ nào trong game** để ra tiếng Việt?

---

## PHẦN 4 — CÔNG CỤ QA CÓ SẴN

| Công cụ | Việc nó làm |
|---|---|
| `tools/pipeline.py` | **CHẠY TRỌN QUY TRÌNH** cho 1 game (build → font → đóng gói → QA), **dừng ngay nếu 1 bước lỗi** |
| `tools/qa_text.py` | **QA tổng hợp cho cả 4 game** (`--game hogwarts\|ori\|hades2\|switchsports`): rỗng, ký tự lạ, tag/placeholder, chưa dịch, `[error:`/`[KEY]`, `\n`, mã điều khiển, độ phủ font, `--leak` soát rò rỉ |
| `tools/check_font_coverage.py` | Font có phủ hết ký tự trong mod không (PASS/FAIL) |
| `tools/check_special_characters.py` | Bắt `/n` gõ nhầm, `{}` lệch, ký tự CJK/Hangul/Kana/Ả Rập |
| `tools/merge_vi_font.py` | Thêm dấu tiếng Việt vào font có sẵn **mà giữ nguyên icon** |
| `tools/unity_text_tool.py` | Bóc & vá text Unity (parse linh hoạt, không hardcode magic) |
| `tools/fix_hogwarts_fr_names.py` | Mẫu sửa tên bị bản địa hóa (đối chiếu cột FR vs ES) |
| `tools/fix_hogwarts_main_errors.py` | Mẫu vá `[error:...]`/`[KEY]` bằng key anh em |
| `tools/fix_hades2_qa_bugs.py` | Mẫu vá `}` thừa + chữ Trung lọt (do cổng QA phát hiện) |
| `tools/README.md` | **Bản đồ công cụ** theo engine — tra nhanh file nào làm việc gì |

---

## PHẦN 5 — NGUYÊN TẮC VÀNG

1. **Không im lặng thất bại.** Nạp 0 file / thiếu dữ liệu → phải báo lỗi to.
2. **Không tin script, tin thành phẩm.** Luôn mở lại file đã build để kiểm.
3. **Không đoán tên riêng.** Dùng ngôn ngữ song song để tra ngược.
4. **Không hardcode magic.** Thử nhiều khả năng và xác thực.
5. **Không thay font khi chưa kiểm PUA** — hợp nhất thay vì thay hẳn.
6. **Không bỏ qua dải ký tự** khi quét — dùng script có sẵn bộ ký tự đầy đủ.
7. **Roundtrip codec trước khi build.**
8. **Kiểm file rời vs UFS trước khi hứa LayeredFS chạy.**
9. **Chỉ push khi được yêu cầu.**
10. **Không xoá dữ liệu nặng khi chưa hỏi.**
