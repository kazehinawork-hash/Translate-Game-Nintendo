import json

with open('games/0100D2F00D5C0000_SwitchSports/source/raw_text_extracted/USen/ProgramMsg__Menu.msbt.json', 'r', encoding='utf-8') as f:
    menu = json.load(f)

m_vi = {}
for k, v in menu.items():
    if k in ['MainMenuTitle_Online_Select1', 'MainMenuTitle_Informal_Select1', 'MainMenuTitle_Offline', 'MainMenuTitle_Friend']:
        m_vi[k] = 'Chọn một môn thể thao để chơi.'
    elif k in ['MainMenuTitle_Online_Select3', 'MainMenuTitle_Informal_Select3']:
        m_vi[k] = 'Chọn từ 1 đến 3 môn thể thao để chơi.'
    elif k == 'MainMenuFriendTitle_Friend':
        m_vi[k] = 'Chơi Cùng Bạn Bè'
    elif k == 'MainMenuFriendTitle_Lan':
        m_vi[k] = 'Chơi Qua Mạng LAN'
    elif k == 'PauseMenu_Continue' or k == 'PauseMenuFriendMatch_Continue' or k == 'PauseMenuTutorial_Continue':
        m_vi[k] = 'Tiếp tục'
    elif k == 'PauseMenu_Restart' or k == 'PauseMenuFriendMatch_Restart':
        m_vi[k] = 'Bắt đầu lại'
    elif k == 'PauseMenu_ChangeRule' or k == 'EndMenu_ChangeRule' or k == 'EndMenuFriendMatch_ChangeRule':
        m_vi[k] = 'Đổi cài đặt trận đấu'
    elif k == 'PauseMenu_Retire' or k == 'EndMenu_End' or k == 'PauseMenuFriendMatch_ChangeSports' or k == 'EndMenuFriendMatch_ChangeSports':
        m_vi[k] = 'Về chọn môn thể thao'
    elif k == 'EndMenu_Retry' or k == 'EndMenuFriendMatch_Retry':
        m_vi[k] = 'Chơi lại trận nữa'
    elif k == 'EndMenu_ChangeUser':
        m_vi[k] = 'Đổi người chơi'
    elif k == 'PauseMenuFriendMatch_ReturnToMatchmake' or k == 'EndMenuFriendMatch_ReturnToMatchmake':
        m_vi[k] = 'Tiếp nhận thành viên'
    elif k == 'PauseMenuTutorial_Retire':
        m_vi[k] = 'Dừng hướng dẫn'
    elif k == 'PauseMenuTutorial_RetireFreePlay':
        m_vi[k] = 'Dừng luyện tập tự do'
    elif k == 'RuleSelectPage_Title_Soccer':
        m_vi[k] = 'Chọn luật thi đấu.'
    elif k == 'RuleSelectPage_Button0_Soccer':
        m_vi[k] = 'Đấu 1 vs 1'
    elif k == 'RuleSelectDescription_Button0_Soccer':
        m_vi[k] = 'Thử thách kỹ năng solo sân cỏ.\nKiểm soát bóng điêu luyện và ghi bàn!'
    elif k == 'RuleSelectPage_Button1_Soccer':
        m_vi[k] = 'Đấu 4 vs 4'
    elif k == 'RuleSelectDescription_Button1_Soccer':
        m_vi[k] = 'Phối hợp đồng đội ăn ý là chìa khóa\nvàng dẫn đến chiến thắng!'
    elif k == 'RuleSelectPage_Button2_Soccer':
        m_vi[k] = 'Luyện tập tự do'
    elif k == 'RuleSelectDescription_Button2_Soccer':
        m_vi[k] = 'Chỉ có bạn và trái bóng tròn. Thỏa sức\ntập các cú sút bao lâu tùy thích.'
    elif k == 'RuleSelectPage_Button3_Soccer':
        m_vi[k] = 'Sút Luân Lưu'
    elif k == 'RuleSelectDescription_Button3_Soccer':
        m_vi[k] = 'Dùng chân sút bóng ghi bàn trong màn\nso tài luân lưu kịch tính 1 đấu 1!'
    elif k == 'RuleSelectPage_Title_SoccerPractice':
        m_vi[k] = 'Chọn kích thước sân bóng.'
    elif k == 'RuleSelectPage_Button0_SoccerPractice':
        m_vi[k] = 'Sân nhỏ'
    elif k == 'RuleSelectPage_Button1_SoccerPractice':
        m_vi[k] = 'Sân lớn'
    elif k == 'RuleSelectPage_Title_PlayerNum':
        m_vi[k] = 'Chọn số lượng người chơi.'
    elif k == 'RuleSelectPage_Button0_PlayerNum':
        m_vi[k] = '1 Người Chơi'
    elif k == 'RuleSelectPage_Button1_PlayerNum':
        m_vi[k] = '2 Người Chơi'
    elif k == 'RuleSelectPage_Button2_PlayerNum':
        m_vi[k] = '3 Người Chơi'
    elif k == 'RuleSelectPage_Button3_PlayerNum':
        m_vi[k] = '4 Người Chơi'
    elif k == 'RuleSelectPage_Title_BowlingType':
        m_vi[k] = 'Chọn thể loại đường ném.'
    elif k == 'RuleSelectPage_Button0_BowlingType' or k == 'RuleSelect_Rule_Bowling_Standard':
        m_vi[k] = 'Tiêu chuẩn'
    elif k == 'RuleSelectDescription_Button0_BowlingType':
        m_vi[k] = 'Bowling truyền thống cổ điển. Lăn bóng\nvà hạ gục các pin để giành điểm cao nhất!'
    elif k == 'RuleSelectPage_Button1_BowlingType' or k == 'RuleSelect_Rule_Bowling_Special':
        m_vi[k] = 'Chướng ngại vật'
    elif k == 'RuleSelectDescription_Button1_BowlingType':
        m_vi[k] = 'Vượt chướng ngại vật để làm đổ pin.\nĐường ném biến hóa liên tục mỗi lượt!'
    elif k in ['RuleSelectPage_Title_BowlingDifficulty', 'RuleSelectPage_Title_BowlingDifficultyFriend']:
        m_vi[k] = 'Chọn cấp độ khó.'
    elif k in ['RuleSelectPage_Button0_BowlingDifficulty', 'RuleSelectPage_Button0_BowlingDifficultyFriend']:
        m_vi[k] = 'Mới chơi'
    elif k in ['RuleSelectPage_Button1_BowlingDifficulty', 'RuleSelectPage_Button1_BowlingDifficultyFriend']:
        m_vi[k] = 'Trung cấp'
    elif k in ['RuleSelectPage_Button2_BowlingDifficulty', 'RuleSelectPage_Button2_BowlingDifficultyFriend']:
        m_vi[k] = 'Nâng cao'
    elif k == 'RuleSelectPage_Button3_BowlingDifficultyFriend':
        m_vi[k] = 'Chọn tự động'
    elif k in ['RuleSelectPage_Title_BowlingTeam', 'RuleSelectPage_Title_GolfTeam']:
        m_vi[k] = 'Chọn thể thức thi đấu.'
    elif k in ['RuleSelectPage_Button0_BowlingTeam', 'RuleSelectPage_Button0_GolfTeam']:
        m_vi[k] = 'Đấu cá nhân'
    elif k in ['RuleSelectPage_Button1_BowlingTeam', 'RuleSelectPage_Button1_GolfTeam']:
        m_vi[k] = 'Đấu đồng đội'
    elif k == 'RuleSelectPage_Title_BowlingAlternate':
        m_vi[k] = 'Chọn cách thức ném bóng.'
    elif k == 'RuleSelectPage_Button0_BowlingAlternate':
        m_vi[k] = 'Lần lượt từng người'
    elif k == 'RuleSelectDescription_Button0_BowlingAlternate':
        m_vi[k] = 'Thay phiên nhau ném bóng y hệt như\ntại sàn bowling thực tế ngoài đời.'
    elif k == 'RuleSelectPage_Button1_BowlingAlternate':
        m_vi[k] = 'Ném cùng lúc'
    elif k == 'RuleSelectDescription_Button1_BowlingAlternate_Team':
        m_vi[k] = 'Hai đội cùng ném một lúc, giúp trận đấu\ndiễn ra nhanh chóng và dồn dập.'
    elif k == 'RuleSelectDescription_Button1_BowlingAlternate_Individual':
        m_vi[k] = 'Tất cả cùng ném một lúc. Mỗi người\ncần một tay cầm Joy-Con riêng.'
    elif k == 'RuleSelectPage_Title_GolfHoleNum':
        m_vi[k] = 'Chọn số lượng lỗ golf.'
    elif k == 'RuleSelectPage_Button0_GolfHoleNum':
        m_vi[k] = '3 Lỗ'
    elif k == 'RuleSelectPage_Button1_GolfHoleNum':
        m_vi[k] = '9 Lỗ'
    elif k == 'RuleSelectPage_Button2_GolfHoleNum':
        m_vi[k] = '18 Lỗ'
    elif k in ['RuleSelectPage_Title_GolfCourseType', 'RuleSelectPage_Title_GolfCourse3Resort', 'RuleSelectPage_Title_GolfCourse3Classic', 'RuleSelectPage_Title_GolfCourse9']:
        m_vi[k] = 'Chọn sân golf.'
    elif k == 'RuleSelectPage_Button0_GolfCourseType':
        m_vi[k] = 'Khu nghỉ dưỡng (Resort)'
    elif k == 'RuleSelectDescription_Button0_GolfCourseType':
        m_vi[k] = 'Chọn Mới chơi, Trung cấp hoặc Nâng cao.\nSân golf tràn ngập không khí nhiệt đới.'
    elif k == 'RuleSelectPage_Button1_GolfCourseType':
        m_vi[k] = 'Cổ điển (Classic)'
    elif k == 'RuleSelectDescription_Button1_GolfCourseType':
        m_vi[k] = 'Chọn Mới chơi, Trung cấp hoặc Nâng cao.\nSân golf bao phủ bởi thảm cỏ xanh mướt mát.'
    elif k == 'RuleSelectPage_Button2_GolfCourseType':
        m_vi[k] = 'Đặc biệt (Special)'
    elif k == 'RuleSelectDescription_Button2_GolfCourseType':
        m_vi[k] = 'Sân dành riêng cho các tay golf cự phách.\nHãy thử sức khi bạn đã tự tin làm chủ đường bóng!'
    elif k == 'RuleSelectPage_Button3_GolfCourseType':
        m_vi[k] = 'Ngẫu nhiên'
    elif k == 'RuleSelectDescription_Button3_GolfCourseType':
        m_vi[k] = '3 lỗ được bốc ngẫu nhiên từ tất cả các sân.\nHãy sẵn sàng cho mọi thử thách bất ngờ!'
    elif k == 'RuleSelectPage_Button0_GolfCourse3Resort':
        m_vi[k] = 'Khu nghỉ dưỡng A'
    elif k == 'RuleSelectDescription_Button0_GolfCourse3Resort':
        m_vi[k] = 'Sân Nghỉ Dưỡng (Mới chơi): 3 Lỗ'
    elif k == 'RuleSelectPage_Button1_GolfCourse3Resort':
        m_vi[k] = 'Khu nghỉ dưỡng B'
    elif k == 'RuleSelectDescription_Button1_GolfCourse3Resort':
        m_vi[k] = 'Sân Nghỉ Dưỡng (Trung cấp): 3 Lỗ'
    elif k == 'RuleSelectPage_Button2_GolfCourse3Resort':
        m_vi[k] = 'Khu nghỉ dưỡng C'
    elif k == 'RuleSelectDescription_Button2_GolfCourse3Resort':
        m_vi[k] = 'Sân Nghỉ Dưỡng (Nâng cao): 3 Lỗ'
    elif k == 'RuleSelectPage_Button0_GolfCourse3Classic':
        m_vi[k] = 'Cổ điển A'
    elif k == 'RuleSelectDescription_Button0_GolfCourse3Classic':
        m_vi[k] = 'Sân Cổ Điển (Mới chơi): 3 Lỗ'
    elif k == 'RuleSelectPage_Button1_GolfCourse3Classic':
        m_vi[k] = 'Cổ điển B'
    elif k == 'RuleSelectDescription_Button1_GolfCourse3Classic':
        m_vi[k] = 'Sân Cổ Điển (Trung cấp): 3 Lỗ'
    elif k == 'RuleSelectPage_Button2_GolfCourse3Classic':
        m_vi[k] = 'Cổ điển C'
    elif k == 'RuleSelectDescription_Button2_GolfCourse3Classic':
        m_vi[k] = 'Sân Cổ Điển (Nâng cao): 3 Lỗ'
    elif k == 'RuleSelectPage_Button0_GolfCourse9':
        m_vi[k] = 'Khu nghỉ dưỡng'
    elif k == 'RuleSelectDescription_Button0_GolfCourse9':
        m_vi[k] = 'Sân Nghỉ Dưỡng: 9 Lỗ'
    elif k == 'RuleSelectPage_Button1_GolfCourse9':
        m_vi[k] = 'Cổ điển'
    elif k == 'RuleSelectDescription_Button1_GolfCourse9':
        m_vi[k] = 'Sân Cổ Điển: 9 Lỗ'
    elif k == 'RuleSelectPage_Button2_GolfCourse9':
        m_vi[k] = 'Ngẫu nhiên'
    elif k == 'RuleSelectDescription_Button2_GolfCourse9':
        m_vi[k] = 'Ngẫu nhiên tất cả các sân: 9 Lỗ'
    elif k == 'RuleSelect_Rule_Practice':
        m_vi[k] = 'Luyện tập tự do'
    elif k in ['RuleSelectDetail_Title_CpuLevel', 'RuleSelectDetail_Title_TennisSingle', 'RuleSelectDetail_Title_Tennis2', 'RuleSelectDetail_Title_Tennis3_4', 'RuleSelectDetail_Title_Friend_Soccer', 'RuleSelectDetail_Title_Friend_Volleyball']:
        m_vi[k] = 'Cài đặt trận đấu'
    elif k in ['RuleSelectDetail_Title_Team', 'RuleSelectDetail_Title_TeamAndCpuLevel', 'RuleSelectDetail_Title_ControllerShare']:
        m_vi[k] = 'Đội hình'
    elif k in ['RuleSelectDetail_Title_Friend_Bowling', 'RuleSelectDetail_Title_CpuSetting']:
        m_vi[k] = 'Cài đặt CPU'
    elif k == 'RuleSelectPage_Title_Basketball':
        m_vi[k] = 'Chọn luật thi đấu.'
    elif k == 'RuleSelectPage_Button0_Basketball':
        m_vi[k] = 'Đấu 2 vs 2'
    elif k == 'RuleSelectDescription_Button0_Basketball':
        m_vi[k] = 'Trận đấu 2 đấu 2. Phối hợp nhịp nhàng cùng\nđồng đội để vươn tới thắng lợi!'
    elif k == 'RuleSelectPage_Button1_Basketball':
        m_vi[k] = 'Thử Thách Ném 3 Điểm'
    elif k == 'RuleSelectDescription_Button1_Basketball':
        m_vi[k] = 'Rất thích hợp để luyện tay ném 3 điểm.\nHãy hướng tới chuỗi ném hoàn hảo!'
    elif k == 'RuleSelectPage_Button2_Basketball':
        m_vi[k] = 'Thi Ném 3 Điểm'
    elif k == 'RuleSelectDescription_Button2_Basketball':
        m_vi[k] = 'Cuộc thi ném rổ. Các đấu thủ tranh tài\nxem ai ném trúng nhiều quả 3 điểm nhất!'
    elif k == 'RuleSelectPage_Button3_Basketball':
        m_vi[k] = 'Chiến Tích 5 Cú Liên Hoàn'
    elif k == 'RuleSelectDescription_Button3_Basketball':
        m_vi[k] = 'Cuộc đấu tài ném rổ. Ai sẽ là người\nđầu tiên ném lọt lưới liên tiếp 5 quả!'
    elif k == 'UserSettingDescription_DeletePlayer':
        m_vi[k] = 'Xóa toàn bộ dữ liệu của người chơi này.'
    elif k == 'UserSettingDescription_Pro':
        m_vi[k] = 'Trong Giải Chuyên Nghiệp, thắng thua quyết định\nthứ hạng của bạn. Nếu tạm dừng chơi giải đấu,\nthứ hạng của bạn sẽ được giữ nguyên.'
    elif k == 'UserSettingDescription_CameraMode':
        m_vi[k] = 'Cài đặt này \u000e\u0000\u0003\u0002\u0000chỉ\u000e\u0000\u0003\u0002 áp dụng cho \u000e\u0000\u0003\u0002\u0000Chế độ hai tay\u000e\u0000\u0003\u0002.\nBình thường: Camera tự động bám theo bóng.\nTự do: Có thể tự do xoay chuyển góc nhìn camera.'
    elif k == 'UserSettingDescription_Camera':
        m_vi[k] = 'Cài đặt này \u000e\u0000\u0003\u0002\u0000chỉ\u000e\u0000\u0003\u0002 áp dụng cho \u000e\u0000\u0003\u0002\u0000Chế độ hai tay\u000e\u0000\u0003\u0002.\nChọn hướng xoay chuyển camera khi bạn gạt cần Stick.'
    elif k == 'UserSettingDescription_Emote':
        m_vi[k] = 'Đặt sang TẮT để ẩn tất cả các tem cảm xúc\n(bao gồm cả tem của chính bạn). Khi có 2 người cùng chơi,\ncài đặt này sẽ áp dụng cho cả hai.'
    elif k == 'UserSettingDescription_MiniMap':
        m_vi[k] = 'Xoay: Bản đồ nhỏ sẽ xoay theo hướng camera nhìn\nCố định: Bản đồ nhỏ luôn cố định hướng ban đầu'
    elif k == 'UserSettingDescription_SoccerFootMove':
        m_vi[k] = 'Cài đặt này chỉ áp dụng cho \u000e\u0000\u0003\u0002\u0000Chế độ dây buộc chân\u000e\u0000\u0003\u0002.\nKhi BẬT, nhân vật sẽ tự động di chuyển theo bóng.\nBạn cũng có thể dùng \u000e\u0000\u0003\u0002\u0000 \u000e\u0000\u0003\u0002để di chuyển tự do.'
    elif k == 'UserSettingDescription_GolfAssist':
        m_vi[k] = 'Cài đặt chỉ áp dụng cho \u000e\u0000\u0003\u0002\u0000Chơi Tại Chỗ \u000e\u0000\u0003\u0002và \u000e\u0000\u0003\u0002\u0000Chơi Cùng Bạn Bè\u000e\u0000\u0003\u0002.\nHỗ trợ đánh bóng là tính năng giúp người mới chơi\ncăn hướng bóng chính xác và dễ dàng hơn.'
    elif k == 'UserSettingDescription_Nickname':
        m_vi[k] = 'Khi TẮT cài đặt này trong Chơi Toàn Cầu, biệt danh\ncủa các đối thủ sẽ hiển thị là \"\u000e\u0000\u0003\u0002\u0000Người chơi\u000e\u0000\u0003\u0002\" và danh hiệu\nsẽ hiển thị là \"\u000e\u0000\u0003\u0002\u0000Trực tuyến\u000e\u0000\u0003\u0002\".'
    elif k == 'CharEdit_PlayerTitle_None':
        m_vi[k] = '\u000e\u0000\u0003\u0002\u0004[Không có]\u000e\u0000\u0003\u0002'
    elif k == 'CharEdit_GuestName_Default':
        m_vi[k] = 'Khách'
    elif k == 'CharEdit_Swkbd_Header':
        m_vi[k] = 'Nhập biệt danh của bạn.'
    elif k == 'CharEdit_Swkbd_Guide':
        m_vi[k] = 'Biệt danh'
    elif k == 'Friend_Swkbd_Header':
        m_vi[k] = 'Nhập mật khẩu gồm 4 chữ số.'
    elif k == 'Friend_RoomIdSwkbd_Header':
        m_vi[k] = 'Vui lòng nhập Mã phòng (Room ID).'
    elif k == 'Friend_RoomIdSwkbd_Guide':
        m_vi[k] = 'Mã phòng'
    elif k == 'Swkbd_Decide':
        m_vi[k] = 'OK'
    elif k == 'InitialGuidance_Type1':
        m_vi[k] = 'Chào mừng đến với Quảng trường Spocco!'
    elif k == 'InitialGuidance_Type2':
        m_vi[k] = 'Tranh tài ở nhiều môn thể thao phong phú cùng\ncác kỳ thủ từ khắp nơi trên thế giới.'
    elif k == 'InitialGuidance_Type3':
        m_vi[k] = 'Nhận điểm thưởng để mở khóa vô vàn trang phục,\nphụ kiện bắt mắt sau mỗi trận đấu!'
    elif k == 'InitialGuidance_Type4':
        m_vi[k] = 'Thỏa sức tùy biến phong cách của riêng bạn\nvà tận hưởng niềm vui thể thao bất tận!'
    elif k == 'InitialGuidance_Type5':
        m_vi[k] = 'Sẵn sàng ra sân chưa nào?\nHãy chọn ngay một môn thể thao nhé!'
    elif k == 'ModeSelect_OnlineButton_Start' or k == 'ModeSelect_OnlineButton_Continue':
        m_vi[k] = 'Bắt đầu'
    elif k in ['ModeSelect_FriendButton_Friend', 'ModeSelect_FriendMode_Friend']:
        m_vi[k] = 'Chơi Cùng Bạn Bè'
    elif k in ['ModeSelect_FriendButton_Lan', 'ModeSelect_FriendMode_Lan']:
        m_vi[k] = 'Chơi Mạng LAN'
    elif k == 'ModeSelect_FriendButtonSub_Friend':
        m_vi[k] = 'Giao lưu trực tuyến cùng bạn hữu phương xa!'
    elif k == 'ModeSelect_FriendButtonSub_Lan':
        m_vi[k] = 'Bấm  +  +  để Chơi Cùng Bạn Bè.'
    elif k == 'SelectedSportsConfirm_Random':
        m_vi[k] = 'Tìm đối thủ thi đấu môn ngẫu nhiên chứ?'
    elif k == 'SelectedSportsConfirm_SingleOpponentSports':
        m_vi[k] = 'Tìm đối thủ cho môn thi đấu đã chọn?'
    elif k == 'SelectedSportsConfirm_MultiOpponentSports':
        m_vi[k] = 'Tìm các đối thủ với danh sách môn đã chọn?'
    elif k == 'ColorSupport_On':
        m_vi[k] = 'Đang bật'
    elif k == 'ControllerShareConfirm_ByPlayer1':
        m_vi[k] = 'Vui lòng nhận lấy Joy-Con\ntừ Người chơi 1.'
    elif k == 'ControllerShareConfirm_ByPlayer2':
        m_vi[k] = 'Vui lòng nhận lấy Joy-Con\ntừ Người chơi 2.'
    elif k == 'ControllerShareConfirm_ByPlayer3':
        m_vi[k] = 'Vui lòng nhận lấy Joy-Con\ntừ Người chơi 3.'
    elif k == 'ControllerSelect_Title_Soccer':
        m_vi[k] = 'Chọn số lượng Dây Buộc Chân'
    elif k in ['ControllerSelect_Title_Bowling', 'ControllerSelect_Title_Golf', 'ControllerSelect_Title_Chanbara']:
        m_vi[k] = 'Chọn số lượng tay cầm Joy-Con'
    elif k == 'OtherUserSetting_Header_Header0':
        m_vi[k] = 'Cài đặt Bóng Đá'
    elif k == 'OtherUserSetting_Header_HeaderGolf':
        m_vi[k] = 'Cài đặt Golf'
    elif k == 'OtherUserSetting_Header_Header1':
        m_vi[k] = 'Cài đặt Tem Cảm Xúc'
    elif k == 'OtherUserSetting_Header_Header2':
        m_vi[k] = 'Hiển thị Biệt danh & Danh hiệu đối thủ'
    elif k == 'OtherUserSetting_Select_CameraMode':
        m_vi[k] = 'Chế độ Camera'
    elif k == 'OtherUserSetting_Select_VerticalCamera':
        m_vi[k] = 'Góc quay (Lên/Xuống)'
    elif k == 'OtherUserSetting_Select_HorizontalCamera':
        m_vi[k] = 'Góc quay (Trái/Phải)'
    elif k == 'OtherUserSetting_Select_MiniMap':
        m_vi[k] = 'Bản đồ nhỏ (Minimap)'
    elif k == 'OtherUserSetting_Select_SoccerFootMove':
        m_vi[k] = 'Tự động di chuyển'
    elif k == 'OtherUserSetting_Select_GolfAssist':
        m_vi[k] = 'Hỗ trợ đánh bóng'
    elif k in ['OtherUserSetting_Select_EmoteEnable', 'OtherUserSetting_Select_Nickname']:
        m_vi[k] = 'Hiển thị'
    elif k in ['OtherUserSetting_Select_Choice0_CameraMode', 'OtherUserSetting_Select_Choice0_VerticalCamera', 'OtherUserSetting_Select_Choice0_HorizontalCamera']:
        m_vi[k] = 'Bình thường'
    elif k == 'OtherUserSetting_Select_Choice0_MiniMap':
        m_vi[k] = 'Xoay'
    elif k in ['OtherUserSetting_Select_Choice0_SoccerFootMove', 'OtherUserSetting_Select_Choice0_EmoteEnable', 'OtherUserSetting_Select_Choice0_Nickname', 'OtherUserSetting_Select_Choice1_GolfAssist']:
        m_vi[k] = 'BẬT'
    elif k in ['OtherUserSetting_Select_Choice0_GolfAssist', 'OtherUserSetting_Select_Choice1_SoccerFootMove', 'OtherUserSetting_Select_Choice1_EmoteEnable', 'OtherUserSetting_Select_Choice1_Nickname']:
        m_vi[k] = 'TẮT'
    elif k == 'OtherUserSetting_Select_Choice1_CameraMode':
        m_vi[k] = 'Tự do'
    elif k in ['OtherUserSetting_Select_Choice1_VerticalCamera', 'OtherUserSetting_Select_Choice1_HorizontalCamera']:
        m_vi[k] = 'Đảo ngược'
    elif k == 'OtherUserSetting_Select_Choice1_MiniMap':
        m_vi[k] = 'Cố định'
    elif k == 'UpdateInfo_Content_Ver120':
        m_vi[k] = '・Bóng Đá nay đã hỗ trợ Chế độ dây buộc chân.\n・Thêm cấp Giải Chuyên Nghiệp mới: Hạng S và Hạng ∞.\n・Có thể vào Trận đấu Bạn bè bằng Mã phòng (Room ID).\n・Bổ sung kỹ thuật Tấn công lao cho môn Bóng Chuyền.'
    elif k == 'UpdateInfo_Content_Ver130':
        m_vi[k] = '・Đã bổ sung môn Golf.\n・Thêm tính năng Chơi qua mạng LAN.'
    elif k == 'UpdateInfo_Content_Ver120_130':
        m_vi[k] = '・Đã bổ sung môn Golf.\n・Bóng Đá nay đã hỗ trợ Chế độ dây buộc chân.\n・Thêm cấp Giải Chuyên Nghiệp mới: Hạng S và Hạng ∞.\n・Có thể vào Trận đấu Bạn bè bằng Mã phòng (Room ID).\n・Bổ sung kỹ thuật Tấn công lao cho môn Bóng Chuyền.\n・Thêm tính năng Chơi qua mạng LAN.'
    elif k == 'UpdateInfo_Content_Ver140':
        m_vi[k] = '・Đã thêm \u000e\u0000\u0003\u0002\u0000Vật phẩm mở lại\u000e\u0000\u0003\u0002 vào Chơi Toàn Cầu. Nếu thu thập đủ vật phẩm hiện có, bộ sưu tập bạn từng bỏ lỡ sẽ mở lại (mỗi tuần 1 lần).\n\n・Bổ sung nhiều \u000e\u0000\u0003\u0002\u0000vật phẩm đặc biệt\u000e\u0000\u0003\u0002. Bạn có thể mở khóa khi đạt đủ các điều kiện thử thách.'
    elif k == 'UpdateInfo_Content_Ver150':
        m_vi[k] = '・Đã bổ sung môn Bóng Rổ.'
    else:
        m_vi[k] = v

with open('games/0100D2F00D5C0000_SwitchSports/translations/ProgramMsg__Menu.msbt.json', 'w', encoding='utf-8') as f:
    json.dump(m_vi, f, ensure_ascii=False, indent=2)

print('Translated ProgramMsg__Menu.msbt.json successfully:', len(m_vi), 'strings')
