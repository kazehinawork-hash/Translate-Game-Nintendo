"""
Script dịch ShellText.en.sjson (Menu chính, Cài đặt, Điều khiển, Hồ sơ lưu game)
cho Hades II (Nintendo Switch).
Bản dịch tự nhiên, chuẩn game thủ, không dịch máy móc.
"""
import os
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from hades2_sjson_helper import apply_translation_to_sjson, parse_sjson_entries, _iter_text_blocks

INPUT_FILE = "games/0100A00019DE0000_Hades2/source/raw_text/en/ShellText.en.sjson"
OUTPUT_DIR = "games/0100A00019DE0000_Hades2/translations/Game/Text/en"
OUTPUT_FILE = f"{OUTPUT_DIR}/ShellText.en.sjson"

TRANSLATIONS = {
    # ===== Main Menu =====
    "MainMenuScreen_PlayGame": {"DisplayName": "Chơi"},
    "MainMenuScreen_CloudSave": {"DisplayName": "Lưu Trữ Đám Mây"},
    "MainMenuScreen_Settings": {"DisplayName": "Tùy Chọn"},
    "MainMenuScreen_Controls": {"DisplayName": "Điều Khiển"},
    "MainMenuScreen_Quit": {"DisplayName": "Thoát"},
    "MainMenuScreen_Discord": {"DisplayName": "Discord"},
    "MainMenuScreen_Website": {"DisplayName": "Trang Chủ"},
    "MainMenuScreen_Soundtrack": {"DisplayName": "Nhạc Game"},
    "MainMenuScreen_MailingList": {"DisplayName": "Nhận Tin"},
    "MainMenuScreen_RoadmapLabel": {"DisplayName": "Lộ Trình"},

    # ===== Profile Screen =====
    "ProfileScreen_Title": {"DisplayName": "CHƠI"},
    "ProfileScreen_ContinueGame": {"DisplayName": "Tiếp Tục"},
    "ProfileScreen_StartNewGame": {"DisplayName": "Trò Chơi Mới"},
    "ProfileScreen_ResetGame": {
        "DisplayName": "Xóa Ô Lưu Này?",
        "Description": "Mọi tiến trình sẽ bị ghi đè sau khi bạn bắt đầu trò chơi mới và lưu lại."
    },
    "ProfileScreen_InProgressSave_LastPlayed": {"DisplayName": "cập nhật: \\n {#NameHighlightFormat}"},
    "ProfileScreen_InProgressSave_Location": {"DisplayName": "vùng đất: \\n {#NameHighlightFormat}"},
    "ProfileScreen_InProgressSave_CompletedRuns": {"DisplayName": "đêm: \\n {#NameHighlightFormat}"},
    "ProfileScreen_InProgressSave_TotalMemPoints": {"DisplayName": "tâm thức: \\n {#NameHighlightFormat}"},
    "ProfileScreen_InProgressSave_TotalCosmeticsPoints": {"DisplayName": "uy tín: \\n {#NameHighlightFormat}"},
    "ProfileScreen_InProgressSave_EasyMode": {"DisplayName": "@GUI\\\\Shell\\\\EasyMode {#SpecialMenuSettingLightFormat}Chế Độ Thần Thoại"},
    "ProfileScreen_EmptySave": {"DisplayName": "( Ô Lưu Trống )"},
    "ProfileScreen_Hint": {"DisplayName": "chọn ô lưu — tiến trình tự lưu khi @GUI\\\\Icons\\\\LoadingSymbol_01 xuất hiện"},
    "ProfileScreen_InstructionHint_Cloud": {"DisplayName": "chọn ô lưu để bắt đầu. lưu đám mây đã bật; chọn 'đồng bộ & thoát' ở menu tạm dừng để tải lên."},

    # ===== Settings Menu =====
    "SettingsMenuScreen_Settings": {"DisplayName": "Cài Đặt"},
    "SettingsMenuScreen_Title": {"DisplayName": "TÙY CHỌN"},
    "SettingsMenuScreen_DisplaySettings": {"DisplayName": "Độ Phân Giải"},
    "SettingsMenuScreen_KeyMapping": {"DisplayName": "Điều Khiển"},
    "SettingsMenuScreen_AboutUs": {"DisplayName": "Tác Giả"},
    "SettingsMenuScreen_Language": {"DisplayName": "Ngôn Ngữ"},

    # ===== Pause Screen =====
    "PauseScreen_Title": {"DisplayName": "Tạm Dừng"},
    "PauseScreen_Resume": {"DisplayName": "Tiếp Tục", "Description": "đóng màn hình này và tiếp tục."},
    "PauseScreen_Settings": {"DisplayName": "Tùy Chọn", "Description": "chỉnh âm thanh, bật chế độ thần thoại, và hơn thế."},
    "PauseScreen_DisplaySettings": {"DisplayName": "Độ Phân Giải", "Description": "đặt độ phân giải màn hình và hơn thế."},
    "PauseScreen_Controls": {"DisplayName": "Điều Khiển", "Description": "gán lại nút bấm và hơn thế."},
    "PauseScreen_Abandon": {"DisplayName": "Hủy Đêm Này"},
    "PauseScreen_Exit": {"DisplayName": "Thoát"},
    "PauseScreen_Exit_Alt": {"DisplayName": "Thoát Về Menu Chính"},
    "PauseScreen_Exit_CrossSaves": {"DisplayName": "Đồng Bộ & Thoát"},
    "PauseScreen_GiveUp_ValidCheckpoint": {"DisplayName": "giả vờ đêm này chưa từng xảy ra?"},
    "PauseScreen_GiveUp_DeathArea": {"DisplayName": "đêm vẫn còn sớm và không thể hủy."},
    "PauseScreen_ValidCheckpoint_Recent": {"DisplayName": "tiến trình đã lưu cách đây chưa đầy một phút."},
    "PauseScreen_ValidCheckpoint": {"DisplayName": "tiến trình đã lưu "},
    "PauseScreen_InvalidCheckpoint": {"DisplayName": "thắng cuộc đối đầu này để thoát an toàn!"},
    "PauseScreen_InvalidCheckpoint_RewardAvailable": {"DisplayName": "nhận thưởng để thoát an toàn!"},
    "PauseScreen_InvalidCheckpoint_EncounterClear": {"DisplayName": "tiến đến địa điểm kế tiếp để thoát an toàn!"},
    "PauseScreen_ExitConfirm_ValidCheckpoint_Recent": {"DisplayName": "Thoát Game?", "Description": "Tiến trình được lưu chưa đầy một phút trước."},
    "PauseScreen_ExitConfirm_ValidCheckpoint": {"DisplayName": "Thoát Game?", "Description": "Tiến trình đã được lưu."},
    "PauseScreen_ExitConfirm_ValidCheckpoint_HasCloudSaves_Recent": {"DisplayName": "Đồng Bộ & Thoát?", "Description": "Tiến trình được lưu chưa đầy một phút trước. Đám mây sẽ được đồng bộ."},
    "PauseScreen_ExitConfirm_ValidCheckpoint_HasCloudSaves": {"DisplayName": "Đồng Bộ & Thoát?", "Description": "Tiến trình đã được lưu. Đám mây sẽ được đồng bộ."},
    "PauseScreen_ExitConfirm_LastSaveSingular": {"DisplayName": "Thoát Game?", "Description": "Lần lưu cuối: {$TempTextData.LastSaveTime}."},
    "PauseScreen_ExitConfirm_LastSavePlural": {"DisplayName": "Thoát Game?", "Description": "Lần lưu cuối: {$TempTextData.LastSaveTime}."},
    "PauseScreen_ExitConfirm_LastSavePluralHours": {"DisplayName": "Thoát Game?", "Description": "Lần lưu cuối: {$TempTextData.LastSaveTime} giờ trước."},
    "PauseScreen_ExitConfirm_LastSavePluralDays": {"DisplayName": "Thoát Game?", "Description": "Lần lưu cuối: {$TempTextData.LastSaveTime} ngày trước."},
    "PauseScreen_ExitConfirm_InvalidCheckpoint": {"DisplayName": "Thoát Không Lưu?", "Description": "Cuộc đối đầu này chưa được lưu. Ngươi sẽ mất tiến trình từ lần lưu gần nhất."},
    "PauseScreen_ExitConfirm_InvalidCheckpointFirstRun": {"DisplayName": "Thoát Không Lưu?", "Description": "Chưa có gì được lưu. Ngươi sẽ bắt đầu lại từ đầu."},
    "PauseScreen_ExitConfirm_AbandonWhileQuitAvailable": {"DisplayName": "Hủy Đêm Này?", "Description": "Tiến trình đêm này sẽ kết thúc ngay lập tức."},

    # ===== Key Mapping / Controls =====
    "KeyMappingScreen_Title": {"DisplayName": "Điều Khiển"},
    "KeyMappingScreen_MouseMoveDefaults": {"DisplayName": "Mặc Định Chuột"},
    "KeyMappingScreen_KeyboardMoveDefaults": {"DisplayName": "Mặc Định WASD"},
    "KeyMappingScreen_GamepadDefaults": {"DisplayName": "Mặc Định"},
    "KeyMappingScreen_UnmappedControl": {
        "DisplayName": "Nút Chưa Gán",
        "Description": "Ít nhất một điều khiển hiện chưa gán cho phím nào: \\n\\n"
    },
    "MoveUp": {"DisplayName": "Di Chuyển Lên"},
    "MoveDown": {"DisplayName": "Di Chuyển Xuống"},
    "MoveLeft": {"DisplayName": "Di Chuyển Trái"},
    "MoveRight": {"DisplayName": "Di Chuyển Phải"},
    "Reload": {"DisplayName": "Nạp Lại"},
    "Shout": {"DisplayName": "Nguyền"},
    "Assist": {"DisplayName": "Hỗ Trợ"},
    "Rush": {"DisplayName": "Lướt"},
    "Use": {"DisplayName": "Tương Tác"},
    "AdvancedTooltip": {"DisplayName": "Ân Huệ"},
    "Gift": {"DisplayName": "Quà"},
    "Reroll": {"DisplayName": "Đổi Lại"},
    "Rarify": {"DisplayName": "Nâng Phẩm"},
    "Select": {"DisplayName": "Chọn"},
    "Cancel": {"DisplayName": "Hủy"},
    "MenuLeft": {"DisplayName": "Tab Trái"},
    "MenuRight": {"DisplayName": "Tab Phải"},
    "ExorcismLeft": {"DisplayName": "Trừ Phong Trái"},
    "ExorcismRight": {"DisplayName": "Trừ Phong Phải"},
    "Emote": {"DisplayName": "Lời Muaa"},
    "Codex": {"DisplayName": "Danh Bạ"},
    "Inventory": {"DisplayName": "Hành Trang"},

    # ===== Misc Settings =====
    "MiscSettingsScreen_GameplayOptions": {"DisplayName": "Lối Chơi"},
    "MiscSettingsScreen_AudioOptions": {"DisplayName": "Âm Thanh"},
    "MiscSettingsScreen_ControlsOptions": {"DisplayName": "Điều Khiển"},
    "MiscSettingsScreen_DisplayOptions": {"DisplayName": "Hình Ảnh"},
    "MiscSettingsScreen_InterfaceOptions": {"DisplayName": "Giao Diện"},
    "MiscSettingsScreen_LanguageOptions": {"DisplayName": "Ngôn Ngữ"},
    "MiscSettingsScreen_CreditsOptions": {"DisplayName": "Tác Giả"},
    "MiscSettingsScreen_GraphicsOptions": {"DisplayName": "Đồ Họa"},
    "MiscSettingsScreen_AccessibilityOptions": {"DisplayName": "Tiện Ích"},
    "MiscSettingsScreen_SavesOptions": {"DisplayName": "Lưu Trữ"},
    "MiscSettingsScreen_RestoreDefaults": {
        "DisplayName": "{MX} ĐẶT LẠI",
        "Description": "Khôi phục cài đặt mặc định cho mọi tùy chọn trong menu con này."
    },
    "MiscSettingsScreen_Back": {"DisplayName": "{CN} QUAY LẠI"},
    "MiscSettingsScreen_Exit": {"DisplayName": "{CN} THOÁT"},
    "MiscSettingsScreen_Confirm": {"DisplayName": "{SL} XÁC NHẬN"},
    "MiscSettingsScreen_Select": {"DisplayName": "{SL} CHỌN"},
    "MiscSettingsScreen_SelectKBM": {"DisplayName": "{SL} ĐẶT"},
    "MiscSettingsScreen_Toggle": {"DisplayName": "{SL} BẬT/TẮT"},
    "MiscSettingsScreen_RequiresRestartWarning": {"DisplayName": "Cần Khởi Động Lại", "Description": "Thay đổi này sẽ có hiệu lực sau khi khởi động lại game."},

    # ===== Cloud Saves =====
    "CloudSettingsScreen_Title": {"DisplayName": "Lưu Trữ Đám Mây"},

    # ===== Audio options =====
    "DisableAudio": {"DisplayName": "Tắt Âm Thanh"},
    "MonoSound": {"DisplayName": "Âm Thanh Mono", "Description": "Âm thanh phát trên một kênh."},
    "MasterVolume": {"DisplayName": "Âm Lượng Tổng"},
    "MusicVolume": {"DisplayName": "Âm Nhạc"},
    "AmbienceVolume": {"DisplayName": "Tiếng Vọng Môi Trường"},
    "FxVolume": {"DisplayName": "Hiệu Ứng Âm Thanh"},
    "DialogueVolume": {"DisplayName": "Giọng Lồng Tiếng"},
    "Subtitles": {"DisplayName": "Phụ Đề"},
    "MusicSubtitles": {"DisplayName": "Phụ Đề Nhạc"},
    "ShowMissingSubtitles": {"DisplayName": "Hiện Phụ Đề Thiếu"},

    # ===== Gameplay options =====
    "EasyMode": {"DisplayName": "{!Icons.EasyModeIcon} Chế Độ Thần Thoại"},
    "EasyModeResistanceCap": {"DisplayName": "{!Icons.EasyModeIcon} Giới Hạn Chế Độ Thần Thoại"},
    "EasyModeResistanceCap_Disabled": {"DisplayName": "Giới Hạn Chế Độ Thần Thoại"},
    "TurboStyle_Off": {"DisplayName": "Tắt", "Description": "Dùng {TB} để đánh liên tiếp khi giữ Tấn Công hoặc Đặc Kỹ."},
    "TurboStyle_Hold": {"DisplayName": "Giữ", "Description": "Giữ {TB} để đánh liên tiếp khi giữ Tấn Công hoặc Đặc Kỹ."},
    "TurboStyle_Toggle": {"DisplayName": "Bật/Tắt", "Description": "Nhấn {TB} để bật/tắt đánh liên tiếp khi giữ Tấn Công hoặc Đặc Kỹ."},
    "SprintAutoHold": {"DisplayName": "Tự Động Chạy Nhanh", "Description": "Tự động chạy nhanh sau khi nhấn Lướt (không cần giữ)."},
    "BlinkAtCursor": {"DisplayName": "Lướt Đến Con Trỏ", "Description": "Lướt về phía con trỏ chuột thay vì thẳng phía trước."},
    "ShowDamageNumbers": {"DisplayName": "Chữ Số Sát Thương", "Description": "Khi ngươi thích bạo lực không thể đếm được."},
    "ShowGameplayTimer": {"DisplayName": "Hiện Đồng Hồ", "Description": "Hiện một thước đo của từng khoảnh khắc phù du."},
    "AutoAdvanceNarration": {"DisplayName": "Tự Động Chuyển Đoạn", "Description": "Bỏ cần tương tác để chuyển tiếp chuỗi hội thoại."},
    "RequireFocusToUpdate": {"DisplayName": "Tạm Dừng Khi Chuyển Ứng Dụng", "Description": "Dừng thời gian (nếu Chronos cho phép) khi ngươi chuyển ứng dụng."},
    "LockInputToWindow": {"DisplayName": "Khóa Chuột", "Description": "Giải phóng con trỏ chuột khỏi giới hạn cửa sổ này."},

    # ===== Display / Interface =====
    "Rumble": {"DisplayName": "Rung Tay Cầm", "Description": "Bật rung tay cầm, với những tay cầm có hỗ trợ."},
    "GeneralRumbleMultiplier": {"DisplayName": "Cường Độ Rung", "Description": "Chỉnh cường độ rung tay cầm."},
    "NoBorder": {"DisplayName": "Không Viền", "Description": "Bỏ viền cửa sổ ở chế độ hiển thị Không Viền."},
    "DrawHealthFX": {"DisplayName": "Hiệu Ứng Viền Màn Hình"},
    "ShowUIAnimations": {"DisplayName": "Hiện Giao Diện Chiến Đấu", "Description": "Tắt tính năng này cho Chế Độ Quay Video, khi nhiều khía cạnh trình bày giao diện bị tắt."},
    "HUDOpacity": {"DisplayName": "Độ Mờ Giao Diện", "Description": "Làm thông tin lối chơi quý giá khó thấy hơn."},
    "UseAltCursor": {"DisplayName": "Con Trỏ Sáng", "Description": "Đổi con trỏ chuột thành màu bạc đánh bóng."},
    "ShowSpeechBubble": {"DisplayName": "Hiện Bong Bóng Lời Nói"},
    "Brightness": {"DisplayName": "Độ Sáng"},
    "FullScreen": {"DisplayName": "Toàn Màn Hình"},
    "VSync": {"DisplayName": "Đồng Bộ Dọc (V-Sync)"},
    "Vsync": {"DisplayName": "Đồng Bộ Dọc (V-Sync)"},
    "Resolution": {"DisplayName": "Độ Phân Giải"},
    "Resolution_InGame": {"DisplayName": "Độ Phân Giải"},
    "ConfirmResolution": {"DisplayName": "Xác Nhận Độ Phân Giải"},
    "RevertResolutionCountdown": {"DisplayName": "Quay Lại Độ Phân Giải Trước"},
    "RevertResolutionCountdownSeconds": {"DisplayName": "Quay Lại Độ Phân Giải Trước"},
    "CameraShake": {"DisplayName": "Rung Màn Hình"},
    "ControlsStyle": {"DisplayName": "Kiểu Điều Khiển"},
    "ControlsStyle_Auto": {"DisplayName": "Tự Động"},
    "ControlsStyle_KeyboardMouse": {"DisplayName": "Bàn Phím & Chuột"},
    "ControlsStyle_TypeA": {"DisplayName": "Kiểu A"},
    "ControlsStyle_TypeB": {"DisplayName": "Kiểu B"},
    "ControlsStyle_TypeC": {"DisplayName": "Kiểu C"},
    "ControlScheme_Mouse": {"DisplayName": "Chuột"},
    "ControlScheme_WASD": {"DisplayName": "WASD"},
    "ControlScheme_GamePad": {"DisplayName": "Tay Cầm"},
    "ApplyDeadZone": {"DisplayName": "Áp Dụng Vùng Chết"},
    "ItemPin": {"DisplayName": "Ghim Vật Phẩm"},

    # ===== General prompts =====
    "Shell_Confirm": {"DisplayName": "Xác Nhận"},
    "Shell_Back": {"DisplayName": "Quay Lại"},
    "On": {"DisplayName": "Bật"},
    "Off": {"DisplayName": "Tắt"},
    "Restore Defaults": {"DisplayName": "Khôi Phục Mặc Định"},
    "ResumeGame": {"DisplayName": "Tiếp Tục Game"},
    "Menu_PressAnyKey": {"DisplayName": "Nhấn Phím Bất Kỳ"},
    "Menu_PressAnyButton": {"DisplayName": "Nhấn Nút Bất Kỳ"},
    "Download": {"DisplayName": "Đang Tải"},
    "Downloading": {"DisplayName": "Đang Tải"},
    "FilterSearchHint": {"DisplayName": "Gõ Để Tìm"},

    # ===== Save / errors =====
    "No_Continue_without_device": {"DisplayName": "Tiếp Tục Không Lưu"},
    "ErrorFailedToSave": {"DisplayName": "Không thể lưu game vào thiết bị."},
    "SaveErrorNoSpace": {"DisplayName": "Không Đủ Dung Lượng", "Description": "Không đủ dung lượng lưu trữ để lưu game."},
    "SaveErrorCorrupt": {"DisplayName": "Dữ Liệu Hỏng", "Description": "Dữ liệu lưu bị hỏng."},
    "SaveErrorGeneric": {"DisplayName": "Lỗi Lưu Trữ", "Description": "Đã xảy ra lỗi khi lưu game."},
    "SaveFileOverwriteWarning": {"DisplayName": "Ghi Đè Lưu Trữ?", "Description": "Lưu trữ này sẽ bị ghi đè."},
    "WarningSaveOverwrite": {"DisplayName": "Ghi Đè Lưu Trữ?", "Description": "Lưu trữ này sẽ bị ghi đè."},
    "CloudSaves_SyncingDialogText": {"DisplayName": "Đang Đồng Bộ Đám Mây..."},
    "CloudSaves_SyncingDialogTextSuccess": {"DisplayName": "Đồng Bộ Đám Mây Thành Công"},
    "CloudSaves_SyncingDialogTextFailure": {"DisplayName": "Đồng Bộ Đám Mây Thất Bại"},
    "CloudSaveError_NoInternet": {"DisplayName": "Không Có Kết Nối Mạng", "Description": "Cần kết nối internet để đồng bộ đám mây."},
    "CloudSaveError_NoNintendoAccount": {"DisplayName": "Cần Tài Khoản Nintendo", "Description": "Cần liên kết tài khoản Nintendo để đồng bộ đám mây."},
    "ScreenshotSaved": {"DisplayName": "Đã Lưu Ảnh Chụp Màn Hình"},
    "InGameUI_Saving": {"DisplayName": "Đang Lưu..."},
    "FileAccessErrorPC": {"DisplayName": "Không Thể Đọc Dữ Liệu"},
    "DataFileCorrupt": {"DisplayName": "Không Thể Đọc Dữ Liệu"},
    "ErrorDuplicateApp": {"DisplayName": "Hades II Đang Chạy"},
    "ErrorOutOfMemory": {"DisplayName": "Lỗi Cấp Phát Bộ Nhớ"},
    "ErrorAccessDenied": {"DisplayName": "Truy Cập File Bị Từ Chối"},

    # ===== Misc visible =====
    "Supergiant": {"DisplayName": "Supergiant"},
    "SoundtrackAvailable": {"DisplayName": "Nhạc Gốc Có Tại:"},
    "MissingGamepad": {"DisplayName": "Không Phát Hiện Tay Cầm"},
    "Gamepad": {"DisplayName": "Tay Cầm"},
    "Graphics": {"DisplayName": "Cài Đặt Đồ Họa"},
    "Display": {"DisplayName": "Hình Ảnh"},
    "AutoSafeMode": {"DisplayName": "Chế Độ An Toàn Tự Động"},
    "FastForward": {"DisplayName": "Tua Nhanh"},
    "FastForwardSpeed": {"DisplayName": "Tốc Độ Tua Nhanh"},
    "DisableDamage": {"DisplayName": "Vô Hiệu Hóa Sát Thương"},
    "DamageTakenMultiplier": {"DisplayName": "Hệ Số Sát Thương Chịu"},
    "DamageMultiplier": {"DisplayName": "Hệ Số Sát Thương"},
    "PauseSoundsWhenPaused": {"DisplayName": "Dừng Âm Thanh Khi Tạm Dừng"},
}


def translate_shell():
    print(">>> Đang dịch ShellText.en.sjson...")
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    src_ids = set(parse_sjson_entries(content).keys())
    used = {k: v for k, v in TRANSLATIONS.items() if k in src_ids}
    skipped = sorted(set(TRANSLATIONS) - src_ids)
    if skipped:
        print(f"⚠ Bỏ {len(skipped)} key không tồn tại: {skipped}")

    new_content = apply_translation_to_sjson(content, used)

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

    # Thống kê dịch
    out_ents = parse_sjson_entries(new_content)
    src_ents = parse_sjson_entries(content)
    translated = sum(
        1 for i in out_ents
        if out_ents[i].get('DisplayName') != src_ents.get(i, {}).get('DisplayName')
    )
    print(f"✅ Đã dịch {translated}/{len(src_ids)} DisplayName ShellText")
    print(f"👉 Lưu tại: {OUTPUT_FILE}")


if __name__ == '__main__':
    translate_shell()
