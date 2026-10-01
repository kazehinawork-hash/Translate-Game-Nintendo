"""Translate the opening family-dialogue sequence in Ares's Hades II text."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from hades2_sjson_helper import apply_translation_to_sjson  # noqa: E402

SRC = ROOT / "working/0100A00019DE0000_Hades2/raw_text/en/_LootData_Ares.en.sjson"
OUT = ROOT / "translations/0100A00019DE0000_Hades2/Game/Text/en/_LootData_Ares.en.sjson"

translations = {
    "MelinoeField_2915": "Ấn ký chiến trận...",
    "MelinoeField_2918": "Thần chiến tranh...",
    "MelinoeField_2919": "Đến đây vì bạo lực...",
    "MelinoeField_2920": "Ngài Ares...",
    "Ares_0079": "Xin thứ lỗi, người nhà của ta, nhưng Đức Vua, phụ vương của ta và ta đang dở cuộc bàn luận mà ta cho rằng không thể chờ được... về những điều ta khám phá trong chuyến ghé thăm các vùng đất xa xôi.",
    "Zeus_0199": "Chuyện đó cứ bình tĩnh đã, Ares! Trước hết ta nên giải quyết việc gần nhà rồi mới lo đến những chuyện có thể xảy ra ở tận góc xa thế giới! Rồi sẽ đến lúc xử lý {#Emph}chúng{#Prev}.",
    "Ares_0156": "Ta chẳng muốn làm mẹ, Đức Nữ hoàng, thêm nặng lòng; vương miện của người đã quá nặng rồi. Nhưng người vẫn khăng khăng có mặt ở đây, có lẽ nghĩ rằng một mình ta giúp sức là chưa đủ. Có phải vậy không, thưa Mẹ?",
    "Hera_0243": "Ares, đừng bận tâm đến ta. Và khi có người ngoài, đừng gọi ta là {#Emph}Mẹ. {#Prev}Nếu đến phép tắc cơ bản con còn không giữ được, sao ta có thể tin vào hiệu quả của những {#Emph}Ân Huệ con ban?",
    "Ares_0081": "Chú Poseidon của chúng ta đây thường khuyên bảo nhiều hơn bất kỳ ai trong nhà, có lẽ nghĩ rằng lời khuyên càng nhiều thì càng hay. Chú nghĩ giờ chúng ta nên làm gì?",
    "Poseidon_0354": "Giờ cứ xông thẳng về phía kẻ địch, nghiền nát chúng như bão tố đánh chìm con tàu! {#Emph}A!{#Prev} Ta thấy trong người sôi sục, sẵn sàng chiến đấu rồi! Nghĩ lại thì lần nào cháu trai Ares yêu quý ở đây ta cũng thế!",
    "Ares_0162": "Ta rất khâm phục cách nữ thần mùa màng vĩ đại của chúng ta nhập cuộc chiến này. Càng xem chuyện này là thù riêng, chúng ta càng chiến đấu quyết liệt! Có đúng vậy không, quý bà Demeter?",
    "Demeter_0191": "Ares, không phải ta biến chuyện này thành thù riêng. Có lẽ sau này, khi con có con cháu và bị cướp mất chúng, con mới hiểu. Còn bây giờ... con chỉ cần làm theo lời ta.",
    "Ares_0158": "Người anh cùng cha khác mẹ Apollo đây nói rằng anh ấy là người đầu tiên trong nhà tìm đến con, người họ hàng của ta. Có lẽ nếu là {#Emph}ta {#Prev}thay vì anh ấy, mọi chuyện đã kết thúc từ lâu rồi...",
    "Apollo_0170": "Thôi nào, Ares, em đâu có giỏi kết thúc xung đột. Chắc vì thế mà em đến muộn trong cuộc chiến này! Nhưng thấy bọn anh vui vẻ thế nào nên em {#Emph}phải {#Prev}nhảy vào cho bằng được.",
    "Ares_0164": "Tình yêu và thù hận, người nhà của ta! Những cảm xúc mãnh liệt nhất, cũng là cội nguồn của chiến tranh. Vì thế Aphrodite rực rỡ đây quan tâm đến bản tính của ta, và ta cũng quan tâm đến nàng.",
    "Aphrodite_0214": "Mối bận tâm của chàng chính là đam mê của thiếp, ngài Ares! Điều gì khiến một người hoàn toàn bị cảm xúc cuốn đi? Thiếp muốn biết {#Emph}mọi {#Prev}lý do có thể.",
    "Ares_0166": "Hephaestus chăm chỉ và ta là hai người con trai ruột duy nhất của Đức Vua và Nữ hoàng núi Olympus. Ta vẫn bảo anh ấy rằng chúng ta phải gánh vác trọng trách, khẳng định vị thế của mình!",
    "Hephaestus_0238": "Muốn thêm trách nhiệm thì cứ nhận lấy đi, Ares! Chứ ta chẳng biết em muốn gì, mà cũng chẳng muốn dính vào. Aphrodite thì ngoại lệ. Có lò rèn, có vợ... thế là đủ rồi.",
    "Ares_0160": "Ta rất mừng khi thấy quý cô Hestia thân mến phát huy năng lực nhiều hơn. Kìa, cô ấy đến rồi! Ta luôn biết nữ thần có bản tính hủy diệt, bởi lửa vốn là một phần lớn của chiến tranh!",
    "Hestia_0205": "Ta chẳng thường muốn bộc lộ khía cạnh này, dù anh có vẻ thích nhìn thấy nó, Ares. Ta nghĩ chúng ta không thể kiểm soát sức mạnh nếu không kiểm soát được bản thân.",
    "MelinoeField_2916": "Ta cứ tưởng người này chẳng bao giờ chịu lộ diện. {#Emph}Nhân danh Hades! Olympus, ta xin nhận thông điệp này!",
    "Ares_0201": "{#Emph}A{#Prev}, người cùng chung chí hướng với cái chết! Ngươi đã nhiệt thành đối đầu Typhon quái dị. Người nhà ta khăng khăng rằng ta phải ra tay khi bạo lực vượt khỏi tầm kiểm soát; còn ta cũng muốn chứng kiến bản lĩnh của ngươi. Vậy nên {#Emph}đây... {#Prev}món đóng góp đầu tiên trong nhiều món cho chính nghĩa.",
    "Ares_0039": "Máu ngươi đỏ như máu anh trai ngươi, mà đêm nay ngươi cũng mất khá nhiều rồi. Ta chỉ ước mình đến sớm hơn để tận mắt chứng kiến thêm.",
    "Ares_0168": "Người nhà của ta, ngươi chịu những vết thương nghiêm trọng quá! Trong chiến tranh, chẳng ai toàn mạng cả. Mong ngươi khiến bất kỳ kẻ nào dám hại chúng ta phải chịu {#Emph}đau đớn hơn nhiều{#Prev}.",
    "Ares_0169": "Đêm nay đã có quá nhiều sinh mạng mất đi; dù chính ta không nên dùng từ ấy. Sinh mạng bị dập tắt chưa bao giờ là {#Emph}mất đi{#Prev}, mà luôn được {#Emph}đem ra đánh đổi... {#Prev}miễn là vì vương quốc của cha ngươi.",
    "Ares_0170": "Ngươi chịu những thương tích đủ khiến cả phàm nhân khỏe nhất cũng gục ngã, vậy mà vẫn chiến đấu như chưa hề hấn gì! Có khi ngươi còn thấy phấn khích vì thế?",
}

source = SRC.read_text(encoding="utf-8-sig")
OUT.parent.mkdir(parents=True, exist_ok=True)
mapped = {key: {"DisplayName": value} for key, value in translations.items()}
OUT.write_text(apply_translation_to_sjson(source, mapped), encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
print(f"Đã dịch {len(translations)} câu mở đầu của Ares.")
