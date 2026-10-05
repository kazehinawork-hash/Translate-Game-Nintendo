"""Sua net 1 chuoi 'Rung Im Lang' con sot trong cac chunk Ori + build lai."""
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
T = os.path.join(ROOT, 'games', '01008DD013200000_OriAndTheWillOfTheWisps', 'translations')

n = 0
for f in sorted(os.listdir(T)):
    if not f.endswith('.json'):
        continue
    p = os.path.join(T, f)
    try:
        d = json.load(open(p, encoding='utf-8'))
    except Exception:
        continue
    ch = 0
    if isinstance(d, list):
        k = 'VI' if d and 'VI' in d[0] else 'vi'
        for x in d:
            v = str(x.get(k, ''))
            if 'Rừng Im Lặng' in v:
                x[k] = v.replace('Rừng Im Lặng', 'Rừng Tĩnh Lặng')
                ch += 1
    if ch:
        json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'  {f}: sua {ch}')
        n += ch
print(f'tong sua {n}')

if n:
    print('\n=== build lai bundle ===')
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'build_ori_mod.py'),
                        '--src', r'E:\ORI_work\Data'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT)
    for l in ((r.stdout or '') + (r.stderr or '')).splitlines():
        if 'xong:' in l or 'loi' in l or 'bundle OK' in l:
            print('  ' + l.strip()[:130])
