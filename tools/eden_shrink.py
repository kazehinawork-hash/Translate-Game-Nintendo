"""Thu nho anh chup man hinh de doc duoc (tranh timeout)."""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'games', '_consistency', 'eden_shot.png')
from PIL import Image

im = Image.open(SRC)
print('goc:', im.size)
w, h = im.size
# thu nho con 900px chieu rong
scale = 900 / w
im2 = im.resize((900, int(h * scale)), Image.LANCZOS)
out = os.path.join(ROOT, 'games', '_consistency', 'eden_small.png')
im2.convert('RGB').save(out, quality=80)
print('nho:', im2.size, os.path.getsize(out), 'b ->', out)

# them ban cat giua man hinh (thuong la menu)
cx, cy = w // 2, int(h * 0.45)
crop = im.crop((max(0, cx - 700), max(0, cy - 350), min(w, cx + 700), min(h, cy + 350)))
crop = crop.resize((840, int(crop.height * 840 / crop.width)), Image.LANCZOS)
out2 = os.path.join(ROOT, 'games', '_consistency', 'eden_center.png')
crop.convert('RGB').save(out2, quality=80)
print('cat giua:', crop.size, os.path.getsize(out2), 'b ->', out2)

# kiem tra anh co phai mau den khong (neu phien khong co desktop)
import collections
px = im2.convert('L').getdata()
avg = sum(px) / len(px)
print(f'do sang trung binh: {avg:.1f} (neu ~0 hoac ~255 thi anh trong)')
