"""Kiem tra cuoi mod Kirby (dung unwrap da sua tu patch_font_kirby)."""
import io
import json
import os
import sys

sys.path.insert(0, r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\tools')
sys.stdout.reconfigure(encoding='utf-8')
from fontTools.ttLib import TTFont
from patch_font_kirby import comp, decomp, unwrap
from extract_msbt import parse_msbt_bytes

ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '01004D300C5AE000'
G = os.path.join(ROOT, 'games', f'{TID}_Kirby')
SRC = os.path.join(G, 'source', 'font', 'ScalableFontBin')
MODF = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'font', 'ScalableFontBin')
MODM = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'msg', 'Kirby15')

vi = json.load(open(os.path.join(G, 'translations', 'kirby_vi.json'), encoding='utf-8'))
# cung ngoai le ngu canh nhu build_kirby_mod.py (de so dung nhu nhau)
for _f, _kv in {'Dialog.msbt': {'Btn_Continue': 'Nghe tiếp'}, 'Figure.msbt': {'$View': 'Ngắm'}}.items():
    vi.setdefault(_f, {}).update(_kv)
used = {c for e in vi.values() for v in e.values() for c in str(v) if c.isprintable()}

print('=== FONT ===')
ok = True
mall = None
for fn in sorted(os.listdir(MODF)):
    if not fn.endswith('.bfotf.cmp'):
        continue
    o, _ = unwrap(decomp(open(os.path.join(SRC, fn), 'rb').read()))
    m, _ = unwrap(decomp(open(os.path.join(MODF, fn), 'rb').read()))
    so = set(TTFont(io.BytesIO(o), lazy=True).getBestCmap())
    sm = set(TTFont(io.BytesIO(m), lazy=True).getBestCmap())
    mall = sm if mall is None else (mall & sm)
    lost = so - sm
    miss = {c for c in used if ord(c) not in sm and ord(c) < 0xE000}
    st = 'OK' if not miss else 'THIEU KY TU'
    if miss:
        ok = False
    print(f'  {fn[:36]:<38} goc {len(so):>6,} -> mod {len(sm):>6,} | mat {len(lost):>3} | thieu chu dich {len(miss)} [{st}]')
    if lost:
        print(f'      glyph goc bi mat (nen kiem tra): {sorted(chr(c) for c in lost)[:30]}')

missing_all = sorted({c for c in used if ord(c) not in (mall or set()) and ord(c) < 0xE000})
print(f'\nky tu thieu o MOI font: {[(c, hex(ord(c))) for c in missing_all]}')

print('\n=== TEXT (10 khe ngon ngu) ===')
tot = bad = 0
for lang in sorted(os.listdir(MODM)):
    d = os.path.join(MODM, lang)
    if not os.path.isdir(d):
        continue
    n = b2 = 0
    for fn in os.listdir(d):
        if not fn.endswith('.msbt'):
            continue
        built = parse_msbt_bytes(open(os.path.join(d, fn), 'rb').read())
        for k, v in vi.get(fn, {}).items():
            n += 1
            if built.get(k, '') != v:
                b2 += 1
    tot += n
    bad += b2
    print(f'  {lang:<12} {n:>5} chuoi | lech {b2}')
print(f'\ntong {tot:,} chuoi | lech {bad}')
print('\nKET QUA:', 'PASS' if bad == 0 else 'CAN XEM LAI')
