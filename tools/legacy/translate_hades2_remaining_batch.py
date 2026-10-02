"""Translate reviewed remaining Hades II strings in small, repeatable batches."""
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from hades2_sjson_helper import apply_translation_to_sjson  # noqa: E402

SRC = ROOT / "games/0100A00019DE0000_Hades2/source/raw_text/en"
TR = ROOT / "games/0100A00019DE0000_Hades2/translations/Game/Text/en"

translations = {
    "ConsoleText.en.sjson": {
        "MainMenu_ChangeProfiles": {"DisplayName": "Đổi hồ sơ"},
        "SignOutDetected": {
            "DisplayName": "Thông báo: Hồ sơ đã đăng xuất",
            "Description": "Chọn 'OK' rồi đăng nhập bằng hồ sơ {#AlertBoldFormat}%s {#Prev}để tiếp tục, nếu không bạn sẽ trở về Menu chính.",
        },
        "NoProfileWarning": {
            "DisplayName": "Thông báo: Chưa chọn hồ sơ",
            "Description": "Tiến trình và cài đặt sẽ không được lưu. Hãy đăng nhập vào một hồ sơ để tự động lưu tiến trình của bạn.",
        },
        "ExitConfirmDialog_SignIn": {"DisplayName": "Đăng nhập"},
        "ExitConfirmDialog_Ignore": {"DisplayName": "Bỏ qua"},
        "MiscSettingsScreen_DeadZone_PlayStation": {
            "DisplayName": "Vùng chết",
            "Description": "Tinh chỉnh độ nhạy cần trái {#AlertItalicFormat}(hãy tăng nếu điều khiển bị giật).",
        },
        "MiscSettingsScreen_DeadZone_Xbox": {
            "DisplayName": "Vùng chết",
            "Description": "Tinh chỉnh độ nhạy cần trái {#AlertItalicFormat}(hãy tăng nếu điều khiển bị giật).",
        },
        "Menu_PressAnyButton_PlayStation": {"DisplayName": "Nhấn nút bất kỳ"},
    },
    "PatchNotes.en.sjson": {
        "LastUpdate": {"DisplayName": "Cập nhật: "},
        "NextUpdateCountdownCustom": {
            "DisplayName": "Sắp ra mắt:\n {#NextUpdateCountFormat}Ra mắt v1.0!!"
        },
        "NextUpdateCountdown": {
            "DisplayName": "Bản cập nhật lớn tiếp theo sau: {#NextUpdateCountFormat}"
        },
        "NextUpdateCountdownPassed": {
            "DisplayName": "Bản cập nhật lớn tiếp theo\n SẮP RA MẮT!"
        },
        "NextUpdateCountdownSingular": {
            "DisplayName": " {#NextUpdateCountFormat}ngày{#NextUpdateBaseFormat}!"
        },
        "NextUpdateCountdownPlural": {
            "DisplayName": " {#NextUpdateCountFormat}ngày{#NextUpdateBaseFormat}!"
        },
        "NextUpdateGeneral": {"DisplayName": "Sắp ra mắt!"},
        "DevBuildWatermark": {"DisplayName": "v0."},
        "ControllerWarning": {
            "DisplayName": "Lưu ý: Nên chơi bằng tay cầm."
        },
        "AudioDriverWarning": {
            "DisplayName": "Âm thanh đã tắt! Hãy cập nhật trình điều khiển âm thanh."
        },
        "PatchNotesScreen_ShowSpoilers": {
            "DisplayName": "{MX} HIỆN SPOILER"
        },
        "PatchNotesScreen_HideSpoilers": {
            "DisplayName": "{MX} ẨN SPOILER"
        },
        "MainMenuScreen_PatchSubHeading": {
            "DisplayName": "@GUI\\Icons\\GhostPack {#CommonFormat} - Thay đổi dựa trên góp ý của cộng đồng!"
        },
        "MainMenuScreen_PatchNotes": {"DisplayName": "Ghi chú cập nhật"},
        "MainMenuScreen_PatchNotesTitle": {"DisplayName": "Ghi chú cập nhật"},
        "MainMenuScreen_Roadmap": {"DisplayName": "Lộ trình phát triển"},
    },
    "_EnemyData_Eris.en.sjson": {
        "ErisField_0074": {"DisplayName": "{#Emph}Được đấy..."},
        "ErisField_0075": {"DisplayName": "Trúng rồi."},
        "ErisField_0076": {"DisplayName": "Muốn nữa không?"},
        "ErisField_0077": {"DisplayName": "Thế nào?"},
        "ErisField_0078": {"DisplayName": "Ta còn nhiều lắm."},
        "ErisField_0079": {"DisplayName": "Ngươi chết chắc rồi."},
        "ErisField_0080": {"DisplayName": "Vui lắm nhỉ?"},
        "ErisField_0081": {"DisplayName": "{#Emph}Ôi {#Prev}, tội nghiệp chưa kìa!"},
        "ErisField_0100": {"DisplayName": "Vẫn trụ được à, {#Emph}hả?"},
        "ErisField_0101": {"DisplayName": "Đầu hàng {#Emph}đi!"},
        "ErisField_0102": {"DisplayName": "Ôi thôi {#Emph}nào!"},
        "ErisField_0103": {"DisplayName": "Chết {#Emph}đi!"},
        "ErisField_0104": {"DisplayName": "Lại nữa à?"},
        "ErisField_0105": {"DisplayName": "Ôi, {#Emph}thật luôn?"},
        "ErisField_0342": {"DisplayName": "Cơ hội cuối {#Emph}đấy!"},
        "ErisField_0343": {"DisplayName": "{#Emph}Không được sai nữa!"},
        "ErisField_0344": {"DisplayName": "{#Emph}Lần này ta sẽ kết liễu ngươi!"},
        "ErisField_0433": {"DisplayName": "{#Emph}Moros...!"},
        "ErisField_0434": {"DisplayName": "Đồ gian lận!"},
        "ErisField_0435": {"DisplayName": "Cái Ghim khốn kiếp đó!"},
        "ErisField_0436": {"DisplayName": "Ta đã {#Emph}tóm được ngươi {#Prev}rồi!"},
        "ErisField_0431": {"DisplayName": "Ngươi cứ tránh đạn của ta mãi!"},
        "ErisField_0432": {"DisplayName": "Đạn của ta không xuyên qua được sao?!"},
        "ErisField_0301": {"DisplayName": "Không-{#Emph}đời nào!"},
        "ErisField_0302": {"DisplayName": "Ta chẳng bao giờ thay đổi đâu!"},
        "ErisField_0160": {"DisplayName": "Cái quái gì vậy?!"},
        "ErisField_0096": {"DisplayName": "Thật à?"},
        "ErisField_0097": {"DisplayName": "Thật sao!"},
        "ErisField_0098": {"DisplayName": "Thôi nào..."},
        "ErisField_0094": {"DisplayName": "Ngươi..."},
        "ErisField_0095": {"DisplayName": "Không ổn rồi...!"},
        "ErisField_0117": {"DisplayName": "Ta cứ tưởng chúng ta là bạn chứ?!"},
        "ErisField_0118": {"DisplayName": "Sao ngươi nỡ làm thế với ta, cưng?!"},
        "ErisField_0121": {"DisplayName": "Không...! Ngươi nhầm rồi...!"},
        "ErisField_0346": {"DisplayName": "...Giờ ta phải... trở về bóng tối sao...?"},
        "ErisField_0348": {"DisplayName": "Đừng hòng lôi ta về địa ngục mà không đánh nhau!"},
        "ErisField_0485": {"DisplayName": "Sao ngươi... nhanh thế?"},
        "MelinoeField_1907": {"DisplayName": "Ngươi khơi mào trước."},
        "MelinoeField_1908": {"DisplayName": "Cô ta khơi mào trước."},
        "MelinoeField_1909": {"DisplayName": "Biến đi."},
        "MelinoeField_1910": {"DisplayName": "Cút đi."},
        "MelinoeField_1911": {"DisplayName": "Nhớ lấy đấy."},
        "MelinoeField_1912": {"DisplayName": "Cô ta chẳng bao giờ rút kinh nghiệm."},
        "MelinoeField_1913": {"DisplayName": "Gặp lại sau nhé, Eris."},
        "MelinoeField_1914": {"DisplayName": "Đỡ hơn rồi..."},
        "MelinoeField_1806": {
            "DisplayName": "Ngươi biết thừa ta định đi đâu rồi. Ta tự đến đó được, cảm ơn."
        },
        "MelinoeField_1807": {
            "DisplayName": "Ta không thích kiểu ám chỉ đó đâu, Eris. Nói thẳng, hoặc tránh đường ta ra."
        },
        "MelinoeField_3267": {
            "DisplayName": "Sao ngươi dồn hết sức ngăn ta? Ngươi là nữ thần Bất Hòa, lẽ ra phải khó đoán chứ! Thử chuyển sang quấy phá quân Chronos xem, đổi gió một chút..."
        },
        "MelinoeField_1921": {
            "DisplayName": "Ngươi đang chắn đường ta đến mục tiêu, Eris... à, đang lơ lửng mới đúng. Dù sao sớm muộn ngươi cũng sẽ hiểu đó là sai lầm."
        },
        "MelinoeField_1922": {
            "DisplayName": "Ta chẳng thể nói mình thích chút nào những trận đánh vô nghĩa này... Dù ít nhất đêm nay trăng đẹp nhỉ?"
        },
        "ErisField_0155": {
            "DisplayName": "Ngươi tưởng chỉ vì thân thiết với ta ở Ngã ba Địa Giới mà ta sẽ nương tay với ngươi ở đây à? Mơ đi, cưng! Ta biết ngươi đang toan tính gì."
        },
        "MelinoeField_3075": {
            "DisplayName": "Ngươi biết ta định làm gì vì ta đã giải thích thẳng thắn không biết bao nhiêu lần. Vậy mà ngươi vẫn giả vờ như chuyện này phức tạp lắm."
        },
        "MelinoeField_3076": {
            "DisplayName": "Lúc nào cũng sẵn sàng lao vào đánh nhau. Ta chưa từng gặp ai quyết tâm đến thế mà lại chẳng có mục đích gì."
        },
    }
}


for filename, entries in translations.items():
    source = SRC / filename
    target = TR / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copy2(source, target)
    original = target.read_text(encoding="utf-8-sig")
    updated = apply_translation_to_sjson(original, entries)
    target.write_text(updated, encoding="utf-8")
    print(f"Translated {len(entries)} entries in {filename}")
