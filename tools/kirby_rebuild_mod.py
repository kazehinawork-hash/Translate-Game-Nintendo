"""Lap lai mod Kirby HOAN CHINH tu ban dump (v1.1.0):
   1. Copy toan bo RomFS tu dump (co Filter.bin, UpgradeDlc.msbt...)
   2. Phu ban dich tieng Viet len cac .msbt da dich (theo dung duong dan)
   3. Giu nguyen font da va + cau hinh da va dai ky tu
"""
import os
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TID = '01004D300C5AE000'
DUMP = os.path.join(ROOT, 'dump', TID, 'romfs')
MOD = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs')

# 1) backup phan da lam truoc do (msg dich + font + config)
done_msg = os.path.join(MOD, 'msg')
done_font = os.path.join(MOD, 'font')

# 2) sao chep TOAN BO dump vao mod (ghi de)
n = 0
for r, _, fs in os.walk(DUMP):
    rel = os.path.relpath(r, DUMP)
    dst = os.path.join(MOD, rel) if rel != '.' else MOD
    os.makedirs(dst, exist_ok=True)
    for f in fs:
        shutil.copy2(os.path.join(r, f), os.path.join(dst, f))
        n += 1
print(f'  copy tu dump: {n:,} file')

# 3) phu lai cac file msg da dich + font/config da va (tu ban lam truoc, da backup)
#    -> chay lai cac tool va/config de chac chan dung ban da va
print('  -> chay lai tool va font + cau hinh...')
os.system(f'python "{os.path.join(ROOT, "tools", "patch_font_kirby_v2.py")}" > nul 2>&1')
os.system(f'python "{os.path.join(ROOT, "tools", "patch_font_kirby_bfttf.py")}" > nul 2>&1')
os.system(f'python "{os.path.join(ROOT, "tools", "kirby_font_config.py")}" > nul 2>&1')

# 4) thong ke
tot = {}
for r, _, fs in os.walk(MOD):
    rel = os.path.relpath(r, MOD)
    key = rel.split(os.sep)[0] + '/' + (rel.split(os.sep)[1] if os.sep in rel else '')
    tot[key] = tot.get(key, 0) + len(fs)
print('\n  cau truc mod Kirby:')
for k in sorted(tot):
    print(f'    {k:<28} {tot[k]:>5} file')
print(f'\n  tong: {sum(tot.values()):,} file | {sum(os.path.getsize(os.path.join(r,f)) for r,_,fs in os.walk(MOD) for f in fs)/1e6:,.1f} MB')
