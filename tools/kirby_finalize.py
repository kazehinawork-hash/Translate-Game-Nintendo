"""Thong nhat not + build lai mod Kirby."""
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
G = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby')
T = os.path.join(G, 'translations')
en = json.load(open(os.path.join(T, 'kirby_en.json'), encoding='utf-8'))

print('=== ngu canh "Fish" / "Listen" / "Look" ===')
for fn, entries in en.items():
    for k, s in entries.items():
        if str(s).strip() in ('Fish', 'Listen', 'Look'):
            vi = json.load(open(os.path.join(T, 'kirby_vi.json'), encoding='utf-8'))
            print(f'  [{fn}/{k}] EN={str(s)!r} -> VI={str(vi.get(fn,{}).get(k,""))!r}')

REPL = [('Nghe tiếp', 'Nghe'), ('Ngắm', 'Nhìn'), ('Kẹo bất tử', 'Kẹo Bất Tử')]
for p in [os.path.join(T, 'kirby_vi.json')] + [os.path.join(T, f'vi_{i:02d}.json') for i in range(1, 11)]:
    if not os.path.exists(p):
        continue
    d = json.load(open(p, encoding='utf-8'))
    ch = 0
    if isinstance(d, dict):
        for fn, entries in d.items():
            for k, v in list(entries.items()):
                nv = str(v)
                for a, b in REPL:
                    nv = nv.replace(a, b)
                if nv != v:
                    entries[k] = nv
                    ch += 1
    else:
        for x in d:
            nv = str(x.get('vi', ''))
            for a, b in REPL:
                nv = nv.replace(a, b)
            if nv != x.get('vi', ''):
                x['vi'] = nv
                ch += 1
    if ch:
        json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'  {os.path.basename(p)}: sua {ch}')

print('\n=== QA lai + build lai + kiem chung ===')
for cmd in (['tools/qa_kirby.py'], ['tools/build_kirby_mod.py'], ['tools/final_check_kirby.py']):
    r = subprocess.run([sys.executable, os.path.join(ROOT, *cmd)], capture_output=True, text=True,
                       encoding='utf-8', errors='replace', cwd=ROOT)
    out = (r.stdout or '') + (r.stderr or '')
    keep = [l for l in out.splitlines() if any(x in l for x in
            ('KET QUA', 'lech', 'thieu chu dich', 'tong', 'da dong goi', 'PASS', 'KY TU'))]
    print(f'--- {cmd[0]} ---')
    for l in keep[:6]:
        print('  ' + l.strip()[:150])
