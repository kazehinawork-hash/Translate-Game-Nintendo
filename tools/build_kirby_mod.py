"""Dong goi mod Kirby and the Forgotten Land: thay chuoi MSBT bang tieng Viet.

- Vá cac khe ngon ngu LATIN (English/Phap/Duc/Y/Italiano/Tay Ban Nha/Ha Lan).
- GIU NGUYEN JP/CN/TW/KR (de nguoi choi cac khu vuc do khong bi loi font).
"""
import json
import os
import sys

sys.path.insert(0, r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\tools')
sys.stdout.reconfigure(encoding='utf-8')
from build_mod import replace_msbt_txt2

ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '01004D300C5AE000'
G = os.path.join(ROOT, 'games', f'{TID}_Kirby')
SRC = os.path.join(G, 'source', 'msg', 'Kirby15')
OUT = os.path.join(ROOT, 'output', 'atmosphere', 'contents', TID, 'romfs', 'msg', 'Kirby15')

LATIN = ['US_English', 'EU_English', 'US_French', 'US_Spanish', 'EU_French', 'EU_German',
         'EU_Italian', 'EU_Spanish', 'EU_Dutch']
SKIP = {'JP_Japanese', 'CN_Chinese', 'TW_Chinese', 'KR_Korean'}

vi = json.load(open(os.path.join(G, 'translations', 'kirby_vi.json'), encoding='utf-8'))

# Ngoai le theo NGU CANH (khong the thong nhat may moc).
# Ghi de ngay trong build de khong phu thuoc trang thai file nguon (OneDrive hay tra ban cu).
CTX_OVERRIDE = {
    'Dialog.msbt': {'Btn_Continue': 'Nghe tiếp'},
    'Figure.msbt': {'$View': 'Ngắm'},
}
for _f, _kv in CTX_OVERRIDE.items():
    vi.setdefault(_f, {}).update(_kv)
print(f'ban dich: {len(vi)} file MSBT, {sum(len(v) for v in vi.values()):,} chuoi '
      f'(+ {sum(len(v) for v in CTX_OVERRIDE.values())} ngoai le ngu canh)')

n_ok = n_skip = n_err = 0
for lang in sorted(os.listdir(SRC)):
    if lang in SKIP or not os.path.isdir(os.path.join(SRC, lang)):
        if lang in SKIP:
            print(f'  [giu nguyen] {lang}')
        continue
    src_lang = os.path.join(SRC, lang)
    out_lang = os.path.join(OUT, lang)
    for r, _, fs in os.walk(src_lang):
        for fn in fs:
            rel = os.path.relpath(os.path.join(r, fn), src_lang).replace('\\', '/')
            entries = vi.get(rel)
            if not entries:
                n_skip += 1
                continue
            orig = open(os.path.join(r, fn), 'rb').read()
            try:
                new = replace_msbt_txt2(orig, entries)
            except Exception as e:
                n_err += 1
                print(f'  LOI {lang}/{rel}: {type(e).__name__} {str(e)[:60]}')
                continue
            dst = os.path.join(out_lang, *rel.split('/'))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            open(dst, 'wb').write(new)
            n_ok += 1
print(f'\n{len(os.listdir(SRC))-len(SKIP)} khe ngon ngu Latin | {n_ok} file MSBT da dong goi | bo qua {n_skip} | loi {n_err}')
import subprocess
tot = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(OUT) for f in fs)
cnt = sum(len(fs) for _, _, fs in os.walk(OUT))
print(f'output: {cnt} file, {tot/1e6:.2f} MB -> {OUT}')
