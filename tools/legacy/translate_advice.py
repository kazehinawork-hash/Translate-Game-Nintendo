import json

with open('games/0100D2F00D5C0000_SwitchSports/source/raw_text_extracted/USen/ProgramMsg__Advice.msbt.json', 'r', encoding='utf-8') as f:
    advice = json.load(f)

# Translation dictionary / mappings for Advice
T = {
    'Passing': 'Chuyền bóng',
    'Avoid Crowds': 'Tránh đám đông',
    '\"Here!\"': '\"Bên này!\"',
    'Stamina': 'Thể lực',
    'Minimap': 'Bản đồ nhỏ',
    'Knockout': 'Hạ đo ván (Knockout)',
    'Free Practice': 'Luyện tập tự do',
    'Goal Area': 'Khu vực khung thành',
    'Diving Header': 'Bay người đánh đầu',
    'Dashing': 'Tăng tốc',
    'Curving the Ball': 'Sút bóng xoáy',
    'Camera Settings': 'Cài đặt Camera',
    'Kicking Tip': 'Mẹo sút bóng',
    'Last-Ditch Diving Header': 'Đánh đầu xả thân',
    'Diving Header Tip': 'Mẹo bay người đánh đầu',
    'Kicking Tip 1': 'Mẹo sút bóng 1',
    'Kicking Tip 2': 'Mẹo sút bóng 2',
    'Timing Is Critical': 'Thời điểm là then chốt',
    'Leg-Strap Mode: Dashing': 'Chế độ buộc chân: Tăng tốc',
    'Leg-Strap Mode: Kick Power': 'Chế độ buộc chân: Lực sút',
    'Managing Stamina': 'Quản lý thể lực',
    'How to Play in Leg-Strap Mode': 'Cách chơi Chế độ buộc chân',
    'Minimap Settings': 'Cài đặt bản đồ nhỏ',
    'Golden Ball': 'Bóng Vàng',
    'Wall Deflections': 'Đập bóng bật tường',
    'Improve Your Accuracy': 'Nâng cao độ chính xác',
    'Tips for Passing': 'Mẹo chuyền bóng',
    'Resetting the Camera': 'Căn chỉnh lại Camera',
    'Leg-Strap Mode: Moving with ': 'Chế độ buộc chân: Di chuyển bằng ',
    'Leg-Strap Mode: Auto Movement Setting': 'Chế độ buộc chân: Tự động di chuyển',
    'Camera Modes': 'Chế độ Camera',
    'Leg-Strap Mode: Kicking-Direction Arrow': 'Chế độ buộc chân: Mũi tên hướng sút',
    'Leg-Strap Mode: Swinging Your Leg': 'Chế độ buộc chân: Vung chân',
    'Leg-Strap Mode: Kicking Tips': 'Chế độ buộc chân: Mẹo sút',
    'Leg-Strap Mode: Adjust with the Stick': 'Chế độ buộc chân: Chỉnh bằng cần Stick',
    'Leg-Strap Mode: Curving': 'Chế độ buộc chân: Sút xoáy',
    'Overhead Kick': 'Ngả bàn đèn (Overhead Kick)',
    'Free-Practice Secret': 'Bí mật Luyện tập tự do',
    'How to Serve': 'Cách phát bóng',
    'How to Spike': 'Cách đập bóng',
    'Hitting Combinations': 'Phối hợp nhịp nhàng',
    'Flying Bump': 'Đệm bóng bay người',
    'Quick Spike': 'Đập bóng nhanh',
    'Use the Stick to Move': 'Dùng cần Stick để di chuyển',
    'Aim Your Spikes': 'Nhắm hướng đập bóng',
    'Watch Out for Blocks': 'Cảnh giác chắn bóng',
    'Block Out': 'Bóng chạm chắn ra ngoài',
    'Controlling Your Serve': 'Kiểm soát quả phát bóng',
    'Teamwork': 'Tinh thần đồng đội',
    'Positioning Against a Spike': 'Chọn vị trí đón cú đập',
    'Stagger Your Spikes': 'Đổi nhịp đập bóng',
    'Slide Attacks': 'Tấn công lao (Slide Attack)',
    'Rocket Serves': 'Cú phát bóng Tên Lửa (Rocket Serve)',
    'Blocking a Slide Attack': 'Chắn cú tấn công lao',
    'Using Quick Spikes 1': 'Tận dụng đập bóng nhanh 1',
    'Using Quick Spikes 2': 'Tận dụng đập bóng nhanh 2',
    'How to Make Shots': 'Cách đánh cầu',
    'Smashes': 'Cú đập Smash',
    'Drop Shots': 'Bỏ nhỏ (Drop Shot)',
    'Super Smashes': 'Siêu đập cầu (Super Smash)',
    'Ready Your Racket': 'Thủ sẵn vợt',
    'Correcting Your Racket\'s Position': 'Căn chỉnh lại góc vợt',
    'Help Your Opponent Miss': 'Khiến đối thủ đánh hỏng',
    'Returning Cleanly': 'Đánh trả bóng chuẩn xác',
    'Reset with a Drop Shot': 'Hãm nhịp bằng cú bỏ nhỏ',
    'Consecutive Super Smashes': 'Chuỗi đập cầu liên hoàn',
    'Close In': 'Áp sát cầu',
    'Defensive Underhand Shot': 'Đánh cầu thấp tay phòng thủ',
    'Offensive Overhead Shot': 'Đánh cầu cao tay tấn công',
    'Returning Low Shots': 'Đón những đường cầu thấp',
    'Advanced Returning Tactics': 'Chiến thuật phản đòn nâng cao',
    'Recalibrating Your Sword': 'Hiệu chuẩn lại kiếm',
    'Moving Left and Right': 'Di chuyển trái và phải',
    'Thrusting': 'Đòn đâm thẳng',
    'Guarding and Counterattacking': 'Đỡ đòn và phản công',
    'Tips for Guarding': 'Bí quyết thủ kiếm',
    'Twin Swords: Spinning Strike': 'Song kiếm: Đòn xoay kiếm',
    'Twin Swords: Twin Thrust': 'Song kiếm: Đòn song đâm',
    'Charge Sword: Timely Block': 'Kiếm tụ lực: Đỡ đòn chuẩn nhịp',
    'Charge Sword: Charge Strike': 'Kiếm tụ lực: Nhát chém tụ lực',
    'Charge Sword: Charge Thrust': 'Kiếm tụ lực: Đòn đâm tụ lực',
    'Get Good at Guarding': 'Thành thạo kỹ năng thủ',
    'Wild Swinging Won\'t Help': 'Đừng vung tay loạn xạ',
    'A Note on Guarding with Twin Swords': 'Lưu ý khi thủ Song Kiếm',
    'Timely Blocks with the Charge Sword': 'Đỡ đòn chuẩn nhịp Kiếm Tụ Lực',
    'Twin Swords: A Perk of the Form': 'Song kiếm: Lợi thế thế đứng',
    'Don\'t Forget the Player at the Net': 'Đừng quên tay vợt trên lưới',
    'Don\'t Just Return': 'Đừng chỉ trả bóng đơn thuần',
    'Steering the Ball Left or Right': 'Điều hướng bóng trái hay phải',
    'When Your Stamina Gets Low': 'Khi thể lực cạn kiệt',
    'Adding Topspin': 'Cú đánh xoáy lên (Topspin)',
    'Adding Backspin': 'Cú đánh xoáy lùi (Backspin)',
    'Using Spin Effectively': 'Tận dụng bóng xoáy hiệu quả',
    'How to Hit a Lob': 'Cách đánh bóng bổng (Lob)',
    'Three Types of Tennis Courts': 'Ba loại mặt sân Quần Vợt',
    'Hard Courts': 'Sân cứng',
    'Clay Courts': 'Sân đất nện',
    'Grass Courts': 'Sân cỏ',
    'Hitting the Ball Out': 'Đánh bóng ra ngoài sân',
    'Using Topspin': 'Tận dụng bóng xoáy lên',
    'Using Backspin': 'Tận dụng bóng xoáy lùi',
    'Using Lobs': 'Tận dụng cú đánh bổng',
    'Hook': 'Ném bóng xoáy (Hook)',
    'Adjust Your Position': 'Điều chỉnh vị trí đứng',
    'Aim Your Throw': 'Nhắm hướng ném',
    'In Case of Split...': 'Khi gặp thế khó (Split)...',
    'Zooming the Camera': 'Thu phóng góc nhìn',
    'Proper Bowling Form': 'Tư thế ném bowling chuẩn',
    'Before Bowling': 'Trước khi ném bóng',
    'Strike Score Bonus': 'Điểm thưởng Strike',
    'Spare Score Bonus': 'Điểm thưởng Spare',
    'Strike with a Hook': 'Cú Strike bằng bóng xoáy Hook',
    'More Spin at the Far End of the Lane': 'Độ xoáy tăng ở cuối đường ném',
    'Hitting with Backspin': 'Đánh bóng xoáy lùi Backspin',
    'Shooting Tip 1': 'Mẹo đánh bóng 1',
    'Shooting Tip 2': 'Mẹo đánh bóng 2',
    'Shooting Tip 3': 'Mẹo đánh bóng 3',
    'Practice Swings': 'Vung gậy tập thử',
    'Resetting Your Stance': 'Căn chỉnh lại thế đứng',
    'Rough and Bunker Effects 1': 'Ảnh hưởng của Rough và Bunker 1',
    'Rough and Bunker Effects 2': 'Ảnh hưởng của Rough và Bunker 2',
    'Putting Tips 1': 'Mẹo gạt bóng Putter 1',
    'Putting Tips 2': 'Mẹo gạt bóng Putter 2',
    'Putting Tips 3': 'Mẹo gạt bóng Putter 3',
    'Wind Direction': 'Hướng gió',
    'Wind Effects Can Vary': 'Ảnh hưởng của gió',
    'Using the Minimap and Shot Meter': 'Dùng bản đồ nhỏ và thanh đo lực',
    'Looking at Minimaps': 'Quan sát bản đồ nhỏ',
    'Shots from Low Terrain': 'Đánh bóng từ vùng đất thấp',
    'Shots from High Terrain': 'Đánh bóng từ vùng đất cao',
    'Changing Clubs': 'Đổi gậy đánh bóng',
    'Clubs to Reduce Rolling': 'Gậy hãm độ lăn của bóng',
    'Club Strengths and Weaknesses': 'Ưu và nhược điểm của các loại gậy',
    'Clubs for Adding Backspin': 'Gậy tạo độ xoáy lùi',
    'Strength of Backspin': 'Độ mạnh của cú xoáy lùi',
    'Curving Shots Intentionally': 'Chủ động đánh bóng lượn vòng',
    'Shots through Trees': 'Đánh bóng xuyên qua rặng cây',
    'Assist Setting': 'Cài đặt hỗ trợ đánh bóng',
    'Sporting Goods for Golf': 'Dụng cụ thể thao cho môn Golf',
    'Grab a Ball': 'Nhặt bóng',
    'Jump Shot': 'Cú nhảy ném rổ (Jump Shot)',
    'Shooting Tip': 'Mẹo ném bóng',
    'Money Ball': 'Bóng Thưởng (Money Ball)',
    'Perfect': 'Hoàn hảo!',
    'Driving': 'Đột phá (Drive)',
    'Driving Tip': 'Mẹo đột phá',
    'Dunking': 'Úp rổ (Dunk)',
    'Blocking': 'Chắn bóng (Block)',
    'Time\'s Running Out!': 'Thời gian sắp hết!',
    'Stealing the Ball': 'Cướp bóng (Steal)',
    'Five-Streak Battle Tips': 'Mẹo Chiến Tích 5 Cú Liên Hoàn',
    'Three-Point Contest Tips': 'Mẹo Thi Ném 3 Điểm',
    'Shooting-Contest Tips': 'Mẹo Thi đấu ném bóng',
    'Fake Out': 'Động tác giả (Fake Out)',
    'Chance to Steal!': 'Cơ hội cướp bóng!'
}

adv_vi = {}
for k, v in advice.items():
    if k.endswith('Title') or 'Title' in k:
        adv_vi[k] = T.get(v, v)
    else:
        s = v
        # Soccer
        if k == 'Soccer_000': s = 'Chuyền bóng cho đồng đội bằng cách sút trong khi\u000e\u0003\u0002\u0002 giữ \u000e\u0003\u0002!\nBóng sẽ bay thẳng về phía đồng đội theo hướng bạn vừa sút.'
        elif k == 'Soccer_001': s = 'Bạn sẽ có cơ hội đón bóng cao hơn nếu đứng một mình\ntại khu vực mà trái bóng chuẩn bị rơi xuống.'
        elif k == 'Soccer_002': s = 'Báo hiệu gọi đồng đội chuyền bóng bằng nút \u000e\u0003\u0002\u0002 Bên này!\u000e\u0003\u0002'
        elif k == 'Soccer_003': s = 'Bay người đánh đầu và tăng tốc đều tiêu tốn \u000e\u0003\u0002\u0002thể lực\u000e\u0003\u0002.\nHãy luôn để mắt tới thanh thể lực của bạn.'
        elif k == 'Soccer_004': s = 'Bạn có thể xem vị trí của tất cả cầu thủ trên bản đồ nhỏ\nở góc dưới cùng bên trái màn hình.'
        elif k == 'Soccer_005': s = 'Khi cách biệt chạm mốc 4 bàn, trận đấu sẽ kết thúc ngay\nđể tránh cách biệt quá lớn cho đội bị dẫn bàn.'
        elif k == 'Soccer_006': s = 'Thoải mái luyện các kỹ thuật đỉnh cao như Bay người đánh đầu\ntrong chế độ \u000e\u0003\u0002\u0001Luyện tập tự do\u000e\u0003\u0002!'
        elif k == 'Soccer_007': s = 'Khung thành sẽ mở rộng hơn trong Hiệp phụ, giúp việc\nghi bàn phân định thắng thua dễ dàng hơn.'
        elif k == 'Soccer_008': s = '\u000e\u0003\u0002\u0002Vung \u000e\u0003\u0002cả hai Joy-Con \u000e\u0003\u0002\u0002xuống cùng một lúc\u000e\u0003\u0002 để tung cú\nBay người đánh đầu! Cú đánh đầu này phát lực mạnh hơn sút thường.'
        elif k == 'Soccer_009': s = 'Tăng tốc bằng cách di chuyển \u000e\u0003\u0002\u0002trong khi giữ phím \u000e\u0003\u0002.\nNhưng hãy nhớ lưu ý thanh thể lực nhé.'
        elif k == 'Soccer_010': s = 'Nếu bạn sút bóng và \u000e\u0003\u0002\u0002xoay nhẹ cổ tay Joy-Con khi vung\u000e\u0003\u0002,\u000e\u0003\u0002\u0002 \u000e\u0003\u0002bóng sẽ lượn theo một đường cong tuyệt đẹp.'
        elif k == 'Soccer_011': s = 'Nếu muốn đảo chiều xoay camera, bạn có thể chỉnh tại\n\u000e\u0003\u0002\u0001Cài đặt người chơi \u000e\u0003\u0002trong mục \u000e\u0003\u0002\u0001Tùy chọn\u000e\u0003\u0002.'
        elif k == 'Soccer_012': s = 'Bạn có thể sút bóng bằng cách vung bất kỳ tay cầm Joy-Con nào.'
        elif k == 'Soccer_013': s = 'Bạn vẫn có thể đánh đầu xả thân ngay cả khi cạn thể lực, nhưng\nthể lực sẽ mất nhiều thời gian hơn để hồi phục sau đó.'
        elif k == 'Soccer_014': s = 'Góc chạm bóng quyết định quỹ đạo bay của trái bóng.\nHãy luyện tập cảm giác này trong các trận đấu.'
        elif k == 'Soccer_015': s = 'Bóng bay theo hướng vung của Joy-Con. Bạn có thể xem lại\ntrong mục \u000e\u0003\u0002\u0001Cách chơi \u000e\u0003\u0002tại \u000e\u0003\u0002\u0001Tùy chọn\u000e\u0003\u0002.'
        elif k == 'Soccer_016': s = 'Để sút bóng theo đường chéo, hãy hướng về màn hình và vung\nJoy-Con \u000e\u0003\u0002\u0002như thể đang vẽ một đường chéo\u000e\u0003\u0002.'
        elif k == 'Soccer_017': s = 'Hướng bóng bay phụ thuộc vào thời điểm chạm bóng.\nCàng chơi nhiều bạn sẽ càng cảm nhận nhịp bóng tốt hơn.'
        elif k == 'Soccer_018': s = 'Trong Chế độ buộc chân, bạn có thể tăng tốc bằng cách \u000e\u0003\u0002\u0002đánh\ntay như đang chạy bộ tại chỗ\u000e\u0003\u0002.'
        elif k == 'Soccer_019': s = 'Không thể đánh đầu trong Chế độ buộc chân.\nBù lại, các cú sút chân sẽ có uy lực và tốc độ khủng khiếp hơn.'
        elif k == 'Soccer_020': s = 'Khi gặp tình thế khó, hãy giữ sức và chờ đối thủ sơ hở.'
        elif k == 'Soccer_021': s = 'Xem thêm về Chế độ buộc chân trong \u000e\u0003\u0002\u0001Cách chơi \u000e\u0003\u0002tại \u000e\u0003\u0002\u0001Tùy chọn\u000e\u0003\u0002.'
        elif k == 'Soccer_022': s = 'Bản đồ nhỏ có 2 chế độ: Xoay và Cố định.\nBạn có thể đổi tại \u000e\u0003\u0002\u0001Cài đặt người chơi \u000e\u0003\u0002trong \u000e\u0003\u0002\u0001Tùy chọn\u000e\u0003\u0002.'
        elif k == 'Soccer_023': s = 'Ghi bàn bằng Bóng Vàng sẽ được tính ngay 2 điểm!\nCơ hội vàng để lội ngược dòng ngoạn mục.'
        elif k == 'Soccer_024': s = 'Thử sút đập bóng vào tường xem sao.\nBiết đâu bạn sẽ lừa bóng qua sau lưng đối thủ một cách bất ngờ?!'
        elif k == 'Soccer_025': s = 'Hãy thử sút bóng \u000e\u0003\u0002\u0002ngay khoảnh khắc bóng vừa chạm đất\u000e\u0003\u0002.'
        elif k == 'Soccer_026': s = 'Vung Joy-Con lên để chuyền bóng bổng.\nVung Joy-Con xuống để chuyền bóng sệt bám đất.'
        elif k == 'Soccer_027': s = 'Căn chỉnh lại góc nhìn camera bằng phím \u000e\u0003\u0002\u0002\u000e\u0003\u0002.\nHãy bấm nút này mỗi khi bạn mất dấu bóng.'
        elif k == 'Soccer_028': s = 'Dù nhân vật tự chạy trong Chế độ buộc chân, bạn vẫn\ncó thể dùng cần \u000e\u0003\u0002\u0002 \u000e\u0003\u0002để tự do di chuyển theo ý muốn.'
        elif k == 'Soccer_029': s = 'Bạn có thể tắt tự động di chuyển tại \u000e\u0003\u0002\u0001Cài đặt người chơi\u000e\u0003\u0002\ntrong mục \u000e\u0003\u0002\u0001Tùy chọn\u000e\u0003\u0002.'
        elif k == 'Soccer_030': s = 'Có 2 chế độ camera: Bình thường và Tự do. Bạn có thể\nchọn tại \u000e\u0003\u0002\u0001Cài đặt người chơi\u000e\u0003\u0002 trong mục \u000e\u0003\u0002\u0001Tùy chọn\u000e\u0003\u0002.'
        elif k == 'Soccer_031': s = 'Hãy để mắt tới \u000e\u0003\u0002\u0002mũi tên chỉ hướng\u000e\u0003\u0002. Nó cho biết hướng bóng\nsẽ bay đi khi bạn vung chân sút.'
        elif k == 'Soccer_032': s = 'Hướng sút đã được căn chỉnh tự động,\nvì vậy bạn chỉ cần vung chân thẳng về phía trước.'
        elif k == 'Soccer_033': s = 'Khi vung chân hãy đảm bảo \u000e\u0003\u0002\u0002nâng cao bắp đùi\u000e\u0003\u0002.\nJoy-Con có thể không nhận nếu bạn chỉ vẩy cổ chân.'
        elif k == 'Soccer_034': s = 'Để sút thẳng đối diện khung thành, hãy dùng \u000e\u0003\u0002\u0002 \u000e\u0003\u0002chỉnh vị trí\nsao cho bóng nằm giữa bạn và cầu môn.'
        elif k == 'Soccer_035': s = 'Để sút bóng xoáy trong Chế độ buộc chân, hãy vừa sút\nvừa \u000e\u0003\u0002\u0002gạt cần  sang cạnh của quả bóng\u000e\u0003\u0002.'
        elif k == 'Soccer_036': s = 'Vung Joy-Con xuống ở điểm nhảy cao nhất để tung cú ngả bàn đèn.\nChiêu này còn giúp bạn đón bóng ở tầm cao hơn bình thường.'
        elif k == 'Soccer_037': s = 'Nếu bạn tâng bóng 10 lần liên tiếp vào tường hoặc chuyền cho\nđồng đội mà không để bóng rơi chạm đất...'

        # Volleyball
        elif k == 'Volleyball_000': s = '\u000e\u0003\u0002\u0002Vung \u000e\u0003\u0002Joy-Con \u000e\u0003\u0002\u0002lên \u000e\u0003\u0002để tung bóng! Rồi \u000e\u0003\u0002\u0001vung xuống \u000e\u0003\u0002để phát bóng!'
        elif k == 'Volleyball_001': s = 'Bạn có thể chọn hướng đập bóng bằng cách vung Joy-Con\nxuống theo\u000e\u0003\u0002\u0002 hướng mà bạn muốn nhắm đến\u000e\u0003\u0002!'
        elif k == 'Volleyball_002': s = 'Tạo tiền đề cho một cú đập sấm sét bằng cách phối hợp\nchuỗi đệm, chuyền hai và đập bóng \"\u000e\u0003\u0002\u0002tuyệt vời\u000e\u0003\u0002\"!'
        elif k == 'Volleyball_003': s = 'Khi bóng ở xa ngoài tầm với, hãy \u000e\u0003\u0002\u0002vung nhanh\nJoy-Con \u000e\u0003\u0002để tung người cứu bóng (Flying Bump)!'
        elif k == 'Volleyball_004': s = 'Bạn có thể đập bóng nhanh bằng cách bật nhảy \u000e\u0003\u0002\u0002ngay trước khi\nđồng đội chuyền bóng lên\u000e\u0003\u0002!'
        elif k == 'Volleyball_005': s = 'Dùng cần \u000e\u0003\u0002\u0002 Stick \u000e\u0003\u0002để di chuyển trái/phải\nkhi chuẩn bị chắn bóng hoặc đệm bóng.'
        elif k == 'Volleyball_006': s = 'Đập bóng hướng vào\u000e\u0003\u0002\u0002 khoảng trống không có đối thủ\u000e\u0003\u0002\nđể đối phương không kịp chắn hoặc đỡ!'
        elif k == 'Volleyball_007': s = 'Bóng sẽ nảy ngược lại nếu bị đối thủ chắn trên lưới,\nhãy \u000e\u0003\u0002\u0002sẵn sàng vị trí \u000e\u0003\u0002để cứu bóng ngay lập tức.'
        elif k == 'Volleyball_008': s = 'Nếu bóng đập trúng tay chắn của đối phương\u000e\u0003\u0002\u0002 rồi rơi ra\nngoài sân\u000e\u0003\u0002, điểm số sẽ thuộc về bạn!'
        elif k == 'Volleyball_009': s = 'Điều khiển hướng và tầm xa của cú phát bóng bằng\n\u000e\u0003\u0002\u0002hướng và lực vung tay cầm \u000e\u0003\u0002Joy-Con.'
        elif k == 'Volleyball_010': s = 'Khi một người bật chắn để chặn cú đập của đối thủ, người\ncòn lại hãy \u000e\u0003\u0002\u0002sẵn sàng đệm bóng\u000e\u0003\u0002 để phản công chớp nhoáng.'
        elif k == 'Volleyball_011': s = 'Bạn có thể di chuyển qua lại khi chờ chắn hoặc đệm.\nHãy cố gắng \u000e\u0003\u0002\u0002đoán trước hướng \u000e\u0003\u0002cú đập của đối thủ.'
        elif k == 'Volleyball_013': s = '\u000e\u0003\u0002\u0002Đổi nhịp đập bóng \u000e\u0003\u0002lệch với nhịp chắn của đối thủ,\nbạn sẽ dễ dàng đưa bóng vào bất cứ góc nào bạn muốn!'
        elif k == 'Volleyball_014': s = 'Dùng cần \u000e\u0003\u0002\u0002 \u000e\u0003\u0002di chuyển ngang ngay sau khi đệm bóng.\nChiến thuật tấn công lao này khiến đối thủ không kịp trở tay.'
        elif k == 'Volleyball_015': s = 'Khi phát bóng, nếu bạn \u000e\u0003\u0002\u0002tung bóng \u000e\u0003\u0002\u000e\u0003\u0002\u0002thật cao\u000e\u0003\u0002,\u000e\u0003\u0002\u0002 rồi \u000e\u0003\u0002\u000e\u0003\u0002\u0002đập bóng\ntại đỉnh cao nhất\u000e\u0003\u0002, bạn sẽ tung ra Cú Phát Bóng Tên Lửa!'
        elif k == 'Volleyball_016': s = 'Nhanh chóng di chuyển đón đầu đối thủ chuẩn bị đập bóng\nbằng cách dùng \u000e\u0003\u0002\u0002\u000e\u0003\u0002 \u000e\u0003\u0002\u0002vào vị trí\u000e\u0003\u0002 để chắn bóng.'
        elif k == 'Volleyball_017': s = 'Nếu bạn bật nhảy trước khi tay chắn đối phương kịp áp sát,\nhọ sẽ rất khó lòng cản phá cú đập nhanh của bạn.'
        elif k == 'Volleyball_018': s = 'Đập nhanh đưa bóng đi chớp nhoáng nhưng lực nhẹ hơn, nếu đối thủ\nđã chờ sẵn để chắn thì một cú đập thường sẽ uy lực hơn.'

        # Badminton
        elif k == 'Badminton_000': s = 'Bạn có thể điều khiển hướng cầu bay bằng cách vung Joy-Con\ntheo \u000e\u0003\u0002\u0002hướng bạn muốn nhắm tới\u000e\u0003\u0002.'
        elif k == 'Badminton_001': s = 'Nếu đón cầu \u000e\u0003\u0002\u0002ở tầm cao nhất trên không\u000e\u0003\u0002,\nbạn sẽ tung ra cú đập Smash cực kỳ hiểm hóc khó đỡ.'
        elif k.startswith('Badminton_002'): s = 'Vung Joy-Con \u000e\u0003\u0002\u0002trong khi giữ phím  / \u000e\u0003\u0002\nđể thả một cú Bỏ Nhỏ rót ngay sát mép lưới!'
        elif k == 'Badminton_003': s = 'Nếu đón được một \u000e\u0003\u0002\u0002quả cầu bay chao đảo \u000e\u0003\u0002lơ lửng trên cao,\nbạn sẽ tung ra một cú Siêu Đập Cầu (Super Smash) bùng nổ!'
        elif k == 'Badminton_004': s = 'Nếu thủ sẵn vợt theo \u000e\u0003\u0002\u0002hướng cú đánh tiếp theo\u000e\u0003\u0002,\nnhân vật trong game sẽ tự động di chuyển đón đầu vị trí.'
        elif k == 'Badminton_005': s = 'Nếu thấy vị trí vợt bị lệch, hãy \u000e\u0003\u0002\u0002chĩa tay cầm\u000e\u0003\u0002 Joy-Con\n\u000e\u0003\u0002\u0002thẳng vào giữa màn hình \u000e\u0003\u0002và bấm nút .'
        elif k == 'Badminton_006': s = 'Điều hướng cầu hiểm hóc để buộc đối phương\n\u000e\u0003\u0002\u0002chạy khắp mặt sân \u000e\u0003\u0002cho tới khi họ đánh hỏng!'
        elif k == 'Badminton_007': s = 'Nếu cầu \u000e\u0003\u0002\u0002bay về bên phải bạn\u000e\u0003\u0002, hãy \u000e\u0003\u0002\u0002vung vợt bên phải\u000e\u0003\u0002 để đánh.\nNếu cầu \u000e\u0003\u0002\u0001bay về bên trái\u000e\u0003\u0002, hãy \u000e\u0003\u0002\u0001vung tay trái\u000e\u0003\u0002!'
        elif k == 'Badminton_008': s = 'Nếu liên tục bị đối thủ smash dồn ép, bạn có thể hãm nhịp\nbằng cách \u000e\u0003\u0002\u0002đáp trả lại bằng một cú Bỏ Nhỏ\u000e\u0003\u0002!'
        elif k == 'Badminton_009': s = 'Khi tung ra các cú \u000e\u0003\u0002\u0002Siêu Đập Cầu liên tiếp\u000e\u0003\u0002, tốc độ bay của\ntrái cầu sẽ càng lúc càng nhanh xé gió!'
        elif k == 'Badminton_010': s = 'Nếu đánh cầu \u000e\u0003\u0002\u0002khi ở khoảng cách quá xa tầm với\u000e\u0003\u0002,\ncú đánh trả sẽ bị chao đảo và tạo cơ hội cho đối phương.'
        elif k == 'Badminton_011': s = 'Cú vung vợt \u000e\u0003\u0002\u0002từ dưới lên trên \u000e\u0003\u0002rất hoàn hảo cho phòng thủ.\nNó giúp bạn cứu những quả cầu thấp sát đất trước khi rơi!'
        elif k == 'Badminton_012': s = 'Cú vung vợt \u000e\u0003\u0002\u0002từ trên xuống dưới \u000e\u0003\u0002rất tuyệt vời cho tấn công.\nĐập trả những quả cầu bổng trên cao một cách đầy uy lực!'
        elif k == 'Badminton_013': s = 'Nếu cầu ở tầm thấp mà bạn lại vung tay bổ từ trên xuống,\ncầu đánh trả sẽ bị chao đảo hỏng nhịp.'
        elif k == 'Badminton_014': s = 'Khi đã đánh chuẩn nhịp không bị chao đảo, hãy thử vung đón cầu\nsớm hơn một chút. Bạn có thể ghi điểm trước khi đối thủ kịp định thần!'

        # Chanbara
        elif k == 'Chanbara_000': s = 'Nếu thấy chuyển động kiếm bị lệch, hãy \u000e\u0003\u0002\u0002chĩa tay cầm\u000e\u0003\u0002 Joy-Con\n\u000e\u0003\u0002\u0002vào giữa màn hình\u000e\u0003\u0002 và bấm nút .'
        elif k == 'Chanbara_001': s = 'Bạn có thể di chuyển bằng cách \u000e\u0003\u0002\u0002nghiêng \u000e\u0003\u0002tay cầm Joy-Con\n\u000e\u0003\u0002\u0002sang trái hoặc phải\u000e\u0003\u0002 để tìm góc hở phòng thủ của đối thủ.'
        elif k == 'Chanbara_002': s = '\u000e\u0003\u0002\u0002Đâm mạnh \u000e\u0003\u0002Joy-Con \u000e\u0003\u0002\u0002thẳng về phía trước \u000e\u0003\u0002để tung Đòn Đâm Thẳng.\nĐối thủ sẽ bị đẩy lùi một khoảng cách rất xa.'
        elif k == 'Chanbara_003': s = 'Khi đỡ đòn thành công cú chém của đối thủ, hãy phản công chớp nhoáng\nngay khi họ còn đang bị choáng váng mất thăng bằng.'
        elif k == 'Chanbara_004': s = 'Giữ thế thủ sao cho thân kiếm của bạn\u000e\u0003\u0002\u0002 vuông góc \u000e\u0003\u0002với hướng chém của đối thủ.'
        elif k == 'Chanbara_005': s = 'Khi thanh năng lượng chiến đấu đạt tối đa, hãy vung cả 2 Joy-Con\n\u000e\u0003\u0002\u0002về cùng một hướng cùng lúc\u000e\u0003\u0002 để tung Đòn Xoay Song Kiếm!'
        elif k == 'Chanbara_006': s = 'Khi năng lượng đạt tối đa, hãy \u000e\u0003\u0002\u0002đâm cả 2 tay cầm \u000e\u0003\u0002\u000e\u0003\u0002\u0002thẳng\nvề phía trước cùng lúc\u000e\u0003\u0002 để thi triển Đòn Song Đâm!'
        elif k.startswith('Chanbara_007') or k.startswith('Chanbara_013'): s = 'Bấm phím đỡ đòn \u000e\u0003\u0002\u0002ngay sát khoảnh khắc \u000e\u0003\u0002đòn đánh của đối phương\n\u000e\u0003\u0002\u0002sắp chạm vào bạn\u000e\u0003\u0002 để Đỡ Đòn Chuẩn Nhịp! Đối thủ sẽ bị bật ngửa rất xa.'
        elif k.startswith('Chanbara_008'): s = 'Sau khi tích đầy năng lượng MAX bằng cách đỡ đòn, hãy vung Joy-Con\n\u000e\u0003\u0002\u0002trong khi giữ phím  /  \u000e\u0003\u0002để tung ra Nhát Chém Tụ Lực đầy uy lực.'
        elif k.startswith('Chanbara_009'): s = 'Khi năng lượng đạt MAX, đâm Joy-Con thẳng về phía trước\n\u000e\u0003\u0002\u0002trong khi giữ phím  /  \u000e\u0003\u0002để thi triển Đòn Đâm Tụ Lực.'
        elif k == 'Chanbara_010': s = 'Phòng thủ chuẩn xác là chìa khóa mở ra cơ hội phản công.\nAi làm chủ thế thủ người đó sẽ làm chủ võ đài Kiếm Đạo.'
        elif k == 'Chanbara_011': s = 'Vung Joy-Con loạn xạ sẽ chỉ tạo ra những đòn chém yếu ớt.\nHãy bình tĩnh đọc thế kiếm của đối thủ và ra đòn dứt khoát.'
        elif k == 'Chanbara_012': s = 'Nhiều người nghĩ có thể dùng một tay thủ và một tay chém cùng lúc,\nnhưng thực tế trong game không thể làm như vậy.'
        elif k == 'Chanbara_014': s = 'Thủ hai kiếm ở \u000e\u0003\u0002\u0002hai góc nghiêng khác nhau\u000e\u0003\u0002. Điều này khiến đối phương\nrất khó phán đoán bạn sắp chém hay thủ theo hướng nào.'

        # Tennis
        elif k == 'Tennis_000': s = 'Bạn điều khiển cả \u000e\u0003\u0002\u0002tay vợt đứng lưới lẫn tay vợt ở vạch cuối sân\u000e\u0003\u0002.\nPhối hợp nhuần nhuyễn cả hai là chìa khóa mở cánh cửa thắng lợi!'
        elif k == 'Tennis_001': s = 'Hãy cố gắng tối đa nhắm các cú đánh vào những góc sân\nxa tầm với của đối thủ.'
        elif k == 'Tennis_002': s = 'Hướng bóng bay được quyết định bởi \u000e\u0003\u0002\u0002thời điểm bạn vung vợt\u000e\u0003\u0002!\nHãy chú ý xem mình đang vung vợt hơi sớm hay hơi muộn một chút.'
        elif k == 'Tennis_004': s = 'Bào mòn thể lực đối phương bằng cách bắt họ phải chạy con thoi\nliên tục giữa hai góc sân. Ai đuối sức trước sẽ rơi vào thế hạ phong.'
        elif k == 'Tennis_005': s = 'Khi thể lực giảm sút, bạn rất dễ đánh ra những đường bóng lỏng lẻo.\nHãy đặc biệt cẩn trọng khi bước vào các loạt bóng giằng co dài.'
        elif k == 'Tennis_006': s = 'Một quả bóng lỏng lẻo của đối thủ chính là cơ hội cho bạn tung cú \u000e\u0003\u0002\u0002Smash\u000e\u0003\u0002.\nHãy tập trung và đập bóng kết liễu!'
        elif k == 'Tennis_007': s = 'Để đánh bóng xoáy lên (Topspin), hãy \u000e\u0003\u0002\u0002cuộn nhẹ cổ tay\nlên trên trái bóng \u000e\u0003\u0002ngay lúc chạm vợt.'
        elif k == 'Tennis_008': s = 'Để đánh bóng xoáy lùi (Backspin), hãy \u000e\u0003\u0002\u0002vẩy cổ tay miết\ntừ dưới lên \u000e\u0003\u0002ngay lúc chạm vợt.'
        elif k == 'Tennis_009': s = 'Xoáy lùi làm bóng liệng nhẹ. Xoáy lên làm tăng tốc độ bóng\nvà khiến bóng nảy vọt đi nhanh hơn sau khi chạm đất.'
        elif k == 'Tennis_010': s = '\u000e\u0003\u0002\u0002Vung \u000e\u0003\u0002Joy-Con \u000e\u0003\u0002\u0002từ dưới lên cao \u000e\u0003\u0002để tung ra cú đánh bóng bổng (Lob)\nvượt qua tầm với trên đầu đối phương!'
        elif k == 'Tennis_011': s = 'Bóng sẽ \u000e\u0003\u0002\u0002nảy \u000e\u0003\u0002và di chuyển rất khác biệt \u000e\u0003\u0002\u0002sau khi chạm đất \u000e\u0003\u0002tùy thuộc\nvào loại mặt sân mà bạn đang thi đấu.'
        elif k == 'Tennis_012': s = 'Sân cứng có màu hồng. Đây là \u000e\u0003\u0002\u0002mặt sân tiêu chuẩn\u000e\u0003\u0002, bóng nảy cao\nvà tốc độ bóng gần như không suy giảm sau khi nảy.'
        elif k == 'Tennis_013': s = 'Sân đất nện có màu nâu. Bóng sẽ chậm lại đáng kể sau khi chạm đất\nvà \u000e\u0003\u0002\u0002các loạt giằng co thường kéo dài hơn\u000e\u0003\u0002, đòi hỏi tính toán chiến thuật.'
        elif k == 'Tennis_014': s = 'Sân cỏ có màu xanh lá. Đây là sân \u000e\u0003\u0002\u0002khó duy trì bóng giằng co nhất\u000e\u0003\u0002\nvì bóng nảy rất thấp mà tốc độ lại lao đi vun vút.'
        elif k == 'Tennis_015': s = 'Nếu đánh bóng xoáy lùi khi bạn đang đứng sát lưới,\n\u000e\u0003\u0002\u0002bóng rất dễ bay ra ngoài sân (Out)\u000e\u0003\u0002. Hãy hết sức cẩn thận!'
        elif k == 'Tennis_016': s = 'Nếu tay vợt trên lưới đánh trả bằng cú xoáy lên cực mạnh,\nđối phương có thể sẽ hoàn toàn đứng chôn chân không kịp phản xạ!'
        elif k == 'Tennis_017': s = 'Khiến đối thủ khốn đốn bằng cách đánh bóng xoáy lùi\nvề hướng xa tầm với của họ.'
        elif k == 'Tennis_018': s = 'Khi bị đối thủ ép chạy mệt nhoài hụt hơi, đó chính là thời điểm\nhoàn hảo để bạn đánh một quả bóng bổng (Lob) câu giờ về lại vị trí.'

        # Bowling
        elif k == 'Bowling_000': s = '\u000e\u0003\u0002\u0002Xoay nhẹ cổ tay\u000e\u0003\u0002 Joy-Con \u000e\u0003\u0002\u0002khi vung ném \u000e\u0003\u0002để ném bóng xoáy Hook!\nBóng sẽ lượn vòng ngoạn mục trước khi lao vào húc đổ các pin.'
        elif k == 'Bowling_001': s = 'Dùng cần \u000e\u0003\u0002\u0002 Stick \u000e\u0003\u0002để di chuyển vị trí đứng\nđến góc ném thuận lợi nhất cho bạn.'
        elif k == 'Bowling_002': s = 'Dùng \u000e\u0003\u0002\u0002 và \u000e\u0003\u0002 để chỉnh hướng ném,\ngiúp căn góc ngắm vào các pin chuẩn xác hơn.'
        elif k == 'Bowling_003': s = 'Khi chỉ còn các pin đứng cách xa nhau, đó gọi là thế \u000e\u0003\u0002\u0002Split\u000e\u0003\u0002.\nHãy nhắm mép ngoài của một pin để nó văng sang húc đổ pin còn lại.'
        elif k == 'Bowling_004': s = 'Bấm phím \u000e\u0003\u0002\u0002 để phóng to góc nhìn\u000e\u0003\u0002. Rất hữu ích khi bạn\ncần quan sát kỹ chướng ngại vật ở các làn ném đặc biệt.'
        elif k == 'Bowling_005': s = '\u000e\u0003\u0002\u0002Sau khi chuẩn bị bóng trước ngực\u000e\u0003\u0002, hãy vung tay mô phỏng\nđộng tác ném bowling thực tế. Kỹ thuật cơ bản là quan trọng nhất!'
        elif k == 'Bowling_006': s = 'Cầm Joy-Con thẳng đứng với \u000e\u0003\u0002\u0002mặt trước hướng về phía bạn\u000e\u0003\u0002.'
        elif k == 'Bowling_007': s = 'Khi ném được Strike, bạn sẽ được \u000e\u0003\u0002\u0002cộng thêm điểm của cả\n2 lượt ném tiếp theo\u000e\u0003\u0002 vào điểm số của lượt ném 10 pin này.'
        elif k == 'Bowling_008': s = 'Khi ném được Spare, bạn sẽ được \u000e\u0003\u0002\u0002cộng thêm điểm của lượt\nném tiếp theo\u000e\u0003\u0002 vào điểm số của lượt ném 10 pin này.'
        elif k == 'Bowling_009': s = 'Để tối đa hóa cơ hội đạt Strike, hãy nhắm bóng xoáy vào \u000e\u0003\u0002\u0002khe giữa\npin trung tâm và pin bên cạnh\u000e\u0003\u0002 (Pocket).'
        elif k == 'Bowling_010': s = 'Đầu làn ném được bôi lớp sáp dày nên bóng ít xoáy hơn.\nKhi ném xoáy, hầu hết độ lượn vòng sẽ diễn ra ở cuối đường băng.'

        # Golf
        elif k == 'Golf_000': s = 'Chọn gậy \u000e\u0003\u0002\u0002kỹ thuật (wedge) \u000e\u0003\u0002hoặc gậy \u000e\u0003\u0002\u0002sắt (iron) \u000e\u0003\u0002và dừng vung tay\ngiữa chừng để tạo độ xoáy lùi (backspin) hãm bóng.'
        elif k == 'Golf_001': s = 'Vung tay như thể bạn đang đánh bóng bằng cạnh bên của Joy-Con.'
        elif k == 'Golf_002': s = 'Bí quyết đánh thẳng là \u000e\u0003\u0002\u0002không vặn cổ tay khỏi tư thế ban đầu\nkhi bạn vừa căn chỉnh thế đứng bằng nút \u000e\u0003\u0002.'
        elif k == 'Golf_003': s = 'Vung tay càng rộng, lực đánh càng mạnh.\nVung tay càng ngắn, lực đánh càng nhẹ.'
        elif k == 'Golf_004': s = '\u000e\u0003\u0002\u0002Vung gậy tập thử \u000e\u0003\u0002chính là bí quyết nâng cao trình độ.\nHãy tập vung vài lần để cảm nhận lực đánh lý tưởng của bạn.'
        elif k == 'Golf_005': s = 'Bạn sẽ tiến bộ vượt bậc nếu \u000e\u0003\u0002\u0002tạo thói quen \u000e\u0003\u0002căn chỉnh lại thế đứng\n\u000e\u0003\u0002\u0002bằng nút  \u000e\u0003\u0002bất cứ khi nào cần trước mỗi cú vung tập hay đánh thật!'
        elif k == 'Golf_006': s = 'Bóng dễ bị lượn cong hơn khi đánh từ vùng cỏ cao (rough) hoặc hố cát (bunker).\nHãy chú ý vung gậy thật thẳng.'
        elif k == 'Golf_007': s = 'Rất khó đánh bóng đi xa từ cỏ cao hoặc hố cát.\nHãy quan sát thanh đo lực trước khi vung gậy.'
        elif k == 'Golf_008': s = 'Khi gạt bóng (putt), \u000e\u0003\u0002\u0002khép sát hai cánh tay vào mạn sườn\u000e\u0003\u0002.\nViệc \u000e\u0003\u0002\u0002khóa cố định cổ tay khi vung\u000e\u0003\u0002 cũng giúp bạn kiểm soát lực gạt dễ dàng hơn.'
        elif k == 'Golf_009': s = 'Đôi khi bạn sẽ muốn ngắm green từ góc khác.\nBạn có thể đổi góc nhìn camera bằng nút \u000e\u0003\u0002\u0002\u000e\u0003\u0002.'
        elif k == 'Golf_010': s = 'Bấm nút \u000e\u0003\u0002\u0002\u000e\u0003\u0002 để hiện các đường đồng mức địa hình green.\nĐộ dốc thoải ảnh hưởng rất lớn đến hướng lăn của bóng.'
        elif k == 'Golf_011': s = 'Gió tác động lớn tới đường bay của bóng.\nHãy kiểm tra tốc độ và hướng gió trước khi phát bóng.'
        elif k == 'Golf_012': s = 'Bóng bay càng cao càng bị gió thổi bạt nhiều. Gậy kỹ thuật\nvà gậy sắt thường đưa bóng lên rất cao, hãy lưu ý hướng gió khi dùng.'
        elif k == 'Golf_013': s = 'Bạn có thể \u000e\u0003\u0002\u0002phóng to \u000e\u0003\u0002green trên bản đồ nhỏ bằng nút \u000e\u0003\u0002\u0002\u000e\u0003\u0002\nngay cả từ khoảng cách xa. Xác định vị trí lỗ cờ trước sẽ giúp ích cho chiến thuật.'
        elif k == 'Golf_014': s = 'Hãy để ý bản đồ nhỏ và thanh đo lực đều có những \u000e\u0003\u0002\u0002chấm trắng\u000e\u0003\u0002 tương ứng.\nBạn có thể dựa vào các chấm này để căn lực đánh chuẩn xác.'
        elif k == 'Golf_015': s = 'Chấm trắng chỉ dự đoán vị trí bóng rơi chạm đất ban đầu.\nHãy tính toán thêm \u000e\u0003\u0002\u0002độ lăn của bóng, hướng gió và độ cao địa hình\u000e\u0003\u0002 khi đánh.'
        elif k == 'Golf_016': s = 'Khi đánh bóng từ vùng đất thấp lên vùng đất cao,\nbóng sẽ rơi ngắn hơn khoảng cách hiển thị trên bản đồ nhỏ.'
        elif k == 'Golf_017': s = 'Khi đánh bóng từ vùng đất cao xuống vùng đất thấp,\nbóng sẽ bay xa hơn khoảng cách hiển thị trên bản đồ nhỏ.'
        elif k == 'Golf_018': s = 'Dùng phím \u000e\u0003\u0002\u0002\u000e\u0003\u0002 / \u000e\u0003\u0002\u0002\u000e\u0003\u0002 để đổi gậy golf.\nKhi đã thành thạo các loại gậy, bạn có thể tự chọn gậy theo ý mình.'
        elif k == 'Golf_019': s = 'Gậy kỹ thuật và gậy sắt đánh không quá xa, nhưng bóng\nsẽ ít bị lăn sau khi chạm đất. Chọn loại này khi cần nhắm đích chuẩn xác.'
        elif k == 'Golf_020': s = 'Đánh bóng từ hố cát bằng gậy Driver hay Spoon rất dễ bị xoáy lệch.\nHãy linh hoạt sử dụng đúng lúc gậy \u000e\u0003\u0002\u0002kỹ thuật (wedge) \u000e\u0003\u0002và \u000e\u0003\u0002\u0002sắt (iron)\u000e\u0003\u0002.'
        elif k == 'Golf_021': s = 'Bạn có thể tạo độ xoáy lùi bằng gậy \u000e\u0003\u0002\u0002kỹ thuật \u000e\u0003\u0002và \u000e\u0003\u0002\u0002sắt\u000e\u0003\u0002.\nGậy Driver và Spoon không thể tạo xoáy lùi.'
        elif k == 'Golf_022': s = 'Cú xoáy lùi mạnh nhất được tạo ra khi bạn \u000e\u0003\u0002\u0002vung mạnh\u000e\u0003\u0002\nvà hãm gậy dừng \u000e\u0003\u0002\u0002ngay phía dưới chân bạn\u000e\u0003\u0002.'
        elif k == 'Golf_023': s = 'Chướng ngại vật trên sân đôi khi đòi hỏi bạn phải đánh đường bóng cong.\nKhi đã quen đánh thẳng, bạn hãy thử chủ động uốn đường bóng xem sao.'
        elif k == 'Golf_024': s = 'Bóng đánh bằng gậy Driver hay Spoon thường bay thấp.\nBóng quệt vào tán lá cây sẽ làm giảm cự ly rất nhiều, hãy tránh ra nhé.'
        elif k == 'Golf_025': s = 'Bạn có thể bật tính năng \u000e\u0003\u0002\u0002Hỗ trợ \u000e\u0003\u0002trong \u000e\u0003\u0002\u0001Cài đặt người chơi \u000e\u0003\u0002mục \u000e\u0003\u0002\u0001Tùy chọn\u000e\u0003\u0002.\nTính năng này giúp người mới dễ ngắm và chỉ dùng được khi Chơi Tại Chỗ hoặc Cùng Bạn Bè.'
        elif k == 'Golf_026': s = 'Các mẫu gậy và bóng tùy chỉnh không làm thay đổi thông số\nnhưng mang lại diện mạo tuyệt đẹp. Bạn có thể mở khóa trong \u000e\u0003\u0002\u0001Chơi Toàn Cầu\u000e\u0003\u0002.'

        # Basketball
        elif k.startswith('Basketball_000'): s = 'Nhặt bóng bằng cách \u000e\u0003\u0002\u0002hạ thấp \u000e\u0003\u0002Joy-Con \u000e\u0003\u0002\u0002và bấm  / \u000e\u0003\u0002.\nHãy tạo cho mình nhịp điệu nhặt bóng và ném rổ liên tục.'
        elif k == 'Basketball_001': s = '\u000e\u0003\u0002\u0002Vung \u000e\u0003\u0002Joy-Con \u000e\u0003\u0002\u0002lên\u000e\u0003\u0002 và bật nhảy.\n\u000e\u0003\u0002\u0002Vẩy cổ tay thẳng về phía trước \u000e\u0003\u0002để ném rổ!'
        elif k == 'Basketball_002': s = 'Cú ném sẽ đi thẳng và chuẩn xác nếu bạn vẩy Joy-Con\n\u000e\u0003\u0002\u0002ngay tại đỉnh cú nhảy mà không làm vặn cổ tay sang trái hay phải\u000e\u0003\u0002.'
        elif k == 'Basketball_003': s = 'Trái \u000e\u0003\u0002\u0002Bóng Thưởng (Money Ball) sẽ mang lại thêm nhiều điểm số\u000e\u0003\u0002!'
        elif k == 'Basketball_004': s = 'Đạt điểm Hoàn hảo bằng cách \u000e\u0003\u0002\u0002ném toàn bộ bóng lọt rổ trong thời gian quy định\u000e\u0003\u0002.\nThời gian còn dư sẽ được quy đổi thành điểm thưởng khích lệ.'
        elif k == 'Basketball_005': s = '\u000e\u0003\u0002\u0002Vung Joy-Con lên xuống theo chiều dọc \u000e\u0003\u0002nhanh và liên tục\nđể nhồi bóng đột phá thẳng về phía bảng rổ.'
        elif k == 'Basketball_006': s = 'Đối thủ \u000e\u0003\u0002\u0002có thể cướp bóng\u000e\u0003\u0002 khi bạn nhồi bóng, nên thỉnh thoảng\nhãy \u000e\u0003\u0002\u0002dừng vung \u000e\u0003\u0002Joy-Con một nhịp để bảo vệ bóng.'
        elif k.startswith('Basketball_007'): s = 'Khi bạn bấm phím \u000e\u0003\u0002\u0002chạy \u000e\u0003\u0002và chữ \"Dunk\" hiện lên, thời cơ úp rổ đã tới!\nSau khi \u000e\u0003\u0002\u0002vung Joy-Con lên để bật nhảy\u000e\u0003\u0002, hãy \u000e\u0003\u0002\u0002gập mạnh tay cầm xuống\u000e\u0003\u0002 để úp rổ!'
        elif k == 'Basketball_008': s = 'Chặn cú ném của đối phương bằng cách \u000e\u0003\u0002\u0002vung Joy-Con lên \u000e\u0003\u0002bật nhảy\nkhớp đúng thời điểm đối thủ vừa nhảy lên ném bóng.'
        elif k == 'Basketball_009': s = 'Ném bóng trước khi còi mãn cuộc vang lên! Hãy chớp lấy cơ hội\nném rổ đến tận những giây tích tắc cuối cùng!'
        elif k == 'Basketball_010': s = 'Khi đồng đội đang ở vị trí trống trải, bấm \u000e\u0003\u0002\u0002 \u000e\u0003\u0002để chuyền bóng.\nHãy làm đối thủ bất ngờ bằng những đường chuyền nhanh như chớp.'
        elif k == 'Basketball_011': s = 'Gọi đồng đội chuyền bóng cho bạn bằng nút \u000e\u0003\u0002\u0002 Bên này!\u000e\u0003\u0002'
        elif k == 'Basketball_012': s = 'Khi đối thủ dẫn bóng áp sát bạn, hãy thử cướp bóng bằng cách\n\u000e\u0003\u0002\u0002nhanh tay vung mạnh \u000e\u0003\u0002Joy-Con.'
        elif k == 'Basketball_013': s = 'Không chỉ cần ném chuẩn, bạn còn phải để mắt tới \u000e\u0003\u0002\u0002chuyển động của\nngười chơi khác\u000e\u0003\u0002 để không bị bóng của họ va chạm làm hỏng cú ném.'
        elif k == 'Basketball_014': s = '\u000e\u0003\u0002\u0002Trái Bóng Thưởng đáng giá tới 3 điểm\u000e\u0003\u0002, hoàn hảo để bạn\nbứt phá điểm số tạo cách biệt an toàn trước đối thủ!'
        elif k == 'Basketball_015': s = 'Hoàn toàn có thể căn thời gian để bóng của bạn va vào bóng đối thủ\nvà phá hỏng cú ném của họ bằng cách \u000e\u0003\u0002\u0002nhảy ném cùng nhịp\u000e\u0003\u0002 với đối phương.'
        elif k == 'Basketball_018': s = 'Sau khi vào tư thế ném, bạn có thể \u000e\u0003\u0002\u0002chậm rãi nâng hạ Joy-Con \u000e\u0003\u0002lên xuống\nđể làm động tác giả nhử đối phương bật nhảy hớ hênh.'
        elif k == 'Basketball_020': s = 'Khi phòng thủ và có dòng \u000e\u0003\u0002\u0002Cơ hội cướp bóng!\u000e\u0003\u0002 hiện trên đầu,\nbạn có thể cướp bóng \u000e\u0003\u0002\u0002kể cả khi đối phương chưa nhồi bóng đột phá\u000e\u0003\u0002.'
        adv_vi[k] = s

with open('games/0100D2F00D5C0000_SwitchSports/translations/ProgramMsg__Advice.msbt.json', 'w', encoding='utf-8') as f:
    json.dump(adv_vi, f, ensure_ascii=False, indent=2)

print('Translated ProgramMsg__Advice.msbt.json successfully:', len(adv_vi))
