import os, sys
sys.stdout.reconfigure(encoding='utf-8')
"""Vá font tiếng Việt cho Ori and the Will of the Wisps.

Chiến lược (đã kiểm chứng bằng dữ liệu thật):
- Candara (data_3)      : font UI chính, atlas động, 0 icon, upm=2048
                          -> THAY HẲN bằng Lato (phủ 120/120 ký tự tiếng Việt dùng trong mod;
                             chỉ mất 2 ký tự vô nghĩa U+2206, U+25AF)
- ProFontWindows (data_0): font text, 0 icon -> THAY HẲN bằng Lato
- keyboard (data_0)      : 52 chữ + 18 glyph ICON (PUA) ĐANG ĐƯỢC DÙNG (~100 lần/bundle)
                          -> HỢP NHẤT: giữ nguyên glyph gốc + thêm dấu tiếng Việt
- moon-tools (data_0)    : 100% glyph icon (PUA) đang dùng -> HỢP NHẤT (giữ icon + thêm dấu)
- Roboto-Thin/Bold/Light : đã phủ đủ tiếng Việt -> GIỮ NGUYÊN

data_0 vừa chứa text vừa chứa font nên script ưu tiên đọc bản trong `output/` (đã vá text)
để KHÔNG ghi đè bản dịch.
"""
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import UnityPy  # noqa: E402
from unity_text_tool import patch_font  # noqa: E402
from merge_vi_font import merge_vn_font  # noqa: E402

SRCD = os.environ.get('ORI_BUNDLES', r'C:\Users\Admin\AppData\Local\Temp\ori_work\Data')
OUT = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01008DD013200000', 'romfs', 'Data')
LATO = os.path.join(ROOT, 'tools', 'fonts_hades2', 'Lato-Regular.ttf')

JOBS = [('data_3.unity3d', 'Candara'), ('data_0.unity3d', 'ProFontWindows')]
MERGES = [('data_0.unity3d', 'keyboard'), ('data_0.unity3d', 'moon-tools')]


def font_bytes(bundle, name):
    for p in (os.path.join(OUT, bundle), os.path.join(SRCD, bundle)):
        if not os.path.exists(p):
            continue
        env = UnityPy.load(p)
        for o in env.objects:
            if o.type.name == 'Font':
                d = o.read()
                if getattr(d, 'm_Name', '') == name:
                    return bytes(d.m_FontData)
    return None


def resolve(bundle):
    p = os.path.join(OUT, bundle)
    return p if os.path.exists(p) else os.path.join(SRCD, bundle)


# 1) Thay hẳn
for bundle, name in JOBS:
    done = patch_font(resolve(bundle), {name: LATO}, OUT, pack='original')
    print(f'{bundle}: thay han {done}')

# 2) Hợp nhất (giữ icon)
by_bundle = {}
for bundle, name in MERGES:
    raw = font_bytes(bundle, name)
    if raw is None:
        print(f'{bundle}/{name}: KHONG THAY FONT'); continue
    by_bundle.setdefault(bundle, {})[name] = merge_vn_font(raw, LATO)

for bundle, mapping in by_bundle.items():
    done = patch_font(resolve(bundle), mapping, OUT, pack='original')
    print(f'{bundle}: hop nhat {done}')
