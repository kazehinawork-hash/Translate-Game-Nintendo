import os, glob, json

# 1. RewardCategory
rew_cat = {
  "BodyColor": "Màu da",
  "HairColor": "Màu tóc",
  "EyeColor": "Màu mắt",
  "Clothes": "Trang phục",
  "Special": "Vóc dáng đặc biệt",
  "Hair": "Kiểu tóc",
  "AccessoryHead": "Phụ kiện đầu",
  "Cap": "Mũ nón",
  "AccessoryEye": "Kính mắt",
  "AccessoryMonocle": "Bịt mắt",
  "AccessoryMouth": "Khẩu trang & Râu",
  "SportsGoodsBowling": "Dụng cụ Bowling",
  "SportsGoodsBadminton": "Dụng cụ Cầu Lông",
  "SportsGoodsVolleyBall": "Dụng cụ Bóng Chuyền",
  "SportsGoodsChanbara": "Dụng cụ Kiếm Đạo",
  "SportsGoodsSoccer": "Dụng cụ Bóng Đá",
  "SportsGoodsTennis": "Dụng cụ Quần Vợt",
  "SportsGoodsGolf": "Dụng cụ Golf",
  "PlayerTitle": "Danh hiệu",
  "EmoteStamp": "Tem cảm xúc",
  "Eyebrow": "Lông mày",
  "EquipmentSet": "Bộ trang phục",
  "Facepaint": "Họa tiết mặt"
}
with open('translations/vi/ProgramMsg__Equipment__RewardCategory.msbt.json', 'w', encoding='utf-8') as f:
    json.dump(rew_cat, f, ensure_ascii=False, indent=2)

# 2. BodyColor
body_color = {
  "BodyColor06": "Màu cơ thể (Trắng)",
  "BodyColor07": "Màu cơ thể (Tím)",
  "BodyColor08": "Màu cơ thể (Xanh lá)",
  "BodyColor09": "Màu cơ thể (Xanh dương)"
}
with open('translations/vi/ProgramMsg__Equipment__BodyColor.msbt.json', 'w', encoding='utf-8') as f:
    json.dump(body_color, f, ensure_ascii=False, indent=2)

# 3. EyeColor
eye_color = {
  "EyeColor07": "Vàng",
  "EyeColor08": "Xanh lá",
  "EyeColor09": "Đỏ",
  "EyeColor10": "Tím nhạt",
  "EyeColor11": "Cam nhạt",
  "EyeColor12": "Xanh lam nhạt",
  "EyeColor13": "Xanh lá nhạt",
  "EyeColor14": "Vàng nhạt",
  "EyeColor15": "Hồng nhạt",
  "EyeColor16": "Tím",
  "EyeColor17": "Hổ phách",
  "EyeColor18": "Xanh hải quân"
}
with open('translations/vi/ProgramMsg__Equipment__EyeColor.msbt.json', 'w', encoding='utf-8') as f:
    json.dump(eye_color, f, ensure_ascii=False, indent=2)

# 4. HairColor
hair_color = {
  "HairColor07": "Tím",
  "HairColor08": "Đỏ",
  "HairColor09": "Xanh lá",
  "HairColor10": "Vàng nhạt",
  "HairColor11": "Hồng nhạt",
  "HairColor12": "Xanh lá nhạt",
  "HairColor13": "Tím hoa cà",
  "HairColor14": "Xanh lam nhạt",
  "HairColor15": "Vàng trắng",
  "HairColor16": "Vàng kim",
  "HairColor17": "Xanh ngọc lục bảo",
  "HairColor18": "Tím hoàng gia",
  "HairColor19": "Xanh hải quân"
}
with open('translations/vi/ProgramMsg__Equipment__HairColor.msbt.json', 'w', encoding='utf-8') as f:
    json.dump(hair_color, f, ensure_ascii=False, indent=2)

# 5. Eyebrow
eyebrow = {
  "Eyebrow00": "Lông mày mỏng cong",
  "Eyebrow01": "Lông mày rậm cong",
  "Eyebrow02": "Lông mày mỏng ngang",
  "Eyebrow03": "Lông mày rậm ngang",
  "Eyebrow04": "Lông mày mỏng cụp",
  "Eyebrow05": "Lông mày rậm cụp",
  "Eyebrow06": "Lông mày sắc sảo",
  "Eyebrow07": "Không lông mày",
  "Eyebrow08": "Lông mày cách điệu",
  "Eyebrow09": "Lông mày kẻ vạch (Slit)"
}
with open('translations/vi/ProgramMsg__Equipment__Eyebrow.msbt.json', 'w', encoding='utf-8') as f:
    json.dump(eyebrow, f, ensure_ascii=False, indent=2)

# 6. Body
body = {
  "BodyHuman00": "Vóc dáng người",
  "HeadMii": "Chọn nhân vật Mii",
  "Special00": "Vóc dáng Thỏ",
  "Special01": "Vóc dáng Sóc",
  "Special02": "Vóc dáng Người máy",
  "Special03": "Vóc dáng Chim",
  "Special04": "Vóc dáng Cá mập",
  "Special05": "Vóc dáng Người máy Mk-II",
  "Special06": "Vóc dáng Quả bóng đá",
  "Special07": "Vóc dáng Người tuyết",
  "Special08": "Vóc dáng Bánh Hamburger",
  "Special09": "Vóc dáng Kẹo mút",
  "Special10": "Vóc dáng Gấu trúc",
  "Special11": "Vóc dáng Bộ xương"
}
with open('translations/vi/ProgramMsg__Equipment__Body.msbt.json', 'w', encoding='utf-8') as f:
    json.dump(body, f, ensure_ascii=False, indent=2)

# 7. AccessoryMonocle
monocle = {
  "AccessoryEye05": "Bịt mắt một bên",
  "AccessoryEye05a": "Bịt mắt một bên (Trắng)"
}
with open('translations/vi/ProgramMsg__Equipment__AccessoryMonocle.msbt.json', 'w', encoding='utf-8') as f:
    json.dump(monocle, f, ensure_ascii=False, indent=2)

print('Translated 7 customization base files successfully!')
