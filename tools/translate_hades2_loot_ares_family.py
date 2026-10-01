"""Translate Ares's family and Olympian relationship dialogue."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from hades2_sjson_helper import apply_translation_to_sjson  # noqa: E402

TR = ROOT / "translations/0100A00019DE0000_Hades2/Game/Text/en/_LootData_Ares.en.sjson"
translations = {
    "Ares_0040": "Khi ngươi bắt đầu chuyến chinh phạt đêm nay, ta sẽ đồng hành từ đầu để ngươi có thể chiến đấu, tiêu diệt kẻ địch mà không chút kiềm chế.",
    "Ares_0041": "Titan Thời Gian đúng là đối thủ khó lường! Ta chưa từng gặp ông Chronos, nhưng có thể hình dung lão ra sao. Trước kia ta cứ thắc mắc sao cha ta với các chú đôi khi lại lươn lẹo thế. Giờ thì biết họ học từ ai rồi!",
    "Ares_0137": "Lần gần nhất ngươi tìm cách ngăn Typhon không diễn ra như ý muốn, nhưng chúng ta vẫn tận dụng được sự đánh lạc hướng ngươi tạo ra. Giờ đến Titan Chronos, phải không?",
    "Ares_0042": "Mặt đất dưới chân ngươi hẳn mềm lắm, mà chắc không phải vì mưa đâu. Nếu muốn thăm thú những vùng đất gần xa bị chiến tranh tàn phá, cứ để ta dẫn đường.",
    "Ares_0043": "Ngươi còn phải đi xa mới đến được chiến trường trên sườn núi của chúng ta; nhưng cứ yên tâm, trên đường sẽ có những trận đánh dữ dội!",
    "Ares_0145": "Tam Nữ Thần Số Mệnh đang bị giam giữ trái ý muốn sao? Ta đã lo cho họ hơn, nếu chuyện này không có nghĩa chiến tranh cuối cùng sẽ chỉ do chính nó định đoạt kết quả...!",
    "Ares_0064": "Phụ vương Zeus dày dạn chiến trận nhất, đã chiến đấu và chiến thắng vô số lần. Vậy mà ông thường nghe Athena hơn ta, dù cô ấy đang chật vật bảo vệ ngọn núi này. Ít nhất ngươi cũng thấy chúng ta nên {#Emph}tấn công.",
    "Ares_0146": "Ân Huệ của cha ta quả là vô cùng mạnh mẽ. Đủ sức đánh bại chính Typhon! Nhưng hoàn cảnh hiện tại đòi hỏi nhiều hơn thế, và ta sẵn sàng giúp sức.",
    "Ares_0065": "Mẹ ta, Đức Nữ hoàng, luôn cẩn thận không thiên vị bất kỳ ai trong gia đình, kể cả những đứa con do chính người sinh ra... Ta thích nghĩ tính khách quan của mình là thừa hưởng từ mẹ.",
    "Ares_0149": "Chú Poseidon luôn tỏ vẻ tự tin, nhưng ta nghĩ thứ đọng trên trán chú thường là mồ hôi chứ chẳng phải nước biển. Chiến tranh quả thật khiến người ta bất an.",
    "Ares_0150": "Anh cùng cha khác mẹ Apollo ban Ân Huệ cho ngươi rồi sao? Trong khi ta theo đuổi nghề của mình, anh ấy lại chạy theo đủ mối quan tâm, tài giỏi nhiều thứ nhưng có lẽ chẳng tinh thông thứ nào.",
    "Ares_0151": "Nữ thần Demeter nổi tiếng khiến mùa màng sinh sôi... nhưng bà cũng có thể gieo nạn đói khắp nơi. Sức mạnh ấy kết hợp với của ta thì thật hoàn hảo.",
    "Ares_0066": "Nếu không có Aphrodite xinh đẹp nhất, ta đã chẳng dễ dàng ban Ân Huệ cho ngươi đến vậy. Ta thấy nàng lại ban phước cho ngươi rồi. Ngươi hiểu vẻ đẹp trong việc ta làm, tất cả là nhờ nàng.",
    "Ares_0067": "Người anh đáng thương Hephaestus bị buộc sống kiếp lao động trong lò rèn... tạo ra vũ khí và áo giáp đem lại vinh quang mà chính anh ấy chẳng bao giờ có. Ít ra anh ấy cũng giúp ích cho {#Emph}ngươi{#Prev}, người nhà của ta.",
    "Ares_0152": "Ngươi đã khơi dậy Hestia vốn miễn cưỡng tham gia cuộc chiến! Nghĩ xem, lửa của cô ấy thường chỉ dùng để sưởi ấm nhà phàm nhân. Ta {#Emph}rất {#Prev}muốn thấy cô ấy phát huy hết sức mạnh!",
    "Ares_0153": "Bản tính của nữ thần săn bắn vốn khiến nàng hiếm khi lộ diện. Ta thường cố thuyết phục Artemis đem tài năng ra chiến trường, chứ đừng chỉ quanh quẩn trong rừng. Nhưng nàng bướng bỉnh, chắc ngươi cũng biết.",
    "Ares_0154": "Muốn tiến hành chiến tranh thành công thì phải liên lạc nhanh chóng, mà ta vẫn phải trông cậy vào Hermes chân nhanh. Chuyện anh ấy đến gặp ngươi trước là đương nhiên; ta mong anh ấy mang Ân Huệ chứ không chỉ đưa tin.",
    "Ares_0155": "Những đêm như thế này, ánh sáng duy nhất đến từ Selene ngự trên cỗ xe rực rỡ. Người nhà của ta, ngươi đang có ánh sáng của nàng bên mình, cả quyền năng bí ẩn nữa, phải không?",
    "Ares_0068": "Em gái Athena thân yêu đang gánh trọng trách lớn, ngoài bộ giáp nặng nề ngươi từng thấy. Cô ấy không chỉ điều hành phòng thủ mà còn phải chịu trách nhiệm cho mọi thất bại. Mong trí tuệ sẽ giúp cô ấy vượt qua.",
    "Ares_0033": "Nếu ông nội chúng ta muốn chiến tranh, sao ta lại từ chối? Ta hiểu sự trớ trêu trong chuyện này; đơn giản là ta nghĩ {#Emph}tất cả {#Prev}chúng ta đều có thể đạt được điều mình muốn.",
    "Ares_0183": "Trước khi Titan chiếm Âm phủ, con gái nữ thần Nyx thường trừng phạt những kẻ lấy quá phần. Nàng tên Nemesis, và ta rất ngưỡng mộ nàng... có lẽ gần đây nàng muốn báo thù cho gia đình mình.",
    "Ares_0184": "Ngươi đã gặp Heracles, dũng sĩ của mẹ ta, nổi danh trong mắt phàm nhân nhờ sức vóc và tài nghệ. Cây chùy của anh ta có lẽ đã lấy đi nhiều mạng hơn cả ngươi! Nhưng anh ta đi trước ngươi lâu rồi.",
    "Ares_0185": "Phù thủy Medea đang giúp ngươi, phải không? Dịch bệnh và độc dược khiến nàng khét tiếng; xét theo một khía cạnh, chúng làm giảm nguy cơ chiến tranh. Nhưng chúng có tác dụng, vậy nên cứ cởi mở nhìn nhận.",
    "Ares_0045": "Ta mang ơn cha ngươi rất nhiều; ta càng làm việc thì ông ấy càng có thêm việc phải xử lý. Ta mong ông ấy cũng trân trọng sự hợp tác của chúng ta. Từ ngày ông ấy vắng mặt, mọi thứ chẳng còn như trước.",
    "Ares_0048": "Người nhà của ta, ta từng quen nữ thần Nyx và nghe bà kể về cõi của ngươi cùng phong tục nơi đó. Bà rất thân thiết với những người ruột thịt gần gũi nhất của ngươi. Nếu phải chiến đấu mới đưa được họ về thì càng tốt.",
    "Ares_0197": "Nữ thần Nyx đã trở về Âm phủ rồi, người nhà của ta! Ta hơi buồn khi nghĩ cuộc chiến sắp kết thúc, nhưng rất mừng khi sự hiện diện của Hiện thân Màn Đêm lại được cảm nhận rõ hơn, đúng như vốn phải thế.",
    "Ares_0057": "Ngươi khiến ta nhớ đến anh trai mình. Anh ấy là bậc thầy đưa cái chết đến, lớn lên giữa áp lực nơi địa ngục sâu thẳm! Dù có lẽ hai người không hợp nhau, giống như anh chị em chúng ta thỉnh thoảng vẫn cãi vã.",
    "Ares_0198": "Anh trai Zagreus của ngươi vẫn khỏe chứ? Ta tin hai người sẽ thân thiết, vì có nhiều điểm chung: tàn bạo, không khoan nhượng...! Giá mà ta cũng có anh em ở đây...",
    "Ares_0059": "Ta biết nữ thần Eris đêm nào cũng bám riết ngươi khi ngươi tiến gần đến đích. Ta phải thú nhận chuyện này khiến mình khó xử; Bất Hòa giúp ích cho việc ta làm hơn hầu hết mọi thứ. Nhưng ta biết chẳng ai kiểm soát được nàng.",
    "Ares_0060": "Nữ thần Eris chẳng được ai trên này ưa, nơi ngươi sống chắc cũng vậy. Nhưng ta phần nào đồng cảm với nàng, vì nàng bị xa lánh. Ta không thể đổi bản tính của mình; chúng ta là thần bất tử, dường như đến hủy diệt cũng không được.",
    "Ares_0199": "Giữa ngươi với Hiện thân Bất Hòa có mối liên hệ nào sao? Ta cứ tưởng hai người chỉ thù ghét nhau. Nhưng hóa ra ngươi nhìn Eris giống ta. Chúng ta đều là những sức mạnh của tự nhiên, phải không?",
    "Ares_0049": "Titan Prometheus rõ ràng chẳng lạ gì chiến tranh. Chẳng hạn, hắn biết liên minh mong manh đến mức nào. Có khi trước kia hắn theo phe cha chúng ta chỉ để tìm hiểu điểm yếu của họ chăng?",
    "Ares_0050": "Ta từng nghĩ Prometheus chỉ là kẻ chủ hòa; hắn chấp nhận số phận dễ dàng thế khi bị bắt vì chống lại ý muốn của phụ vương ta. Giờ hắn đã tìm lại tinh thần chiến đấu rồi sao? Đôi khi phải trải qua đau khổ mới hiểu được chính mình.",
    "Ares_0200": "Vậy là ngươi với Prometheus vẫn tiếp tục xung đột? Hắn có lý do phức tạp riêng, người nhà của ta cũng miễn cưỡng chấp nhận. Còn ta chỉ mừng khi thấy hắn chiến đấu.",
}

source = TR.read_text(encoding="utf-8-sig")
mapped = {key: {"DisplayName": value} for key, value in translations.items()}
TR.write_text(apply_translation_to_sjson(source, mapped), encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
print(f"Đã bổ sung {len(translations)} câu thoại gia đình/thần thoại của Ares.")
