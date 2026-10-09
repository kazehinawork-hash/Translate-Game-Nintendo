"""Chup man hinh cua so Eden dang chay -> file PNG de kiem tra tieng Viet."""
import ctypes
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'games', '_consistency', 'eden_shot.png')
os.makedirs(os.path.dirname(OUT), exist_ok=True)

from PIL import ImageGrab

# dua cua so eden len truoc
try:
    u32 = ctypes.windll.user32
    hwnds = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def cb(h, l):
        buf = ctypes.create_unicode_buffer(512)
        u32.GetWindowTextW(h, buf, 512)
        if 'eden' in buf.value.lower() or 'monopoly' in buf.value.lower():
            hwnds.append((h, buf.value, u32.IsWindowVisible(h)))
        return True

    u32.EnumWindows(cb, 0)
    for h, t, v in hwnds:
        print(f'  cua so: {t!r} visible={bool(v)}')
    target = None
    for h, t, v in hwnds:
        if v:
            target = h
    if target:
        u32.SetForegroundWindow(target)
        u32.ShowWindow(target, 9)
        time.sleep(1.5)
except Exception as e:
    print('  loi dua cua so len:', e)

im = ImageGrab.grab()
im.save(OUT)
print(f'  da chup: {OUT} ({os.path.getsize(OUT):,} b) {im.size}')
