"""Translate remaining player-facing storage, cloud-save, and error UI."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from hades2_sjson_helper import apply_translation_to_sjson  # noqa: E402

TR = ROOT / "games/0100A00019DE0000_Hades2/translations/Game/Text/en/ShellText.en.sjson"
translations = {
    "forceCanceledReselection": "Chưa chọn thiết bị lưu. Cần có thiết bị lưu để tiếp tục.",
    "forceDisconnectedReselectionMessage": "Thiết bị lưu đã bị ngắt kết nối. Cần có thiết bị lưu để tiếp tục.",
    "promptForCancelledMessage": "Chưa chọn thiết bị lưu. Tiến trình sẽ không được lưu. Chọn thiết bị hoặc tiếp tục mà không lưu?",
    "promptForDisconnectedMessage": "Thiết bị lưu đã bị ngắt kết nối. Chọn thiết bị khác hoặc tiếp tục mà không lưu?",
    "Reselect_Storage_Device": "Chọn lại thiết bị lưu?",
    "Storage_Device_Required": "Cần có thiết bị lưu.",
    "StorageDevice_is_not_valid": "Thiết bị lưu không hợp lệ.",
    "GraphicsDriverWarning": "Đã phát hiện trình điều khiển đồ họa cũ! Hãy thoát game và cập nhật trình điều khiển.",
    "SignedInAsGuest": "Bạn đang đăng nhập bằng hồ sơ khách. Hãy đăng nhập bằng hồ sơ người chơi không phải khách.",
    "SignInChangeOccurred": "Hồ sơ đăng nhập đã thay đổi. Bạn sẽ được đưa về màn hình tiêu đề.",
    "NoStorageDeviceSelected": "Chưa chọn thiết bị lưu. Tiến trình sẽ không được lưu. Chọn thiết bị hoặc tiếp tục mà không lưu?",
    "CloudSaves_SyncingDialogTextLongWait": "Đang đồng bộ dữ liệu lưu",
    "CloudSaves_SyncingOnQuitDialogText": "Đang đồng bộ dữ liệu lưu",
    "CloudSaves_SyncingOnQuitDialogTextLongWait": "Đang đồng bộ dữ liệu lưu",
    "CloudSaves_SyncingOnQuitDialogTextSuccess": "Đang đồng bộ dữ liệu lưu",
    "CloudSaves_SyncingOnQuitDialogTextFailure": "Đang đồng bộ dữ liệu lưu",
    "CloudSaves_SyncingOnQuitDialogTextDeferResolution": "Đang đồng bộ dữ liệu lưu",
    "ErrorOfflineProfile": "Bạn cần đăng nhập để sử dụng tính năng này.",
    "ErrorMissingStorageDevice": "Không tìm thấy thiết bị lưu. Hãy kiểm tra thiết bị của bạn.",
    "ErrorAchievementFailed": "Không thể trao danh hiệu vì hồ sơ người chơi hiện tại không khả dụng.",
    "DisableScreenSaver": "Tắt trình bảo vệ màn hình",
    "ResChangeWarning": "Bạn có muốn giữ thiết lập này không? Thiết lập trước sẽ được khôi phục sau 10 giây.",
    "WaitingForDownload": "Đang chờ tải xuống",
    "SaveErrorInvalidUserLogin": "Bạn đã đăng xuất; không thể lưu vào thiết bị lưu.",
    "ErrorSendCrashReport": "Thông báo: Đã phát hiện game bị lỗi",
    "ErrorCrashReport": "Hades II gặp sự cố",
    "ErrorDirectXDriver": "Lỗi: Thiết bị DirectX",
    "ErrorVulkanStartup": "Lỗi khởi chạy Vulkan",
    "ScreenshotFailed": "Không thể lưu ảnh chụp màn hình. Vui lòng thử lại.",
    "CloudSaveError_SteamAuthFailure": "Thông báo: Kết nối thất bại",
    "CloudSaveError_SteamSessionExpired": "Thông báo: Kết nối hết hạn",
    "CloudSaveError_Corrupt": "Thông báo: Dữ liệu lưu bị hỏng",
    "CloudSaveMessage_SteamPrompt": "Bạn có muốn tải hồ sơ từ Steam không? {#ExitConfirmItalicFormat}Lưu ý{#Prev}: Thao tác này sẽ mở trình duyệt để xác thực tài khoản Steam nếu bạn chưa đăng nhập.",
    "CloudSaveError_SyncTimeout": "Thông báo: Chưa đồng bộ dữ liệu lưu",
    "CloudSaveButton_DisconnectEpic": "Ngắt kết nối Epic Games",
    "CloudSaveMessage_StorageConflictShort": "{#SpecialMenuSettingLightFormat}{SL} Sửa xung đột dữ liệu  \n",
    "CloudSaveMessage_StorageConflict": "Xung đột dữ liệu lưu",
    "CloudSaveMessage_DisconnectedSteam": "Đã ngắt kết nối lưu liên nền tảng",
    "CloudSaveMessage_DisconnectedEpic": "Đã ngắt kết nối lưu liên nền tảng",
    "CloudSaves_LinkedSteamFail": "Thông báo: Kết nối thất bại",
    "CloudSaves_LinkedEpicFail": "Thông báo: Kết nối thất bại",
    "CloudSaves_LinkOnlyOnePlease_Steam": "Thông báo: Đã kết nối tài khoản",
    "CloudSaves_LinkOnlyOnePlease_Epic": "Thông báo: Đã kết nối tài khoản",
    "SaveErrorIncompatible": "Cảnh báo: Dữ liệu lưu không tương thích!",
    "CloudSaves_ComingSoon": "Lưu liên nền tảng: Sắp ra mắt",
    "CloudSaves_EpicDoYouWant": "Bật Epic Online Services?",
    "CloudSaves_InstructionHint": "{#AlertHeaderFormat}Lưu ý: {#Prev}Khi đã kết nối, dữ liệu lưu sẽ được tải lên nếu bạn chọn 'Đồng bộ & Thoát' trong Menu tạm dừng.",
    "CloudSaves_Corrupt": "{#ExitConfirmWarningFormat}(lỗi dữ liệu)",
    "CloudSaves_Incompatible": "{#ExitConfirmWarningFormat}(lỗi phiên bản)",
    "CloudSaves_BadPickAreYouSure": "Tải dữ liệu lưu cũ hơn?",
    "CloudSaves_BadPickAreYouSureFewerRuns": "Tải dữ liệu lưu trước đó?",
    "BootWarning_FailedToQuitProperly": "Game chưa thoát đúng cách",
    "CrashPopup_TransmitData": "LƯU Ý: Bạn đã bật tùy chọn 'Gửi dữ liệu', nên chúng tôi tự động nhận được thông tin này. Bạn không cần gửi báo cáo thêm. Cảm ơn đã kiên nhẫn chờ chúng tôi điều tra sự cố!",
    "CrashPopup_NoTransmitData": "LƯU Ý: Bạn đã tắt tùy chọn 'Gửi dữ liệu', nên chúng tôi không nhận được thông tin này.",
}

source = TR.read_text(encoding="utf-8-sig")
mapped = {key: {"DisplayName": value} for key, value in translations.items()}
TR.write_text(apply_translation_to_sjson(source, mapped), encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
print(f"Đã dịch {len(translations)} thông báo lưu trữ và lỗi trong ShellText.")
