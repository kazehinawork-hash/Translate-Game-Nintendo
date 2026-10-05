"""Va font LastResort.ttf cho It Takes Two: giu glyph goc + them dau tieng Viet (BH-20)."""
import json
import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')
from fontTools.ttLib import TTFont
from fontTools.subset import Options, Subsetter, load_font, save_font

ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '010092A0172E4000'
G = os.path.join(ROOT, 'games', f'{TID}_ItTakesTwo')
ORIG = os.path.join(G, 'source', 'Engine__Content__SlateDebug__Fonts__LastResort.ttf')
OUTDIR = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'Engine', 'Content', 'SlateDebug', 'Fonts')
SUPPLY = r'C:\Windows\Fonts\ARIALUNI.TTF'

# 1. ky tu dung trong ban dich
vi = json.load(open(os.path.join(G, 'translations', 'itt_vi.json'), encoding='utf-8'))
used = {c for v in vi.values() for c in str(v) if c.isprintable()}

f = TTFont(ORIG, lazy=True)
orig_cm = set(f.getBestCmap())
print(f'LastResort goc: {len(orig_cm):,} glyph | dinh dang: {"OTTO" if f.sfntVersion == "OTTO" else "TTF"}')
miss_in_orig = sorted(c for c in used if ord(c) not in orig_cm)
print(f'  ky tu ban dich ma font goc THIEU: {len(miss_in_orig)} -> {"".join(miss_in_orig[:40])}')

sup = TTFont(SUPPLY, lazy=True)
sup_cm = set(sup.getBestCmap())
still = [c for c in miss_in_orig if ord(c) not in sup_cm]
print(f'  trong do Arial Unicode cung thieu: {len(still)} {still[:20]}')

# 2. subset Arial = (cmap goc U ky tu ban dich) -> giu dung do phu goc, them tieng Viet
keep = sorted(orig_cm | {ord(c) for c in used})
opts = Options(layout_features=[], notdef_outline=True, recalc_bounds=True, glyph_names=False,
               legacy_kern=False, drop_tables=['DSIG'], hinting=False)
font = load_font(SUPPLY, opts)
s = Subsetter(options=opts)
s.populate(unicodes=keep)
s.subset(font)
os.makedirs(OUTDIR, exist_ok=True)
out = os.path.join(OUTDIR, 'LastResort.ttf')
save_font(font, out, opts)

# 3. kiem chung
chk = TTFont(out, lazy=True)
cm = set(chk.getBestCmap())
lost = orig_cm - cm
miss = [c for c in used if ord(c) not in cm and ord(c) < 0xE000]
print(f'\nfont moi: {len(cm):,} glyph | mat glyph goc: {len(lost)} | ky tu ban dich con thieu: {len(miss)}')
if lost:
    print(f'  (mat: {"".join(chr(c) for c in sorted(lost)[:40])})')
print(f'\nda ghi: {out} ({os.path.getsize(out):,} byte)')
print('KET QUA:', 'PASS' if not miss else 'CAN XEM LAI')
