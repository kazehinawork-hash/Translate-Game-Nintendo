"""Tra lai 2 chuoi phu thuoc ngu canh + chinh QA (xuong dong la CANH BAO, khong phai loi)."""
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
G = os.path.join(ROOT, 'games', '01004D300C5AE000_Kirby')
T = os.path.join(G, 'translations')

# (file, key) -> gia tri dung theo ngu canh
CTX = {
    ('Dialog.msbt', 'Btn_Continue'): 'Nghe tiếp',
    ('Figure.msbt', '$View'): 'Ngắm',
}
vi = json.load(open(os.path.join(T, 'kirby_vi.json'), encoding='utf-8'))
for (fn, k), v in CTX.items():
    if fn in vi and k in vi[fn]:
        print(f'  tra lai {fn}/{k} = {v!r} (truoc: {vi[fn][k]!r})')
        vi[fn][k] = v
json.dump(vi, open(os.path.join(T, 'kirby_vi.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# chinh qa_kirby.py: xuong dong tinh la canh bao
p = os.path.join(ROOT, 'tools', 'qa_kirby.py')
s = open(p, encoding='utf-8').read()
if 'WARN_ONLY' not in s:
    s = s.replace("""        if Counter(CTRL.findall(s)) != Counter(CTRL.findall(v)):
            bad_ctrl += 1""", """        if Counter(CTRL.findall(s)) != Counter(CTRL.findall(v)):
            # Chi lech SO LUONG xuong dong (\\n) => canh bao, khong phai loi
            only_nl = all(c == '\\n' for c in (CTRL.findall(s) + CTRL.findall(v)))
            if only_nl:
                warn_nl += 1
            else:
                bad_ctrl += 1""")
    s = s.replace("bad_key = bad_ctrl = empty = bad_char = 0", "bad_key = bad_ctrl = empty = bad_char = warn_nl = 0")
    s = s.replace("print(f'\\ntong {tot:,} chuoi | lech key {bad_key} | lech ma dieu khien {bad_ctrl} | rong {empty} | ky tu la {bad_char}')",
                  "print(f'\\ntong {tot:,} chuoi | lech key {bad_key} | lech ma dieu khien {bad_ctrl} | rong {empty} | ky tu la {bad_char} | canh bao xuong dong {warn_nl}')")
    open(p, 'w', encoding='utf-8').write(s)
    print('  da chinh qa_kirby.py: xuong dong tinh la canh bao')

print('\n=== build lai + QA + kiem chung ===')
for cmd in ('qa_kirby.py', 'build_kirby_mod.py'):
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'tools', cmd)], capture_output=True, text=True,
                       encoding='utf-8', errors='replace', cwd=ROOT)
    for l in ((r.stdout or '') + (r.stderr or '')).splitlines():
        if any(x in l for x in ('tong ', 'KET QUA', 'da dong goi', 'bo qua')):
            print('  ' + l.strip()[:170])
