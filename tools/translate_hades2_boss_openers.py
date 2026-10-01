"""Translate a first reviewed set of Hades II boss combat barks."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from hades2_sjson_helper import apply_translation_to_sjson  # noqa: E402

SRC = ROOT / "working/0100A00019DE0000_Hades2/raw_text/en"
TR = ROOT / "translations/0100A00019DE0000_Hades2/Game/Text/en"

translations = {
    "_EnemyData_Hecate.en.sjson": {
        "HecateField_0395": "Con chồn hung dữ!", "Hecate_0108": "Đừng giữ sức!", "Hecate_0110": "Đó!", "Hecate_0112": "Nhanh lên!", "Hecate_0113": "Lại nào.", "Hecate_0114": "Lại nữa!", "Hecate_0115": "Tấn công tiếp đi!", "Hecate_0116": "Đúng thế!",
        "HecateField_0040": "Đòn tốt đấy.", "HecateField_0041": "Làm tốt lắm.", "HecateField_0045": "Theo đà mà đánh.", "Hecate_0109": "{#Emph}Ừm...", "Hecate_0364": "{#Emph}Kh...", "Hecate_0366": "{#Emph}Ư...", "Hecate_0367": "Phong độ tốt lắm...", "Hecate_0368": "Kết thúc đi...!",
        "HecateField_0046": "Tấn công tiếp đi...!", "HecateField_0047": "Con ngày càng mạnh rồi.", "HecateField_0049": "Kết liễu đi!", "Hecate_0011": "Dừng tay!",
        "HecateField_0219": "Ta sẽ giữ hình dạng này, cảm ơn.", "HecateField_0384": "Trò đó không có tác dụng với ta.", "HecateField_0385": "Ở tuổi này thì đừng hòng!", "HecateField_0386": "Ta không thể đổi {#Emph}điều đó{#Prev} dễ dàng đến vậy.",
        "HecateField_0070": "Con láu cá thật đấy!", "HecateField_0068": "Thật vậy sao?", "HecateField_0396": "{#Emph}Lẹ lên{#Prev}, ếch!", "HecateField_0397": "Con ếch đó...", "HecateField_0398": "Con với con ếch của con...",
        "HecateField_0388": "Con quạ này.", "HecateField_0389": "Con quạ nhỏ gan dạ...", "HecateField_0235": "Lùi lại, mèo.", "HecateField_0236": "Con {#Emph}mèo này...", "HecateField_0237": "Mèo...?", "HecateField_0238": "Con mèo chết tiệt...",
        "HecateField_0390": "Ngoan lắm, Hecuba!", "HecateField_0391": "Nhe nanh ra!", "HecateField_0392": "Chó săn ngoan!", "HecateField_0393": "Gale, ta cảm nhận được đòn đó!", "HecateField_0394": "Con dám làm thế sao, Gale?",
        "Hecate_0498": "Con nổi nóng dữ vậy!", "Hecate_0499": "Giữ bình tĩnh.", "Hecate_0500": "Đừng sơ suất ở đây.", "Hecate_0501": "Chưa muốn quay về sao?", "Hecate_0502": "Cứng cỏi đấy.", "Hecate_0503": "Lại chống đối ta nữa rồi.", "Hecate_0504": "Bình tĩnh lại.",
        "HecateField_0053": "Rút kinh nghiệm đi.", "HecateField_0054": "Ta đi tiếp thôi...", "Hecate_0505": "Hết giờ.", "Hecate_0506": "Con hết thời gian rồi.", "Hecate_0507": "Con định làm gì?",
        "Hecate_0118": "Tiếc là không.", "Hecate_0119": "Ta chẳng cảm thấy gì cả.", "Hecate_0120": "Chẳng liên quan!", "Hecate_0121": "Kiểm soát bản thân đi.", "Hecate_0122": "Ta không nghĩ vậy.", "Hecate_0123": "Thử cách khác đi!",
        "HecateField_0056": "Con đánh cũng vô ích.", "HecateField_0057": "Con không phá được kết giới của ta.", "HecateField_0058": "Lùi lại.", "HecateField_0059": "Giữ sức đi.", "HecateField_0220": "{#Emph}Hừ.",
        "Hecate_0095": "Con đã có thể tránh đòn đó.", "Hecate_0096": "Đứng dậy, Melinoë!", "Hecate_0097": "Chậm quá!", "Hecate_0098": "Để lộ sơ hở rồi.", "Hecate_0099": "Con đã mất cảnh giác.", "Hecate_0100": "Đòn đó hoàn toàn tránh được!", "Hecate_0101": "Tự bảo vệ mình đi!", "Hecate_0102": "Nào, cố lên.",
        "HecateField_0030": "Bị bất ngờ rồi.", "HecateField_0031": "Bắt được con rồi.", "HecateField_0032": "Đoán trước đòn đánh của ta đi.", "HecateField_0033": "Phản công đi!", "HecateField_0034": "Con tránh được mà.", "HecateField_0035": "Ta sẽ không nương tay đâu.", "HecateField_0036": "Luôn cảnh giác!", "HecateField_0037": "Né đi!", "Hecate_0339": "Chà chà!", "Hecate_0340": "Tập trung, Melinoë!", "Hecate_0341": "Đúng thế!", "Hecate_0342": "Con đã chống đỡ được đòn của ta sao?", "Hecate_0343": "Phản kháng đi!", "Hecate_0344": "Vững vàng lên, Phù thủy!", "Hecate_0345": "Vẫn đứng vững à?", "Hecate_0346": "Con chịu được đòn đó sao?", "Hecate_0497": "Bóng tối sẽ nuốt chửng con.",
    },
    "_EnemyData_Polyphemus.en.sjson": {
        "Polyphemus_0256": "Được rồi, đến nước này thì...", "Polyphemus_0257": "Thế là đủ rồi.", "Polyphemus_0258": "Ngươi làm ta nổi cáu rồi đấy.", "Polyphemus_0259": "Hết đùa giỡn nhé.", "Polyphemus_0260": "Được thôi...", "Polyphemus_0261": "Ngươi sắp phải trả giá...", "Polyphemus_0262": "Ta chẳng thích chuyện này chút nào.", "Polyphemus_0263": "Đồ nhãi ranh khốn kiếp...", "Polyphemus_0369": "Ta bắt đầu ngán ngươi rồi đấy, thịt tươi!", "Polyphemus_0370": "Đồ thối tha vô dụng, {#Emph}ưrgh!", "Polyphemus_0371": "Ta hết tử tế với ngươi rồi.", "Polyphemus_0372": "Ngươi làm ta bực mình rồi!", "Polyphemus_0373": "Hay kết thúc chuyện này đi?", "Polyphemus_0374": "Ta chịu ngươi hết nổi rồi...", "Polyphemus_0375": "Ngươi phải ở lại ăn thêm chứ...", "Polyphemus_0376": "Được, {#Emph}đủ {#Prev}rồi đấy.", "Polyphemus_0054": "Thích thế à?", "Polyphemus_0055": "Vẫn còn giãy được sao?", "Polyphemus_0056": "Ta chưa xử ngươi xong đâu.", "Polyphemus_0057": "{#Emph}Ôi{#Prev}, sao thế?", "Polyphemus_0058": "Đáng đời ngươi.", "Polyphemus_0059": "{#Emph}Khà khà khà...", "Polyphemus_0060": "Ta sẽ ăn thịt ngươi...", "Polyphemus_0061": "Ta sẽ ăn thịt ngươi...!", "Polyphemus_0232": "Chính thế.",
    },
    "_EnemyData_Prometheus.en.sjson": {
        "Prometheus_0103": "Nhưng ta thì có.", "Prometheus_0103_B": "Nhưng ta thì có.", "Prometheus_0104": "Ta không nghĩ vậy.", "Prometheus_0180": "Nhưng cũng sắp thôi.", "Prometheus_0181": "{#Emph}Không đời nào.", "Prometheus_0182": "Chưa hẳn.", "Prometheus_0183": "Ngươi sẽ còn chịu khổ nhiều.", "Prometheus_0184": "Đừng hòng.", "Prometheus_0185": "Rồi ngươi sẽ thấy.", "Prometheus_0186": "Chẳng được bao lâu đâu.", "Prometheus_0187": "Ta {#Emph}có{#Prev} đấy.", "Prometheus_0188": "Phải.", "Prometheus_0188_B": "Phải.", "Prometheus_0189": "Khốn {#Emph}kiếp ngươi.", "Prometheus_0105": "Sức ngươi đang cạn dần.", "Prometheus_0106": "Vậy mà ngươi chống đỡ được...", "Prometheus_0099": "Không đau đớn thì đời còn gì thú vị?", "Prometheus_0100": "Hãy chịu khổ như ta từng chịu.", "Prometheus_0101": "Vậy thì chịu khổ đi.", "Prometheus_0102": "Quay đầu đi.", "Prometheus_0172": "Quay về đi.", "Prometheus_0173": "Trở về địa ngục đi.", "Prometheus_0174": "Rời khỏi nơi này.", "Prometheus_0175": "Thấy chưa?", "Prometheus_0176": "Ta sẽ không nương tay đâu.",
    },
    "_EnemyData_Scylla.en.sjson": {
        "Scylla_0101": "{#Emph}Ái!!", "Scylla_0102": "{#Emph}Ái!", "Scylla_0103": "{#Emph}Này!", "Scylla_0104": "{#Emph}Nàyyy!", "Scylla_0105": "{#Emph}Ư...!", "Scylla_0106": "{#Emph}Hả!", "Scylla_0107": "Đánh đi chứ!", "Scylla_0108": "Đánh ta đi!", "Scylla_0109": "Đánh ta một phát đi!", "Scylla_0110": "Ồ!", "Scylla_0111": "{#Emph}Ưrgh!", "Scylla_0112": "{#Emph}Này...!", "Scylla_0113": "{#Emph}Ư...!", "Scylla_0114": "Ngươi!", "Scylla_0079": "{#Emph}Chà!", "Scylla_0080": "{#Emph}Ha!", "Scylla_0081": "{#Emph}Ha!", "Scylla_0082": "{#Emph}Mọi người ơi!", "Scylla_0083": "Mọi người, cùng nào!", "Scylla_0098": "{#Emph}Ha ha ha!", "Scylla_0100": "{#Emph}Hả!", "Scylla_0236": "Ta... chính là... {#Emph}Scylla!!", "Scylla_0237": "{#Emph}Nào nào{#Prev}, mọi người!", "Scylla_0238": "Cô ta là của ta...", "Scylla_0239": "Ai cơ, ta á?",
    },
}


translations["_EnemyData_Hecate.en.sjson"].update({
    "Hecate_0124": "?? r?i!", "Hecate_0125": "?? l?m r?i ??y!", "Hecate_0126": "T?t!", "Hecate_0127": "R?t t?t!",
    "Hecate_0128": "Th? l?ng ?i!", "Hecate_0129": "Xu?t s?c.", "Hecate_0130": "{#Emph}Kh... {#Prev}xu?t s?c.",
    "Hecate_0131": "???c r?i, ???c r?i!", "Hecate_0369": "L?m t?t l?m!", "Hecate_0370": "?? r?i!",
    "Hecate_0371": "?? r?i! Ta xin thua.", "Hecate_0372": "D?ng l?i! ??nh hay l?m.", "Hecate_0373": "???c r?i, d?ng tay!",
    "Hecate_0374": "??t y?u c?u!", "Hecate_0375": "{#Emph}?... {#Prev}??t y?u c?u!", "Hecate_0376": "V?... d?ng!",
    "HecateField_0080": "D?ng!", "HecateField_0081": "D?ng! Ta xin thua.", "HecateField_0082": "D?ng! Ngh? ?i.",
    "HecateField_0083": "D?ng! T?t l?m.", "HecateField_0084": "D?ng! Xu?t s?c.", "HecateField_0085": "?? l?m r?i ??y!",
    "Hecate_0104": "T?t.", "Hecate_0107": "L?m t?t l?m!", "Hecate_0111": "Th? ??nh kh? l?m.", "Hecate_0117": "??nh tr?ng r?i.",
    "HecateField_0038": "??ng ham ??nh qu?.", "HecateField_0039": "{#Emph}??n ?? {#Prev}?au ??y.",
    "HecateField_0042": "C?n th?n.", "HecateField_0043": "??ng r?i.", "HecateField_0044": "C? th?.",
    "Hecate_0103": "T?t!", "Hecate_0106": "L?m t?t l?m.", "Hecate_0105": "{#Emph}?... {#Prev}t?t!",
    "Hecate_0365": "{#Emph}H?m...", "HecateField_0048": "C? th?...!",
})

for filename, values in translations.items():
    source = (SRC / filename).read_text(encoding="utf-8-sig")
    mapped = {key: {"DisplayName": value} for key, value in values.items()}
    target = TR / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(apply_translation_to_sjson(source, mapped), encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"{filename}: {len(values)} câu đã dịch")
