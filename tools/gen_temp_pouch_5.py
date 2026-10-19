# -*- coding: utf-8 -*-
import json
import os

# 1. Load source
source_path = 'games/0100F2C0115B6000_ZeldaTotK/source/pouch_part_5.json'
pb_path = 'games/0100F2C0115B6000_ZeldaTotK/translations/ActorMsg__PictureBook.msbt.json'
out_path = 'games/0100F2C0115B6000_ZeldaTotK/translations/temp_pouch_5.json'

with open(source_path, 'r', encoding='utf-8') as f:
    source = json.load(f)

with open(pb_path, 'r', encoding='utf-8') as f:
    pb = json.load(f)

trans = {}

# 2. Inherit 83 exact matches from ActorMsg__PictureBook.msbt.json
for k in source:
    if k in pb:
        trans[k] = pb[k]

print(f"Inherited {len(trans)} keys from PictureBook.")

# 3. Define dictionaries for specific groups
# Roasts (102 keys)
roasts = {
    # 01
    "Item_Roast_01_Name": "Bít Tết Nướng",
    "Item_Roast_01_Caption": "Thịt được nướng trực tiếp trên ngọn lửa trần. Nướng chín\ngiúp tăng thêm hương vị đậm đà và gia tăng lượng\ntrái tim hồi phục.",
    # 02
    "Item_Roast_02_Name": "Đùi Chim Nướng Giòn",
    "Item_Roast_02_Caption": "Đùi chim được nướng giòn rụm cả phần da. Tuy không tẩm ướp\ngia vị, món ăn vẫn giữ trọn hương vị mộc mạc, thơm ngon.\nHồi phục nhiều trái tim hơn so với khi ăn sống.",
    # 03
    "Item_Roast_03_Name": "Táo Nướng",
    "Item_Roast_03_Caption": "Sức nóng trực tiếp đã làm quả táo mềm ra và ngọt lịm.\nĂn vào sẽ hồi phục ba phần tư trái tim.",
    # 04
    "Item_Roast_04_Name": "Nấm Thể Lực Nướng Giòn",
    "Item_Roast_04_Caption": "Cây nấm thể lực stamella nướng này không mang lại hiệu ứng\nđặc biệt nào, nhưng vẫn giúp hồi phục một chút sức khỏe.",
    # 05
    "Item_Roast_05_Name": "Nấm Truffle Trái Tim Nướng Giòn",
    "Item_Roast_05_Caption": "Nấm truffle trái tim được nướng đến khi lớp vỏ ngoài giòn rụm.\nMùi vị rất thơm ngon, nhưng nấm truffle trái tim sẽ phát huy\nhiệu quả tối đa hơn nhiều nếu dùng nấu theo công thức.",
    # 06
    "Item_Roast_06_Name": "Nấm Hylian Nướng Giòn",
    "Item_Roast_06_Caption": "Cây nấm Hylian được nướng vàng giòn hoàn hảo.\nHương thơm và mùi vị đều đậm đà hơn,\ngiúp người ăn hồi phục nhiều sức khỏe hơn.",
    # 07
    "Item_Roast_07_Name": "Quả Dại Nướng",
    "Item_Roast_07_Caption": "Quả dại này được hơ trên lửa trần để biến đổi vị ngọt ngào.\nĂn vào sẽ hồi phục nhiều sức khỏe hơn so với ăn sống.",
    # 08
    "Item_Roast_08_Name": "Quả Sấm Nướng Voltfruit",
    "Item_Roast_08_Caption": "Quả sấm voltfruit từ Sa mạc Gerudo này được nướng xém cạnh\nđể làm dậy lên trọn vẹn hương vị chua ngọt quyến rũ.",
    # 10
    "Item_Roast_10_Name": "Quả Cọ Nướng",
    "Item_Roast_10_Caption": "Quả cọ được nướng trực tiếp trên nhiệt độ cao,\nlàm chín mềm phần thịt bên trong lớp vỏ dày.\nNgon nhất khi thưởng thức ngay lúc nước mật ứa ra khi nướng.",
    # 11
    "Item_Roast_11_Name": "Chuối Dũng Mãnh Nướng",
    "Item_Roast_11_Caption": "Những trái chuối dũng mãnh này được nướng nguyên quả.\nNhiệt độ đã chuyển hóa phần ruột quả bên trong\nthành lớp siro quánh dẻo, đậm đà và ngào ngạt hương thơm.",
    # 12
    "Item_Roast_12_Name": "Dưa Mát Nướng Hydromelon",
    "Item_Roast_12_Caption": "Trái dưa mát hydromelon được nướng nguyên quả cho ra lớp ruột\nmềm mại, mọng nước cùng hương vị vô cùng kích thích vị giác.\nĐây quả thực là một món ăn đáng đồng tiền bát gạo!",
    # 13
    "Item_Roast_13_Name": "Ớt Nướng Xém Cạnh",
    "Item_Roast_13_Caption": "Trái ớt được mơn trớn nhẹ nhàng qua ngọn lửa hồng.\nVị cay giờ đây đã dịu đi rất nhiều.",
    # 15
    "Item_Roast_15_Name": "Bí Đỏ Kiên Cố Nướng",
    "Item_Roast_15_Caption": "Quả bí đỏ kiên cố được nướng nguyên vẹn.\nLớp vỏ cứng đóng vai trò như chiếc nồi hấp giữ trọn\nphần ruột bí mềm ngọt và nóng hổi bên trong.",
    # 16
    "Item_Roast_16_Name": "Hạt Sen Nhanh Nhẹn Nướng",
    "Item_Roast_16_Caption": "Hạt sen nhanh nhẹn được nướng chín trên lửa.\nHãy bóc lớp vỏ ngoài để thưởng thức phần nhân mềm bùi\nvà thơm ngậy bên trong.",
    # 18
    "Item_Roast_18_Name": "Củ Cải Trái Tim Nướng",
    "Item_Roast_18_Caption": "Củ cải trái tim nướng thơm lừng và ấm nóng.\nDù không còn hiệu ứng gia tăng sinh lực đặc biệt nào,\nmón ăn vẫn giúp hồi phục một lượng trái tim đáng kể.",
    # 19
    "Item_Roast_19_Name": "Củ Cải Lớn Nướng",
    "Item_Roast_19_Caption": "Củ cải trái tim lớn đem nướng than hồng.\nĐem một loại nông sản quý hiếm như thế này nướng trực tiếp\ntrên lửa quả là một thú thưởng thức có phần xa xỉ.",
    # 24
    "Item_Roast_24_Name": "Cà Rốt Thần Tốc Nướng",
    "Item_Roast_24_Caption": "Củ cà rốt thần tốc thơm nức mũi được nướng sơ qua lửa.\nNó không còn tác dụng tăng tốc độ, nhưng vẫn giúp\nhồi phục một chút sức khỏe.",
    # 27
    "Item_Roast_27_Name": "Cây Kế Dũng Mãnh Nướng",
    "Item_Roast_27_Caption": "Cây kế dũng mãnh nướng vàng giòn. Dù không còn hiệu ứng tăng lực,\nnhưng sau khi được nướng chín, các đầu gai nhọn trở nên giòn mềm\nvà rất dễ nuốt.",
    # 28
    "Item_Roast_28_Name": "Cỏ Giáp Sắt Nướng Armoranth",
    "Item_Roast_28_Caption": "Cỏ giáp sắt armoranth mộc mạc nướng chín.\nSức nóng đã làm tơi các thớ xơ dai cứng vừa đủ\nđể bạn có thể nhai nuốt một cách dễ dàng.",
    # 31
    "Item_Roast_31_Name": "Nấm Băng Giá Nướng Giòn",
    "Item_Roast_31_Caption": "Cây nấm băng giá nướng chín đều. Nấm được nướng vàng ruộm,\nmùi vị ngon lành hơn nhiều so với khi ăn sống.\nThưởng thức nó sẽ hồi phục một chút sức khỏe.",
    # 32
    "Item_Roast_32_Name": "Nấm Mặt Trời Nướng Giòn",
    "Item_Roast_32_Caption": "Luôn là ý hay nếu bạn trữ sẵn một hoặc hai cây nấm mặt trời nướng\ntrong túi đồ phòng khi cần kíp. Ăn vào sẽ hồi phục một chút sức khỏe.",
    # 33
    "Item_Roast_33_Name": "Nấm Sấm Sét Nướng Giòn",
    "Item_Roast_33_Caption": "Không có gì đáng ngạc nhiên khi cây nấm sấm sét nướng chín này\nlại thơm ngon đến thế. Ăn vào giúp hồi phục một chút sức khỏe.",
    # 36
    "Item_Roast_36_Name": "Nấm Leo Núi Nướng Giòn",
    "Item_Roast_36_Caption": "Cây nấm leo núi rushroom được tôi luyện qua ngọn lửa.\nCó thể nó đã mất đi dược tính gia tốc, nhưng ít nhất\nbây giờ hương vị của nó đã ngon hơn rất nhiều.",
    # 37
    "Item_Roast_37_Name": "Nấm Lưỡi Dao Nướng Giòn",
    "Item_Roast_37_Caption": "Cây nấm lưỡi dao razorshroom tiếp xúc trực tiếp với nhiệt độ cao.\nLớp ngoài sắc nhọn của nó đã mềm đi đáng kể.\nĂn vào giúp hồi phục một chút sức khỏe.",
    # 38
    "Item_Roast_38_Name": "Nấm Giáp Sắt Nướng Giòn",
    "Item_Roast_38_Caption": "Cây nấm giáp sắt nướng trên lửa trần.\nLớp vỏ từng cứng như sắt giờ trở nên giòn rụm và đậm vị.\nGiúp hồi phục một chút sức khỏe.",
    # 39
    "Item_Roast_39_Name": "Nấm Tĩnh Lặng Nướng Giòn",
    "Item_Roast_39_Caption": "Cây nấm tĩnh lặng nướng nguyên tai.\nNhiệt độ cao có thể đã dập tắt ánh lân quang dịu nhẹ của nó,\nnhưng bù lại giờ đây nó rất thơm và ngon miệng.",
    # 40
    "Item_Roast_40_Name": "Bít Tết Thượng Hạng Nướng",
    "Item_Roast_40_Caption": "Thịt thượng hạng được nướng trên ngọn lửa trần.\nBên ngoài xém vàng hoàn hảo, trong khi bên trong\nchảy nước thịt ngọt lịm khó cưỡng.",
    # 41
    "Item_Roast_41_Name": "Má Đùi Chim Nướng Thượng Hạng",
    "Item_Roast_41_Caption": "Má đùi chim hảo hạng được nướng lửa đạt đến độ hoàn mỹ.\nLớp da ngoài giòn rụm nhưng phần thịt bên trong mềm mọng nước.\nĂn vào giúp hồi phục trái tim.",
    # 45
    "Item_Roast_45_Name": "Bít Tết Tuyệt Hảo Nướng",
    "Item_Roast_45_Caption": "Miếng thịt chất lượng thượng thừa nhất chỉ vừa chạm nhẹ qua lửa hồng.\nHoàn toàn không thêm thắt gia vị, để trọn vẹn vị ngọt nguyên bản\nđỉnh cao của thớ thịt được tỏa sáng rực rỡ.",
    # 46
    "Item_Roast_46_Name": "Nguyên Con Chim Nướng Tuyệt Hảo",
    "Item_Roast_46_Caption": "Cả con chim được mơn trớn trên ngọn lửa để khơi dậy trọn vẹn hương vị.\nĐơn giản là tuyệt nhất, bởi việc không nêm thêm gia vị giúp vị ngọt béo\ntự nhiên của thịt gia cầm tỏa sáng ngây ngất.",
    # 48
    "Item_Roast_48_Name": "Hạt Sồi Nướng",
    "Item_Roast_48_Caption": "Hạt sồi được nướng trực tiếp trên nhiệt độ cao.\nHương thơm bùi ngậy đặc trưng đã được nhân lên gấp bội.",
    # 49
    "Item_Roast_49_Name": "Nấm Truffle Lớn Nướng Giòn",
    "Item_Roast_49_Caption": "Cây nấm truffle lớn quý giá được nướng nguyên tai.\nMón ăn đạt điểm tuyệt đối cả về mùi thơm lẫn giá trị dinh dưỡng.\nĂn vào sẽ hồi phục rất nhiều trái tim.",
    # 50
    "Item_Roast_50_Name": "Cà Rốt Bền Bỉ Nướng",
    "Item_Roast_50_Caption": "Củ cà rốt bền bỉ bén lửa này tạo nên một món ăn đơn lẻ\nnhưng vô cùng xa hoa. Ngọn lửa đã làm dậy lên vị ngọt đậm đà\nđặc biệt của nó.",
    # 51
    "Item_Roast_51_Name": "Trứng Lửa Trại",
    "Item_Roast_51_Caption": "Nướng nguyên quả trứng chim còn cả vỏ thế này giúp giữ lại độ ẩm,\nkhiến lòng trắng trứng trở nên dai mềm, đậm đà hơn bình thường.",
    # 52
    "Item_Roast_52_Name": "Hạt Cây Nướng",
    "Item_Roast_52_Caption": "Hạt cây được nướng chín để tăng cường hương thơm.\nHồi phục nhiều trái tim hơn so với hạt sống.",
    # 53
    "Item_Roast_53_Name": "Nấm Bền Bỉ Nướng Giòn",
    "Item_Roast_53_Caption": "Cây nấm bền bỉ endura shroom nướng giòn.\nNó không ban cho hiệu ứng tăng thể lực nào, nhưng ôi chao,\nhương vị của nó mới thật tuyệt vời làm sao!",
    # 54
    "Item_Roast_54_Name": "Cà Chua Hylian Nướng",
    "Item_Roast_54_Caption": "Quả cà chua Hylian nướng nguyên trái.\nBên trong căng mọng nước ngọt ngào và sẽ hồi phục\nnhiều sức khỏe hơn khi thưởng thức.",
    # 55
    "Item_Roast_55_Name": "Bí Đỏ Mặt Trời Nướng",
    "Item_Roast_55_Caption": "Quả bí đỏ mặt trời cỡ lớn được nướng chín nguyên quả.\nNó đã mất đi dược tính ban đầu qua quá trình nướng,\nnhưng thịt bí lại mềm mại và rất thơm ngon.",
    # 56
    "Item_Roast_56_Name": "Nấm Bầu Trời Nướng Giòn",
    "Item_Roast_56_Caption": "Nấm bầu trời skyshroom nướng mộc mạc.\nNhiệt độ làm dậy lên hương vị đặc trưng và gia tăng\nlượng sức khỏe có thể hồi phục.",
    # 58
    "Item_Roast_58_Name": "Nấm Dạ Quang Nướng Giòn",
    "Item_Roast_58_Caption": "Cây nấm dạ quang brightcap nướng nguyên vẹn.\nDù đã mất đi các enzym phát quang sinh học, nhưng thân nấm mềm hơn\nvà dễ nhai hơn rất nhiều.",
    # 59
    "Item_Roast_59_Name": "Táo Vàng Nướng",
    "Item_Roast_59_Caption": "Món ăn vặt xa xỉ từ quả táo vàng nướng trực tiếp trên lửa than.\nSự cân bằng hoàn hảo không tì vết giữa vị chua thanh và ngọt ngào\nmang đến một hương vị mỹ vị như đến từ thế giới khác.",
    # RoastFish
    # 01
    "Item_RoastFish_01_Name": "Cá Vược Nướng",
    "Item_RoastFish_01_Caption": "Cá vược được nướng nguyên con trên ngọn lửa trần.\nThịt cá mềm thơm, bốc khói ngào ngạt.\nCung cấp nhiều trái tim hơn so với cá sống.",
    # 02
    "Item_RoastFish_02_Name": "Cá Vược Trái Tim Nướng",
    "Item_RoastFish_02_Caption": "Ngọn lửa hồng đã nướng lớp da cá vược trái tim giòn rụm hoàn hảo.\nPhần cá khá lớn và chứa lượng mỡ vừa vặn để tạo nên\nmột món ăn thơm ngon thượng hạng.",
    # 03
    "Item_RoastFish_03_Name": "Cá Hồi Chum Nướng",
    "Item_RoastFish_03_Caption": "Loài cá hồi chum này có thể bắt gặp ở khắp mọi nơi tại Hyrule.\nĐem từ sông thẳng lên bàn ăn, cá được chế biến đơn giản\ncho ra phần thịt mềm, tơi xốp với vị ngọt thanh khiết.",
    # 04
    "Item_RoastFish_04_Name": "Cá Hồi Trái Tim Nướng",
    "Item_RoastFish_04_Caption": "Cá hồi trái tim tươi ngon nướng mộc mạc trên lửa than,\nkhông cần thêm bất kỳ gia vị nào.\nKhông chỉ lớp da giòn ăn được mà nó còn tỏa ra mùi thơm ngào ngạt.",
    # 07
    "Item_RoastFish_07_Name": "Cá Chép Nướng",
    "Item_RoastFish_07_Caption": "Nướng cá chép nước ngọt giúp át đi mùi tanh bùn,\nkhiến món ăn dễ thưởng thức hơn rất nhiều.\nBạn có thể thỏa thích cắn ngập răng vào thớ thịt dày béo ngậy.",
    # 09
    "Item_RoastFish_09_Name": "Cá Tráp Biển Nướng",
    "Item_RoastFish_09_Caption": "Độ mềm mại, tơi xốp của loài cá biển này càng đậm đà hơn\nkhi được nướng trên than hồng. Lớp da cá giòn thơm ngậy\nlà phần đặc biệt thơm ngon nhất.",
    # 13
    "Item_RoastFish_13_Name": "Ốc Sông Ẩn Thân Nướng",
    "Item_RoastFish_13_Caption": "Ốc sông ẩn thân nướng nguyên vỏ trên than hồng.\nThịt ốc mềm ngọt và hơi dai giòn. Cảm giác khều được nguyên vẹn\nruột ốc ra khỏi vỏ chỉ trong một lần kéo khiến bạn ngập tràn thỏa mãn.",
    # 15
    "Item_RoastFish_15_Name": "Cua Nướng Xém Vỏ",
    "Item_RoastFish_15_Caption": "Nguyên con cua nướng chậm trong mai giáp.\nThịt cua ngọt mềm tơi xốp hòa quyện cùng mùi thơm cháy cạnh của lớp vỏ,\ntạo nên bữa tiệc kích thích cả năm giác quan một cách trọn vẹn nhất.",
    # 16
    "Item_RoastFish_16_Name": "Cá Rồng Cổ Đại Nướng",
    "Item_RoastFish_16_Caption": "Cá rồng cổ đại grilled nguyên con.\nThịt cá chín đều thấu suốt và đạt đến độ mềm ngọt hoàn mỹ.",
    # 18
    "Item_RoastFish_18_Name": "Cá Hang Dạ Quang Nướng",
    "Item_RoastFish_18_Caption": "Món cá hang dạ quang nướng than hồng.\nThớ thịt mềm của cá được nướng chín tới mang lại\ncả hương vị thơm ngon lẫn độ mềm mọng xuất sắc."
}

trans.update(roasts)
print(f"Added {len(roasts)} roast items. Total so far: {len(trans)}")

# 4. Paraglider Fabric (Obj_SubstituteCloth - 105 keys)
cloth_names = {
    "Obj_SubstituteCloth_00_Name": "Vải Tộc Goron",
    "Obj_SubstituteCloth_01_Name": "Vải Tộc Zora",
    "Obj_SubstituteCloth_02_Name": "Vải Tộc Gerudo",
    "Obj_SubstituteCloth_03_Name": "Vải Hoàng Gia Hyrule",
    "Obj_SubstituteCloth_04_Name": "Vải Tộc Zonai",
    "Obj_SubstituteCloth_05_Name": "Vải Tộc Sheikah",
    "Obj_SubstituteCloth_06_Name": "Vải Bang Yiga",
    "Obj_SubstituteCloth_07_Name": "Vải Đội Tuần Tra Tiễu Quái",
    "Obj_SubstituteCloth_08_Name": "Vải Đội Khảo Sát Zonai",
    "Obj_SubstituteCloth_09_Name": "Vải Thần Ngựa Malanya",
    "Obj_SubstituteCloth_10_Name": "Vải Làng Lurelin",
    "Obj_SubstituteCloth_11_Name": "Vải Tòa Báo Cỏ Bốn Lá",
    "Obj_SubstituteCloth_12_Name": "Vải Xây Dựng Hudson",
    "Obj_SubstituteCloth_13_Name": "Vải Koltin Satori",
    "Obj_SubstituteCloth_14_Name": "Vải Tộc Korok",
    "Obj_SubstituteCloth_15_Name": "Vải Gấu Xám Grizzlemaw",
    "Obj_SubstituteCloth_16_Name": "Vải Robbie Purah Pad",
    "Obj_SubstituteCloth_17_Name": "Vải Thương Hiệu Cece",
    "Obj_SubstituteCloth_18_Name": "Vải Quái Điểu Aerocuda",
    "Obj_SubstituteCloth_19_Name": "Vải Đà Điểu Eldin",
    "Obj_SubstituteCloth_20_Name": "Vải Gà Cucco",
    "Obj_SubstituteCloth_21_Name": "Vải Ngựa",
    "Obj_SubstituteCloth_22_Name": "Vải Quái Nhầy Chuchu",
    "Obj_SubstituteCloth_23_Name": "Vải Quái Thú Lynel",
    "Obj_SubstituteCloth_24_Name": "Vải Rồng Ba Đầu Gleeok",
    "Obj_SubstituteCloth_25_Name": "Vải Độc Nhãn Xương Stalnox",
    "Obj_SubstituteCloth_26_Name": "Vải Áo Hồi Tưởng",
    "Obj_SubstituteCloth_27_Name": "Vải Mũ Trùm Hylian",
    "Obj_SubstituteCloth_28_Name": "Vải Công Chúa Hyrule",
    "Obj_SubstituteCloth_29_Name": "Vải Anh Hùng Goron",
    "Obj_SubstituteCloth_30_Name": "Vải Anh Hùng Rito",
    "Obj_SubstituteCloth_31_Name": "Vải Anh Hùng Zora",
    "Obj_SubstituteCloth_32_Name": "Vải Anh Hùng Gerudo",
    "Obj_SubstituteCloth_33_Name": "Vải Sheikah Cổ Đại",
    "Obj_SubstituteCloth_34_Name": "Vải Quái Bokoblin",
    "Obj_SubstituteCloth_35_Name": "Vải Ma Vương Ganondorf",
    "Obj_SubstituteCloth_36_Name": "Vải Vua Thuyền Sư Tử Đỏ",
    "Obj_SubstituteCloth_37_Name": "Vải Chiến Binh Sheik",
    "Obj_SubstituteCloth_38_Name": "Vải Gương Hoàng Hôn",
    "Obj_SubstituteCloth_39_Name": "Vải Công Chúa Hoàng Hôn",
    "Obj_SubstituteCloth_40_Name": "Vải Trang Trại Lon Lon",
    "Obj_SubstituteCloth_41_Name": "Vải Mặt Nạ Majora",
    "Obj_SubstituteCloth_43_Name": "Vải Vương Triều Cổ Xưa",
    "Obj_SubstituteCloth_45_Name": "Vải Linh Hồn Thanh Kiếm",
    "Obj_SubstituteCloth_46_Name": "Vải Pixel Cổ Điển",
    "Obj_SubstituteCloth_48_Name": "Vải Quả Trứng Đảo Koholint",
    "Obj_SubstituteCloth_49_Name": "Vải Nữ Thần Hylia",
    "Obj_SubstituteCloth_51_Name": "Vải Giáp Da Anh Hùng",
    "Obj_SubstituteCloth_52_Name": "Vải Công Chúa Zelda",
    "Obj_SubstituteCloth_53_Name": "Vải Vua Tộc Gerudo",
    "Obj_SubstituteCloth_55_Name": "Vải Hoài Niệm",
    "Obj_SubstituteCloth_56_Name": "Vải Chân Dung Addison",
    "Obj_SubstituteCloth_Default_Name": "Vải Bình Thường"
}

cloth_first_sentences = {
    "Obj_SubstituteCloth_00_Caption": "Tấm vải bền chắc mang hoa văn họa tiết của tộc Goron.",
    "Obj_SubstituteCloth_01_Caption": "Tấm vải bền chắc mang hoa văn họa tiết của tộc Zora.",
    "Obj_SubstituteCloth_02_Caption": "Tấm vải bền chắc mang hoa văn họa tiết của tộc Gerudo.",
    "Obj_SubstituteCloth_03_Caption": "Tấm vải bền chắc mang hoa văn biểu tượng Hoàng gia Hyrule.",
    "Obj_SubstituteCloth_04_Caption": "Tấm vải bền chắc mang hoa văn họa tiết của tộc Zonai.",
    "Obj_SubstituteCloth_05_Caption": "Tấm vải bền chắc mang hoa văn họa tiết của tộc Sheikah.",
    "Obj_SubstituteCloth_06_Caption": "Tấm vải bền chắc mang hoa văn biểu tượng của Bang Yiga.",
    "Obj_SubstituteCloth_07_Caption": "Tấm vải bền chắc mang biểu trưng của Đội tuần tra tiễu quái.",
    "Obj_SubstituteCloth_08_Caption": "Tấm vải bền chắc mang biểu trưng của Đội khảo sát Zonai.",
    "Obj_SubstituteCloth_09_Caption": "Tấm vải bền chắc mang hình ảnh của Thần Ngựa Malanya.",
    "Obj_SubstituteCloth_10_Caption": "Tấm vải bền chắc mang họa tiết đặc trưng của Làng Lurelin.",
    "Obj_SubstituteCloth_11_Caption": "Tấm vải bền chắc mang biểu trưng của Tòa báo Cỏ Bốn Lá.",
    "Obj_SubstituteCloth_12_Caption": "Tấm vải bền chắc mang biểu trưng của Công ty Xây dựng Hudson.",
    "Obj_SubstituteCloth_13_Caption": "Tấm vải bền chắc mang họa tiết Thần Satori, do chính tay Koltin làm.",
    "Obj_SubstituteCloth_14_Caption": "Tấm vải bền chắc mang hoa văn họa tiết của tộc Korok.",
    "Obj_SubstituteCloth_15_Caption": "Tấm vải bền chắc mang hình ảnh một chú gấu xám Grizzlemaw.",
    "Obj_SubstituteCloth_16_Caption": "Tấm vải thủ công bền chắc mang hình dáng thiết bị Purah Pad.",
    "Obj_SubstituteCloth_17_Caption": "Tấm vải bền chắc mang hoa văn họa tiết thương hiệu Cece.",
    "Obj_SubstituteCloth_18_Caption": "Tấm vải bền chắc mang hình ảnh loài quái điểu Aerocuda.",
    "Obj_SubstituteCloth_19_Caption": "Tấm vải bền chắc mang hình ảnh chú đà điểu Eldin.",
    "Obj_SubstituteCloth_20_Caption": "Tấm vải bền chắc mang hình ảnh chú gà Cucco đáng yêu.",
    "Obj_SubstituteCloth_21_Caption": "Tấm vải bền chắc mang hình ảnh loài ngựa dũng mãnh.",
    "Obj_SubstituteCloth_22_Caption": "Tấm vải bền chắc mang hình ảnh loài quái nhầy Chuchu.",
    "Obj_SubstituteCloth_23_Caption": "Tấm vải bền chắc mang hình ảnh quái thú nhân mã Lynel.",
    "Obj_SubstituteCloth_24_Caption": "Tấm vải bền chắc mang hình ảnh rồng ba đầu Gleeok hung tợn.",
    "Obj_SubstituteCloth_25_Caption": "Tấm vải bền chắc mang hình ảnh quái khổng lồ một mắt Stalnox.",
    "Obj_SubstituteCloth_26_Caption": "Tấm vải bền chắc mang hoa văn chiếc Áo Hồi Tưởng.",
    "Obj_SubstituteCloth_27_Caption": "Tấm vải bền chắc mang hình ảnh chiếc Mũ trùm Hylian.",
    "Obj_SubstituteCloth_28_Caption": "Tấm vải bền chắc mang họa tiết biểu trưng của công chúa.",
    "Obj_SubstituteCloth_29_Caption": "Tấm vải bền chắc mang biểu trưng của vị Anh Hùng tộc Goron.",
    "Obj_SubstituteCloth_30_Caption": "Tấm vải bền chắc mang biểu trưng của vị Anh Hùng tộc Rito.",
    "Obj_SubstituteCloth_31_Caption": "Tấm vải bền chắc mang biểu trưng của vị Anh Hùng tộc Zora.",
    "Obj_SubstituteCloth_32_Caption": "Tấm vải bền chắc mang biểu trưng của vị Anh Hùng tộc Gerudo.",
    "Obj_SubstituteCloth_33_Caption": "Tấm vải bền chắc mang hoa văn họa tiết Sheikah cổ đại.",
    "Obj_SubstituteCloth_34_Caption": "Tấm vải bền chắc mang hình ảnh quái vật Bokoblin.",
    "Obj_SubstituteCloth_35_Caption": "Tấm vải bền chắc mang họa tiết hắc ám của Ma Vương.",
    "Obj_SubstituteCloth_36_Caption": "Tấm vải bền chắc mang hình ảnh Thuyền Sư Tử Đỏ.",
    "Obj_SubstituteCloth_37_Caption": "Tấm vải bền chắc mang họa tiết chiến binh Sheik.",
    "Obj_SubstituteCloth_38_Caption": "Tấm vải bền chắc mang hình ảnh Chiếc Gương Hoàng Hôn.",
    "Obj_SubstituteCloth_39_Caption": "Tấm vải bền chắc mang hình ảnh Công Chúa Hoàng Hôn.",
    "Obj_SubstituteCloth_40_Caption": "Tấm vải bền chắc mang biểu trưng của Trang trại Lon Lon.",
    "Obj_SubstituteCloth_41_Caption": "Tấm vải bền chắc mang hình ảnh Mặt Nạ Majora kỳ quái.",
    "Obj_SubstituteCloth_43_Caption": "Tấm vải bền chắc mang hoa văn của một vương triều xa xưa.",
    "Obj_SubstituteCloth_45_Caption": "Tấm vải bền chắc mang hình ảnh linh hồn thanh kiếm cổ đại.",
    "Obj_SubstituteCloth_46_Caption": "Tấm vải bền chắc mang phong cách điểm ảnh pixel cổ điển.",
    "Obj_SubstituteCloth_48_Caption": "Tấm vải bền chắc mang họa tiết quả trứng khổng lồ.",
    "Obj_SubstituteCloth_49_Caption": "Tấm vải bền chắc mang hình ảnh Nữ Thần cao quý.",
    "Obj_SubstituteCloth_51_Caption": "Tấm vải bền chắc mang họa tiết Giáp da Anh Hùng.",
    "Obj_SubstituteCloth_52_Caption": "Tấm vải bền chắc mang hình ảnh Công Chúa Zelda.",
    "Obj_SubstituteCloth_53_Caption": "Tấm vải bền chắc mang họa tiết vua tộc Gerudo thuở xưa.",
    "Obj_SubstituteCloth_55_Caption": "Tấm vải bền chắc mang hoa văn đậm chất hoài niệm quá khứ.",
    "Obj_SubstituteCloth_56_Caption": "Tấm vải bền chắc mang hình vẽ Hudson, do chính tay Addison vẽ."
}

for k, name in cloth_names.items():
    trans[k] = name

for k, first in cloth_first_sentences.items():
    trans[k] = f"{first}\nCó vẻ như tấm vải này có thể dùng để căng lại\nbề mặt dù lượn."

print(f"Added cloths. Total so far: {len(trans)}")

# 5. Non-Obj misc items (80 keys)
non_obj_misc = {
    # Coupon & Blade
    "Item_StableHostelAccommodationCoupon_A_Name": "Phiếu Nghỉ Trọ",
    "Item_StableHostelAccommodationCoupon_A_Caption": "Phiếu nghỉ ngơi miễn phí cho một giường tiêu chuẩn tại trạm ngựa.\nPhần thưởng khi tích lũy Điểm thưởng Pony Point. Hãy sử dụng nó\ntại trạm ngựa để nghỉ ngơi và xua tan mọi mệt mỏi đường xa.",
    "Item_Weapon_01_Name": "Lưỡi Kiếm Cổ Đại",
    "Item_Weapon_01_Caption": "Lưỡi đoản kiếm cổ xưa tựa dao găm. Nó quá nhỏ bé để vung chém\nnhư một vũ khí thông thường, nhưng có thể gắn lên mũi tên\nđể làm đầu tên chiến đấu.",
    # KeySmall
    "KeySmall_Name": "Chìa Khóa Nhỏ",
    "KeySmall_Caption": "Chiếc chìa khóa dùng để mở cánh cửa bên trong Đền thờ Ánh sáng.",
    # MinusRupee (Poe)
    "MinusRupee_00_Name": "Linh Hồn Poe",
    "MinusRupee_00_Caption": "Một khối linh hồn phát sáng lập lòe tìm thấy khắp Lòng Đất.\nHãy dâng những linh hồn này cho Tượng Người Mặc Cả để đổi lấy\nnhiều phần thưởng giá trị.",
    "MinusRupee_01_Name": "Linh Hồn Poe Lớn",
    "MinusRupee_01_Caption": "Một khối linh hồn phát sáng lập lòe tìm thấy khắp Lòng Đất.\nHãy dâng chúng cho Tượng Người Mặc Cả để nhận phần thưởng.\nChúng dường như chứa đựng nguồn năng lượng to lớn.",
    "MinusRupee_02_Name": "Đại Linh Hồn Poe",
    "MinusRupee_02_Caption": "Khối linh hồn phát quang tìm thấy khắp các ngóc ngách Lòng Đất.\nHãy dâng chúng cho Tượng Người Mặc Cả để nhận phần thưởng.\nKhối cầu này dường như sở hữu nguồn sức mạnh khổng lồ.",
    # Parasail
    "Parasail_Name": "Dù Lượn",
    "Parasail_Caption": "Vật phẩm do Purah trao cho bạn, cho phép bạn cưỡi gió\nvà lượn bay lơ lửng trên bầu trời. Nhấn \x0e\x01\x04\x02\ucd0c\nkhi đang ở trên không để bung dù.",
    # PutRupee
    "PutRupee_Name": "Rupee Xanh Lá",
    "PutRupee_Caption": "Một đồng rupee lẻ. Ánh sáng xanh êm dịu của nó\nkhiến lòng bạn không khỏi mỉm cười.",
    "PutRupee_Blue_Name": "Rupee Xanh Dương",
    "PutRupee_Blue_Caption": "Năm rupee. Những mặt cắt lấp lánh sắc xanh biếc\nkhiến đôi chân bạn rộn ràng muốn bước tiếp.",
    "PutRupee_Red_Name": "Rupee Đỏ",
    "PutRupee_Red_Caption": "20 rupee. Ánh hào quang đỏ rực rỡ làm xao xuyến\ntừng sợi dây cảm xúc nơi đáy tim bạn.",
    "PutRupee_Purple_Name": "Rupee Tím",
    "PutRupee_Purple_Caption": "50 rupee. Ánh sáng tím huyền ảo lấp đầy trái tim bạn\nvới sự hào sảng và rộng lượng.",
    "PutRupee_Silver_Name": "Rupee Bạc",
    "PutRupee_Silver_Caption": "100 rupee! Luồng ánh bạc rực rỡ phản chiếu nụ cười rạng rỡ\ntrên gương mặt bạn.",
    "PutRupee_Gold_Name": "Rupee Vàng",
    "PutRupee_Gold_Caption": "300 rupee! Ánh hoàng kim rực rỡ chói lòa bừng sáng\ncả tâm hồn bạn.",
    # SpObj capsules
    "SpObj_BalloonEnvelope_Capsule_A_01_Name": "Khí Cầu",
    "SpObj_BalloonEnvelope_Capsule_A_01_Caption": "Thiết bị Zonai bay lên cao khi được nạp đầy khí nóng.\nKhông khí càng nóng, khí cầu bay lên càng nhanh.",
    "SpObj_Beamos_Capsule_A_01_Name": "Bộ Phát Tia Laze",
    "SpObj_Beamos_Capsule_A_01_Caption": "Thiết bị Zonai bắn ra chùm tia sáng hủy diệt từ phần sừng,\ngây sát thương nặng nề cho mục tiêu ở khoảng cách cực xa.",
    "SpObj_Cannon_Capsule_A_01_Name": "Đại Bác",
    "SpObj_Cannon_Capsule_A_01_Caption": "Thiết bị Zonai bắn ra đạn pháo theo từng đợt ngắt quãng.\nPhát bắn phát nổ khi va chạm mục tiêu. Đây là thiết bị uy lực lớn,\nnhưng cần căn góc bắn thật chuẩn xác.",
    "SpObj_Cart_Capsule_A_01_Name": "Xe Trượt",
    "SpObj_Cart_Capsule_A_01_Caption": "Thiết bị Zonai chế tạo để di chuyển êm ái trên các bề mặt bằng phẳng.\nChỉ cần tác động lực là xe sẽ chuyển bánh, miễn là còn nguồn năng lượng.",
    "SpObj_Chaser_Capsule_A_01_Name": "Xe Tự Hành Tầm Nhiệt",
    "SpObj_Chaser_Capsule_A_01_Caption": "Thiết bị Zonai tự động di chuyển truy lùng quái vật.\nNgười ta tin rằng tộc Zonai xưa kia từng dùng nó\nnhư một biện pháp tuần tra phòng thủ an ninh.",
    "SpObj_ControlStick_Capsule_A_01_Name": "Cần Điều Khiển",
    "SpObj_ControlStick_Capsule_A_01_Caption": "Thiết bị Zonai dùng để kiểm soát hướng lái khi gắn vào phương tiện.\nNó sẽ kích hoạt đồng loạt tất cả thiết bị Zonai kết nối cùng lúc.",
    "SpObj_CookSet_Capsule_A_01_Name": "Nồi Nấu Di Động",
    "SpObj_CookSet_Capsule_A_01_Caption": "Thiết bị Zonai giúp nấu nướng thức ăn mọi lúc, mọi nơi.\nNồi chỉ dùng được cho một lần nấu duy nhất.\nThiết bị sẽ dễ đặt vững hơn trên mặt đất bằng phẳng.",
    "SpObj_ElectricBoxGenerator_Capsule_A_01_Name": "Bộ Phóng Điện",
    "SpObj_ElectricBoxGenerator_Capsule_A_01_Caption": "Thiết bị Zonai phóng ra luồng điện giật từ sừng khi bị tác động.\nKỳ lạ thay, chỉ có phần sừng dẫn điện, còn lại toàn bộ phần đầu\nđều an toàn để cầm nắm.",
    "SpObj_EnergyBank_Capsule_A_01_Name": "Pin Năng Lượng",
    "SpObj_EnergyBank_Capsule_A_01_Caption": "Thiết bị Zonai tích trữ năng lượng Zonai cô đặc.\nDùng để cung cấp nguồn điện tạm thời cho các thiết bị Zonai khác hoạt động.",
    "SpObj_EnergyBank_Capsule_A_02_Name": "Pin Năng Lượng Lớn",
    "SpObj_EnergyBank_Capsule_A_02_Caption": "Viên pin có tỷ lệ nén năng lượng vượt trội. Dù là loại dùng một lần,\nnó chứa nguồn năng lượng gấp nhiều lần viên pin thông thường.",
    "SpObj_FastWheel_Capsule_A_01_Name": "Bánh Xe Nhỏ",
    "SpObj_FastWheel_Capsule_A_01_Caption": "Bánh xe trợ lực Zonai quay rất nhanh và hoạt động tối ưu\ntrên mặt phẳng. Nó không thích hợp khi leo đồi dốc\nhay vượt địa hình gồ ghề.",
    "SpObj_FastWheel_Capsule_B_01_Name": "Bánh Xe Lớn",
    "SpObj_FastWheel_Capsule_B_01_Caption": "Cỗ máy trợ lực mạnh mẽ luôn muốn tiến lên! Bánh xe to lớn gồ ghề\nchuyên phá vỡ và vượt qua những địa hình hiểm trở mà bánh xe nhỏ chào thua.\nNó thậm chí có thể chạy băng qua vùng nước nông.",
    "SpObj_FlameThrower_Capsule_A_01_Name": "Bộ Phun Lửa",
    "SpObj_FlameThrower_Capsule_A_01_Caption": "Thiết bị Zonai phun ra luồng lửa dữ dội. Người ta cho rằng\nban đầu nó được dùng để tự vệ và xua đuổi quái vật.",
    "SpObj_FlashLight_Capsule_A_01_Name": "Đèn Chiếu Sáng",
    "SpObj_FlashLight_Capsule_A_01_Caption": "Thiết bị Zonai đem lại nguồn sáng cho những nơi tăm tối.\nĐèn rọi theo một hướng, tầm chiếu sáng không quá xa\nnhưng rất hữu ích trên những con đường đêm hay trong hang động.",
    "SpObj_FloatingStone_Capsule_A_01_Name": "Đá Lơ Lửng",
    "SpObj_FloatingStone_Capsule_A_01_Caption": "Thiết bị Zonai thách thức trọng lực và đứng yên lơ lửng tại chỗ.\nThuở xưa, tộc Zonai có thể đã dùng công nghệ này\nđể tạo nên những hòn đảo bay lơ lửng giữa lưng chừng trời.",
    "SpObj_GolemHead_Capsule_A_01_Name": "Đầu Golem Định Vị",
    "SpObj_GolemHead_Capsule_A_01_Caption": "Thiết bị Zonai luôn tự động quay mặt về bất cứ mục tiêu nào nó coi là kẻ thù.\nGắn thiết bị Zonai chiến đấu lên đầu nó để tự động tung đòn tấn công dẫn đường.",
    "SpObj_LiftableWaterPump_Capsule_A_01_Name": "Vòi Phun Nước",
    "SpObj_LiftableWaterPump_Capsule_A_01_Caption": "Thiết bị Zonai phun trào dòng nước khi bị đánh trúng.\nTheo truyền thuyết, quần đảo bầu trời từng thiếu nước ngọt thuở xưa,\nnhưng đã trở nên tươi tốt trù phú nhờ công nghệ vòi phun này.",
    "SpObj_LiftGeneratorWing_Capsule_A_01_Name": "Cánh Bay",
    "SpObj_LiftGeneratorWing_Capsule_A_01_Caption": "Thiết bị Zonai tận dụng lực nâng khí động học để cưỡi gió bay lượn.\nĐể bay xa hơn, hãy cố gắng giữ thăng bằng ngay trọng tâm cánh.",
    "SpObj_LightMirror_Capsule_A_01_Name": "Gương Phản Chiếu",
    "SpObj_LightMirror_Capsule_A_01_Caption": "Thiết bị Zonai hội tụ và phản chiếu ánh sáng.\nNó mang lại nguồn sáng mạnh mẽ tầm xa, có thể xua đuổi\nmột số loài quái vật trong bóng tối.",
    "SpObj_Pile_Capsule_A_01_Name": "Cọc Cố Định",
    "SpObj_Pile_Capsule_A_01_Caption": "Thiết bị Zonai có thể ghim chặt cố định xuống mặt đất hoặc lên vách đá.\nChúng từng được dùng làm điểm tựa và nền móng công trình\nnhờ độ vững chãi bất di bất dịch khi đã đóng cọc.",
    "SpObj_Rocket_Capsule_A_01_Name": "Tên Lửa",
    "SpObj_Rocket_Capsule_A_01_Caption": "Thiết bị Zonai tạo ra lực đẩy xung kích cực mạnh.\nUy lực phóng vô cùng lớn nhưng nhiên liệu sẽ tiêu hao rất nhanh chóng.",
    "SpObj_SlipBoard_Capsule_A_01_Name": "Ván Trượt",
    "SpObj_SlipBoard_Capsule_A_01_Caption": "Thiết bị Zonai có mặt đáy nhẵn bóng giúp giảm thiểu tối đa ma sát.\nThời cổ đại, có lẽ nó từng được dùng để vận chuyển đồ đạc\nlướt đi trên cỏ và cát lún.",
    "SpObj_SnowMachine_Capsule_A_01_Name": "Bộ Phun Băng Giá",
    "SpObj_SnowMachine_Capsule_A_01_Caption": "Thiết bị Zonai thổi ra luồng khí băng giá buốt giá, rất tiện dụng\nđể làm chậm và hạ gục quái vật. Ngoài ra, một số nguyên liệu\nsẽ biến đổi thuộc tính khi tiếp xúc với hơi lạnh cực độ.",
    "SpObj_SpringPiston_Capsule_A_01_Name": "Lò Xo",
    "SpObj_SpringPiston_Capsule_A_01_Caption": "Thiết bị Zonai co lại rồi bung nở với lực đẩy cực mạnh\nđể hất văng mọi vật thể vọt lên không trung.",
    "SpObj_TiltingDoll_Capsule_A_01_Name": "Con Lật Đật Cân Bằng",
    "SpObj_TiltingDoll_Capsule_A_01_Caption": "Thiết bị Zonai cân bằng hoàn hảo, luôn tự động đứng thẳng tắp\nkhi kích hoạt. Từng được dùng để tạo chỗ đứng vững chắc\ntại các vị trí chênh vênh như trên các hòn đảo bầu trời.",
    "SpObj_TimerBomb_Capsule_A_01_Name": "Bom Hẹn Giờ",
    "SpObj_TimerBomb_Capsule_A_01_Caption": "Thiết bị Zonai tạo vụ nổ có đếm ngược thời gian.\nSóng xung kích từ vụ nổ có thể kích hoạt các thiết bị Zonai khác.",
    "SpObj_WindGenerator_Capsule_A_01_Name": "Quạt Gió",
    "SpObj_WindGenerator_Capsule_A_01_Caption": "Thiết bị Zonai tạo ra luồng gió mạnh bằng cánh quạt bên trong.\nNhiều khả năng tộc Zonai đã khéo léo tận dụng sức gió này\nđể vận chuyển đồ vật và tạo lực đẩy cho phương tiện."
}

trans.update(non_obj_misc)
print(f"Added non-obj misc. Total so far: {len(trans)}")

# 6. Obj miscellaneous items (111 keys)
obj_misc = {
    # Amiibo
    "Obj_AmiiboItem_Name": "amiibo",
    # ArrowBundle
    "Obj_ArrowBundle_A_01_Name": "Mũi Tên x 5",
    "Obj_ArrowBundle_A_01_Caption": "Một bó gồm 5 mũi tên thông thường.\nThân tên được đẽo gọt từ loại gỗ cây vô cùng chắc chắn.",
    "Obj_ArrowBundle_A_02_Name": "Mũi Tên x 10",
    "Obj_ArrowBundle_A_02_Caption": "Một bó gồm 10 mũi tên thông thường.\nThân tên được đẽo gọt từ loại gỗ cây vô cùng chắc chắn.",
    # Autobuild
    "Obj_AutoBuilder_Name": "Autobuild",
    "Obj_AutoBuilder_Caption": "\x0e\x00\x03\x02\x01Tái tạo tức thì\x0e\x00\x03\x02\uffff các công trình lắp ráp Ultrahand của bạn,\nsử dụng các vật phẩm xung quanh và quặng zonaite.\nAutobuild sẽ tự động lưu lại các bản dựng trước đây của bạn.",
    # Schema Stone
    "Obj_AutoBuilderDraft_00_Name": "Đá Bản Thiết Kế",
    "Obj_AutoBuilderDraft_00_Caption": "Một phiến đá khắc những đường nét tựa bản vẽ thiết kế.\nNó có vẻ sẽ rất hữu ích...",
    "Obj_AutoBuilderDraft_00_Caption_HasAutoBuilder": "Những phiến đá này phác thảo bản thiết kế của các khí cụ\nchẳng hạn như phương tiện Zonai. Autobuild sẽ lưu bản thiết kế\nvà tự động lắp ráp theo lệnh của bạn.",
    # Yiga Schematic
    "Obj_AutoBuilderDraftAssassin_00_Name": "Bản Thiết Kế Yiga",
    "Obj_AutoBuilderDraftAssassin_00_Caption": "Bản thiết kế cho một phát minh kỳ quặc ghép từ các thiết bị Zonai\nvà vật liệu xây dựng. Trông có vẻ khá hữu dụng...",
    "Obj_AutoBuilderDraftAssassin_00_Caption_HasAutoBuilder": "Bản vẽ nguệch ngoạc của cỗ máy chế tạo từ thiết bị Zonai\nvà vật liệu xây dựng. Bạn có thể dùng Autobuild để lưu bản thiết kế\nvà tiến hành lắp ráp trực tiếp từ đó.",
    # Energy Cell (Battery)
    "Obj_Battery_Get_Name": "Pin Năng Lượng",
    "Obj_Battery_Get_Caption": "Món quà từ một Ma Tượng Golem Zonai. Được thiết kế để đeo bên hông,\ncung cấp năng lượng vận hành các thiết bị Zonai.",
    "Obj_Battery_Get_Caption_Unlock": "Nguồn năng lượng di động tích trữ điện năng cần thiết để vận hành\nmột số thiết bị Zonai. Nó sẽ tự động sạc đầy lại theo thời gian.",
    # Camera
    "Obj_Camera_Name": "Máy Ảnh",
    "Obj_Camera_Caption": "Chụp lại các bức ảnh bằng Purah Pad.\nSau đó bạn có thể lưu giữ chúng vào album ảnh.",
    # Well & Lightroot Honors
    "Obj_CaveWellHonor_00_Name": "Mô Hình Giếng Nước Hoàn Mỹ",
    "Obj_CaveWellHonor_00_Caption": "Để cảm ơn bạn đã khám phá ra toàn bộ vị trí các giếng nước tại Hyrule,\nFera đã trao tặng bạn mô hình giếng nước tuyệt đẹp\nđược lồng cẩn thận bên trong quả cầu thủy tinh trong suốt này.",
    "Obj_CheckPointHonor_00_Name": "Huy Chương Xua Tan Bóng Tối",
    "Obj_CheckPointHonor_00_Caption": "Phần thưởng vinh danh người đã chinh phục bóng đêm bằng cách thắp sáng\ntất cả các Cội Rễ Ánh Sáng dưới Lòng Đất. Món bảo vật đặc biệt này\nghi dấu những lời chúc phúc đã được ban trao.",
    # Monster Medals (DefeatHonor)
    "Obj_DefeatHonor_00_Name": "Huy Chương Tiễu Quái Đá Talus",
    "Obj_DefeatHonor_00_Caption": "Huy chương danh dự do Đội tuần tra tiễu quái trao tặng nhằm tri ân\nchiến công tiêu diệt toàn bộ Quái Đá Stone Talus trên khắp Hyrule.\nHuy chương được chạm khắc tinh xảo theo hình dáng loài quái vật này.",
    "Obj_DefeatHonor_01_Name": "Huy Chương Tiễu Quái Hinox",
    "Obj_DefeatHonor_01_Caption": "Huy chương danh dự do Đội tuần tra tiễu quái trao tặng nhằm tri ân\nchiến công tiêu diệt toàn bộ Độc Nhãn Hinox trên khắp Hyrule.\nHuy chương được chạm khắc tinh xảo theo hình dáng loài quái vật này.",
    "Obj_DefeatHonor_02_Name": "Huy Chương Tiễu Quái Molduga",
    "Obj_DefeatHonor_02_Caption": "Huy chương danh dự do Đội tuần tra tiễu quái trao tặng nhằm tri ân\nchiến công tiêu diệt toàn bộ Kình Ngư Cát Molduga trên khắp Hyrule.\nHuy chương được chạm khắc tinh xảo theo hình dáng loài quái vật này.",
    "Obj_DefeatHonor_03_Name": "Huy Chương Tiễu Quái Frox",
    "Obj_DefeatHonor_03_Caption": "Huy chương danh dự do Đội tuần tra tiễu quái trao tặng nhằm tri ân\nchiến công tiêu diệt toàn bộ Cóc Khổng Lồ Frox trên khắp Hyrule.\nHuy chương được chạm khắc tinh xảo theo hình dáng loài quái vật này.",
    "Obj_DefeatHonor_04_Name": "Huy Chương Tiễu Quái Ma Tượng Ma Trận",
    "Obj_DefeatHonor_04_Caption": "Huy chương danh dự do Đội tuần tra tiễu quái trao tặng nhằm tri ân\nchiến công tiêu diệt toàn bộ Ma Tượng Ma Trận Flux Construct tại Hyrule.\nHuy chương được chạm khắc tinh xảo theo hình dáng loài quái vật này.",
    "Obj_DefeatHonor_05_Name": "Huy Chương Tiễu Quái Rồng Gleeok",
    "Obj_DefeatHonor_05_Caption": "Huy chương danh dự do Đội tuần tra tiễu quái trao tặng nhằm tri ân\nchiến công tiêu diệt toàn bộ Rồng Ba Đầu Gleeok trên khắp Hyrule.\nHuy chương được chạm khắc tinh xảo theo hình dáng loài quái vật này.",
    # DRStone (Purah Pad)
    "Obj_DRStone_Get_Name": "Purah Pad",
    "Obj_DRStone_Get_Caption": "Thiết bị quý giá của Công Chúa Zelda. Nó sở hữu vô số tính năng\nthiết yếu và không thể thiếu cho chuyến phiêu lưu.",
    # Light of Blessing
    "Obj_DungeonClearSeal_Name": "Ánh Sáng Chúc Phúc",
    "Obj_DungeonClearSeal_Caption": "Viên tinh thể rực sáng với nguồn quang năng thanh tẩy tà ma cổ đại\nvà gột rửa mọi uế tạp bằng ánh hào quang thuần khiết.",
    # Energy Well & Heart/Stamina Containers
    "Obj_EnergyUtuwa_A_01_Name": "Cột Năng Lượng",
    "Obj_EnergyUtuwa_A_01_Caption": "Bộ phận nhỏ được chế tác từ các khối tinh thể năng lượng.\nNó gia tăng lượng năng lượng tối đa có thể tích trữ\ntrong Pin Năng Lượng của bạn.",
    "Obj_FireWoodBundle_Name": "Gỗ Củi",
    "Obj_FireWoodBundle_Caption": "Bó củi gỗ tiện lợi. Bạn có thể dùng bó củi này để nhóm lửa trại\nnếu có trong tay dụng cụ đánh lửa.",
    "Obj_HeartUtuwa_A_01_Name": "Bình Chứa Tim",
    "Obj_HeartUtuwa_A_01_Caption": "Vật phẩm quý hiếm giúp phục hồi một phần sinh lực mà bạn từng đánh mất\ndo chướng khí Gloom, đồng thời tăng vĩnh viễn giới hạn máu của bạn thêm một trái tim.",
    "Obj_StaminaUtuwa_A_01_Name": "Bình Chứa Thể Lực",
    "Obj_StaminaUtuwa_A_01_Caption": "Vật phẩm quan trọng giúp phục hồi một phần thể lực mà bạn từng đánh mất\ndo chướng khí Gloom, đồng thời mở rộng vĩnh viễn kích thước của Vòng Thể Lực.",
    # Earthwake Manual
    "Obj_HiddenScroll_00_Name": "Bí Kíp Địa Chấn Earthwake",
    "Obj_HiddenScroll_00_Caption": "Cuốn bí kíp tâm truyền hé lộ bí mật về tuyệt kỹ Địa Chấn Earthwake\nvốn chỉ những bậc thầy kiếm thuật Bang Yiga mới được truyền thụ.\nChiêu thức này cho phép tung đòn tụ lực mà không cần bất kỳ vũ khí nào.",
    # Item Sharing & Daily Challenge
    "Obj_ItemBox_00_Name": "Chia Sẻ Vật Phẩm",
    "Obj_ItemBox_00_Caption": "Bạn có thể gửi và rút vật phẩm\nbằng cách dùng \x0e\x01\x04\x02\ucd2c GHI CHÚ ZELDA.",
    "Obj_DailyChallenge_00_Name": "Thưởng Mỗi Ngày",
    "Obj_DailyChallenge_00_Caption": "Bạn có thể kích hoạt các phần thưởng từ Điểm Thưởng Mỗi Ngày,\nnhận được từ \x0e\x01\x04\x02\ucd2c GHI CHÚ ZELDA.",
    # Korok Seed & Gift
    "Obj_KorokNuts_Name": "Hạt Korok Seed",
    "Obj_KorokNuts_Caption": "Hạt giống nhỏ này do một bé Korok trao tặng cho bạn.\nNó mang một mùi hương rất đặc trưng. Nếu bạn thu thập thật nhiều hạt,\nbiết đâu điều kỳ diệu sẽ xảy ra...",
    "Obj_ProofKorok_Name": "Món Quà Của Hestu",
    "Obj_ProofKorok_Caption": "Món quà tình bạn do Hestu trao tặng cho bạn.\nMùi của nó thật sự khá là kinh khủng.",
    # Fuse, Recall, Ascend, Ultrahand
    "Obj_OneTouchBond_Name": "Fuse",
    "Obj_OneTouchBond_Caption": "\x0e\x00\x03\x02\x01Hợp nhất vật thể\x0e\x00\x03\x02\uffff vào vũ khí hoặc khiên đang trang bị\nđể \x0e\x00\x03\x02\x01cường hóa sức mạnh\x0e\x00\x03\x02\uffff. Bạn có thể tháo rời mối hợp nhất,\nnhưng hành động đó sẽ phá hủy vật thể đã gắn kèm.",
    "Obj_ReverseRecorder_Name": "Recall",
    "Obj_ReverseRecorder_Caption": "\x0e\x00\x03\x02\x01Đảo ngược chuyển động của vật thể\x0e\x00\x03\x02\uffff quay trở lại vị trí ban đầu.\nBạn có thể dừng chuyển động đảo ngược này vào bất kỳ lúc nào.",
    "Obj_Tooreroof_Name": "Ascend",
    "Obj_Tooreroof_Caption": "Bơi ngược thẳng lên xuyên qua các bề mặt cứng rắn\nvà \x0e\x00\x03\x02\x01nhô lên trên đỉnh của chúng\x0e\x00\x03\x02\uffff.",
    "Obj_UltraHand_Name": "Ultrahand",
    "Obj_UltraHand_Caption": "\x0e\x00\x03\x02\x01Nắm lấy và di chuyển\x0e\x00\x03\x02\uffff vật thể, \x0e\x00\x03\x02\x01xoay chuyển\x0e\x00\x03\x02\uffff chúng,\nvà \x0e\x00\x03\x02\x01dán dính\x0e\x00\x03\x02\uffff chúng vào các vật thể khác.",
    # Photos
    "Obj_Photo_Animal_Name": "Ảnh Hệ Động Vật",
    "Obj_Photo_Animal_Caption": "Bức ảnh chụp một loài thú, chim muông, cá hoặc côn trùng.",
    "Obj_Photo_BossEnemy_Name": "Ảnh Kẻ Địch Tinh Anh",
    "Obj_Photo_BossEnemy_Caption": "Bức ảnh chụp một con quái vật hùng mạnh từng một thời cản bước chân bạn.",
    "Obj_Photo_Enemy_Name": "Ảnh Kẻ Địch",
    "Obj_Photo_Enemy_Caption": "Bức ảnh chụp một trong vô số loài quái vật lang thang khắp Hyrule.",
    "Obj_Photo_Material_Name": "Ảnh Nguyên Liệu",
    "Obj_Photo_Material_Caption": "Bức ảnh chụp một nguyên liệu nấu nướng, chẳng hạn như táo hay nấm.",
    "Obj_Photo_Other_Name": "Ảnh Chủ Đề Khác",
    "Obj_Photo_Other_Caption": "Bức ảnh chụp một đối tượng thú vị, chẳng hạn như rương báu hay quặng khoáng sản.",
    "Obj_Photo_Weapon_Name": "Ảnh Vũ Khí",
    "Obj_Photo_Weapon_Caption": "Bức ảnh chụp một món vũ khí từng trải qua trận mạc, như gươm kiếm, thương giáo hay cung tên.",
    "Obj_PictureBook_Name": "Bách Khoa Toàn Thư Hyrule",
    # Sage Vows (Obj_SageSoul)
    "Obj_SageSoul_Gerudo_Name": "Lời Thề Của Riju, Hiền Nhân Sấm Sét",
    "Obj_SageSoul_Gerudo_Caption": "Minh chứng cho lời thề của Riju, Hiền Nhân Sấm Sét.\nSử dụng nó để triệu hồi hoặc giải tán hóa thân của Riju.",
    "Obj_SageSoul_Goron_Name": "Lời Thề Của Yunobo, Hiền Nhân Lửa",
    "Obj_SageSoul_Goron_Caption": "Minh chứng cho lời thề của Yunobo, Hiền Nhân Lửa.\nSử dụng nó để triệu hồi hoặc giải tán hóa thân của Yunobo.",
    "Obj_SageSoul_Rito_Name": "Lời Thề Của Tulin, Hiền Nhân Gió",
    "Obj_SageSoul_Rito_Caption": "Minh chứng cho lời thề của Tulin, Hiền Nhân Gió.\nSử dụng nó để triệu hồi hoặc giải tán hóa thân của Tulin.",
    "Obj_SageSoul_Zonau_Name": "Lời Thề Của Mineru, Hiền Nhân Linh Hồn",
    "Obj_SageSoul_Zonau_Caption": "Minh chứng cho lời thề của Mineru, Hiền Nhân Linh Hồn.\nSử dụng nó để triệu hồi hoặc thu hồi cỗ người máy chứa linh hồn Mineru.",
    "Obj_SageSoul_Zora_Name": "Lời Thề Của Sidon, Hiền Nhân Nước",
    "Obj_SageSoul_Zora_Caption": "Minh chứng cho lời thề của Sidon, Hiền Nhân Nước.\nSử dụng nó để triệu hồi hoặc giải tán hóa thân của Sidon.",
    # Solemn Vows (Obj_SageSoulPlus)
    "Obj_SageSoulPlus_Gerudo_Name": "Lời Thề Kiên Định Của Riju, Hiền Nhân Sấm Sét",
    "Obj_SageSoulPlus_Gerudo_Caption": "Lời thề đã được gia tăng sức mạnh của Riju, Hiền Nhân Sấm Sét.\nMối gắn kết sâu sắc giữa bạn và Riju đã nâng cao sức tấn công của hóa thân.",
    "Obj_SageSoulPlus_Goron_Name": "Lời Thề Kiên Định Của Yunobo, Hiền Nhân Lửa",
    "Obj_SageSoulPlus_Goron_Caption": "Lời thề đã được gia tăng sức mạnh của Yunobo, Hiền Nhân Lửa.\nMối gắn kết sâu sắc giữa bạn và Yunobo đã nâng cao sức tấn công của hóa thân.",
    "Obj_SageSoulPlus_Rito_Name": "Lời Thề Kiên Định Của Tulin, Hiền Nhân Gió",
    "Obj_SageSoulPlus_Rito_Caption": "Lời thề đã được gia tăng sức mạnh của Tulin, Hiền Nhân Gió.\nMối gắn kết sâu sắc giữa bạn và Tulin đã nâng cao sức tấn công của hóa thân.",
    "Obj_SageSoulPlus_Zonau_Name": "Lời Thề Kiên Định Của Mineru, Hiền Nhân Linh Hồn",
    "Obj_SageSoulPlus_Zonau_Caption": "Lời thề đã được gia tăng sức mạnh của Mineru, Hiền Nhân Linh Hồn.\nMối gắn kết sâu sắc giữa bạn và Mineru đã nâng cao sức tấn công của người máy.",
    "Obj_SageSoulPlus_Zora_Name": "Lời Thề Kiên Định Của Sidon, Hiền Nhân Nước",
    "Obj_SageSoulPlus_Zora_Caption": "Lời thề đã được gia tăng sức mạnh của Sidon, Hiền Nhân Nước.\nMối gắn kết sâu sắc giữa bạn và Sidon đã nâng cao sức tấn công của hóa thân.",
    # Sage's Will
    "Obj_SageWill_Name": "Ý Chí Của Hiền Nhân",
    "Obj_SageWill_Caption": "Viên đá nhỏ được tin là từng thuộc về một vị Hiền Nhân thuở trước.\nCầm nó trên tay, bạn có thể cảm nhận tàn dư của một mối gắn kết thiêng liêng.",
    "Obj_SageWill_Caption_HasSageSoul": "Tàn tích của ý chí quyết tử từ một cựu Hiền Nhân xưa kia.\nNếu thu thập đủ bốn viên và dâng lên Tượng Nữ Thần, bạn có thể\nthắt chặt mối liên kết linh hồn với các Hiền Nhân.",
    # Sheik Sensor
    "Obj_SheikSensor_Name": "Cảm Biến",
    "Obj_SheikSensorLv2_Name": "Cảm Biến +",
    # StableHostlePointCard
    "Obj_StableHostlePointCard_Name": "Thẻ Điểm Thưởng Pony Point",
    "Obj_StableHostlePointCard_Caption": "Sử dụng dịch vụ trạm ngựa để nhận điểm. Tích lũy điểm để đổi phần thưởng.\nSố điểm cần thiết cho phần thưởng tiếp theo: \x0e\x02\x02>8HorseInn_NextRewardNeetPoint\uffff\ucd00",
    "Obj_StableHostlePointCard_Caption_ReceiveBenefits": "Sử dụng dịch vụ trạm ngựa để nhận điểm. Tích lũy điểm để đổi phần thưởng.\nBạn đã \x0e\x00\x03\x02\x01đủ điều kiện nhận phần thưởng\x0e\x00\x03\x02\uffff.",
    # Treasure Map
    "Obj_TreasureMap_00_Name": "Bản Đồ Cổ",
    "Obj_TreasureMap_00_Caption": "Tấm bản đồ rất xưa cũ đánh dấu một vị trí bí ẩn.\nLiệu điều gì đang chờ đón ở nơi đó?",
    # Travel Medallions (WarpDLC)
    "Obj_WarpDLC_Name": "Huy Hiệu Dịch Chuyển",
    "Obj_WarpDLC_Caption": "Công cụ kỳ bí do kỹ sư Robbie chế tạo.\nĐặt nó bằng cách mở túi đồ và đăng ký vị trí hiện tại\nlàm cổng dịch chuyển tức thời.",
    "Obj_WarpDLC_Prototype_Name": "Bản Mẫu Huy Hiệu Dịch Chuyển",
    "Obj_WarpDLC_Prototype_Caption": "Robbie đã mổ xẻ nghiên cứu một huy hiệu dịch chuyển để tạo nên bản mẫu này,\nnhưng hiện tại nó chưa thể sử dụng được vì còn thiếu một số dữ liệu quan trọng."
}

trans.update(obj_misc)
print(f"Added obj misc. Total so far: {len(trans)}")

# 7. Verification
missing = [k for k in source if k not in trans]
print(f"Missing keys: {len(missing)}")
if missing:
    print("Sample missing:", missing[:10])

extra = [k for k in trans if k not in source]
print(f"Extra keys: {len(extra)}")

# Save to output
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(trans, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {out_path} with {len(trans)} keys.")
