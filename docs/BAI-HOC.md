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

---

## PHẦN 2 — BẢNG LỖI THEO GAME (để tra nhanh)

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
