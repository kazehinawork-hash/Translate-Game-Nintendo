"""Xac nhan file nguon + dong bo neu can + build + kiem chung (chay 2 lan cho chac)."""
import json
import os
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
G = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby')
P = os.path.join(G, 'translations', 'kirby_vi.json')

for attempt in (1, 2):
    d = json.load(open(P, encoding='utf-8'))
    a = d.get('Dialog.msbt', {}).get('Btn_Continue')
    b = d.get('Figure.msbt', {}).get('$View')
    print(f'lan {attempt}: Btn_Continue={a!r} | $View={b!r}')
    if a == 'Nghe tiếp' and b == 'Ngắm':
        print('  -> file nguon DA DUNG')
        break
    d.setdefault('Dialog.msbt', {})['Btn_Continue'] = 'Nghe tiếp'
    d.setdefault('Figure.msbt', {})['$View'] = 'Ngắm'
    with open(P, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.flush()
        os.fsync(f.fileno())
    print('  -> da ghi lai, doc lai kiem tra...')
    time.sleep(1)

print('\n=== build lai + kiem chung ===')
for cmd in ('build_kirby_mod.py', 'final_check_kirby.py'):
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', cmd)],
                       capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT)
    for l in ((r.stdout or '') + (r.stderr or '')).splitlines():
        if any(x in l for x in ('dong goi', '^tong', 'Eblong', 'KET QUA')) or l.startswith('tong '):
            print(f'  [{cmd}] ' + l.strip()[:120])
