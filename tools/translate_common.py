import json

with open('working/extracted_texts/USen/ProgramMsg__Common.msbt.json', 'r', encoding='utf-8') as f:
    comm = json.load(f)

c_vi = {}
for k, v in comm.items():
    if k == 'UserSelect_Reward':
        c_vi[k] = 'Chọn người chơi để xem danh sách phần thưởng.'
    elif k == 'UserSelect_ChangeClothes':
        c_vi[k] = 'Chọn người chơi để tùy chỉnh ngoại hình.'
    elif k in ['UserSelect_Setting', 'UserSelect_Tutorial']:
        c_vi[k] = 'Chọn người chơi.'
    elif k == 'UserSelect_InviteNso':
        c_vi[k] = 'Người chơi nào muốn ghé thăm Nintendo eShop?'
    elif k.startswith('Order_'):
        num = k.split('_')[-1]
        c_vi[k] = f'Hạng {num}'
    elif k == 'RewardPointType_Tns_OnTheLine':
        c_vi[k] = 'Bóng chạm vạch chính xác'
    elif k == 'RewardPointType_Cha_FinalRound':
        c_vi[k] = 'Hiệp đấu chung cuộc!'
    elif k == 'RewardPointType_Cha_Guard':
        c_vi[k] = 'Chuyên gia phòng thủ'
    elif k == 'RewardPointType_Cha_Attack':
        c_vi[k] = 'Bậc thầy tấn công'
    elif k == 'RewardPointType_Cha_ReversalWin':
        c_vi[k] = 'Lội ngược dòng ngoạn mục'
    elif k == 'RewardPointType_Vol_Deuce':
        c_vi[k] = 'Thắng giằng co (Deuce)'
    elif k == 'RewardPointType_Vol_LongRally':
        c_vi[k] = 'Thưởng pha giằng co dài'
    elif k == 'RewardPointType_Vol_Combination':
        c_vi[k] = 'Thưởng phối hợp đồng đội'
    elif k == 'RewardPointType_Soc_Overtime':
        c_vi[k] = 'Bước vào hiệp phụ'
    elif k == 'RewardPointType_Soc_Mvp':
        c_vi[k] = 'Cầu thủ xuất sắc nhất (MVP)'
    elif k == 'RewardPointType_Soc_Knockout':
        c_vi[k] = 'Hạ đo ván (Knockout)!'
    elif k == 'RewardPointType_Bow_1Strike':
        c_vi[k] = 'Thưởng 1 Strike'
    elif k == 'RewardPointType_Bow_3Strikes':
        c_vi[k] = 'Thưởng cú đúp 3 Strike'
    elif k == 'RewardPointType_Bow_5Strikes':
        c_vi[k] = 'Thưởng chuỗi 5 Strike'
    elif k == 'RewardPointType_Bow_5Spares':
        c_vi[k] = 'Thưởng chuỗi 5 Spare'
    elif k == 'RewardPointType_Bow_SplitGet':
        c_vi[k] = 'Phá Split thành công'
    elif k == 'RewardPointType_Bow_100Points':
        c_vi[k] = 'Thưởng đạt trên 100 điểm'
    elif k == 'RewardPointType_Bow_200Points':
        c_vi[k] = 'Thưởng đạt trên 200 điểm'
    elif k == 'RewardPointType_Bow_Perfect':
        c_vi[k] = 'Trận đấu hoàn hảo (300 điểm)!'
    elif k == 'RewardPointType_Bow_1Strike_S':
        c_vi[k] = 'Thưởng 1 Strike (Đặc biệt)'
    elif k == 'RewardPointType_Bow_3Strikes_S':
        c_vi[k] = 'Thưởng 3 Strike (Đặc biệt)'
    elif k == 'RewardPointType_Bow_5Strikes_S':
        c_vi[k] = 'Thưởng 5 Strike (Đặc biệt)'
    elif k == 'RewardPointType_Bow_5Spares_S':
        c_vi[k] = 'Thưởng 5 Spare (Đặc biệt)'
    elif k == 'RewardPointType_Bow_SplitGet_S':
        c_vi[k] = 'Phá Split thành công (Đặc biệt)'
    elif k == 'RewardPointType_Bow_100Points_S':
        c_vi[k] = 'Thưởng trên 100 điểm (Đặc biệt)'
    elif k == 'RewardPointType_Bow_200Points_S':
        c_vi[k] = 'Thưởng trên 200 điểm (Đặc biệt)'
    elif k == 'RewardPointType_Bow_Perfect_S':
        c_vi[k] = 'Trận đấu hoàn hảo (Đặc biệt)!'
    elif k == 'RewardPointType_Glf_NiceShot':
        c_vi[k] = 'Thưởng cú đánh đẹp mắt'
    elif k == 'RewardPointType_Glf_1UnderPar':
        c_vi[k] = 'Thưởng âm 1 gậy (Under Par)'
    elif k == 'RewardPointType_Glf_2UnderPar':
        c_vi[k] = 'Thưởng âm 2 gậy (Under Par)'
    elif k == 'RewardPointType_Glf_3UnderPar':
        c_vi[k] = 'Thưởng âm 3 gậy (Under Par)'
    elif k == 'RewardPointType_Glf_Fairway':
        c_vi[k] = 'Tỷ lệ bóng trúng Fairway: 100%'
    elif k == 'RewardPointType_Glf_GreatApproach':
        c_vi[k] = 'Cú tiếp cận cờ xuất sắc'
    elif k == 'RewardPointType_Glf_HitPole':
        c_vi[k] = 'Bóng chạm trực tiếp vào cờ'
    elif k == 'RewardPointType_Glf_LongPutter':
        c_vi[k] = 'Thưởng cú gạt bóng xa'
    elif k == 'RewardPointType_Glf_ChipIn':
        c_vi[k] = 'Thưởng cú Chip-In'
    elif k == 'RewardPointType_Glf_HoleInOne':
        c_vi[k] = 'Hole in One!'
    elif k == 'RewardPointType_Glf_Eagle':
        c_vi[k] = 'Thưởng cú Eagle'
    elif k == 'RewardPointType_Glf_Par':
        c_vi[k] = 'Thưởng đạt điểm Par'
    elif k == 'RewardPointType_Glf_NearPin':
        c_vi[k] = 'Phân định thắng thua bằng Gần cờ nhất'
    elif k == 'RewardPointType_Glf_HitFlag':
        c_vi[k] = 'Thưởng bắn trúng lá cờ'
    elif k == 'RewardPointType_Glf_Albatross':
        c_vi[k] = 'Thưởng cú Albatross'
    elif k == 'RewardPointType_Bsk_3ThreePoint':
        c_vi[k] = 'Tay thiện xạ 3 điểm'
    elif k == 'RewardPointType_Bsk_5Assist':
        c_vi[k] = 'Vua kiến tạo'
    elif k == 'RewardPointType_Bsk_5Defence':
        c_vi[k] = 'Lá chắn thép'
    elif k == 'RewardPointType_Bsk_BuzzerBeater':
        c_vi[k] = 'Ghi điểm giây cuối (Buzzer Beater)'
    elif k == 'SpecialReward_WinHard_Volleyball':
        c_vi[k] = '【Bóng Chuyền】Đánh bại máy cấp "Cao thủ".'
    elif k == 'SpecialReward_WinHard_Badminton':
        c_vi[k] = '【Cầu Lông】Đánh bại máy cấp "Cao thủ".'
    elif k == 'SpecialReward_WinHard_Soccer':
        c_vi[k] = '【Bóng Đá】Đánh bại máy cấp "Cao thủ".'
    elif k == 'SpecialReward_WinHard_Chanbara':
        c_vi[k] = '【Kiếm Đạo】Đánh bại máy cấp "Cao thủ".'
    elif k == 'SpecialReward_WinHard_Tennis':
        c_vi[k] = '【Quần Vợt】Đánh bại máy cấp "Cao thủ".'
    elif k == 'SpecialReward_WinHard_Bowling':
        c_vi[k] = '【Bowling】Ghi trên 200 điểm.'
    elif k == 'SpecialReward_WinHard_Golf':
        c_vi[k] = '【Golf】Tổng điểm 18 lỗ đạt âm gậy (Under Par).'
    elif k == 'SpecialReward_WinHard_Basketball':
        c_vi[k] = '【Bóng Rổ】Đánh bại máy cấp "Cao thủ".'
    elif k == 'SpecialReward_LeagueA_Volleyball':
        c_vi[k] = '【Bóng Chuyền】Thăng lên Hạng A.'
    elif k == 'SpecialReward_LeagueA_Badminton':
        c_vi[k] = '【Cầu Lông】Thăng lên Hạng A.'
    elif k == 'SpecialReward_LeagueA_Soccer':
        c_vi[k] = '【Bóng Đá】Thăng lên Hạng A.'
    elif k == 'SpecialReward_LeagueA_Chanbara':
        c_vi[k] = '【Kiếm Đạo】Thăng lên Hạng A.'
    elif k == 'SpecialReward_LeagueA_Tennis':
        c_vi[k] = '【Quần Vợt】Thăng lên Hạng A.'
    elif k == 'SpecialReward_LeagueA_Bowling':
        c_vi[k] = '【Bowling】Thăng lên Hạng A.'
    elif k == 'SpecialReward_LeagueA_Golf':
        c_vi[k] = '【Golf】Thăng lên Hạng A.'
    elif k == 'SpecialReward_LeagueA_Basketball':
        c_vi[k] = '【Bóng Rổ】Thăng lên Hạng A.'
    elif k == 'SpecialReward_PlayNum_Volleyball':
        c_vi[k] = '【Bóng Chuyền】Đã chơi 15 trận.'
    elif k == 'SpecialReward_PlayNum_Badminton':
        c_vi[k] = '【Cầu Lông】Đã chơi 15 trận.'
    elif k == 'SpecialReward_PlayNum_Soccer':
        c_vi[k] = '【Bóng Đá】Đã chơi 15 trận.'
    elif k == 'SpecialReward_PlayNum_Chanbara':
        c_vi[k] = '【Kiếm Đạo】Đã chơi 15 trận.'
    elif k == 'SpecialReward_PlayNum_Tennis':
        c_vi[k] = '【Quần Vợt】Đã chơi 15 trận.'
    elif k == 'SpecialReward_PlayNum_Bowling':
        c_vi[k] = '【Bowling】Đã chơi 15 trận.'
    elif k == 'SpecialReward_PlayNum_Golf':
        c_vi[k] = '【Golf】Đã chơi 15 trận.'
    elif k == 'SpecialReward_PlayNum_Basketball':
        c_vi[k] = '【Bóng Rổ】Đã chơi 15 trận.'
    elif k == 'SpecialReward_OnlinePairPlay':
        c_vi[k] = 'Đã chơi cùng người khác 30 trận.'
    elif k == 'SpecialReward_PlayedBasketball':
        c_vi[k] = 'Đã chơi bóng rổ ít nhất một lần.'
    elif k == 'CpuLevel_Easy':
        c_vi[k] = 'Bình thường'
    elif k == 'CpuLevel_Normal':
        c_vi[k] = 'Mạnh'
    elif k == 'CpuLevel_Hard':
        c_vi[k] = 'Cao thủ'
    elif k.startswith('DominantHand_Name_') and k.endswith('_Left'):
        c_vi[k] = 'Tay trái / Chân trái' if 'Soccer' in k else 'Tay trái'
    elif k.startswith('DominantHand_Name_') and k.endswith('_Right'):
        c_vi[k] = 'Tay phải / Chân phải' if 'Soccer' in k else 'Tay phải'
    elif k in ['TableMode_MenuOffline', 'TableMode_MenuOnline', 'TableMode_MenuFriend']:
        c_vi[k] = 'Khi có từ 2 người chơi trở lên,\nbạn cần chơi ở chế độ TV.\n\nVui lòng gắn máy Nintendo Switch\nvào Dock cắm TV.'
    elif k == 'TableMode_Sports':
        c_vi[k] = 'Không thể chuyển sang chế độ để bàn lúc này.\n\nVui lòng cắm máy Nintendo Switch\nvào dock kết nối TV.'
    elif k == 'JoyconHold_Single':
        c_vi[k] = 'Chơi bằng 1 Joy-Con'
    elif k == 'JoyconHold_Dual':
        c_vi[k] = 'Chơi bằng 2 Joy-Con'
    elif k == 'JoyconHold_Others':
        c_vi[k] = 'Cách cầm tay cầm Joy-Con'
    elif k == 'JoyconHold_LegBand':
        c_vi[k] = 'Cầm Joy-Con (R)'
    elif k == 'ChanbaraWeaponDescription_OneSword':
        c_vi[k] = 'Kiểu đánh kiếm cơ bản, linh hoạt. Sở hữu\nlực chém thường uy lực nhất trong ba loại.'
    elif k == 'ChanbaraWeaponDescription_MagicSword':
        c_vi[k] = 'Tích lũy năng lượng khi đỡ đòn chuẩn xác,\nsau đó tung ra những Nhát Chém Tụ Lực cực mạnh.'
    elif k == 'ChanbaraWeaponDescription_TwoSword':
        c_vi[k] = 'Chiến đấu bằng song kiếm 2 tay. Nắm bắt thời cơ\ngiành thắng lợi bằng Đòn Xoay Song Kiếm!'
    elif k == 'Tutorial_Pause':
        c_vi[k] = 'Dừng phần hướng dẫn'
    elif k == 'FreePlay_Pause':
        c_vi[k] = 'Dừng luyện tập tự do'
    elif k == 'Penalty_B':
        c_vi[k] = 'Trận đấu trực tuyến lần trước đã không kết thúc bình thường.\nNếu tiếp tục tái diễn, bạn có thể bị tạm khóa chơi một thời gian.\n\nVui lòng kiểm tra lại đường truyền internet\nvà thử lại.'
    elif k == 'Penalty_C':
        c_vi[k] = 'Trận trực tuyến liên tục bị ngắt kết nối bất thường,\nbạn tạm thời không thể tham gia trận đấu mới.\nVui lòng kiểm tra kết nối mạng và thử lại sau ít phút.'
    elif k == 'Searching_MultiPlayer':
        c_vi[k] = 'Đang tìm kiếm các đối thủ...'
    elif k == 'Searching_SinglePlayer':
        c_vi[k] = 'Đang tìm kiếm đối thủ...'
    elif k == 'Searching1_MultiPlayer':
        c_vi[k] = 'Quá trình tìm đối thủ đang mất nhiều thời gian hơn dự kiến.\nVui lòng chờ thêm một chút...'
    elif k == 'Searching1_SinglePlayer':
        c_vi[k] = 'Quá trình tìm đối thủ đang mất chút thời gian.\nVui lòng chờ thêm giây lát...'
    elif k == 'Searching2_MultiPlayer':
        c_vi[k] = 'Vẫn đang tiếp tục tìm các đối thủ phù hợp.\nXin vui lòng kiên nhẫn đợi...'
    elif k == 'Searching2_SinglePlayer':
        c_vi[k] = 'Vẫn đang tiếp tục tìm đối thủ.\nXin vui lòng kiên nhẫn đợi...'
    elif k == 'Matched_MultiPlayer':
        c_vi[k] = 'Đã tìm thấy các đối thủ!'
    elif k == 'Matched_SinglePlayer':
        c_vi[k] = 'Đã tìm thấy đối thủ!'
    elif k == 'ModeControllerSelect_Attention_Default':
        c_vi[k] = 'Bạn không thể chơi Bóng Đá hoặc phong cách\nSong Kiếm trong Kiếm Đạo.'
    elif k == 'FriendHostWaiting_Result':
        c_vi[k] = 'Chủ phòng đang quyết định có chơi tiếp hay không'
    elif k == 'DlgPlayAgain_Soccer1vs1':
        c_vi[k] = 'Bóng Đá: 1 vs 1'
    elif k == 'DlgPlayAgain_Soccer4vs4':
        c_vi[k] = 'Bóng Đá: 4 vs 4'
    elif k == 'DlgPlayAgain_Badminton':
        c_vi[k] = 'Cầu Lông'
    elif k == 'DlgPlayAgain_Volleyball':
        c_vi[k] = 'Bóng Chuyền'
    elif k == 'DlgPlayAgain_BowlingSpecial':
        c_vi[k] = 'Bowling: Chướng ngại vật'
    elif k == 'DlgPlayAgain_Chanbara':
        c_vi[k] = 'Kiếm Đạo (Chambara)'
    elif k == 'DlgPlayAgain_Tennis':
        c_vi[k] = 'Quần Vợt (Tennis)'
    elif k == 'DlgPlayAgain_Golf':
        c_vi[k] = 'Golf'
    elif k == 'DlgPlayAgain_Basketball':
        c_vi[k] = 'Bóng Rổ'
    elif k == 'FriendTopMenu_Friend':
        c_vi[k] = 'Chơi Cùng Bạn Bè'
    elif k == 'FriendTopMenu_LAN':
        c_vi[k] = 'Chơi Qua Mạng LAN'
    else:
        c_vi[k] = v

with open('translations/vi/ProgramMsg__Common.msbt.json', 'w', encoding='utf-8') as f:
    json.dump(c_vi, f, ensure_ascii=False, indent=2)

print('Translated ProgramMsg__Common.msbt.json successfully:', len(c_vi), 'strings')
