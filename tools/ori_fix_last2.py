"""Tim + sua chuoi 'Rung Im Lang' con sot o BAT KY file nao cua Ori, roi build lai."""
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
G = os.path.join(ROOT, 'games', '01008DD013200000_OriAndTheWillOfTheWisps')
n = 0
for r, _, fs in os.walk(G):
    for f in fs:
        if not f.endswith('.json'):
            continue
        p = os.path.join(r, f)
        try:
            d = json.load(open(p, encoding='utf-8'))
        except Exception:
            continue
        ch = 0
        if isinstance(d, list):
            k = 'VI' if d and 'VI' in d[0] else ('vi' if d and 'vi' in d[0] else None)
            if k:
                for x in d:
                    v = str(x.get(k, ''))
                    if 'Rừng Im Lặng' in v:
                        x[k] = v.replace('Rừng Im Lặng', 'Rừng Tĩnh Lặng')
                        ch += 1
        elif isinstance(d, dict):
            for kk, vv in list(d.items()):
                if isinstance(vv, str) and 'Rừng Im Lặng' in vv:
                    d[kk] = vv.replace('Rừng Im Lặng', 'Rừng Tĩnh Lặng')
                    ch += 1
        if ch:
            json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            print(f'  {os.path.relpath(p, G)}: sua {ch}')
            n += ch
print(f'tong {n} cho')

if n:
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', 'build_ori_mod.py'),
                        '--src', r'E:\ORI_work\Data'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT)
    for l in ((r.stdout or '') + (r.stderr or '')).splitlines():
        if 'xong:' in l:
            print('  ' + l.strip()[:120])
