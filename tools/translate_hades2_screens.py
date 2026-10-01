"""
Script dịch ScreenText.en.sjson (Giao diện HUD, Bàn thờ Tro Tàn, Vạc Thần, Cửa hàng Charon)
cho Hades II (Nintendo Switch).
Bảo tồn 100% control tag ({CN}, {SL}, {MR}, {ML}, {!Icons...}, {$...}).
"""
import os
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from hades2_sjson_helper import apply_translation_to_sjson, parse_sjson_entries

INPUT_FILE = "working/0100A00019DE0000_Hades2/raw_text/en/ScreenText.en.sjson"
OUTPUT_DIR = "translations/0100A00019DE0000_Hades2/Game/Text/en"
OUTPUT_FILE = f"{OUTPUT_DIR}/ScreenText.en.sjson"

TRANSLATIONS = {
    # ===== Nút bấm menu chung =====
    "Menu_Exit": {"DisplayName": "{CN} THOÁT"},
    "Menu_Close": {"DisplayName": "{CN} ĐÓNG"},
    "Menu_Continue": {"DisplayName": "{CN} TIẾP TỤC"},
    "Menu_NextCategory": {"DisplayName": "{MR} TIẾP"},
    "Menu_MoreContents": {"DisplayName": "{MR} THÊM..."},
    "Menu_PrevCategory": {"DisplayName": "{ML} TRƯỚC"},
    "Menu_FewerContents": {"DisplayName": "{ML} TRƯỚC"},
    "Menu_CloseSubmenu": {"DisplayName": "{CN} QUAY LẠI"},
    "Menu_Buy": {"DisplayName": "{SL} MUA"},
    "Menu_Rush": {"DisplayName": "{SL} THỦ"},
    "Menu_Order": {"DisplayName": "{SL} ĐẶT"},
    "Menu_Sell": {"DisplayName": "{SL} BÁN 1"},
    "Menu_SellAll": {"DisplayName": "{IP} BÁN TẤT"},
    "Menu_Exchange": {"DisplayName": "{SL} TÁI CHẾ"},
    "Menu_ExchangeAll": {"DisplayName": "{IP} TÁI CHẾ TẤT"},
    "Menu_Purge": {"DisplayName": "{SL} THANH TẨY"},
    "Menu_Unlock": {"DisplayName": "{SL} MỞ KHÓA"},
    "Menu_Plant": {"DisplayName": "{SL} GIEO"},
    "Menu_MultiPlant": {"DisplayName": "{IP} GIEO x{$TempTextData.PlantAmount}"},
    "Menu_Gift": {"DisplayName": "{SL} TẶNG"},
    "Menu_Pin": {"DisplayName": "{IP} GHIM"},
    "Menu_PinBoon_On": {"DisplayName": "{IP} THEO DÕI"},
    "Menu_PinBoon_Off": {"DisplayName": "{IP} BỎ THEO DÕI"},
    "Menu_SaveKeepsake": {"DisplayName": "{IP} ƯU TIÊN"},
    "Menu_UnSaveKeepsake": {"DisplayName": "{IP} BỎ ƯU TIÊN"},
    "Menu_TraitPin": {"DisplayName": "{SL} GHIM"},
    "Menu_TraitUnPin": {"DisplayName": "{SL} BỎ GHIM"},
    "Menu_BoonInfo": {"DisplayName": "{MX} ÂN HUỆ"},
    "Menu_TraitList": {"DisplayName": "{MX} LỄ VẬT"},
    "Menu_QuestLog": {"DisplayName": "{SL} NHẬN"},
    "Menu_Equip": {"DisplayName": "{SL} TRANG BỊ"},
    "Menu_ChangeAspect": {"DisplayName": "{SL} CHỌN"},
    "Menu_Unequip": {"DisplayName": "{SL} GỠ"},
    "Menu_Upgrade": {"DisplayName": "{SL} NÂNG CẤP"},
    "Menu_Info": {"DisplayName": "{MX} CHI TIẾT"},
    "Menu_OpenTraitTray": {"DisplayName": "{AT} ÂN HUỆ"},
    "Menu_Sort": {"DisplayName": "{MX} SẮP XẾP"},
    "Menu_CauldronUnlock": {"DisplayName": "{SL} THIÊU"},
    "Menu_CosmeticsUnlock": {"DisplayName": "{SL} DUYỆT"},
    "Menu_CosmeticsRemove": {"DisplayName": "{SL} GỠ"},
    "Menu_CosmeticsReAdd": {"DisplayName": "{SL} CHỌN"},
    "Menu_FamiliarCostumeUnlock": {"DisplayName": "{SL} BIẾN HÌNH"},
    "Menu_FamiliarCostumeReAdd": {"DisplayName": "{SL} ĐỔI"},
    "Menu_MusicPlayerPurchase": {"DisplayName": "{SL} MỞ KHÓA"},
    "Menu_MusicPlayerPlay": {"DisplayName": "{SL} TRÌNH DIỄN"},
    "Menu_MusicPlayerPause": {"DisplayName": "{SL} DỪNG"},
    "Menu_MusicPlayerShuffle": {"DisplayName": "{CF} NGẪU NHIÊN"},

    # ===== Độ hiếm Ân Huệ =====
    "Boon_Rare": {"DisplayName": "Hiếm"},
    "Boon_Epic": {"DisplayName": "Sử Thi"},
    "Boon_Heroic": {"DisplayName": "Anh Hùng"},
    "Boon_Legendary": {"DisplayName": "Huyền Thoại"},
    "Boon_Duo": {"DisplayName": "Song Tinh"},
    "Boon_Infusion": {"DisplayName": "Hòa Tan"},

    # ===== Chọn Ân Huệ =====
    "UpgradeChoiceMenu_Title": {"DisplayName": "Ân Huệ của {{GodName}}"},
    "UpgradeChoiceMenu_Artemis": {"DisplayName": "Ân Huệ của Artemis"},
    "UpgradeChoiceMenu_Chaos": {"DisplayName": "Ân Huệ của Chaos"},
    "UpgradeChoiceMenu_Dionysus": {"DisplayName": "Ân Huệ của Dionysus"},
    "UpgradeChoiceMenu_Athena": {"DisplayName": "Ân Huệ của Athena"},
    "UpgradeChoiceMenu_Hades": {"DisplayName": "Ân Huệ của Hades"},
    "StackUpgradeChoiceMenu_Title": {"DisplayName": "Quả Cầu Sức Mạnh"},
    "WeaponUpgradeChoiceMenu_Title": {"DisplayName": "Búa Daedalus"},
    "Boon_Select": {"DisplayName": "{SL} CHỌN"},
    "Boon_Sacrifice": {"DisplayName": "{SL} NHẬN"},
    "Boon_Upgrade": {"DisplayName": "{RY} NÂNG PHẩm"},
    "Boon_Upgrade_Count": {"DisplayName": "{$Keywords.Temp}{RY} NÂNG PHẨM{#StatFormat}\\[{$TempTextData.Amount}\\]"},
    "Boon_Reroll": {"DisplayName": "{RR} ĐỔI LẠI {#StatFormat}\\[-{$TempTextData.Amount}{!Icons.ReRoll}\\]"},

    # ===== Hestia =====
    "HestiaUpgrade": {"DisplayName": "Hestia", "Description": "Nữ Thần Lửa"},
    "HestiaUpgrade_FlavorText01": {"DisplayName": "từ chỗ ấm êm của lò sưởi, đến cơn thịnh nộ của ngọn lửa địa ngục."},
    "HestiaUpgrade_FlavorText02": {"DisplayName": "vị thần Olympus cả kín nhất, lão thành nhất, trong tim mang lửa."},
    "HestiaUpgrade_FlavorText03": {"DisplayName": "ngọn lửa của nàng mang đến ấm áp dịu dàng, hoặc hủy diệt tang thương."},
    "HestiaUpgrade_SacrificeBoon": {"DisplayName": "Lễ Vật Thiêu Đốt"},
    "HestiaUpgrade_SacrificeBoon_FlavorText": {"DisplayName": "hãy dâng lễ vật lên nữ thần của lò sưởi."},

    "Talent_Select": {"DisplayName": "{SL} CHỌN"},
    "Talent_Deselect": {"DisplayName": "{SL} GỠ"},
    "Spell_Select": {"DisplayName": "{SL} CHỌN"},

    # ===== Hồ Sơ Vũ Khí (Silver Pool) =====
    "WeaponUpgrade_FlavorText01": {"DisplayName": "nghệ nhân luôn ẩn dật, để tuyệt tác tự nói thay người."},
    "WeaponUpgrade_FlavorText02": {"DisplayName": "không thợ rèn tầm thường nào mài dũa được vũ khí đêm — chỉ người tài năng hơn cả thần linh mới làm được."},
    "WeaponUpgrade_FlavorText03": {"DisplayName": "kỹ năng vượt trội của ông với tư cách thợ thủ công và nhà phát minh đã được công nhận ngay cả khi qua đời."},
    "WeaponUpgradeScreen_Kills": {"DisplayName": "Kẻ Đã Bị Tiêu Diệt:"},
    "WeaponUpgradeScreen_Clears": {"DisplayName": "Đêm Đã Thắng:"},
    "WeaponUpgradeScreen_ClearTimeRecord_Underworld": {"DisplayName": "{!Icons.UnderworldIcon} Chiến Thắng Nhanh Nhất:"},
    "WeaponUpgradeScreen_ClearTimeRecord_Surface": {"DisplayName": "{!Icons.SurfaceIcon} Chiến Thắng Nhanh Nhất:"},
    "WeaponUpgradeScreen_ShrinePointRecord_Underworld": {"DisplayName": "{!Icons.UnderworldIcon} {!Icons.ShrinePoint}{#BoldFormatGraft}Nỗi Sợ{#Prev} Cao Nhất:"},
    "WeaponUpgradeScreen_ShrinePointRecord_Surface": {"DisplayName": "{!Icons.SurfaceIcon} {!Icons.ShrinePoint}{#BoldFormatGraft}Nỗi Sợ{#Prev} Cao Nhất:"},
    "StackUpgrade_FlavorText01": {"DisplayName": "từng hạt giống, như một giọt máu; vừa là sự sống, vừa là cái chết."},
    "StackUpgrade_FlavorText02": {"DisplayName": "dù mọc lên từ mặt đất hay từ âm phủ, giờ ai còn dám nói?"},
    "StackUpgrade_FlavorText03": {"DisplayName": "sức mạnh của hơi ấm mùa xuân; sức mạnh của bóng tối lòng đất."},
    "AdditionalTalentPointDisplay": {"DisplayName": "Điểm Tài Năng"},

    # ===== Danh Sách Định Mệnh (Quest) =====
    "UseQuestLog": {"DisplayName": "{I} Soi Sắc"},
    "QuestLogScreen_Title": {"DisplayName": "Danh Sách Định Mệnh"},
    "QuestLogScreen_Flavor": {"DisplayName": "“Cuộn Dệt Của Ba Mụ Định Mệnh Chắc Chắn Sẽ Thành Sự Thật”"},
    "QuestLogReward": {"DisplayName": "{#HighlightQuestReward}{#Prev}+{$TempTextData.Amount}{!TempTextData.Icon}"},
    "QuestLog_SelectHint": {"DisplayName": "Hãy Chọn Một Lời Tiên Tri"},
    "QuestLog_SelectHintAllClear": {"DisplayName": "\\n\\n Mọi Lời Tiên Tri Nhỏ Đã Hoàn Thành \\n\\n Cảm Ơn Ngươi Đã Giữ Vận Mệnh"},
    "QuestLog_ProgressCountIncomplete": {"DisplayName": "{!Icons.QuestProgressIncomplete} {$TempTextData.Current} {!Icons.SlashDark} {$TempTextData.Goal}"},
    "QuestLog_ProgressCountComplete": {"DisplayName": "{!Icons.QuestProgressComplete} {$TempTextData.Current} {!Icons.Slash} {$TempTextData.Goal}"},
    "QuestLog_QuestProgressIncomplete": {"DisplayName": "{!Icons.QuestProgressIncomplete}"},
    "QuestLog_QuestProgressComplete": {"DisplayName": "{!Icons.QuestProgressComplete}"},
    "QuestLog_QuestProgressRequirement": {"DisplayName": "{$TempTextData.Requirement}"},
    "QuestLog_QuestAdded": {"DisplayName": "Lời Tiên Tri Đã Báo..."},
    "QuestLog_QuestComplete": {"DisplayName": "Lời Tiên Tri Đã Thành!!"},

    # ===== Bảng Thử Thách =====
    "BountyBoard_StartChallenge": {"DisplayName": "{SL} BẮT ĐẦU"},
    "BountyBoard_RepeatChallenge": {"DisplayName": "{SL} LÀM LẠI"},
    "BountyBoard_ClearMessage": {"DisplayName": "đã thắng: {$TempTextData.ClearCount}        tốt nhất: {$TempTextData.BestClearTimeString}"},
    "BountyBoard_ClearMessageStreaks": {"DisplayName": "chuỗi hiện tại: {$TempTextData.CurrentStreak}        chuỗi dài nhất: {$TempTextData.BestStreak}"},
    "BountyBoard_ClearMessage_NonRepeatable": {"DisplayName": "đã thắng!!"},
    "BountyBoard_RandomWeapon": {"DisplayName": "Vũ Khí Ngẫu Nhiên"},
    "BountyBoard_RandomKeepsake": {"DisplayName": "Kỷ Vật Ngẫu Nhiên"},
    "BountyBoard_UnderworldRun": {"DisplayName": "Âm Phủ"},
    "BountyBoard_SurfaceRun": {"DisplayName": "Mặt Đất"},
    "BountyBoard_Reward": {"DisplayName": "{#HighlightFormatGraft}thưởng: {#Prev}{#LegendaryFormat}+{$TempTextData.Amount}{!TempTextData.Icon}"},
    "BountyBoard_RewardEarned": {"DisplayName": "{#HighlightFormatGraft}đã nhận thưởng"},

    # ===== Túi Đồ =====
    "InventoryScreen_Title": {"DisplayName": "Túi Thần"},
    "InventoryScreen_ResourceNotFound": {"DisplayName": "Chưa Có", "Description": "Ngươi vẫn chưa tìm thấy thứ này."},
    "InventoryScreen_GiftNotWanted": {"DisplayName": "Không Thích", "Description": "Dường như đây không phải món quà phù hợp."},
    "InventoryScreen_GiftNotAvailable": {"DisplayName": "Hết Rồi", "Description": "Sẽ tặng được nếu ngươi còn."},
    "InventoryScreen_SeedNotWanted": {"DisplayName": "Không Gieo Được", "Description": "Dường như đây không phải hạt giống phù hợp."},
    "InventoryScreen_SeedNotAvailable": {"DisplayName": "Chưa Có", "Description": "Hiện ngươi không có gì để gieo trồng."},
    "InventoryScreen_NoPinsHint": {"DisplayName": "Chưa ghim món Hoa Cúc nào. \\n\\n Nhấn {IP} trên công thức để theo dõi thứ ngươi cần."},
    "InventoryScreen_LineHistoryTab": {"DisplayName": "Lời Mới Nhất"},
    "InventoryScreen_ResourcesTab": {"DisplayName": "Nguyên Liệu"},
    "InventoryScreen_GiftsTab": {"DisplayName": "Quà Tặng"},
    "InventoryScreen_GardenTab": {"DisplayName": "Lâm Thạch"},
    "InventoryScreen_FishTab": {"DisplayName": "Cá"},
    "InventoryScreen_PinTab": {"DisplayName": "Hoa Cúc"},
    "InventoryScreen_RemovePin": {"DisplayName": "{IP} BỎ GHIM"},
    "InventoryScreen_UnknownDetails": {"DisplayName": "· ? ? ?"},

    # ===== Chợ Xương =====
    "MarketScreen_Hint": {"DisplayName": "nguyên liệu quý giá, đổi lấy xương cốt người chết"},
    "MarketScreen_FlavorText01": {"DisplayName": "xương người khuất vẫn giữ một loại sức mạnh nào đó, và một chút kiêu hãnh."},
    "MarketScreen_FlavorText02": {"DisplayName": "trong cõi người chết, có một thứ tiền tệ được coi trọng hơn tất cả."},
    "MarketScreen_FlavorText03": {"DisplayName": "người chết càng tồn tại lâu, càng trân trọng những gì còn sót của cuộc sống trần gian."},
    "Market_LimitedTimeOffer": {"DisplayName": "{!Icons.LimitedTimeOffer}"},
    "MarketScreen_Resources": {"DisplayName": "Chợ Nguyên Liệu"},
    "MarketScreen_Sell": {"DisplayName": "Đổi Xương"},
    "MarketScreen_Gifts": {"DisplayName": "Hàng Quý Hiếm"},
    "MarketScreen_Exchange": {"DisplayName": "Dịch Vụ Tái Chế"},
    "MarketScreen_BuyAmount": {"DisplayName": "x{$TempTextData.BuyAmount}"},
    "MarketScreen_SellAmount": {"DisplayName": "-1"},
    "MarketScreen_InventoryAmount": {"DisplayName": "{!Icons.InventoryIcon} x{$TempTextData.InventoryAmount}"},
    "MarketScreen_Cost": {"DisplayName": "{$TempTextData.CostAmount} {$TempTextData.CostIcon}"},
    "MarketScreen_CurrentAmountsHeader": {"DisplayName": "Ngươi Có"},
    "MarketScreen_BuyingHeader": {"DisplayName": "Giá Mua"},
    "MarketScreen_SellingHeader": {"DisplayName": "Giá Trị Đổi"},
    "MarketScreen_SellAllPrompt": {
        "DisplayName": "Xác Nhận Đổi",
        "Description": "Ngươi sẽ quyên góp {#BoldFormatGraft}{$TempTextData.SellAmount}{!TempTextData.SellResourceIcon} {#Prev}cho {$Keywords.Broker}. \\n\\n Đổi lại, ngươi nhận {#UpgradeFormat}+{$TempTextData.BuyAmount}{!TempTextData.BuyResourceIcon} {#Prev}. \\n\\n Mọi giao dịch là cuối cùng."
    },
    "MarketScreen_ConfirmSellAll": {"DisplayName": "Tiến Hành"},
    "MarketScreen_CancelSellAll": {"DisplayName": "Hủy"},

    # ===== Giao Dịch Công Bằng (Nemesis) =====
    "TradeScreen_Title": {"DisplayName": "Giao Dịch Công Bằng"},
    "TradeScreen_Subtitle": {"DisplayName": "hiện thân của báo ứng đảm bảo ai cũng nhận phần mình."},
    "TradeScreen_GiveHint": {"DisplayName": "ngươi đưa:"},
    "TradeScreen_GetHint": {"DisplayName": "ngươi nhận:"},
    "TradeScreen_CurrentMoney": {"DisplayName": "ngươi có: {#MoneyFormatBold}{$TempTextData.Amount}{!Icons.Currency}"},
    "TradeScreen_CurrentMoney_CantAfford": {"DisplayName": "ngươi có: {#MoneyFormatCantAffordBold}{$TempTextData.Amount}{!Icons.Currency}"},
    "TradeScreen_Accept": {"DisplayName": "{CF} ĐỒNG Ý"},
    "TradeScreen_Decline": {"DisplayName": "{CN} TỪ CHỐI"},
    "TradeScreen_TradeCost": {"DisplayName": "{$TooltipData.Cost} {$TooltipData.ResourceName}", "Description": "Một khoản {!Icons.Currency}, đổi lấy những gì {$Keywords.CharNemesis} có."},
    "TradeScreen_ResourceCost": {"DisplayName": "{$TooltipData.ResourceName} {#TooltipUpgradeFormat}({$TooltipData.Cost})"},
    "TradeScreen_DamageAmount": {"DisplayName": "{#AltPenaltyFormat}Miễn Phí Đánh", "Description": "Mời {$Keywords.CharNemesis} tung đòn mạnh nhất. Nàng sẽ gây {#AltPenaltyFormat}{$TooltipData.DamageAmount} {#Prev}sát thương."},

    "WeaponShopItemConfirm": {"DisplayName": "{SL} Khám Phá..."},

    # ===== Bàn thờ Tro Tàn (Arcana) =====
    "MetaUpgrade_Locked": {"DisplayName": "? ? ?"},
    "MetaUpgrade_CostPrefix": {"DisplayName": "Linh Hồn:"},
    "MetaUpgrade_Slash": {"DisplayName": " {!Icons.Slash}"},
    "MetaUpgrade_EquipAvailable": {"DisplayName": "Năng Lượng Chưa Khai Thác!"},
    "MetaUpgrade_CardUnlocksAvailable": {
        "DisplayName": "Hãy Lật Lá Bài!",
        "Description": "Ngươi có thể sử dụng {#BoldFormatGraft}Lá Bài Arcana{#Prev}. Mỗi lá kích hoạt giúp ngươi mạnh lên theo cách riêng.\\n\\n        Chọn lá {#BoldFormatGraft}Bài {#Prev}đã lật để mở khóa vĩnh viễn."
    },
    "MetaUpgradeEquip_CardUnlockBack": {"DisplayName": "Mở Khóa Bài"},
    "MetaUpgradeEquip_Proceed": {"DisplayName": "Vẫn Thoát"},
    "MetaUpgradeEquip_Back": {"DisplayName": "Dùng Thêm Bài"},
    "MetaUpgradeTable_UnableToEquip": {"DisplayName": "{#MemFormat}Đã Đạt Giới Hạn {#Prev}Dung Lượng Tâm Thức!"},
    "MetaUpgradeTable_UnableToEquip_Alt": {"DisplayName": "{#MemFormat}Đã Đạt Giới Hạn {#Prev}Dung Lượng Tâm Thức!"},
    "MetaUpgradeTable_UnableToEquip_Alt2": {"DisplayName": "Vượt Quá Giới Hạn!"},
    "MetaUpgrade_UpgradesAvailable": {
        "DisplayName": "{#BoldFormatGraft}Thông Tuệ {#Prev}Đã Mở!",
        "Description": "Giờ ngươi có thể dùng {!Icons.CardUpgradePoints} {#BoldFormatGraft}{$ResourceData.CardUpgradePoints.Name} {#Prev}để khai mở tiềm năng đầy đủ của từng {#BoldFormatGraft}Lá Bài Arcana{#Prev}. \\n\\n Tại {#BoldFormatGraft}Bàn Thờ{#Prev}, nhấn {CF} để chuyển sang {#BoldFormatGraft}Thông Tuệ{#Prev}."
    },
    "MetaUpgrade_UpgradesAvailable_Close": {"DisplayName": "Tiếp Tục"},
    "ElementalPrompt": {"DisplayName": "{#BoldFormatGraft}Nguyên Tố {#Prev}Đã Tiết Lộ!"},
    "ElementalPrompt_Close": {"DisplayName": "Tiếp Tục"},
    "MetaUpgrade_Ineligible": {"DisplayName": "-"},
    "MetaUpgrade_Equip": {"DisplayName": "{SL} KÍCH HOẠT"},
    "MetaUpgrade_Unequip": {"DisplayName": "{SL} TẮT"},
    "MetaUpgrade_Unlock": {"DisplayName": "{SL} MỞ KHÓA"},
    "MetaUpgradeMem_Upgrade": {"DisplayName": "{SL} MỞ RỘNG"},
    "MetaUpgradeCard_Upgrade": {"DisplayName": "{SL} CẢI TIẾN"},
    "MetaUpgradeCard_Inspect": {"DisplayName": "{IP} XEM"},
    "MetaUpgradeMem_UpgradeMode": {"DisplayName": "{CF} THÔNG TUỆ {#StatFormat}\\[{$TempTextData.Amount}{!Icons.CardUpgradePoints}\\]"},
    "MetaUpgrade_PrevLayout": {"DisplayName": "{PL} BỘ TRƯỚC"},
    "MetaUpgrade_NextLayout": {"DisplayName": "{NL} BỘ SAU"},
    "MetaUpgrade_SwapLayoutArt": {"DisplayName": "{IP} CHỦ ĐỀ"},
    "MetaUpgrade_SwapLayoutArtSelect": {"DisplayName": "{SL} CHỌN"},
    "MetaUpgradeMem_ExitUpgradeMode": {"DisplayName": "{CF} QUAY LẠI"},
    "MetaUpgradeMem_Exit": {"DisplayName": "{CN} THOÁT"},
    "MetaUpgrade_Hidden": {"DisplayName": "{#ItalicFormat}Mở lá kề bên để lộ lá này"},
    "MetaUpgrade_Pin": {"DisplayName": "{IP} HOA CÚC"},
    "MetaUpgrade_StartSwap": {"DisplayName": "{A3} BẮT ĐẦU ĐỔI"},
    "MetaUpgrade_EndSwap": {"DisplayName": "{A3} XÁC NHẬN ĐỔI"},
    "MetaUpgrade_CancelSwap": {"DisplayName": "{A3} HỦY ĐỔI"},
    "MetaUpgradeCardLimit_Upgrade": {"DisplayName": "Dung Lượng Tâm Thức Arcana"},
    "ElementalPrompt_Close": {"DisplayName": "Tiếp Tục"},

    # ===== Hồ Bạc (Vũ Khí) =====
    "UseWeaponShop": {"DisplayName": "{I} Xem"},
    "WeaponShopScreen_Title": {"DisplayName": "Hồ Bạc"},
    "WeaponShopUnlock": {"DisplayName": "VẬT PHẨM ĐÃ THỨC TỈNH"},
    "WeaponShopAspectUnlock": {"DisplayName": "HÌNH THÁI ĐÃ TIẾT LỘ"},
    "WeaponShop_Weapons": {"DisplayName": "Vũ Khí Màn Đêm"},
    "WeaponShop_StaffUpgrades": {"DisplayName": "Hình Thái Của Trượng Phù Thủy"},
    "WeaponShop_DaggerUpgrades": {"DisplayName": "Hình Thái Của Song Đao"},
    "WeaponShop_TorchUpgrades": {"DisplayName": "Hình Thái Của Lửa Âm"},
    "WeaponShop_AxeUpgrades": {"DisplayName": "Hình Thái Của Rìu Nguyệt"},
    "WeaponShop_LobUpgrades": {"DisplayName": "Hình Thái Của Đầu Lộn"},
    "WeaponShop_SuitUpgrades": {"DisplayName": "Hình Thái Của Áo Choàng Đen"},
    "WeaponShop_Tools": {"DisplayName": "Dụng Cụ Thu Hoạch"},
    "WeaponShop_ToolUpgrades": {"DisplayName": "Hoàn Thiện Dụng Cụ"},
    "WeaponShopScreen_Hint": {"DisplayName": "“Nhìn Sâu Vào Nội Tâm, Người Kế Vị Vũ Khí Màn Đêm”"},

    # ===== Codex =====
    "Codex_NextEntry": {"DisplayName": "{DN} Mục Sau"},
    "Codex_PrevEntry": {"DisplayName": "{UP} Mục Trước"},
    "Codex_NextChapter": {"DisplayName": "{MR} TIẾP"},
    "Codex_PrevChapter": {"DisplayName": "{ML} TRƯỚC"},

    # ===== Thông Tin Ân Huệ =====
    "BoonInfo_BulletPoint": {"DisplayName": "{!Icons.Bullet}{$TempTextData.TraitName}"},
    "BoonInfo_BulletPoint_NoTraitName": {"DisplayName": "{!Icons.Bullet}"},
    "BoonInfo_Requirements": {"DisplayName": "Yêu Cầu Hiến Dâng"},
    "BoonInfo_NoRequirements": {"DisplayName": "(Không Gì Đặc Biệt)"},
    "BoonInfo_OneOf_Singular": {"DisplayName": "Cái Sau:"},
    "BoonInfo_OneOf": {"DisplayName": "Một Trong:"},
    "BoonInfo_TwoOf": {"DisplayName": "Hai Trong:"},
    "BoonInfo_LinkedGod_Header": {"DisplayName": ""},
    "BoonInfo_LinkedGod_Boon": {"DisplayName": "{!Icons.Bullet}Bất Kỳ Ân Huệ Nào Của {$TempTextData.LinkedGod}"},
    "BoonInfo_CountRequirement": {"DisplayName": "{!Icons.Bullet}{$TempTextData.FinalKey}: {$TempTextData.Value}"},
    "BoonInfo_CountRequirementIcon": {"DisplayName": "{$TempTextData.Value}{!TempTextData.FinalKeyIcon}"},
    "BoonInfo_Elements": {"DisplayName": "Nguyên Tố:"},
    "BoonInfo_GodBoonRarities": {"DisplayName": "Độ Hiếm:"},
    "BoonInfo_HighestBaseElementCount": {"DisplayName": "{$TempTextData.Value}{!Icons.EarthNoTooltip}, {$TempTextData.Value}{!Icons.WaterNoTooltip}, {$TempTextData.Value}{!Icons.AirNoTooltip}, hoặc {$TempTextData.Value}{!Icons.FireNoTooltip}"},
    "BoonInfo_NoneOf": {"DisplayName": "Không Trong:"},
    "BoonInfo_PageNumber": {"DisplayName": "{$TempTextData.CurrentPageNum} {!Icons.Slash} {$TempTextData.NumPages}"},
    "BoonInfo_ShowTooltips": {"DisplayName": "{CF} XEM MẸO"},
    "BoonInfo_ShowRequirements": {"DisplayName": "{CF} XEM YÊU CẦU"},

    # ===== Hộp Kỷ Vật =====
    "AwardMenu_Title": {"DisplayName": "Kỷ Vật"},
    "AwardMenu_SubTitle": {"DisplayName": "“Ở Đây, Ngay Cả Tình Bạn Phàm Sinh Cũng Có Thể Bất Tử”"},
    "Keepsake_Level_1": {"DisplayName": "hạng   {!Icons.AwardRank1}"},
    "Keepsake_Level_2": {"DisplayName": "hạng   {!Icons.AwardRank2}"},
    "Keepsake_Level_3": {"DisplayName": "hạng   {!Icons.AwardRank3}"},
    "LegendaryKeepsake_Level_1": {"DisplayName": "hạng   {!Icons.LegendaryAwardRank1}"},
    "LegendaryKeepsake_Level_2": {"DisplayName": "hạng   {!Icons.LegendaryAwardRank2}"},
    "LegendaryKeepsake_Level_3": {"DisplayName": "hạng   {!Icons.LegendaryAwardRank3}"},
    "LegendaryKeepsake_Level_4": {"DisplayName": "hạng   {!Icons.LegendaryAwardRank4}"},
    "LegendaryKeepsake_Level_5": {"DisplayName": "hạng   {!Icons.LegendaryAwardRank5}"},
    "Keepsake_Level_Progress": {"DisplayName": "Thắng {#BoldFormatGraft}{$TempTextData.Chambers} {#Prev}{$Keywords.Encounter} với vật này để {#BoldFormatGraft}lên hạng{#Prev}!"},
    "Keepsake_Level_Progress_Few": {"DisplayName": "Thắng {#BoldFormatGraft}{$TempTextData.Chambers} {#Prev}{$Keywords.EncounterPlural} với vật này để {#BoldFormatGraft}lên hạng{#Prev}!"},
    "Keepsake_Level_Progress_Many": {"DisplayName": "Thắng {#BoldFormatGraft}{$TempTextData.Chambers} {#Prev}{$Keywords.EncounterPlural} với vật này để {#BoldFormatGraft}lên hạng{#Prev}!"},
    "Keepsake_Level_Progress_Other": {"DisplayName": "Thắng {#BoldFormatGraft}{$TempTextData.Chambers} {#Prev}{$Keywords.EncounterPlural} với vật này để {#BoldFormatGraft}lên hạng{#Prev}!"},
    "Keepsake_Level_Progress_Max": {"DisplayName": " "},
    "Equipped_Subtitle": {"DisplayName": "Đã Trang Bị!"},
    "Keepsake_Blocked_Subtitle": {"DisplayName": "Hết Hạn (Tạm Thời...)"},
    "NewTraitUnlocked_Subtitle": {"DisplayName": "{$TempTextData.Gift}"},

    # ===== Thống Kê =====
    "GameStats_Weapons": {"DisplayName": "Vũ Khí Màn Đêm"},
    "GameStats_Boons": {"DisplayName": "Ân Huệ Olympus"},
    "GameStats_WeaponUpgrades": {"DisplayName": "Nâng Cấp Búa"},
    "GameStats_Aspects": {"DisplayName": "Hình Thái Dự Phòng"},
    "GameStats_Keepsakes": {"DisplayName": "Kỷ Vật Đặc Biệt"},
    "GameStats_Missing": {"DisplayName": "--"},

    # ===== Lịch Sử Hành Trình =====
    "RunHistoryScreen_Title": {"DisplayName": "Ưu Kích Qua"},
    "RunHistoryScreen_RunName": {"DisplayName": "{$TempTextData.RouteName} Đêm {$TempTextData.RunNum}"},
    "RunHistoryScreen_Num": {"DisplayName": "Đêm"},
    "RunHistoryScreen_RouteF": {"DisplayName": "{!Icons.UnderworldIcon}"},
    "RunHistoryScreen_RouteN": {"DisplayName": "{!Icons.SurfaceIcon}"},
    "RunHistoryScreen_RouteBounty": {"DisplayName": "{!Icons.ChaosIcon}"},
    "RunHistoryScreen_RunErased": {"DisplayName": "{#LockedFormat}Mất Trong Thời Gian..."},
    "RunHistoryScreen_Cleared": {"DisplayName": "{#RunHistorySuccessFormat}Thắng!!"},
    "RunHistoryScreenResult_Erebus": {"DisplayName": "Thất bại tại {#RunHistoryFailureFormat}{$RoomSetData.F.BaseF.SaveProfileLocationText}{#Prev}"},
    "RunHistoryScreenResult_Oceanus": {"DisplayName": "Thất bại tại {#RunHistoryFailureFormat}{$RoomSetData.G.BaseG.SaveProfileLocationText}{#Prev}"},
    "RunHistoryScreenResult_Fields": {"DisplayName": "Thất bại tại {#RunHistoryFailureFormat}{$RoomSetData.H.BaseH.SaveProfileLocationText}{#Prev}"},
    "RunHistoryScreenResult_ClockworkTartarus": {"DisplayName": "Thất bại tại {#RunHistoryFailureFormat}{$RoomSetData.I.BaseI.SaveProfileLocationText}{#Prev}"},
    "RunHistoryScreenResult_Ephyra": {"DisplayName": "Thất bại tại {#RunHistoryFailureFormat}{$RoomSetData.N.BaseN.SaveProfileLocationText}{#Prev}"},
    "RunHistoryScreenResult_Thessaly": {"DisplayName": "Thất bại tại {#RunHistoryFailureFormat}{$RoomSetData.O.BaseO.SaveProfileLocationText}{#Prev}"},
    "RunHistoryScreenResult_Olympus": {"DisplayName": "Thất bại trên {#RunHistoryFailureFormat}{$RoomSetData.P.BaseP.SaveProfileLocationText}{#Prev}"},
    "RunHistoryScreenResult_Q": {"DisplayName": "Thất bại trên {#RunHistoryFailureFormat}{$RoomSetData.Q.BaseQ.SaveProfileLocationText}{#Prev}"},
    "RunHistoryScreenResult_Anomaly": {"DisplayName": "Thất bại tại {#RunHistoryFailureFormat}{$RoomSetData.Anomaly.BaseAnomaly.SaveProfileLocationText}{#Prev}"},
    "RunHistoryScreenResult_Secret": {"DisplayName": "Thất bại tại {#RunHistoryFailureFormat}{$RoomSetData.Chaos.BaseChaos.SaveProfileLocationText}{#Prev}"},
    "RunHistoryScreenResult_BountyFailed": {"DisplayName": "{#RunHistoryFailureFormat}Thất Bại"},
    "RunHistoryScreenResult_BountyCleared": {"DisplayName": "{#RunHistorySuccessFormat}Thắng!"},
    "RunHistoryScreenResult_UnknownFail": {"DisplayName": ""},
    "RunHistoryScreen_PackagedBounty": {"DisplayName": "- {$TooltipData.BountyName} -"},
    "RunHistoryScreen_Weapon": {"DisplayName": "Vũ Khí"},
    "RunHistoryScreen_Keepsake": {"DisplayName": "Kỷ Vật"},
    "RunHistoryScreen_KeepsakePlural": {"DisplayName": "Kỷ Vật"},
    "RunHistoryScreen_Assist": {"DisplayName": "Đồng Hành"},

    # ===== Màn hình thắng =====
    "RunClearScreen_Title": {"DisplayName": "V i c t o r y !"},
    "RunClearScreen_Title_Surface": {"DisplayName": "G l o r y !"},
    "RunClearScreen_EasyModeLevel": {"DisplayName": "{!Icons.EasyModeIcon}"},
    "RunClearScreen_ClearTime": {"DisplayName": "Thời Gian Thắng:"},
    "RunClearScreen_RunStats": {"DisplayName": "Thống Kê Hành Trình"},
    "RunClearScreen_ClearTimeRecord": {"DisplayName": "Nhanh Nhất:"},
    "RunClearScreen_ShrinePoints": {"DisplayName": "{!Icons.ShrinePoint} Đã Dùng:"},
    "RunClearScreen_ShrinePointsRecord": {"DisplayName": "{!Icons.ShrinePoint} Cao Nhất:"},
    "RunClearScreen_DamageDealt": {"DisplayName": "Sát Thương Gây Ra Nhiều Nhất"},
    "RunHistoryScreenResult_UnknownFail": {"DisplayName": ""},
    "RunClearScreen_DamageDealtAllies": {"DisplayName": "Đồng Đội"},
    "RunClearScreen_DamageTaken": {"DisplayName": "Sát Thương Chịu Nhiều Nhất"},
    "RunClearScreen_TotalClears": {"DisplayName": "Tổng Số Lần Thắng:"},
    "RunClearScreen_ClearStreak": {"DisplayName": "Chuỗi Hiện Tại:"},
    "RunClearScreen_ClearStreakRecord": {"DisplayName": "Chuỗi Dài Nhất:"},
    "RunClearScreen_NewRecord": {"DisplayName": "Kỷ Lục Mới!"},
    "RunClearScreen_Header_Weapon": {"DisplayName": "Vũ Khí"},
    "RunClearScreen_Header_Clears": {"DisplayName": "Lần Thắng"},
    "RunClearScreen_Header_RecordClearTime_Underworld": {"DisplayName": "{!Icons.UnderworldIcon}"},
    "RunClearScreen_Header_RecordShrinePoints_Underworld": {"DisplayName": "{!Icons.UnderworldFearIcon}"},
    "RunClearScreen_Header_RecordClearTime_Surface": {"DisplayName": "{!Icons.SurfaceIcon}"},
    "RunClearScreen_Header_RecordShrinePoints_Surface": {"DisplayName": "{!Icons.SurfaceFearIcon}"},

    # ===== Vũ khí biến hình =====
    "WeaponMorphedAttack": {"DisplayName": "Đòn Cừu"},
    "WeaponMorphedAttack_Pig": {"DisplayName": "Đợt Lợn"},
    "WeaponMorphedAttack_Rat": {"DisplayName": "Cào Chuột"},

    # ===== Thất bại / thành tựu =====
    "ClearRequiredTraitsZeus": {"DisplayName": "{!Icons.RunClearDotsLeft}Bàn Tay Zeus{!Icons.RunClearDotsRight}"},
    "ClearRequiredTraitsHera": {"DisplayName": "{!Icons.RunClearDotsLeft}Bàn Tay Hera{!Icons.RunClearDotsRight}"},
    "ClearRequiredTraitsPoseidon": {"DisplayName": "{!Icons.RunClearDotsLeft}Bàn Tay Poseidon{!Icons.RunClearDotsRight}"},
    "ClearRequiredTraitsApollo": {"DisplayName": "{!Icons.RunClearDotsLeft}Bàn Tay Apollo{!Icons.RunClearDotsRight}"},
    "ClearRequiredTraitsDemeter": {"DisplayName": "{!Icons.RunClearDotsLeft}Bàn Tay Demeter{!Icons.RunClearDotsRight}"},
    "ClearRequiredTraitsAphrodite": {"DisplayName": "{!Icons.RunClearDotsLeft}Bàn Tay Aphrodite{!Icons.RunClearDotsRight}"},
    "ClearRequiredTraitsHephaestus": {"DisplayName": "{!Icons.RunClearDotsLeft}Bàn Tay Hephaestus{!Icons.RunClearDotsRight}"},
    "ClearRequiredTraitsHestia": {"DisplayName": "{!Icons.RunClearDotsLeft}Bàn Tay Hestia{!Icons.RunClearDotsRight}"},
    "ClearRequiredTraitsHermes": {"DisplayName": "{!Icons.RunClearDotsLeft}Bàn Tay Hermes{!Icons.RunClearDotsRight}"},
    "ClearRequiredTraitsAres": {"DisplayName": "{!Icons.RunClearDotsLeft}Bàn Tay Ares{!Icons.RunClearDotsRight}"},
    "ClearRequiredTraitsChaos": {"DisplayName": "{!Icons.RunClearDotsLeft}Tác Nhân Hỗn Loạn{!Icons.RunClearDotsRight}"},
    "ClearFullHealth": {"DisplayName": "{!Icons.RunClearDotsLeft}Sức Khỏe Trọn Vẹn{!Icons.RunClearDotsRight}"},
    "ClearHighArmor": {"DisplayName": "{!Icons.RunClearDotsLeft}Giáp Dày{!Icons.RunClearDotsRight}"},
    "ClearHighMaxHealth": {"DisplayName": "{!Icons.RunClearDotsLeft}Da Dày Meat{!Icons.RunClearDotsRight}"},
    "ClearSynergyTraits": {"DisplayName": "{!Icons.RunClearDotsLeft}Cặp Đôi Hoàn Hảo{!Icons.RunClearDotsRight}"},
    "ClearLegendaryTraits": {"DisplayName": "{!Icons.RunClearDotsLeft}Niềm Tự Hào Olympus{!Icons.RunClearDotsRight}"},
    "ClearRequiredIntactArachneDress": {"DisplayName": "{!Icons.RunClearDotsLeft}Bảo Vụ Lụa{!Icons.RunClearDotsRight}"},
    "ClearNoOlympianBoons": {"DisplayName": "{!Icons.RunClearDotsLeft}Nữ Thần Không Thần{!Icons.RunClearDotsRight}"},
    "ClearHighSacrificeBoons": {"DisplayName": "{!Icons.RunClearDotsLeft}Bậc Thầy Hiến Tế{!Icons.RunClearDotsRight}"},
    "ClearHighMaxMana": {"DisplayName": "{!Icons.RunClearDotsLeft}Chủ Nhân Pháp Lực{!Icons.RunClearDotsRight}"},
    "ClearHighSpentLastStands": {"DisplayName": "{!Icons.RunClearDotsLeft}Kẻ Không Chết{!Icons.RunClearDotsRight}"},
    "ClearElementalTraits": {"DisplayName": "{!Icons.RunClearDotsLeft}Siêu Hòa Tan{!Icons.RunClearDotsRight}"},
    "ClearHighOlympianBoons": {"DisplayName": "{!Icons.RunClearDotsLeft}Họp Mặt Gia Đình{!Icons.RunClearDotsRight}"},
    "ClearNoNPCs": {"DisplayName": "{!Icons.RunClearDotsLeft}Không Đồng Đội{!Icons.RunClearDotsRight}"},
    "ClearHighFear": {"DisplayName": "{!Icons.RunClearDotsLeft}Đêm Kinh Hoàng{!Icons.RunClearDotsRight}"},
    "ClearRequiredIntactIcarusArmor": {"DisplayName": "{!Icons.RunClearDotsLeft}Tùy Chỉnh Riêng{!Icons.RunClearDotsRight}"},
    "ClearHighHammerCount": {"DisplayName": "{!Icons.RunClearDotsLeft}Kho Búa{!Icons.RunClearDotsRight}"},
    "ClearLowMetaUpgradeTraits": {"DisplayName": "{!Icons.RunClearDotsLeft}Cần Gì Arcana?{!Icons.RunClearDotsRight}"},
    "ClearHighMetaUpgradeTraits": {"DisplayName": "{!Icons.RunClearDotsLeft}Arcana Đầy Bàn{!Icons.RunClearDotsRight}"},

    # ===== Bàn Thờ Nỗi Sợ (Shrine / Oath) =====
    "UseOrSpecialShrineObject": {"DisplayName": "{I} Quỳ Lễ\\n {SI} Tôn Kính"},
    "ShrineIntro": {"DisplayName": "Lời Thề"},
    "ShrineScreen_BountyHeader": {"DisplayName": "{$Keywords.Bounties} ({$TempTextData.Completed} {!Icons.Slash} {$TempTextData.Total})"},
    "ShrineMenu_Flavor": {"DisplayName": "“Nỗi Sợ Healthy Giữ Thần Linh và Phàm Nhân Luôn Biết Tự Kiểm”"},
    "ShrineMenu_Info": {"DisplayName": "Thông Tin"},
    "ShrineScreen_NextRankPoints": {"DisplayName": "+{$TempTextData.NextRankPoints}{!Icons.ShrinePoint}"},
    "ShrineScreen_BountyShrinePoints": {"DisplayName": "{$TempTextData.RequiredShrinePoints}{!Icons.ShrinePoint}"},
    "ShrineScreen_RankMaxed": {"DisplayName": "TỐI ĐA"},
    "ShrineScreen_Activate": {"DisplayName": "{SL} KÍCH HOẠT"},
    "ShrineScreen_RankUp": {"DisplayName": "{SL} TĂNG"},
    "ShrineScreen_RankDown": {"DisplayName": "{RD} GIẢM"},
    "ShrineScreen_ResetAll": {"DisplayName": "{ML} ĐẶT LẠI"},
    "ShrineScreen_UpgradeMaxed": {"DisplayName": "tối đa"},
    "ShrineScreen_BountyProgress": {"DisplayName": "{#LockedFormat}Đã Thực Hiện: {#Prev}{#BoldFormat}{$TempTextData.Completed} {!Icons.Slash} {$TempTextData.Total}"},
    "ShrineScreen_ActivePoints": {"DisplayName": "{$GameState.SpentShrinePointsCache}{!Icons.ShrinePoint}"},
    "ShrineScreen_SkellyHeader": {"DisplayName": "Trở Thành {#VowScreenNightsChampion}Nhà Vô Địch Đêm{#Prev}!"},
    "ShrineScreen_SkellyHeader_Complete": {"DisplayName": "Chúng Ta Tôn Vinh {#VowScreenNightsChampion}Nhà Vô Địch Đêm{#Prev}!"},
    "ShrineScreen_SkellyStatueSurface_Incomplete": {"DisplayName": "Chinh Phục {#BoldFormatGraft}Mặt Đất {#Prev}— {#ShrineHighlightFormat}{$ActiveScreens.Shrine.NextSurfaceSkellyShrinePointGoal}{!Icons.ShrinePoint}"},
    "ShrineScreen_SkellyStatueSurface_Insufficient": {"DisplayName": "Chinh Phục {#BoldFormatGraft}Mặt Đất {#Prev}— {#ShrineHighlightInsufficientFormat}{$ActiveScreens.Shrine.NextSurfaceSkellyShrinePointGoal}{!Icons.ShrinePoint}"},
    "ShrineScreen_SkellyStatueSurface_Complete": {"DisplayName": ""},
    "ShrineScreen_SkellyStatueUnderworld_Incomplete": {"DisplayName": "Chinh Phục {#BoldFormatGraft}Âm Phủ {#Prev}— {#ShrineHighlightFormat}{$ActiveScreens.Shrine.NextUnderworldSkellyShrinePointGoal}{!Icons.ShrinePoint}"},
    "ShrineScreen_SkellyStatueUnderworld_Insufficient": {"DisplayName": "Chinh Phục {#BoldFormatGraft}Âm Phủ {#Prev}— {#ShrineHighlightInsufficientFormat}{$ActiveScreens.Shrine.NextUnderworldSkellyShrinePointGoal}{!Icons.ShrinePoint}"},
    "ShrineScreen_SkellyStatueUnderworld_Complete": {"DisplayName": ""},
    "ShrineScreen_NoBountyAvailable": {"DisplayName": "Ý Chí của Đêm đã viên mãn."},
    "ShrineScreen_NoBountyAvailable_CurrentWeapon": {"DisplayName": "Không có {$Keywords.Bounties} cho vũ khí hiện tại. Nhưng {$TempTextData.WeaponName} thì..."},
    "ShrineScreen_NoBountyAvailable_Staff": {"DisplayName": "Không có {$Keywords.Bounties} cho vũ khí hiện tại. Nhưng {$TempTextData.WeaponName} đang rung lên..."},
    "ShrineScreen_NoBountyAvailable_Dagger": {"DisplayName": "Không có {$Keywords.Bounties} cho vũ khí hiện tại. Nhưng {$TempTextData.WeaponName} đang sáng lên..."},
    "ShrineScreen_NoBountyAvailable_Torch": {"DisplayName": "Không có {$Keywords.Bounties} cho vũ khí hiện tại. Nhưng {$TempTextData.WeaponName} đang bùng cháy..."},
    "ShrineScreen_NoBountyAvailable_Axe": {"DisplayName": "Không có {$Keywords.Bounties} cho vũ khí hiện tại. Nhưng {$TempTextData.WeaponName} đang đói..."},
    "ShrineScreen_NoBountyAvailable_Lob": {"DisplayName": "Không có {$Keywords.Bounties} cho vũ khí hiện tại. Nhưng {$TempTextData.WeaponName} đang nhìn chằm chằm..."},
    "ShrineScreen_NoBountyAvailable_Suit": {"DisplayName": "Không có {$Keywords.Bounties} cho vũ khí hiện tại. Nhưng {$TempTextData.WeaponName} đang ngân vang..."},
    "ShrineScreen_BountyAvailable_ZeroPoints": {"DisplayName": "Kích hoạt Lời Thề để đánh dấu {$Keywords.Bounty}."},
    "ShrineScreen_BountyAvailable_BelowPoints": {"DisplayName": "Cần thêm {$Keywords.ShrinePoints} cho {$Keywords.Bounty} kế tiếp."},
    "ShrineScreen_BountyAvailable_ExactPoints": {"DisplayName": "{$Keywords.Bounty} đã đánh dấu. Thực hiện nó, và nhận thưởng từ Đêm."},
    "ShrineScreen_BountyAvailable_ExcessPoints1": {"DisplayName": "{$Keywords.Bounty} đã đánh dấu. {$Keywords.ShrinePoints} vượt yêu cầu."},
    "ShrineScreen_BountyAvailable_ExcessPoints2": {"DisplayName": "{$Keywords.Bounty} đã đánh dấu. {$Keywords.ShrinePoints} vượt yêu cầu khá nhiều."},
    "ShrineScreen_BountyAvailable_ExcessPoints3": {"DisplayName": "{$Keywords.Bounty} đã đánh dấu. {$Keywords.ShrinePoints} vượt yêu cầu, mà ngươi cũng chẳng quan tâm."},
    "ShrineScreen_BountyAvailable_MaxPoints": {"DisplayName": "{$Keywords.Bounty} đã đánh dấu. {$Keywords.ShrinePoints} chỉ dành cho kẻ yếu, ngươi nghĩ sao?"},

    # ===== Hồ Thanh Tẩy =====
    "UseTraitShop_Unlocked": {"DisplayName": "{I} Bán"},
    "UseTraitShop_Locked": {"DisplayName": "{I} {#UseTextDisabledFormat}Bán?"},
    "SellTrait_Title": {"DisplayName": "Hồ Thanh Tẩy"},
    "SellTraitPrefix": {"DisplayName": "Thanh Tẩy"},
    "SellTrait_Hint": {"DisplayName": "hy sinh ân huệ để đổi lấy {!Icons.Currency}."},
    "SellTrait_FlavorText01": {"DisplayName": "người ta có thể tự giải phóng khỏi ảnh hưởng mạnh mẽ nhất."},
    "SellTrait_FlavorText02": {"DisplayName": "ý chí của các vị thần Olympus rất mong manh, ở mức tốt nhất, trong âm phủ."},
    "SellTrait_FlavorText03": {"DisplayName": "món quà của thần linh đáng giá một số tiền kha khá ở cõi người chết."},
}


def translate_screens():
    print(">>> Đang dịch ScreenText.en.sjson...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Chỉ giữ key thực sự tồn tại trong file nguồn
    src_ids = set(parse_sjson_entries(content).keys())
    used = {k: v for k, v in TRANSLATIONS.items() if k in src_ids}
    skipped = sorted(set(TRANSLATIONS) - src_ids)
    if skipped:
        print(f"⚠ Bỏ {len(skipped)} key không tồn tại: {skipped[:10]}...")

    new_content = apply_translation_to_sjson(content, used)

    # Kiểm tra không có block 2 DisplayName
    from hades2_sjson_helper import _iter_text_blocks
    dup = 0
    for eid, full, body, *_ in _iter_text_blocks(new_content):
        if body.count('DisplayName') > 1:
            dup += 1
            print(f"  ❌ DUP DisplayName: {eid}")
    if dup:
        raise SystemExit(f"FAIL: {dup} block có duplicate DisplayName")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
        f.write(new_content)

    out_ids = set(parse_sjson_entries(new_content).keys())
    assert out_ids == src_ids, "Số entry thay đổi!"

    print(f"✅ Đã dịch {len(used)} chuỗi ScreenText (guồn {len(src_ids)} entry)")
    print(f"👉 Lưu tại: {OUTPUT_FILE}")


if __name__ == '__main__':
    translate_screens()
