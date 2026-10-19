# Trạng thái dự án bản địa hóa Game Nintendo Switch

## 0. The Legend of Zelda: Tears of the Kingdom (TotK)
- **Title ID**: `0100F2C0115B6000` (Base / Update Product.142 v1.4.2)
- **Engine**: Nintendo First-Party (EPD LunchPack)
- **Cấu trúc Text/Font**:
  - Mals archive: `Mals/USen.Product.142.sarc.zs` (MSBT trong SARC, nén Zstandard với dictionary `zs.zsdic`).
  - Font: `Font/Font.Nin_NX_NVN.bfarc.zs` (BFFNT/BFOTF font nhị phân Nintendo mã hóa XOR key `0xD99B871A`).
- **Trạng thái hiện tại**:
  - Đã trích xuất toàn bộ 1.511 file MSBT (47.800 strings) từ RomFS Dump tại `E:\RomFS_Dump\0100F2C0115B6000\romfs`.
  - **ĐÃ HOÀN THÀNH 100% CÁC DANH MỤC LỚN (14.537 chuỗi)**:
    - `StaticMsg` (100% - 1.509 chuỗi): Toàn bộ mẹo chơi, chỉ dẫn, hiệu ứng nấu nướng, ký ức rồng, bản đồ phím.
    - `ChallengeMsg` (100% - 1.097 chuỗi / 253 files): 100% nhiệm vụ chính, đền thờ, nhiệm vụ phụ, phiêu lưu bên lề.
    - `LocationMsg` (100% - 1.709 chuỗi / 2 files): 100% địa danh Hyrule, hầm ngục Dungeon, đền thờ.
    - `ShoutMsg` (100% - 176 chuỗi / 5 files): Giọng nói kêu gọi chiến đấu của cả 5 Hiền nhân.
    - `LayoutMsg` (100% - 1.311 chuỗi / 59 files): 100% giao diện UI hệ thống, Album, Cài đặt, Bản đồ, Pouch UI, Shop...
    - `ActorMsg` (100% - 5.618 chuỗi / 11 files): 100% Túi đồ Pouch (2.882 chuỗi vũ khí Master Sword/khiên/cung/đồ Zonai/nguyên liệu nấu ăn), Bách khoa toàn thư Hyrule PictureBook (1.019 chuỗi), Quái vật Boss, Chế tạo Zonai, NPC.
    - `StaffRollMsg` (100% - 1.548 chuỗi / 2 files): 100% Danh đề Credits nhà sản xuất và chức danh.
    - `NpcTerrorMsg` (100% - 1.569 chuỗi / 29 files): 100% câu thoại cảm thán, la hét, kinh ngạc của NPC.
  - **EventFlowMsg (Hội thoại cốt truyện & minigame - 33.263 chuỗi / 1.139 files)**:
    - **PIPELINE MỚI (batch + masking)** — tool dùng chung:
      - `tools/totk_text.py`: tách/che MỘT TOKEN HÓA 100% mã điều khiển Nintendo (`\x0e…`) thành `[[n]]`
        để subagent dịch mà KHÔNG thể phá thẻ; khôi phục lại đúng byte gốc. Tự kiểm roundtrip toàn 47.800 chuỗi.
      - `tools/totk_make_event_batches.py`: sinh chunk (`source/ev_batches/batch_NNN.json`, ~250 chuỗi/chunk, đã che token).
      - (giao subagent dịch) -> `translations/ev_batches/batch_NNN.json`
      - `tools/totk_apply_batches.py`: khôi phục token + hợp nhất vào `translations/<file>.json` (đủ nhãn),
        tự bắt lỗi JSON/lệch token/lệch `\n`.
      - `glossary/totk.csv` (1.693 thuật ngữ, sinh từ `StaticMsg__Reference` + `LocationMsg`).
      - Cổng QA: `python tools/qa_text.py --game totk` (đã thêm adapter).
    - Tiến độ: ✅ **HOÀN THÀNH 100% EventFlowMsg (33.263 / 33.263 chuỗi, 1.137 file có nội dung)**;
      **139 / 139 batch đã dịch**. (2 file `Dm_ZO_0016`, `Dm_ZO_0030` chỉ chứa chuỗi rỗng nên không cần dịch.)
      Pipeline: sinh batch -> giao subagent dịch -> `totk_apply_batches.py` -> build -> QA.
    - ⚠️ Lỗi cũ đã vá: 51 chuỗi ở `DmF_SY_StatueDevil/Venus` từng ghi literal `\n` (2 ký tự) thay vì xuống dòng thật
      → `tools/totk_apply_batches.py` nay tự sửa; `LayoutMsg__AppMap_00::Scroll` (`[Hold]`→`[Giữ]`) là NGOẠI LỆ hợp lệ (đã whitelist QA).
  - **TỔNG KẾT BẢN MOD HIỆN TẠI** (build 17/10):
    - **1.509 / 1.511 file MSBT** đã inject tiếng Việt (2 file còn lại chỉ có chuỗi rỗng); gói `USen.Product.142.sarc.zs` = **2.269.137 byte**.
    - 🚨 **BẮT BUỘC kèm `System/Resource/ResourceSizeTable...rsizetable.zs`** (BH-49): TotK dùng bảng RSTB
      (magic `RESTBL`, cặp `crc32(path không .zs) -> size giải nén`) để cấp phát resource. Thay Mals/Font mà
      không vá RSTB → **treo ở "Launching..." / crash**. Vá bằng `python tools/patch_totk_rstb.py`
      (size Mals 11.595.592, Font 1.501.836).
    - **Lưu ý phiên bản:** game 1.4.3 vẫn đọc `Mals/USen.Product.142.sarc.zs` (RSTB 143 KHÔNG có entry 143).
    - Gói mod hiện có: `Mals/USen.Product.142.sarc.zs`, `Mals/USen.Product.143.sarc.zs` (dự phòng),
      `Font/Font.Nin_NX_NVN.bfarc.zs`, `System/Resource/ResourceSizeTable.Product.{142,143}[.Nin_NX_NVN].rsizetable.zs`.
    - `qa_text.py --game totk`: **PASS** (0 lỗi; cảnh báo: 3.489 lệch ngắt dòng, 580 rỗng-cả-nguồn, 1 lệch mã điều khiển; còn 1.703 chuỗi giống nguồn — tuyệt đại đa số là tên riêng/tên quái/nhân sự credits/lời hát, đã rà thủ công).
    - Bộ Font `Font.Nin_NX_NVN.bfarc.zs` đã vá và mã hóa XOR chuẩn Nintendo (`0xD99B871A`).
    - Bản mod LayeredFS: `output/atmosphere/contents/0100F2C0115B6000/romfs/` (`Mals/` + `Font/` + `System/Resource/`).
    - Build: `python tools/build_totk_mod.py`; vá RSTB: `python tools/patch_totk_rstb.py`;
      QA: `python tools/qa_text.py --game totk`.
  - **PORT BẢN VIỆT HOÁ "THE RED TEAM" (TRT) SANG 1.4.3** (18/10) — cho chơi được ngay, khỏi dịch lại:
    - Patch TRT (Patch 142) **không chạy trên 1.4.3** vì: (a) không có `ResourceSizeTable` cho Product.143,
      (b) SARC của họ **thiếu file `LayoutMsg/AppLoadingMessage_00.msbt`** (file màn hình chờ!),
      (c) thiếu **140 nhãn** ở 11 file do 1.4.3 thêm chuỗi (Staff +15, InstantTips +39, Pouch_00 +36...).
    - Tool: `python tools/build_totk_trt_mod.py --trt "<...>/USen.Product.142.sarc.zs"` → `output/TRT143/`.
      Ghép: cấu trúc file/nhãn lấy từ Mals gốc **1.4.3**, văn bản ưu tiên **TRT** → thiếu thì lấy **bản của mình**
      → còn lại EN; tự bỏ qua nhãn có thẻ điều khiển lệch giữa 2 bản (321 nhãn).
    - Kết quả: 1511/1511 file, 47.800 nhãn (47.336 TRT + 464 của mình), 0 nhãn thiếu/0 rỗng oan;
      Mals `USen.Product.142.sarc.zs` = 2.248.333 B (giải nén 11.830.232) + Font TRT (569.084 B) + RSTB 143 đã vá.
    - File tham chiếu đối chiếu: `glossary/totk_trt_names_ref.csv` (12.961 dòng `file,label,en,ours,redteam`).
    - ✅ **GÓI ĐỂ CHƠI (chốt 18/10): `output/TRT143/`** — bản TRT port sang 1.4.3.
      143 nhãn mới của 1.4.3 (5 vải dù Hiền Nhân, Item Sharing, Daily Bonus, ZELDA NOTES) lấy tạm bản dịch của mình;
      người dùng quyết định **không dịch lại**. Bản dịch của mình (`output/` + `games/.../translations/`) **giữ nguyên làm dự phòng**, không xoá.
    - Đồng bộ Eden: `output/TRT143/.../0100F2C0115B6000/romfs/` → `%APPDATA%\eden\load\0100F2C0115B6000\romfs\` (đã đồng bộ).
    - ✅ **Toàn bộ text đã Việt hóa xong.** Việc còn lại: **test trong game** (Eden/Switch).


## 1. Hogwarts Legacy (Nintendo Switch)
- **Title ID**: `0100F7E00C70E000` (Base) / `0100F7E00C70E800` (Update v1.0.5)
- **Engine**: Unreal Engine 4.27 (Custom Avalanche Software Build)
- **Định dạng Text**: AVAFDICT 2.0 (`MAIN-*.bin`, `SUB-*.bin`)
- **Tiến độ dịch thuật & Đóng gói Mod**:
  - Đã trích xuất hoàn chỉnh 17.737 entries giao diện (MAIN) và 35.431 dialogues hội thoại (SUB).
  - **MAIN (UI/Menu/HUD): HOÀN THÀNH 100% — 17.737/17.737 chuỗi tiếng Việt.**
    - Dịch từ nguồn tiếng Trung (`Source_ZH`), chia 29 chunk × 400 chuỗi và dịch song song bằng subagent.
    - QA: 0 ký tự Hán sót, 0 sai lệch placeholder/tag, 0 chuỗi rỗng; 681 chuỗi giữ nguyên là các nhãn hợp lệ (độ phân giải `1280x720`, `120 FPS`, tên phím `Enter/Tab`, `[error:...]`).
  - **SUB (hội thoại): đã dịch 100% — 35.431/35.431 chuỗi** (nay **đã vào mod**: 97,7% VI).
    - Kho SUB gốc bóc lại từ NSP bằng `nsz` + Oodle (9 từ điển ngôn ngữ) → dùng bản tiếng Pháp (`SUB-koKR.bin`, 35.431 entries) làm nguồn dịch (NSP base không có tiếng Anh).
    - Gộp trùng còn **26.296 chuỗi duy nhất**, chia 53 chunk × 500 (một số chunk tách nhỏ 250 khi quá dài) và dịch song song bằng subagent.
    - QA: keys khớp 100%, 0 sai lệch placeholder/tag (`<i>`, `\n`, `[[ ]]`...), 0 chuỗi rỗng; 77 chuỗi giữ nguyên là thán từ (`Hmm.`, `Argh…`), tên bùa trong tag (`<i>Nox</i>.`) và tên người.
    - Truy vết nguồn: `games/0100F7E00C70E000_Hogwarts/source/extracted_json/hogwarts_dialogs_fr.json`, `dialogs_fr_unique.json`; bản dịch ở `games/0100F7E00C70E000_Hogwarts/translations/sub_trans/sub_*.json`.
    - Đã chuẩn hóa nốt tên Pháp hóa còn sót (đối chiếu chéo bằng cột tiếng Tây Ban Nha song song): `Cheek→Deek` (234), `Pallow→Sallow` (28), `Bôbalais→Spintwitches` (12), `Campolard-en-Haut/Bas→Upper/Lower Hogsfield` (5).
  - **Kiểm toán tổng hợp cuối (MAIN + SUB):** keys khớp 100%, **0** ký tự lạ (CJK/Hàn/Nhật/Ả Rập), **0** sai lệch placeholder/tag, **0** chuỗi rỗng, **0** tên Pháp hóa sót. Font đã cài phủ **223/223** ký tự dùng trong mod.
  - **Font chữ (Giai đoạn 3): ĐÃ VÁ (font dự phòng).**
    - Cấu trúc RomFS: text/font nằm trong pak IoStore (`Phoenix/Content/Paks/pakchunk*-Switch.pak/.ucas/.utoc`), **không** có file rời.
    - File font rời duy nhất là `Engine/Content/SlateDebug/Fonts/LastResort.ttf` — chính là font UE dùng dự phòng khi thiếu glyph (đúng trường hợp dấu tiếng Việt).
    - Đã thay bằng **Lato Regular** (phủ đủ 224 ký tự dùng trong bản dịch, gồm toàn bộ dấu tiếng Việt) tại:
      `output/atmosphere/contents/0100F7E00C70E000/romfs/Engine/Content/SlateDebug/Fonts/LastResort.ttf`
    - Font gốc lưu tại `games/0100F7E00C70E000_Hogwarts/source/romfs_dump/LastResort.ttf` (backup).
  - ✅ **ĐÃ XỬ LÝ việc engine bỏ qua file rời:** kiểm tra `Manifest_NonUFSFiles_Switch.txt` xác nhận
    `Phoenix/Content/Localization/SWITCH/*.bin` là **UFS (nằm trong pakchunk0-Switch.pak)**, không phải file rời
    → file `.bin` đặt rời bị engine bỏ qua (đã test thực tế: không lên tiếng Việt).
  - **Giải pháp: patch pak UE4** — `Phoenix/Content/Paks/pakchunk0-Switch_p.pak` (33,8 MB), chứa bản dịch cho
    **cả 14 ngôn ngữ** của game (arAE deDE enUS esES esMX frFR itIT jaJP koKR plPL ptBR ruRU zhCN zhTW).
    Build bằng `tools/build_patch_pak.py` (dùng thư viện `repak`, pak version V11, mount point `../../../`).
  - 🐞 **BUG CHÍ MẠNG ĐÃ SỬA (nguyên nhân gốc):** file AVAFDICT của game dùng magic **UTF-16LE**
    (`41 00 56 00 41 00…`, 32 byte), nhưng `tools/avaf_codec.py` ghi magic **ASCII** (`41 56 41 46…`).
    Game không đọc được từ điển → hiển thị toàn bộ chuỗi dạng `[KEY]` (đã thấy trong game).
    Đã sửa codec; kiểm chứng: `pack_avafdict(unpack_avafdict(file_gốc)) == file_gốc` → **True**.
    (Trước khi sửa luôn False → mọi bản mod trước đây đều vô hiệu vì lý do này.)
  - Công cụ hỗ trợ: `tools/ue_romfs_tool.py` (liệt kê/trích file RomFS), đọc mục lục pak bằng `repak` (xem Phụ lục A của skill `/dich`).
  - Mod LayeredFS hiện tại:
    `output/atmosphere/contents/0100F7E00C70E000/romfs/`
    - `Phoenix/Content/Paks/pakchunk0-Switch_p.pak` (33,8 MB) — **phần chính, chứa text bản dịch**.
    - `Phoenix/Content/Localization/SWITCH/` — 5 `MAIN-*.bin` + 5 `SUB-*.bin` (giữ cho đầy đủ).
    - `Engine/Content/SlateDebug/Fonts/LastResort.ttf` — font tiếng Việt (file rời, LayeredFS ăn).
  - 🐞 **BUG ĐÃ SỬA (2026-10-01): phụ đề trong game vẫn tiếng Pháp.**
    `tools/build_hogwarts_sub.py` đọc bản dịch ở `source/split_tasks/sub_trans/` — **không tồn tại**;
    bản dịch thật ở `translations/sub_trans/`. `glob` trả 0 file → `id2vi` rỗng → **SUB-*.bin giữ
    nguyên tiếng Pháp** (chỉ 2,6% tiếng Việt do trùng ký tự) **mà không hề báo lỗi**.
    → Đã sửa đường dẫn + thêm cảnh báo khi thiếu bản dịch; build lại **26.296/26.296 chuỗi**,
    `SUB-enUS.bin` nay **97,7% tiếng Việt**; patch pak build lại (28 entry, đã verify khớp).
    Bản dịch **chưa từng thiếu** — lỗi nằm hoàn toàn ở script build (im lặng khi nạp 0 file).

---

## 2. Hades II (Nintendo Switch)
- **Title ID**: `0100A00019DE0000`
- **Trạng thái**: Hoàn thành 100%, SpriteFont XNB sắc nét, mod hoàn chỉnh tại `output/atmosphere/contents/0100A00019DE0000/`.

---

## 3. Nintendo Switch Sports
- **Title ID**: `0100D2F00D5C0000`
- **Trạng thái**: ✅ **ĐÃ BUILD LẠI FONT ĐÚNG CHUẨN NINTENDO (10/10)** — text 100% + font gốc + tiếng Việt.
  - File mod: `output/atmosphere/contents/0100D2F00D5C0000/romfs/`
    (`Font/Font.Nin_NX_NVN.bfarc.zs` 9,88 MB + `Mals/USen.Product.150.sarc.zs` 355.880 B).
  - ⚠️ **CHƯA test trên máy thật** (lỗi người dùng báo trước đó là *"Unable to start software"*).
- **🐞 NGUYÊN NHÂN GỐC (xác nhận 10/10):** bản mod cũ dùng **SAI** font do `tools/build_custom_font.py`
  (Nunito) sinh ra: **thay hẳn** 4 font Latin của Nintendo (`scft/VDL-LOGOG-BOLD.bfotf`,
  `VDL-LOGOG-ULTRA`, `VDL-GigaJr-ExtraBold-003_Gaiji`, `VDL-GigaJr-Ultra`) bằng **TTF/glyf**
  → **mất 7.888 / 8.207 glyph (96%)**: font gốc **8.207 glyph** (OTTO/CFF) → font mod cũ **938 glyph**;
  mất trọn **fullwidth/halfwidth 164/164, số trong vòng 76/76, mũi tên 13/13, hình khối 20/20**
  → vừa gây **crash khi boot** (HAL từ chối font sai cấu trúc — xem **BH-38**) vừa làm **UI tỷ số mất glyph**.
  Ghi chú cũ ở mục "ĐÃ SỬA XONG (03/10)" là **sai** — file output khi đó vẫn là font Nunito hỏng.
- ✅ **CÁCH SỬA ĐÚNG (10/10 — theo phương pháp gốc Nintendo, BH-38):**
  - **Tool mới:** `tools/patch_font_switchsports_native.py` — **KHÔNG thay font**, mà **tiêm glyph tiếng Việt
    thẳng vào các slot CFF còn trống** của chính 4 font VDL gốc:
    - Giữ nguyên **OTTO/CFF**, `upem=1000`, **CID-keyed** (LOGOG) / name-keyed (GigaJr), **số glyph không đổi**
      (9.355 / 9.705) → HAL Nintendo chấp nhận, không crash.
    - Glyph tiếng Việt được **ghép từ chính chữ cái + dấu tổ hợp có sẵn trong font** (NFD); dấu móc/horn,
      mũ, dấu chấm dưới, gạch ngang được vẽ theo tỷ lệ x-height của font.
    - Kết quả: mỗi font **+104 glyph** (cmap 8.207 → **8.311**) với LOGOG; **+92** (8.555 → **8.647**) với GigaJr.
      **0 ký tự tiếng Việt bị thiếu**, giữ nguyên lớp `GPOS/GSUB/GDEF`, đầy đủ fullwidth/số vòng/mũi tên/hình khối.
    - 35 ký tự không ghép được (Hangul `U+CA00…` + icon PUA `\ue0xx`) **vốn cũng không có trong font Latin gốc**
      → không đổi hành vi; các ký tự này do **font Hàn `AsiaKTITGD4-R_KRko.bfttf`** phủ (font này giữ nguyên).
  - **Bản dịch:** giữ nguyên (250 file, 0 lệch key/tag); `_all_strings.json` là file tổng hợp, không nằm trong SARC.
  - Kiểm tra: `python tools/qa_switchsports.py` → glyph mất **0**, VI thiếu **0**;
    `python tools/qa_text.py --game switchsports` → **PASS**;
    `python tools/final_check_switchsports.py` → **PASS**;
    `python tools/sws_fix_zs.py` → frame Zstd **windowLog=21, checksum=False** khớp bản gốc (BH-27 OK).
  - ⚠️ **Bài học:** danh sách glyph cần giữ phải lấy từ **ký tự THỰC DÙNG trong bản dịch** (không chỉ cmap gốc).
  - ⚠️ **KHÔNG dùng lại** `tools/build_custom_font.py` (Nunito) và `tools/patch_font_switchsports.py`
    (thay sang Arial TTF — mất cấu trúc CFF) cho game Nintendo.

---

## 4. Ori and the Will of the Wisps (Nintendo Switch)
- **Title ID**: `01008DD013200000` (Base) + `01008DD013200800` (Update 1.2.1)
- **Engine**: Unity (IL2CPP) — engine **mới**, pipeline đang được dựng.
- **Text**: 307 AssetBundle `Data/data_*.unity3d` (~1,36 GB), mỗi đoạn hội thoại là 1
  MonoBehaviour `TextMessageProvider` chứa **20 ngôn ngữ** (không có tiếng Việt).
- **Trạng thái**: ✅ **ĐÃ BUILD MOD** — text 1.877 mục (1.793 chuỗi duy nhất) dịch 100%, QA 0 lỗi;
  **cả 7 font đều đã phủ 100% dấu tiếng Việt** (Candara/ProFontWindows thay bằng Lato;
  keyboard/moon-tools hợp nhất giữ icon; Roboto-* vốn đã đủ); đóng gói **103 file (871,6 MB)** tại
  `output/atmosphere/contents/01008DD013200000/romfs/Data/`.
- **Sửa bản dịch**: `games/01008DD013200000_OriAndTheWillOfTheWisps/translations/ori_vi.json`
  (mảng `{Id, EN, VI}`) → chạy lại `python tools/build_ori_mod.py` + `python tools/patch_font_ori.py`.
- **Lưu ý kỹ thuật**: sau tên `...TextMessageProvider`, cờ trước chuỗi có thể là 1 hoặc 2 (hoặc không có)
  — tool đã sửa để thử cả hai (nếu chỉ nhận cờ = 1 sẽ **sót ~298 mục hội thoại**).
- **Cách chơi**: đặt ngôn ngữ game = **English** (tiếng Việt ghi đè lên khe tiếng Anh).
- Chi tiết + việc còn lại: `games/01008DD013200000_OriAndTheWillOfTheWisps/README.md`.

---

## 5. Ori and the Blind Forest: Definitive Edition (Nintendo Switch)
- **Title ID**: `010061D00DB74000` (Base) + `010061D00DB74800` (Update v131072)
- **Engine**: Unity **IL2CPP** 2018.4.1f1; bundle `Data/data.unity3d` (1,74 GB) + ~130 `sharedassets*.resource`
- **Text**: MonoBehaviour `*TextMessageProvider` → **679 mục** (656 khoá), tiếng Anh
- **Trạng thái**: ✅ **HOÀN THÀNH** — text dịch 100% (659 chuỗi) · tag/placeholder 0 lệch · **font tiếng Việt đã vá**
  (78 glyph sinh vào atlas SDF + đổi mã ký tự, kiểm chứng bằng ảnh cắt: `ạ ắ ệ ợ ự Ứ Ờ Ư ơ` đủ dấu) ·
  cổng QA **PASS** → `output/atmosphere/contents/010061D00DB74000/romfs/Data/data.unity3d` (1,74 GB)
- 🔑 **Kỹ thuật font (BitmapFont/SDF atlas):** xem `games/010061D00DB74000_OriAndTheBlindForest/README.md`
  và `tools/unity_bitmapfont.py` + `tools/patch_font_obf.py`. **Chưa test trong game** — cần người dùng kiểm.
- Công cụ mới: `tools/extract_il2cpp.py` (bóc `main` + `global-metadata.dat` để dựng typetree).
- ROM đã chuyển sang `E:\ROM_Backup\OriBlindForest\`.

---

## 3. Nintendo Switch Sports
- ✅ **ĐÃ SỬA LỖI CRASH (07/10):** vào game báo lỗi software vì file `.zs` được nén lại bằng
  **windowLog 22** trong khi file gốc dùng **21** → decoder của game **từ chối frame**.
  Đã sửa tận gốc: `tools/build_mod.py` + `tools/build_custom_font.py` nay dùng
  `tools/zs_util.py::compress_like(file_goc, du_lieu_moi)` để **nén khớp tham số gốc**. (BH-27)
- ✅ **ĐÃ DỊCH NỐT 173 CHUỖI UI** còn tiếng Anh (hướng dẫn chơi, hộp thoại tay cầm, thưởng,
  nhãn golf, 99 chức danh Staff Roll). Chưa dịch **173 → 21** (21 mục còn lại là **nhãn golf giữ
  nguyên tiếng Anh có chủ đích** + 1 chuỗi chỉ có mã điều khiển). QA `qa_text.py --game switchsports`: **PASS**.
  Công cụ: `list_untranslated.py`, `sws_prepare/apply_untranslated.py` (che mã điều khiển thành token `[[n]]`).
- Thành phẩm: `output/atmosphere/contents/0100D2F00D5C0000/romfs/{Mals,Font}/` (4,6 MB).

### 4b. Kirby and the Forgotten Land — SỬA DỨT ĐIỂM LỖI Ô VUÔNG BẰNG NATIVE CID (10/10)
- 🐛 **Nguyên nhân gốc của ảnh lỗi ô vuông:**
  - Ở lần thử trước, việc dùng `cidFlatten()` của FontForge đã chuyển font thành Name-Keyed font thông thường (`is_CID = False`).
  - Loader của Nintendo HAL bắt buộc cấu trúc **CID-Keyed font (`Adobe-Japan1-3`)** $\to$ Game từ chối nạp file mod font và rơi về font fallback tối thiểu (dẫn đến ngay cả các chữ gốc như `ó, ô, ê, à, é` cũng thành `□`).
- ✅ **Đã xử lý tận gốc bằng `tools/kirby_patch_all_fonts_native.py` (BH-38):**
  - **11 font `.bfotf` (CFF)**: Giữ nguyên vẹn 100% định dạng CID-Keyed (`is_CID = True, ROS = ('Adobe', 'Japan1', 3)`). Bơm trực tiếp các glyph tiếng Việt vào các slot **CID chưa sử dụng (unused CIDs)** và liên kết với PrivateDict chuẩn của `FDArray[0]`.
  - **34 font `.bfttf` (TrueType)**: Giữ nguyên cấu trúc TrueType native, duỗi phẳng glyph tiếng Việt qua `DecomposingRecordingPen` và cập nhật chuẩn xác bảng `glyf/hmtx/maxp/cmap`.
  - Mã hóa chuẩn XOR magic `0x36F81A1E` và nén zstandard level 15 chuẩn xác.
- ✅ **Kiểm chứng thành phẩm:**
  - `FOT-RodinNTLGPro-B`: `is_CID = True`, `ROS = ('Adobe', 'Japan1', 3)`, các ký tự `ạ, ế, ó, ô, đ` đều đã được gán vào CIDs hợp lệ và trỏ đúng trên cmap.
  - `K15-LocalCharacter-M`: Đầy đủ 100% glyph tiếng Việt và giữ nguyên toàn bộ 15 bảng TrueType.
  - **Sửa dứt điểm tầng lọc Filter.bin (BH-39)**: Giải mã cấu trúc XBIN4 của `Filter.bin`. Tự động bổ sung 100% ký tự ASCII và 144 ký tự tiếng Việt vào toàn bộ 31 font theo đúng repeat count, sắp xếp tăng dần 100% cho Binary Search.
  - **Sửa dứt điểm lỗi giải mã Header Font (BH-40)**: Trường độ dài giải mã (byte 4..7) của header font Nintendo HAL bắt buộc phải mã hóa XOR cùng `key` (`len(font) ^ key`). Đã rebuild lại toàn bộ 45 font ScalableFontBin khớp 100% chuẩn giải mã của engine HAL.
  - **Khóa chuẩn Advance Width & Cân bằng Bearing LSB/RSB (BH-41)**: Khắc phục triệt để hiện tượng chữ tiếng Việt bị co rúm / dính chữ / xấu nét bằng cách khóa Advance Width khớp 100% với Base Latin cơ sở (`a` -> 602, `o` -> 649, `e` -> 612...), căn giữa glyph bằng `TransformPen`, và tận dụng ký tự `Eth` (0x00D0) có sẵn nét tròn đậm nguyên bản của font để map cho `Đ` (0x0110).
  - Đã xuất thành phẩm vào `output/atmosphere/contents/01004D300C5AE000/` và đồng bộ sang thư mục mod của Eden.


## 5. 🔄 ĐANG LÀM: Unravel Two (Nintendo Switch)
- **Title ID**: `0100E5D00CC0C000` (Base) / `0100E5D00CC0C800` (Update v65536)
- **Engine**: Native Switch (NVN), engine riêng Coldwood — **không** phải Unity/UE.
- **Giai đoạn 1 — gần xong:**
  - ✅ ROM có sẵn trong `input/` (Base 2,81 GB + Update 20,5 MB).
  - ✅ **Bóc RomFS được** (`ue_romfs_tool.py list` → 22 file) — không vướng titlekey.
  - ✅ **Đã giải mã định dạng `.kit`**: `[u32 dài][khối LZ4] → JSON` (kiểm chứng: 309 record giải nén OK).
    Codec: `tools/kit_codec.py`.
  - ✅ **Đã định vị kho text UI** trong `Data.kit.0` (~`0x1EFA000`): `Options`, `Pause`, `Resume`,
    `SecondPlay`, `AssistMode`, `Volume`, `Switch/PS4/XBoxOne`… + **bảng offset u32** ngay sau.
  - ✅ `.kit*` là **file rời RomFS** → mod LayeredFS thay trực tiếp, **không cần patch pak**.
  - ✅ Font: `fonts/unravel.fgen` (định dạng riêng, chưa giải mã).
  - ✅ **Đã bóc toàn bộ 12 phần** (`Data.kit.0..11`, 2,2 GB) ra `E:\UNR_work\parts\`.
  - ✅ **Quét toàn bộ**: ~70.000 record. Nội dung chủ yếu là **dữ liệu asset**
    (schema/biến vật lý, tên menu, đường dẫn scene `|/scenes/Levels/Menu/...|`) —
    **chưa cô lập được bảng chuỗi hiển thị (localization)**.
  - ✅ **ĐÃ TÌM RA KHO TEXT** trong `Data.kit.0` (3 record lớn):
    - `@~0x7e44e73` (15 MB) — **BẢNG DỊCH**: có `LANG_RULE_NON_ENDING`, thẻ `<loca>`, nhãn `NOLOCA`,
      và **credits thật**: `THANK_YOU`, `ROLE`, `<large>Coldwood</…>`, `Sam Addo…`, `Dick Adolfsson`,
      `Linus…`, `Joshua Baldwin`, `Victor Bohl`, `Karl Broström`, `Håkan Dalsfelt`, `Michael Gill`…
    - `@~0x26412df` (16,8 MB) — **script UI + khoá text**: `MENU_BUTTON_BAR_TEXT_ACTIVATE`,
      `CONTROLLER_LOST`, `m_text = StoredGameObjectHandle()`…
    - `@~0x644d639` (24,6 MB) — dữ liệu menu/scene.
  - ✅ **ĐÃ GIẢI MÃ XONG CODEC (03/10) — codec thật là `LZ4 + TỪ ĐIỂN` (solid archive):**
    - Điểm mấu chốt: token `0xb6` = 11 literal `"ichael Gill"` rồi match 6 byte lấy từ **dữ liệu
      đã giải nén trước đó** (chữ `M` nằm ở entry trên) → phải giải mã **tuần tự, giữ từ điển 64 KB**.
    - Kết quả `Data.kit.0`: **10.117 record** (10.116 LZ4-từ-điển + 1 raw) — parse sạch toàn file.
    - Tool: `tools/kit_lz4dict.py` (bộ giải mã LZ4-có-từ-điển) + `tools/kit_unpack.py` (bóc + tự đồng bộ).
  - ✅ **BÓC ĐƯỢC BẢNG DỊCH THẬT** — record `@0x865b1aa` (65.536 byte = đúng 64 KB, cỡ cửa sổ từ điển):
    - Định dạng cực đơn giản: `KHOÁ` ⏎⏎ `giá trị` ⏎⏎ `KHOÁ` ⏎⏎ `giá trị`… (bắt đầu bằng `v0.01`)
    - Thẻ định dạng: `<NEWLINE>`, `<loca>…</loca>`, `<large>…</large>`
    - **Record này là bản TIẾNG PHÁP** (`Vous avez terminé l'histoire…`) → game có **một record cho
      mỗi ngôn ngữ** → cần tìm record **tiếng Anh** làm nguồn dịch.
  - ✅ **ĐÃ DỊCH XONG 463/463 CHUỖI sang tiếng Việt (03/10):**
    - Kho text: 468 mục (313 UI ngắn + 148 vừa + 2 dài + 5 mục `NOLOCA`/EULA **giữ nguyên**
      vì chính game đánh dấu "không bản địa hóa").
    - Chia 6 chunk, giao **4 subagent dịch song song** → `translations/vi_ui_01,02 / vi_mid_03,04,05 / vi_long_06.json`
    - **QA (`tools/qa_unravel.py`): PASS** — 0 lệch thẻ `<...>`, 0 lệch placeholder, 0 chuỗi rỗng,
      0 ký tự lạ (CJK/Hangul/Kana/Kyrillic/Ả Rập).
  - ✅ **ĐÓNG GÓI XONG MOD (03/10):**
    - Bộ **NÉN LZ4**: `tools/kit_repack.py` (khối literal hợp lệ) — giữ nguyên byte nén của record
      không sửa, chỉ nén lại record bị thay.
    - `tools/build_unravel_mod.py`: thay giá trị bảng dịch bằng **regex** (không phụ thuộc ranh giới
      chunk), rồi **vá dây chuyền** các record bị ảnh hưởng do tham chiếu chéo (26 record/vòng 1 → 0/vòng 2).
    - Thành phẩm: `output/atmosphere/contents/0100E5D00CC0C000/romfs/NVNKits/Data.kit.0` (211 MB).
    - **Kiểm chứng (`tools/verify_unravel_mod.py`): PASS** — 12.698 record + 24 gap nguyên vẹn,
      **chỉ đúng 6 record thay đổi** (đều chứa tiếng Việt).
  - ⚠️ **CẦN TEST TRÊN MÁY:** font `fonts/unravel.fgen` (dạng riêng, chưa giải mã) — nếu vào game
    thấy ô vuông thì phải vá font. Nếu không thấy tiếng Việt thì kiểm tra lại bảng ngôn ngữ theo máy.
  - 🐛 **NGHI VẤN CHÍNH của "treo ở logo Nintendo Switch" (07/10):** file `Data.kit.0` trong mod
    là **211.149.762 byte**, còn bản gốc `E:\UNR_work\parts\Data.kit.0` là **209.689.438 byte**
    → **LỚN HƠN 1.460.324 byte**. `kit_repack.py` nén record bị sửa bằng **khối LZ4 literal-only
    (không dùng match)** nên phình to; game rất có thể kiểm tra kích thước file theo index
    (`Data.kit`, 1,4 MB) → treo ngay khi nạp.
    **Hướng sửa:** viết encoder **LZ4-có-từ-điển** (giữ cửa sổ 64 KB như `kit_lz4dict.decode_block`)
    để record sửa nằm **trong đúng ngân sách byte cũ**, giữ **kích thước file bằng đúng bản gốc**.
  - 🧹 Đã xoá file rác `README.md` nằm lẫn trong thư mục mod.
  - ⏳ Còn lại: vá font `.fgen` (nếu cần, sau khi test máy) + chạy `qa_text.py --game unravel`.
- **Chi tiết định dạng + việc còn lại:** `games/0100E5D00CC0C000_UnravelTwo/README.md`.

---

## 6. ⛔ ĐÃ BỎ: Super Mario Party Jamboree (Nintendo Switch)
- **Title ID**: `0100965017338000` (Base) + `0100965017338800` (Update v2.3.0), game 10/2024 (NCA3, SDK 17.5.4)
- **Lý do bỏ (theo yêu cầu người dùng 03/10):** bộ tool hiện tại **không bóc được RomFS** của game này
  (`hactool` → "Failed to read RomFS directory cache"; `nsz` → lỗi đọc section; `ue_romfs_tool` → 0 file).
  Titlekey **đã tìm được** (ticket lưu dạng thô: `e943b92149e3e36aa9445c9167b40f36`) và hactool giải mã NCA OK,
  nhưng phần bảng RomFS (offset metadata > 4 GB) thì chưa tool nào đọc nổi.
- **Không tạo** thư mục game, **không có** gì trong `output/`. File tạm (10,58 GB) đã xoá.
  ROM đã chuyển sang `E:\ROM_Backup\MarioPartyJamboree\` (2 file, SHA256 xác minh).
- **Nếu muốn làm lại:** cần **NSP đã giải mã**, hoặc tự viết module đọc NCA/RomFS. Chi tiết: BH-19 trong `docs/BAI-HOC.md`.

---

## 8. Kirby and the Forgotten Land (Nintendo Switch)
- **Title ID**: `01004D300C5AE000` (Base) / `01004D300C5AE800` (Update v1.1.0)
- **Engine**: Nintendo/HAL (engine "basil") — first-party, **MSBT** + font **BFFNT/BFOTF**
- **Trạng thái**: ✅ **HOÀN THÀNH — đã đóng gói mod (05/10)**
  - **Kho text**: `msg/Kirby15/<LANG>/*.msbt` — **13 ngôn ngữ × 42 file** (+ `Kirby15.msbp`), bóc đủ 547 file.
  - **Dịch**: **2.508 chuỗi** (41 file MSBT) sang tiếng Việt — 10 chunk, giao 5+2 subagent.
    - **QA (`tools/qa_kirby.py`): PASS** — 0 lệch key, 0 sai mã điều khiển, 0 chuỗi rỗng, 0 ký tự lạ.
  - **Font**: 11 font Latin trong `font/ScalableFontBin/*.bfotf.cmp`
    - Định dạng đã giải mã: `.cmp` = `[u32 size][zstd]`; bên trong `.bfotf` = **OTF bọc XOR**
      (magic Kirby `0x36F81A1E`, key khác nhau từng file).
    - ✅ **Cách vá cuối cùng (10/10) — GHÉP glyph tiếng Việt TỪ CHÍNH font gốc**
      (`tools/kirby_patch_all_fonts_native.py`): chữ cái cơ sở lấy nguyên từ font + **glyph dấu rời
      (combining) có sẵn trong font** (`U+0300..0307`); chỉ **vẽ thêm 2 dấu** (móc `ơ ư`, dấu hỏi);
      `đ = d + gạch`; advance width = chữ cái cơ sở. Giữ nguyên cấu trúc CID-Keyed.
    - **11/11 font CFF phủ đủ 146 ký tự VI** (`tools/kirby_verify_mod_fonts.py`), mod **109,5 MB**.
    - 🐛 **Đã sửa lỗi "hiển thị chưa đẹp" (10/10) — BH-42:** trước đó glyph VI lấy từ font ngoài
      **Nunito-Bold** (`vi_only.ttf`) → chữ có dấu đậm/sắc khác chữ thường. Nguyên nhân phụ: thư mục
      `font_edit/` bị FontForge ghi đè bản trộn Nunito (nay **đã khôi phục nguyên bản** từ dump).
    - 🐛 **Đã sửa lỗi "chữ đ thành chữ d trong sub" (10/10) — BH-45:** trong bộ ghép font CFF native (`tools/kirby_patch_all_fonts_native.py`), hàm lọc dấu thanh thiếu mã gạch ngang `0x0335` khiến chữ `đ` thường không bao giờ kích hoạt lệnh vẽ gạch, chỉ trả về chữ `d` trơn. Đã bổ sung `0x0335`, định vị chuẩn nét gạch theo stem của `d` và vá lại toàn bộ 11 font CFF native. Build và đồng bộ mod hoàn tất.
    - Filter.bin (XBIN) đã mở rộng đủ ASCII + VI cho 31 font (`tools/kirby_build_filter_universal.py`).
  - **Đóng gói**: **369 file MSBT ở 9 khe ngôn ngữ Latin** (`US/EU_English, French, Spanish, German,
    Italian, Dutch`) + 11 font. **Giữ nguyên JP/CN/TW/KR** (không phá font khu vực).
  - **Kiểm chứng thành phẩm (`tools/final_check_kirby.py`): PASS** — **15.975/15.975 chuỗi khớp**.
  - Mod: `output/atmosphere/contents/01004D300C5AE000/` — 380 file, 18,2 MB.
  - ROM đã chuyển `E:\ROM_Backup\Kirby\` (2 file, SHA256 xác minh).
  - **Glossary**: ✅ **`glossary/kirby.csv`** — 36 thuật ngữ (kèm **ngoại lệ theo ngữ cảnh** cho
    `Listen`/`Look`/`Fish`). Sau khi dịch đã soát nhất quán: 7 câu nguồn dịch 2 kiểu → đã thống nhất
    (còn lại 3 ngoại lệ **cố ý** theo ngữ cảnh, đã ghi rõ trong glossary).
  - **QA bản dịch cuối (`tools/qa_kirby.py`): PASS** — 2.508 chuỗi, 0 lệch key, **0 lệch mã điều khiển**,
    0 chuỗi rỗng, 0 ký tự lạ (7 cảnh báo ngắt dòng lại — chấp nhận được).
  - ⚠️ **Lỗi quy trình đã ghi bài học (BH-22):** glossary được tạo **SAU** khi dịch (đúng ra phải nạp
    `glossary/master.csv` + tạo glossary game **trước** khi giao subagent). Lần sau làm đúng thứ tự.
- **Cách chơi**: để ngôn ngữ máy = một ngôn ngữ **Latin** (English/Pháp/Đức/Ý/Tây Ban Nha/Hà Lan).
- **Bài học**: **BH-21** trong `docs/BAI-HOC.md` (bẫy "dò khoá vòng tròn" khi gói lại `.bfotf`;
  MSBT nuốt `\0` cuối chuỗi). Chi tiết: `games/01004D300C5AE000_Kirby/README.md`.

---

## 10. It Takes Two (Nintendo Switch)
- **Title ID**: `010092A0172E4000` (Base) / `010092A0172E4800` (Update) + 2 DLC
- **Engine**: Unreal Engine 4 (Hazelight, codename "Nuts")
- **Trạng thái**: ✅ **ĐÃ NÂNG CẤP TOÀN DIỆN & VÁ FONT (11/10)**
  - 🐞 **SỬA LỖI MENU TIẾNG ANH & LỖI FONT (BH-46):**
    - Menu chính (`Play Local`, `Play Online`, `Options`, `Credits`...) và toàn bộ cài đặt game nằm trong `Nuts/Content/Localization/Nuts/*/Nuts.locres` (8.475 entries) và `Untold.locres` (74 entries), trước đây bị sót vì chỉ trích xuất subtitle asset.
    - Đã trích xuất và dịch thêm **4.909 chuỗi UI/Menu** bằng 10 subagent (đối chiếu song ngữ Anh - Trung - Tây Ban Nha). Tổng số chuỗi trong bản dịch nâng lên **7.559 chuỗi**.
    - Đã vá đồng bộ cả 12 ngôn ngữ của `Nuts.locres` và `Untold.locres` (đạt tỷ lệ Việt hóa 98.9% - 100%).
    - **Vá 9 font UI nhị phân (`.ufont`)**: Menu bị lỗi hình thoi do các font TTF gốc (`MarkW1G-Heavy`, `MarkW1G-Medium`, `Poppins-Medium`, `NotoSans`...) trong gói pak thiếu glyph tiếng Việt có dấu (`ơ`, `ư`, `ộ`, `ụ`). Đã dùng `fontTools.merge` tích hợp đầy đủ 100% glyph tiếng Việt vào toàn bộ 9 font `.ufont`.
  - **Đóng gói**: `Nuts-Switch_p.pak` (625 entries gồm 295 .uasset + .uexp phụ đề, 24 file `.locres` của 12 ngôn ngữ, và 11 font UI `.ufont`), dung lượng 7,3 MB.
  - **Đồng bộ**: Đã copy vào `output/atmosphere/contents/010092A0172E4000/` và sync trực tiếp sang Eden (`%APPDATA%\eden\load\010092A0172E4000\`).
- **Công cụ**: `tools/itt_uasset_tool/`, `pylocres`, `tools/build_itt_pak.py`. Glossary: `glossary/ittakestwo.csv`.
- **Bài học**: **BH-23**, **BH-46**. Chi tiết: `games/010092A0172E4000_ItTakesTwo/README.md`.

---

## 11. ✅ XONG PHẦN TEXT: MONOPOLY (2024) (Nintendo Switch)
- **Title ID**: `01002C201BC40000` (Base) / `01002C201BC40800` (Update v1.6)
- 🚨 **SỬA LỖI TREO SPLASH (09/10) — NGUYÊN NHÂN: LỆCH PHIÊN BẢN.**
  - Bản mod đầu tiên được build từ bundle **base v1.0** (`E:\MONO_work\data.unity3d`) trong khi máy chạy
    **v1.6** → game treo ở màn hình splash.
  - Bằng chứng: bundle base = **520.071.132** byte / **198.295 object**; bundle v1.6 = **534.254.661** byte /
    **199.781 object**; các file Oasis base **2.063 mục** vs v1.6 **2.106 mục (+43)**.
  - **Cách lấy bundle v1.6:** trong emulator (Eden/yuzu) chuột phải game → **Dump RomFS** →
    **Dump Mode: FULL** → chọn thư mục (ở đây: `dump/01002C201BC40000/romfs/`).
    ✅ **Đây là cách chuẩn để lấy dữ liệu game — không cần máy Switch, không vướng giải mã NCA/titlekey.**
  - ⛔ Đã thử và KHÔNG dùng được để bóc bản update: `nsz` (ra rác), `hactool` (Invalid NCA header),
    `nstool --basenca` (Hash layer 0 failed hash validation — vì là **Patch NCA**). Chỉ cần Dump RomFS từ emulator.
- **Kết quả build lại từ bundle v1.6:**
  - ✅ Thay **2.106 mục** ở **cả 13 file ngôn ngữ** = **27.378 chỗ**, theo **id**.
  - ✅ Dịch thêm **72 chuỗi mới của v1.6** → **CHƯA DỊCH: 0** (2.106/2.106 mục tiếng Việt).
  - ✅ QA (`tools/mono_final_qa.py`, đối chiếu với bundle v1.6 gốc): 199.781 object khớp · 2.106 id/file ·
    **0 lệch tag · 0 lệch xuống dòng · 0 ký tự lạ · 0 chuỗi rỗng** → **PASS**.
  - Thành phẩm: `output/atmosphere/contents/01002C201BC40000/romfs/Data/data.unity3d`
    (**536.471.432 byte**, gốc v1.6 534.254.661 — chênh 2,2 MB do văn bản tiếng Việt dài hơn).
- **Kho text = hệ thống "Oasis" của Ubisoft** (TextAsset trong `Data/data.unity3d`, XML UTF-16):
  `<oasis><translations language="EnglishGB"><t id="2" text="Online"/>…` — 13 file ngôn ngữ.
- **Kết quả đã build:**
  - ✅ Dịch **1.704 chuỗi duy nhất** (3 subagent, chunk 350) → **thay 2.036 mục** trong XML.
  - ✅ **Vá CẢ 13 file ngôn ngữ** (theo **`id`**, không theo chuỗi) = **26.819 mục** → chọn ngôn ngữ nào
    trong game cũng ra tiếng Việt (giống cách làm Hogwarts): FR/DE/ES/IT/NL/PL/RU/JA/KO/ZH-Hans/ZH-Hant/PT-BR/EnglishGB.
    `oasis__global` là file master (không có `<translations>`) nên bỏ qua đúng.
  - ✅ **QA cuối PASS** (`tools/mono_final_qa.py`, đối chiếu từng mục gốc ↔ thành phẩm, cả 13 file):
    198.295 object khớp · 2.063 id/file khớp · **0 lệch tag** · **0 lệch xuống dòng** ·
    **0 ký tự lạ mới sinh** · 0 chuỗi rỗng · 0 id thiếu/thừa. **id khớp giữa các ngôn ngữ** đã kiểm chứng
    (id 5 = Play/Spielen/プレイ/Jugar/Играть → đều ra "Chơi").
  - ✅ Glossary tạo **TRƯỚC khi dịch** (BH-22): `glossary/monopoly.csv` (47 thuật ngữ chuẩn + gợi ý).
  - ✅ Thành phẩm: `output/atmosphere/contents/01002C201BC40000/romfs/Data/data.unity3d` (**522 MB**, giữ nguyên nén gốc).
  - ✅ `Data/data.unity3d` là **file rời trong RomFS** → **LayeredFS thay trực tiếp, KHÔNG cần patch pak**.
- 🐛 **Lỗi nặng đã tìm ra & sửa ở lần QA cuối (BH-25):** nguồn lưu ngắt dòng bằng tham chiếu ký tự
  `&#xA;` trong thuộc tính XML; bản build đầu ghi **xuống dòng THẬT** → XML chuẩn hoá thuộc tính biến
  thành **dấu cách** → mất ngắt dòng ở **124 mục**. Đã sửa `esc_attr()` (`\n→&#xA;`, `\r→&#xD;`, `\t→&#x9;`).
- 🐛 **Lỗi thứ 2 (BH-26):** `set_raw_data()` cho TextAsset phải **đệm cuối cho tròn 4 byte**,
  nếu không UnityPy đọc lại báo `Expected to read N bytes, but only read N+2`.
  Cũng lưu ý một số file có **NUL ở cuối** (oasis_french) và XML **hỏng sẵn** → **không dùng XML parser**
  cho file dịch, chỉ thay `<t id=".." text="..">` bằng regex theo id.
- ⏳ **Font — cần test trong game:**
  - Game có 80 font TTF đóng trong bundle. **74 font đã đủ ký tự tiếng Việt** ([A-Za-z] + dấu).
  - 6 font còn thiếu: `NotoSans-CondensedBold`, `aline_font`, `LiberationSans` **chỉ thiếu `┿`** (ký hiệu tiền của chính game);
    `PerfectDOSVGA437` (font kiểu DOS) thiếu 93; **`KabelBold` + `KabelMedium` thiếu 88 ký tự có dấu** ← đáng lo nhất.
  - **Nguyên nhân ghép font thất bại:** 2 font Kabel là **OTF/CFF** (`CFF `, `sfntVersion = OTTO`),
    còn `fontTools.merge` chỉ ghép được khi cùng định dạng outline (Arial là `glyf`/TrueType).
    → Muốn ghép phải **dựng lại CFF** (`FontBuilder(isTTF=False)` + `T2CharStringPen`), chưa làm.
- 🐛 **Lỗi công cụ đã gặp & sửa:** file `inspect.py` trong thư mục script tạm **che module chuẩn `inspect`**
  → `import UnityPy` chạy nhầm script cũ. Xem **BH-24**.
- 🐛 **Bài học mới:** `env.save()` **không có** `pack='original'` sẽ xuất bundle **không nén** (520 MB → 1,27 GB).
  Luôn dùng `env.save(pack='original', out_path=…)`.
- Chi tiết: `games/01002C201BC40000_Monopoly/README.md`.
- 🚨 **CÀI MOD (game có update): dùng ID *base* + bundle ĐÚNG PHIÊN BẢN — ĐÃ KIỂM CHỨNG CHẠY THẬT (10/10).**
  - Triệu chứng đã gặp trên Switch: đặt ở ID update `…800` → **không** lên tiếng Việt; đặt **cả 2** folder → **TREO màn hình chờ**.
  - Nguyên nhân: **Atmosphere key LayeredFS theo ID *base* (ID chương trình) và đè lên RomFS đã GỘP (base + update)** —
    khác **Eden/yuzu** (nạp theo ID *update*). Nên folder phải là `…000`, nhưng **nội dung phải là bundle khớp
    phiên bản máy đang chạy** (v1.6).
  - **Cách cài ĐÚNG (Switch, máy có update v1.6):** chỉ **1** folder
    `output/atmosphere/contents/01002C201BC40000/romfs/Data/data.unity3d` = **bundle v1.6** (đã set sẵn trong `output/`).
  - **Eden/yuzu:** dùng folder `…800` (như đang chạy) — Eden nạp mod theo ID update.
  - ⛔ Không đặt cả 2 folder; không để bundle v1.0 ở máy chạy v1.6 (lệch phiên bản → treo/không ăn).
  - ⚠️ Đối chiếu với **Kirby**: Kirby **không có update** nên mod ở ID base là đúng và chạy được (trùng hợp đúng luôn).
- 🚨 **SỬA LỖI [NO_ID]Menu/... (10/10) — LỆCH OFFSET NHỊ PHÂN TEXTASSET (BH-37):**
  - Triệu chứng: Vào game toàn bộ chữ biến thành chuỗi phân cấp hierarchy GameObject dạng `[NO_ID]Menu/Settings/Game`...
  - Nguyên nhân: Script cũ gộp nhầm header nhị phân của Unity vào XML rồi bọc thêm lần nữa làm offset thụt lùi -> engine Oasis không đọc được XML -> fallback in tên GameObject.
  - Cách sửa: Script `tools/mono_build_fixed.py` trích chính xác payload XML từ offset `[4 + name_len + pad + 4]`, giữ BOM UTF-16LE, đệm 4 byte chuẩn xác và thay thế 29.484 mục (cả 13 file ngôn ngữ `<t>` và master `oasis__global` `<l>`).
  - Build sẵn cả 2 Title ID (`0000` = base v1.0, `0800` = update v1.6) — nhưng **khi cài CHỈ dùng 1 ID** khớp phiên bản máy (xem mục trên; đặt cả 2 là treo).
  - Kiểm chứng QA (`tools/mono_final_qa.py`): 199.781 objects khớp, 14/14 file Oasis giải mã hợp lệ, 0 lệch tag/dòng/ký tự lạ -> **PASS 100%**. Game đã lên tiếng Việt hoàn chỉnh.



---

## 13. God Eater 3 (Nintendo Switch)
- **Title ID**: `01001C700873E000`
- **Engine**: Bandai Namco in-house — kho `PKH/PFS/PK` (big-endian), entry nén **zlib**.
- **Nguồn**: `E:\RomFS_Dump\01001C700873E000\romfs\resource\target\nx\pack\mount\retail\{archive00,archive01}.{pfs,pkh,pk}`.
- **Kho text**: `archive00.pk` — **5.516 bảng TSV UTF-16LE** (cột `TextId … Text …`), 694.638 dòng, **26.844 TextId duy nhất** đa ngôn ngữ.
- **Dịch**: **26.844/26.844 TextId** sang tiếng Việt (68 chunk + 1.398 ID vá lỗi) —
  `games/01001C700873E000_GodEater3/translations/{chunks,repair_chunks,vi_master.json}`.
- **Đóng gói**: `tools/ge3_build_mod.py` — thay cột `Text` cho **673.642 dòng** trong 5.494 entry, rebuild `archive00.pk/.pkh`.
- **Font**: vá **14 font** (OTF/CFF + TTF) đủ **217 ký tự** dùng trong bản dịch.
- **QA**: `tools/ge3_qa_final.py` → 0 lệch dòng/key, 0 ô rỗng, 0 ký tự Hán/Nhật/Hàn mới; còn 552 dòng thiếu thẻ mở `<$01/$02/$03>` (cảnh báo).
  `tools/ge3_qa_fonts.py` → 0 ký tự thiếu trên cả 14 font.
- **Thành phẩm**: `output/atmosphere/contents/01001C700873E000/romfs/resource/target/nx/pack/mount/retail/archive00.{pk,pkh}`.
  `archive00.pfs` + `archive01.*` giữ nguyên.
- 🐞 **Lỗi đã sửa:** 2.226 dòng bị xoá trắng do `unique_texts` lấy phải đại diện rỗng → quét lại, dịch bổ sung 1.398 ID, build lại (0 lỗi rỗng).

---

## 12. Hạ tầng repo & đóng gói
- **ĐỢT THỐNG NHẤT THUẬT NGỮ (05/10):** tạo glossary cho Ori WotW / Ori BF / Unravel Two /
  Kirby; sửa `master.csv` (trước đây chứa nội dung Switch Sports) → `switchsports.csv`,
  `master.csv` giờ chỉ còn 4 thuật ngữ **thật sự dùng chung**. Giao 3 subagent thống nhất
  thuật ngữ cho hades2 (586→193), hogwarts (480→260), switchsports (145→101) và build lại mod.
  Ori WotW đã bóc lại bundle + build lại với 4 tên gọi đã sửa. Danh sách còn lại (chủ yếu là
  khác ngữ cảnh hợp lệ): `games/_consistency/*.json`.
- **Glossary hiện có:** `master.csv` (4), `hogwarts_legacy.csv`, `hades2.csv`, `switchsports.csv`,
  `ori.csv`, `ori_bf.csv`, `unravel.csv`, `kirby.csv`.
- **Bài học kinh nghiệm (BẮT BUỘC ĐỌC):** `docs/BAI-HOC.md` — 12 lỗi đã từng xảy ra thật + quy tắc
  chống lặp + checklist bàn giao. **Cổng QA bắt buộc:** `python tools/qa_text.py --game <ten_game>`
  (đã chạy PASS cho hogwarts và ori).
- **Quản lý ROM (BẮT BUỘC):** ROM chỉ nằm trong `input/` trong lúc bóc dữ liệu; **bóc xong chuyển ngay
  ra `E:\ROM_Backup\<Tên game>\`** bằng `python tools/archive_rom.py` (copy → xác minh SHA256 → xoá bản
  trong input; **không dùng `move`** vì file OneDrive là reparse point — xem BH-16 trong `docs/BAI-HOC.md`).
  Hiện `input/` **chỉ còn `prod.keys` + `titlekeys.txt`**; ROM của 4 game đã nằm ở `E:\ROM_Backup`
  (HogwartsLegacy, Hades2, Ori, SwitchSports).
- **Git**: đã khởi tạo (`git init`) + commit đầu; `.gitignore` ẩn khoá (`prod.keys`, `titlekeys.txt`), ROM, cache và dữ liệu nặng.
- **Gói phát hành**: dùng trực tiếp thư mục `output/atmosphere/` — chép nguyên thư mục này vào gốc thẻ nhớ Switch (gộp vào `atmosphere` có sẵn). Gồm cả 3 mod: `0100F7E00C70E000`, `0100A00019DE0000`, `0100D2F00D5C0000`. Hướng dẫn cài: `docs/INSTALL-MOD.txt`.
- **Dọn dẹp**: đã xoá 35 file rác ở thư mục gốc, toàn bộ `__pycache__`, và thư mục `archive/` (~5 MB phụ phẩm cũ).
- **Cấu trúc**: dữ liệu mỗi game nằm trong `games/<TitleID>_<Tên>/{source,translations}`.
