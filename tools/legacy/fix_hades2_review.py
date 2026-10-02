"""Apply reviewed Hades II wording fixes using UTF-8-safe file writes."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from hades2_sjson_helper import _iter_text_blocks  # noqa: E402

TR = ROOT / "games/0100A00019DE0000_Hades2/translations/Game/Text/en"

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def set_field(filename: str, entry_id: str, field: str, value: str) -> None:
    path = TR / filename
    raw = path.read_text(encoding="utf-8-sig")
    for current_id, full, body, start, end in _iter_text_blocks(raw):
        if current_id != entry_id:
            continue
        pattern = re.compile(
            rf'({field}\s*=\s*)(?:"""(.*?)"""|"((?:[^"\\]|\\.)*)")',
            re.S,
        )
        match = pattern.search(body)
        if not match:
            raise ValueError(f"Field missing: {filename}/{entry_id}/{field}")
        if "\n" in value:
            replacement = match.group(1) + '"""' + value + '"""'
        else:
            # The SJSON parser used by this project reads field contents as-is;
            # preserve deliberate backslash control sequences such as \n.
            escaped = value.replace('"', '\\"')
            replacement = match.group(1) + '"' + escaped + '"'
        body = body[:match.start()] + replacement + body[match.end():]
        id_prefix = re.match(r'\{\s*Id\s*=\s*"[^"]+"', full).group(0)
        raw = raw[:start] + id_prefix + body + "}" + raw[end + 1:]
        path.write_text(raw, encoding="utf-8")
        return
    raise ValueError(f"Entry missing: {filename}/{entry_id}")


repairs = {
    ("ScreenText.en.sjson", "MetaUpgrade_CardUnlocksAvailable", "Description"):
        "Ngươi có thể dùng {#BoldFormatGraft}Lá Bài Arcana{#Prev}. Mỗi lá được kích hoạt sẽ giúp ngươi mạnh lên theo cách riêng.\n\n        Chọn một {#BoldFormatGraft}Lá Bài {#Prev}đã mở để mở khóa vĩnh viễn.",
    ("ScreenText.en.sjson", "MetaUpgradeTable_UnableToEquip", "DisplayName"):
        "{#MemFormat}Đã đạt {#Prev}giới hạn Tâm thức!",
    ("ScreenText.en.sjson", "MetaUpgradeTable_UnableToEquip_Alt", "DisplayName"):
        "{#MemFormat}Đã đạt {#Prev}giới hạn Tâm thức!",
    ("ScreenText.en.sjson", "TradeScreen_Title", "DisplayName"): "Trao đổi",
    ("ScreenText.en.sjson", "BoonInfo_LinkedGod_Boon", "DisplayName"):
        "{!Icons.Bullet}Ân huệ bất kỳ của {$TempTextData.LinkedGod}",
    ("ScreenText.en.sjson", "RunClearScreen_RunStats", "DisplayName"): "Thống kê",
    ("ShellText.en.sjson", "EasyModeResistanceCap", "DisplayName"):
        "{!Icons.EasyModeIcon} Giới hạn Thần Thoại",
    ("ShellText.en.sjson", "EasyModeResistanceCap_Disabled", "DisplayName"):
        "Giới hạn Thần Thoại",
    ("ShellText.en.sjson", "SprintAutoHold", "DisplayName"): "Tự chạy nhanh",
    ("ShellText.en.sjson", "VSync", "DisplayName"): "V-Sync",
    ("ShellText.en.sjson", "Vsync", "DisplayName"): "V-Sync",
    ("ShellText.en.sjson", "DrawHealthFX", "DisplayName"): "Tối viền màn hình",
    ("ShellText.en.sjson", "ShowUIAnimations", "DisplayName"): "Hiện HUD chiến đấu",
    ("ShellText.en.sjson", "RequireFocusToUpdate", "DisplayName"):
        "Tạm dừng khi Alt-Tab",
    ("ShellText.en.sjson", "DisableDamage", "DisplayName"): "Tắt sát thương",
    ("ShellText.en.sjson", "SaveErrorNoSpace", "DisplayName"): "Thông báo",
    ("ShellText.en.sjson", "SaveErrorNoSpace", "Description"):
        "Thiết bị lưu trữ không còn đủ dung lượng. \\n\\n Thử lại?",
    ("ShellText.en.sjson", "SaveErrorGeneric", "Description"):
        "Không thể lưu tiến trình vào thiết bị lưu trữ. \\n \\n Thử lại?",
    ("ShellText.en.sjson", "ConfirmResolution", "DisplayName"): "Thông báo",
    ("ShellText.en.sjson", "ScreenshotSaved", "DisplayName"):
        "Đã lưu ảnh chụp màn hình: %s",
    ("ShellText.en.sjson", "PauseScreen_ExitConfirm_ValidCheckpoint_Recent", "Description"):
        "Bạn sẽ trở về Menu chính và có thể tiếp tục tại chính Khu vực này. \\n \\n Tiến trình vừa được lưu chưa đầy một phút trước.",
    ("ShellText.en.sjson", "PauseScreen_ExitConfirm_ValidCheckpoint", "Description"):
        "Bạn sẽ trở về Menu chính và có thể tiếp tục tại chính Khu vực này. \\n \\n Tiến trình đã được lưu ",
    ("ShellText.en.sjson", "PauseScreen_ExitConfirm_ValidCheckpoint_HasCloudSaves_Recent", "Description"):
        "Tải tiến trình hiện tại lên đám mây rồi trở về Menu chính? Bạn có thể tiếp tục từ điểm này. \\n\\n Tiến trình vừa được lưu chưa đầy một phút trước.",
    ("ShellText.en.sjson", "PauseScreen_ExitConfirm_ValidCheckpoint_HasCloudSaves", "Description"):
        "Tải tiến trình hiện tại lên đám mây rồi trở về Menu chính? Bạn có thể tiếp tục từ đây. \\n\\n Tiến trình đã được lưu ",
    ("_NPCData_Circe.en.sjson", "Circe_0065", "DisplayName"):
        r"{#Emph}Cơn gió lốc, bọt biển tung, \n" + "\t" + "{#Emph}Nắm đất nâu, cành cây rừng,",
    ("_NPCData_Circe.en.sjson", "Circe_0077", "DisplayName"):
        r"{#Emph}Tắm ánh trăng, tất cả các ngươi, \n" + "\t" + "{#Emph}Cho đến khi thành thuốc phù thủy!",
    ("_NPCData_Hecate.en.sjson", "Melinoe_0970", "DisplayName"):
        "Con lại mơ thấy Cha. Chronos đến bắt Cha, còn cô đưa con đến nơi an toàn. Nhưng lần này, con ở lại đó lâu hơn trước.",
    ("_NPCData_Hecate.en.sjson", "Melinoe_2916", "DisplayName"):
        "Con biết Chronos muốn Cha chỉ cho hắn nơi tìm Ba Mệnh Nữ. Chronos ghét họ, hay sợ họ. Hắn tìm họ suốt bấy lâu nay, đúng không? Cuối cùng thì hắn cũng tìm ra.",
    ("_NPCData_Hecate.en.sjson", "Melinoe_1178", "DisplayName"):
        "Hắn cảm ơn các Mệnh Nữ vì cuối cùng chúng ta cũng gặp nhau, như thể hắn đã tìm con suốt bấy lâu... rồi bảo con đừng lặp lại sai lầm của gia đình.",
    ("_NPCData_Hecate.en.sjson", "Melinoe_2914", "DisplayName"):
        "Tối qua, Hiệu trưởng, con đi qua cánh cổng dẫn xuống tận đáy Chaos... và gặp chủ nhân nơi đó! Con đã nghe Người kể nhiều về Nyx, nhưng không ngờ lại gặp cả cha mẹ nàng.",
    ("_NPCData_Hecate.en.sjson", "Melinoe_4943", "DisplayName"):
        "Mà, {#Emph}sao...? {#Prev}Người được gặp lại Mẫu thân, Phụ thân và Nyx! Con thấy họ biết ơn Người lắm! {#Emph}Con {#Prev}cũng biết ơn Người vô cùng! Mọi chuyện có thể không diễn ra đúng như kế hoạch, nhưng kết quả lại đúng như điều chúng ta mong muốn, phải không?",
    ("_NPCData_Hades.en.sjson", "Melinoe_1057_B", "DisplayName"):
        "{#Emph}<Gasp> {#Prev}Cha Hades, người là... Cha của con. Con là... Melinoë. Con là con gái của Cha.",
    ("_NPCData_Chronos.en.sjson", "Chronos_1031", "DisplayName"):
        "Ừ, ta khá chắc chắn! Những ảo ảnh Asphodel ta có thể tạo ra cũng dựa trên nguyên lý tương tự. Con cũng đã chứng tỏ mình giỏi thoát khỏi gông cùm thời gian.",
    ("_NPCData_Chronos.en.sjson", "MelinoeField_4131", "DisplayName"):
        "Chưa hẳn. Chuyện này sẽ giống trên đỉnh Olympus chứ? Như cách ngài tạo ra ảo ảnh về một thời khắc lẽ ra đã xảy ra...",
    ("_NPCData_Chronos.en.sjson", "MelinoeField_4133", "DisplayName"):
        "Chưa hẳn. Chuyện này sẽ giống ở Dinh Thự của cha con chứ? Như cách ngài tạo ra ảo ảnh về một thời khắc lẽ ra đã xảy ra...",
    ("HelpText.en.sjson", "EpilogueReached", "DisplayName"):
        "ĐỊNH MỆNH VIÊN MÃN",
    ("HelpText.en.sjson", "QuestRandomBountyClearStreak", "Description"):
        "Con gái của chúa tể thần chết phải hoàn thành ít nhất hai lần các Thử thách {$BountyData.PackageBountyRandomSurface_Difficulty1.Name} hoặc {$BountyData.PackageBountyRandomUnderworld_Difficulty1.Name} xuất hiện trên {$Keywords.BountyBoard}, không được thất bại lần nào. Kết quả không tưởng.",
    ("HelpText.en.sjson", "QuestRandomBountyClearStreak_Condition", "DisplayName"):
        "{!Icons.QuestProgressIncomplete} Hoàn thành liên tiếp hai {$Keywords.PackagedBounties} ngẫu nhiên bất kỳ",
    ("HelpText.en.sjson", "QuestRandomBountyClearStreak_Cleared", "DisplayName"):
        "{!Icons.QuestProgressComplete} Hoàn thành liên tiếp hai {$Keywords.PackagedBounties} ngẫu nhiên bất kỳ",
    ("_NPCData_Hecate.en.sjson", "Melinoe_0582", "DisplayName"):
        "{#Emph}Hừm... {#Prev}Hiệu trưởng, chỉ là... con khó khơi dậy cơn giận lẽ ra mình phải có. Con được giao nhiệm vụ giết một Titan còn chẳng quen biết, để trả thù cho gia đình mà con không thể nhớ...",
    ("_NPCData_Hecate.en.sjson", "Hecate_0707", "DisplayName"):
        "{#Emph}Ta {#Prev}cũng là một nữ Titan, Selene cũng vậy, đừng quên! Dòng dõi không nhất thiết quyết định lòng trung thành hay nguyên tắc của chúng ta. Dù có lẽ Prometheus lại nghĩ khác.",
    ("_NPCData_Hecate.en.sjson", "Melinoe_2799", "DisplayName"):
        "Con tới rìa Tartarus rồi tiến vào Dinh Thự, đúng như kế hoạch. Chronos ở đó, ngồi trên ngai của Cha. Bọn con giao chiến. Hắn thua. Nhưng con biết hắn chưa biến mất. Con cũng không thể nấn ná lâu.",
    ("_NPCData_Hecate.en.sjson", "Melinoe_4733", "DisplayName"):
        "Ngọn giáo Gigaros của cha con... nó nằm trong phòng của Hoàng tử để con tìm thấy. Hẳn Zagreus đã lấy được nó trước đây, như con bây giờ. Vậy chỉ còn bước cuối cùng thôi nhỉ?",
    ("_NPCData_Hecate.en.sjson", "Melinoe_1029", "DisplayName"):
        "Con tìm thấy Cha rồi, Hiệu trưởng! Cha bị Chronos giam ở Tartarus. Nhưng con không thể cứu Cha... Cha bảo con cứ để Cha lại...",
    ("_NPCData_Hecate.en.sjson", "Melinoe_3456", "DisplayName"):
        "Hiệu trưởng, Cha nhờ con chuyển lời: Cha xin gửi lời cảm ơn sâu sắc nhất...",
    ("_NPCData_Hecate.en.sjson", "Melinoe_3457", "DisplayName"):
        "Cha kể với con chuyện Cha giao con cho Người chăm sóc khi Chronos tấn công. Hẳn Cha đã lo điều tồi tệ nhất. Giờ Cha biết con vẫn bình an... tất cả đều nhờ Người.",
    ("_NPCData_Hecate.en.sjson", "Melinoe_2909", "DisplayName"):
        "Ở rìa Cánh đồng U buồn... con chạm trán một con quái thú địa ngục đen sì. Ba cái mõm chó quái dị gầm lên đầy giận dữ và đau buồn. Đó là con chó già của Cha... của {#Emph}gia đình {#Prev}con... đúng không?",
    ("_NPCData_Hades.en.sjson", "Hades_0054", "DisplayName"):
        "Không. Điều khiến ta đau lòng nhất... là mẹ con, ta, anh trai con và cả con chó này đã không thể ở đó nhìn con lớn lên. Mỗi lần gặp con giờ đây... lại lấp đầy khoảng trống trong lòng ta.",
    ("_NPCData_Chronos.en.sjson", "Chronos_0615", "DisplayName"):
        "Con trai yêu quý của ta, Zeus, lại tiếp tay cho ngươi đêm nay sao? Ta chẳng sợ tia sét lừng danh của nó, thằng nhóc ngốc nghếch ấy.",
    ("_NPCData_Chronos.en.sjson", "Chronos_1030", "DisplayName"):
        "Tốt, cuối cùng con cũng đến! Giờ con đã lần theo lộ trình cũ, ta có thể thao túng dòng thời gian để đưa con tới Dinh Thự, trong lúc một tàn ảnh của ta ngồi trên ngai của cha con. Sẵn sàng chưa?",
    ("_NPCData_Chronos.en.sjson", "Chronos_1085", "DisplayName"):
        "Cha con và em trai ông ấy là Zeus đã rộng lòng cho ta cơ hội được phụng sự Âm phủ đôi chút. Quần đảo Phúc Lạc là nơi tuyệt vời nhất Elysium! Ta nhất định sẽ giữ chúng như vậy.",
}


def recover_mojibake(text: str) -> str:
    # These literals were accidentally saved after a UTF-8/Windows-1252 round trip.
    try:
        return text.encode("cp1252").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


for (filename, entry_id, field), text in repairs.items():
    text = recover_mojibake(text)
    set_field(filename, entry_id, field, text)

print(f"Đã khôi phục {len(repairs)} câu/chú thích bằng UTF-8.")
