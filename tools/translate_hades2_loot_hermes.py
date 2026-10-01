"""Translate a contextual first batch of Hermes dialogue in Hades II."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from hades2_sjson_helper import apply_translation_to_sjson  # noqa: E402

SRC = ROOT / "working/0100A00019DE0000_Hades2/raw_text/en/_LootData_Hermes.en.sjson"
OUT = ROOT / "translations/0100A00019DE0000_Hades2/Game/Text/en/_LootData_Hermes.en.sjson"

translations = {
    "Melinoe_1884": "Ngài Hermes, mong ngài đi trong thầm lặng.",
    "Hermes_0128": "Cô cũng vậy!", "Hermes_0129": "Chào chào!", "Hermes_0130": "Chào!", "Hermes_0131": "Đỉnh thật!", "Hermes_0132": "Cạn ly!", "Hermes_0133": "Ta cũng thế!", "Hermes_0134": "Ừ!", "Hermes_0135": "Được thôi!",
    "MelinoeField_2002": "Hermes...!", "Melinoe_1161": "Olympus cần ta... trên mặt đất ư?",
    "Hermes_0158": "{#Emph}Ối!", "Hermes_0159": "Được!", "Hermes_0160": "{#Emph}Ơ!", "Hermes_0161": "...đúng rồi.", "Hermes_0162": "{#Emph}Hự!", "Hermes_0163": "{#Emph}Ờm!", "Hermes_0164": "{#Emph}Ừm!", "Hermes_0165": "{#Emph}Ồ!",
    "Hermes_0049": "Có vẻ cô gặp vài chướng ngại trên đường đến đây, M! Nhớ nhìn đường nhé. Biết là đi nhanh thì khó để ý lắm!",
    "Hermes_0050": "Đêm nay ngoài kia khắc nghiệt nhỉ, M? Cứ vững bước nhé, biết đâu {#Emph}mấy thứ này {#Prev}giúp cô đi xa hơn, {#Emph}nhanh hơn!",
    "Hermes_0051": "Ôi không! Cô bị thương rồi! Chuyện gì xảy ra vậy, M? Ông già đã tìm được cô trước ta à! Sao có thể...?",
    "Hermes_0052": "Chỗ cô vừa đi qua nguy hiểm lắm nhỉ, M? Trầy xước đôi chút thì sao chứ! Giờ cô sẽ được tăng tốc đây!",
    "Hermes_0053": "Chào M! Nghe nói cô lại lên đường nên ta ghé qua tiễn một đoạn! Thượng lộ bình an nhé, đại khái vậy!",
    "Hermes_0054": "Từ đó đến đích còn xa lắm nhỉ, M? Để xem ta có rút ngắn được chút thời gian cho chặng đường tiếp theo không!",
    "Hermes_0055": "Ta đoán cô sắp đi nên ghé đón ngay đây! Đi xa cũng thú vị, nhưng đôi khi chỉ muốn đến nơi cần đến thật nhanh thôi!",
    "Hermes_0056": "Lại bắt đầu cuộc đua về đích rồi nhỉ, M? Vậy thì {#Emph}sẵn sàng{#Prev} đi, ta sẽ đưa cô đến đó trong chớp mắt! Miễn là cô sống sót đã...",
    "Hermes_0210": "M, ta đâu muốn làm cô chậm trễ, nhất là lúc cô vừa bắt đầu hành trình! Cứ chọn một món rồi {#Emph}đi {#Prev}ngay đi!",
    "Hermes_0211": "Cô tưởng có thể lẻn đi mà không nhận Ân Huệ của ta sao? Nhầm to rồi, M! Mà cô sắp nhanh hơn nhiều đấy!",
    "Hermes_0088": "Cô muốn tạm rời không khí mặt đất rồi, ta hiểu mà, M. Con đường quen thuộc thường vẫn tốt nhất! Cứ thong thả nhé, không ai giục cô đâu! Trừ ta.",
    "Hermes_0086": "Cô cho ông già thấy ai mới là người làm chủ rồi! {#Emph}Giỏi lắm, M! {#Prev}Thế cũng khiến lão chùn bước. Đúng lúc cô lên đây giúp chúng ta đẩy quân của lão khỏi {#Emph}lãnh địa của mình{#Prev}. Cô thấy sao?",
    "Hermes_0087": "Ông già đúng là đối thủ khó nhằn, tiếc là đêm qua lão hạ được cô. Nhưng cảm ơn cô đã lên {#Emph}đây{#Prev}! {#Emph}Thời gian{#Prev} chưa biến mất đâu, nhưng ngọn núi này thì có thể đấy!",
    "Hermes_0212": "Tuyệt, cô đang trên đường đến đây và vẫn chưa đi quá xa! Cô có thể đến đây thật nhanh, nhưng tùy cô quyết định!",
    "Hermes_0213": "Ta biết cô không thể hít thở không khí mặt đất mãi được, M, nên may là ta gặp cô ngay lúc vừa khởi hành! Chẳng mấy chốc ta sẽ đưa cô lên đỉnh núi thôi.",
    "Hermes_0034": "M, ta biết chuyến đi lên đây chẳng dễ dàng, thậm chí giờ còn bất khả thi với cô. Nhưng hãy thử nghĩ xem gia đình ta phải nuốt tự ái đến mức nào mới mở lời cầu cứu! Tình hình tệ đến vậy đấy!",
    "Hermes_0074": "Đang lúc nguy cấp, M! Chúng ta cần cô ở đáy Âm phủ, {#Emph}lẫn {#Prev}trên đỉnh Olympus! Phải có mặt ở hai nơi cùng lúc, khổ thân cô. {#Emph}Bí quyết{#Prev} là chạy thật, thật nhanh!",
    "Hermes_0064": "Lần trước cô đã xuống khá sâu rồi! Giỏi lắm, ta biết cô làm được mà, M! Nhưng ông già vẫn chưa chịu lùi bước nhỉ? Ít ra có lẽ lão cũng bắt đầu lung lay!",
    "Hermes_0065": "Cô đang giúp cán cân nghiêng về phía chúng ta! Phá vòng vây, giúp họ hàng có được chút thời gian nghỉ ngơi. Trận chiến chưa xong đâu, nhưng ta nghĩ rồi sẽ sớm đến lúc đó!",
}

source = SRC.read_text(encoding="utf-8-sig")
OUT.parent.mkdir(parents=True, exist_ok=True)
mapped = {key: {"DisplayName": value} for key, value in translations.items()}
OUT.write_text(apply_translation_to_sjson(source, mapped), encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
print(f"Đã dịch {len(translations)} câu Hermes: {OUT.relative_to(ROOT)}")
