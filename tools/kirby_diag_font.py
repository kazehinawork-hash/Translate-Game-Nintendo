"""Chan doan 1 font da giai ma: bang muc luc co gi, fontTools loi o dau."""
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

P = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'font_edit', 'FOT-RodinNTLGPro-B.otf')
if not os.path.exists(P):
    import glob
    c = glob.glob(os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby', 'font_edit', 'FOT-RodinNTLGPro-B.*'))
    print('cac file khop:', [os.path.basename(x) for x in c])
    P = [x for x in c if x.endswith(('.otf', '.ttf'))][0]
b = open(P, 'rb').read()
print(f'file {len(b):,} b | sfntVersion={b[:4].hex(" ")} | 12 byte dau: {b[:12].hex(" ")}')
ntab = struct.unpack_from('>H', b, 4)[0]
print(f'so bang = {ntab}')
tabs = {}
for i in range(ntab):
    tag, cks, off, ln = struct.unpack_from('>4sIII', b, 12 + 16 * i)
    t = tag.decode('latin1')
    tabs[t] = (off, ln)
    ok = (off + ln) <= len(b)
    print(f'  {t:<6} off={off:>9,} len={ln:>9,} {"OK" if ok else "VUOT FILE!"}')
print(f'\ntong {len(tabs)} bang')

# thu fontTools
from fontTools.ttLib import TTFont
try:
    f = TTFont(P, lazy=True)
    print('TTFont load OK; cac bang fontTools thay:', sorted(f.reader.tables.keys()))
except Exception as e:
    print(f'TTFont load LOI: {type(e).__name__}: {str(e)[:100]}')
try:
    f2 = TTFont(P)
    print('head unitsPerEm =', f2['head'].unitsPerEm)
except Exception as e:
    print(f'f["head"] LOI: {type(e).__name__}: {str(e)[:120]}')
