import os, sys
sys.stdout.reconfigure(encoding='utf-8')
"""Vá font tiếng Việt cho Ori (thay TTF nhúng của Candara)."""
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from unity_text_tool import patch_font

SRCD = os.environ.get('ORI_BUNDLES', r'C:\Users\Admin\AppData\Local\Temp\ori_work\Data')
OUT = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01008DD013200000', 'romfs', 'Data')
LATO = os.path.join(ROOT, 'tools', 'fonts_hades2', 'Lato-Regular.ttf')

# Candara = font UI chinh (thieu dau tieng Viet) -> Lato
# Cac font dev (keyboard / ProFontWindows / moon-tools) giu nguyen vi chua glyph ky hieu rieng.
for bundle, mapping in [('data_3.unity3d', {'Candara': LATO})]:
    src = os.path.join(SRCD, bundle)
    if not os.path.exists(src):
        print('thieu bundle goc:', src); continue
    done = patch_font(src, mapping, OUT, pack='original')
    print(f'{bundle}: da va font {done}')
