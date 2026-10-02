"""Translate Ares's compact combat and boon dialogue strings."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from hades2_sjson_helper import apply_translation_to_sjson  # noqa: E402

TR = ROOT / "games/0100A00019DE0000_Hades2/translations/Game/Text/en/_LootData_Ares.en.sjson"
translations = {
    "Ares_0003": "Còn gì bằng tận mắt chứng kiến kẻ địch bị tàn sát, phải không?",
    "Ares_0004": "Nơi nào sắp đổ máu, ta đều có mặt để theo dõi, nếu không trực tiếp tham chiến.",
    "Ares_0005": "Phàm nhân rồi ai cũng phải chết; ta chỉ mong họ chết cho xứng đáng.",
    "Ares_0006": "Có xung đột chỉ giải quyết được bằng bạo lực; đừng kìm nén thôi thúc ấy.",
    "Ares_0007": "Nơi nào có dòng người chết, ta tìm đến nơi đó. Dạo này ngươi cũng ở đó.",
    "Ares_0008": "Sự sống lan khắp thế gian như dịch bệnh, nhưng vẫn có cách giữ nó trong tầm kiểm soát.",
    "Ares_0009": "Không cuộc chiến nào kéo dài mãi mãi, nhưng cũng chẳng cuộc chiến nào là cuộc cuối cùng.",
    "Ares_0010": "Kẻ địch của ngươi hết lần này đến lần khác lao mình vào cảnh tàn sát, thật dễ dàng biết bao.",
    "Ares_0011": "Đau đớn rồi sẽ nguôi ngoai; vậy nên hãy để chuyện này làm lời cảnh tỉnh cho tất cả.",
    "Ares_0012": "Đổ máu thường có thể tránh được, nhưng ta chẳng bao giờ để cơ hội ấy trôi qua.",
    "Ares_0013": "Thời đại chúng ta thật lạ lùng: ngay cả người chết cũng phải nếm trọn chiến tranh.",
    "Ares_0014": "Hãy tận hưởng khoảnh khắc này khi tro tàn hủy diệt dần lắng xuống.",
    "Ares_0015": "Linh hồn người chết ám ảnh mọi chiến trường, phải không? Có lẽ ngươi còn nhìn thấy họ ở đó.",
    "Ares_0016": "Chiến tranh nằm trong bản tính của chúng ta; đừng khước từ, hãy đón nhận nó.",
    "Ares_0017": "Bạo lực không phải lúc nào cũng chấm dứt xung đột, nhưng có thể khiến nó tạm lắng.",
    "Ares_0018": "Mỗi trận chiến của ngươi đều là cảnh tượng đáng thưởng thức, người nhà sinh ra từ địa ngục.",
    "Ares_0019": "Nhiều cuộc chiến đã bị thời gian vùi lấp, nhưng cuộc này có lẽ sẽ chưa sớm bị lãng quên.",
    "Ares_0020": "Một cuộc chiến lan khắp mặt đất lẫn bên dưới... người nhà của ta, lần này chúng ta làm lớn thật rồi.",
    "Ares_0021": "Đừng kéo dài cuộc đổ máu này chỉ để báo thù; còn nhiều lý do chính đáng khác lắm.",
    "Ares_0022": "Nhiều người thấy việc ta làm thật khó chịu! Ngươi đã tận mắt chứng kiến và hiểu sự thật rồi.",
    "Ares_0023": "Biết bao trận chiến phải tham gia! Đôi khi đúng là ngợp thật.",
    "Ares_0024": "Chiến thắng luôn đắng cay ngọt bùi; nhưng đoạn kết hiếm khi là phần hay nhất.",
    "Ares_0025": "Việc ta làm có vẻ chẳng bao giờ đem lại kết cục hoàn hảo; rồi có lẽ ngươi sẽ hiểu như ta.",
    "Ares_0026": "Ta khâm phục sự quyết đoán của ngươi, nhưng hãy dành chút thời gian tận hưởng sự yên bình sau bão tố.",
    "Ares_0027": "Mỗi đêm lại cho ta cơ hội mới để tạo ra cảnh tàn sát theo những cách khác nhau.",
    "Ares_0028": "Với những cuộc xung đột lớn nhất, ta luôn sẵn sàng góp sức và đem lại kết cục hợp lý.",
    "Ares_0029": "Ai trong chúng ta cũng có ý chí chiến đấu, phải không? Ta chỉ mong mọi người sống đúng với bản tính.",
    "Ares_0030": "Trận chiến đêm nay chỉ vừa bắt đầu; ta không muốn bỏ lỡ bất kỳ kẻ nào bị hạ gục.",
    "Ares_0031": "Nếu đêm nay phải đổ máu, hãy khiến từng giọt đều có ý nghĩa.",
    "Ares_0069": "Nếu không dùng bạo lực, làm sao chúng ta khẳng định quyền thống trị thế gian?",
    "Ares_0095": "Bạo lực không phải lúc nào cũng cần thiết, nhưng thường có hiệu quả.",
    "Ares_0208": "Kẻ bảo bạo lực chẳng giải quyết được gì chắc chưa từng thử bao giờ!",
    "Ares_0209": "Cứ hạ gục mọi kẻ cản đường theo cách quyết đoán hay tàn nhẫn tùy ngươi.",
    "Ares_0210": "Đất Mẹ uống cạn máu ngươi đổ xuống; ta muốn ngươi làm dịu cơn khát của bà.",
    "Ares_0211": "Nhiều kẻ địch trong vương quốc của cha ngươi chẳng có máu thịt, nhưng đành dùng tạm vậy.",
    "Ares_0212": "Không ngờ chiến tranh còn bùng nổ cả dưới lòng đất; thời buổi thú vị thật!",
    "Ares_0213": "Ngươi định mở thêm một con đường đẫm máu lên núi của chúng ta à? Ta muốn tận mắt thấy lắm!",
    "Ares_0214": "Tàn quân của Titan khát máu chiến trận đến mức ta thấy cũng đáng nể.",
    "Ares_0215": "Chiến tranh không dành cho kẻ yếu tim, nhưng ta thấy ngươi thật sự say mê nó.",
    "Ares_0216": "Đêm nào ta cũng mong được thấy ngươi dùng cách gì để đối phó kẻ địch!",
    "Ares_0217": "Tối nay chúng ta cần một câu hô xung trận chứ, người nhà của ta. {#Emph}Giết sạch chúng{#Prev} thì sao?",
}

source = TR.read_text(encoding="utf-8-sig")
mapped = {key: {"DisplayName": value} for key, value in translations.items()}
TR.write_text(apply_translation_to_sjson(source, mapped), encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
print(f"Đã dịch thêm {len(translations)} câu Ân Huệ/chiến đấu của Ares.")
