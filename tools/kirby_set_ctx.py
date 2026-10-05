"""Dat dung 2 ngoai le ngu canh + build lai + kiem chung (mot lenh)."""
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
G = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby')
T = os.path.join(G, 'translations')

vi = json.load(open(os.path.join(T, 'kirby_vi.json'), encoding='utf-8'))
print('TRUOC khi sua:')
print('  Dialog.Btn_Continue =', repr(vi.get('Dialog.msbt', {}).get('Btn_Continue')))
print('  Figure.$View        =', repr(vi.get('Figure.msbt', {}).get('$View')))

vi.setdefault('Dialog.msbt', {})['Btn_Continue'] = 'Nghe tiếp'
vi.setdefault('Figure.msbt', {})['$View'] = 'Ngắm'
json.dump(vi, open(os.path.join(T, 'kirby_vi.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# kiem tra lai file vua ghi
chk = json.load(open(os.path.join(T, 'kirby_vi.json'), encoding='utf-8'))
print('SAU khi sua:')
print('  Dialog.Btn_Continue =', repr(chk['Dialog.msbt']['Btn_Continue']))
print('  Figure.$View        =', repr(chk['Figure.msbt']['$View']))

# dong bo sang chunk tuong ung
for p in (os.path.join(T, 'vi_02.json'), os.path.join(T, 'vi_03.json'), os.path.join(T, 'vi_04.json'),
          os.path.join(T, 'vi_05.json'), os.path.join(T, 'vi_06.json'), os.path.join(T, 'vi_07.json')):
    if not os.path.exists(p):
        continue
    d = json.load(open(p, encoding='utf-8'))
    ch = 0
    for x in d:
        if x.get('file') == 'Dialog.msbt' and x.get('key') == 'Btn_Continue' and x.get('vi') != 'Nghe tiếp':
            x['vi'] = 'Nghe tiếp'
            ch += 1
        if x.get('file') == 'Figure.msbt' and x.get('key') == '$View' and x.get('vi') != 'Ngắm':
            x['vi'] = 'Ngắm'
            ch += 1
    if ch:
        json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'  dong bo {os.path.basename(p)}: {ch}')

print('\n=== build lai ===')
r = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'build_kirby_mod.py')],
                   capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT)
for l in ((r.stdout or '') + (r.stderr or '')).splitlines():
    if 'dong goi' in l or 'output:' in l:
        print('  ' + l.strip()[:150])

print('\n=== kiem chung thanh pham ===')
r = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'verify_kirby_fixes.py')],
                   capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT)
for l in ((r.stdout or '') + (r.stderr or '')).splitlines():
    if '[OK' in l or '[LOI' in l or 'KET QUA' in l:
        print('  ' + l.strip()[:130])
