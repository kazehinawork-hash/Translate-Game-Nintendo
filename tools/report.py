"""
report.py — Báo cáo tổng hợp TOÀN DỰ ÁN (1 lệnh biết hết).

Với mỗi game: số chuỗi, số đã dịch, tỉ lệ, kích thước mod, trạng thái cổng QA,
và tổng dung lượng. Không cần mở từng README.

Dùng:
    python tools/report.py                 # tất cả game
    python tools/report.py --game hogwarts
    python tools/report.py --md > BAO-CAO.md
"""
import argparse
import json
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))

GAMES = [('hogwarts', '0100F7E00C70E000', 'Hogwarts Legacy'),
         ('ori', '01008DD013200000', 'Ori and the Will of the Wisps'),
         ('hades2', '0100A00019DE0000', 'Hades II'),
         ('switchsports', '0100D2F00D5C0000', 'Nintendo Switch Sports')]

FOLDER = {
    'hogwarts': '0100F7E00C70E000_Hogwarts',
    'ori': '01008DD013200000_OriAndTheWillOfTheWisps',
    'hades2': '0100A00019DE0000_Hades2',
    'switchsports': '0100D2F00D5C0000_SwitchSports',
}


def dir_size(p):
    total = 0
    for r, _, fs in os.walk(p):
        for f in fs:
            try:
                total += os.path.getsize(os.path.join(r, f))
            except OSError:
                pass
    return total


def mb(n):
    return f'{n / 1024 / 1024:.1f} MB'


def qa_status(game):
    """Chạy cổng QA, trả (đã_pass, số_lỗi, cảnh_báo, ghi_chú)."""
    cmd = [sys.executable, 'tools/qa_text.py', '--game', game]
    if game == 'hogwarts':
        cmd += ['--font', 'tools/fonts_hades2/Lato-Regular.ttf']
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = (r.stdout or '') + (r.stderr or '')
    err = re.search(r'còn (\d+) LỖI', out)
    warn = re.search(r'kèm (\d+) cảnh báo', out)
    entries = re.search(r'entry: nguồn (\d+) \| build (\d+) \| chưa dịch \(giống nguồn\): (\d+)',
                        out)
    return (r.returncode == 0,
            int(err.group(1)) if err else 0,
            int(warn.group(1)) if warn else 0,
            entries)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', default=None)
    ap.add_argument('--md', action='store_true', help='xuất Markdown')
    ap.add_argument('--no-qa', action='store_true', help='bỏ qua cổng QA (nhanh hơn)')
    a = ap.parse_args()

    rows = []
    tot_mod = tot_src = 0
    for key, tid, name in GAMES:
        if a.game and a.game != key:
            continue
        mod = os.path.join(ROOT, 'output', 'atmosphere', 'contents', tid)
        src = os.path.join(ROOT, 'games', FOLDER[key])
        msize = dir_size(mod) if os.path.isdir(mod) else 0
        ssize = dir_size(src) if os.path.isdir(src) else 0
        tot_mod += msize
        tot_src += ssize
        ok, errs, warns, ent = (True, 0, 0, None)
        if not a.no_qa:
            ok, errs, warns, ent = qa_status(key)
        rows.append(dict(key=key, tid=tid, name=name, mod=msize, src=ssize,
                         qa_ok=ok, errs=errs, warns=warns, ent=ent))

    if a.md:
        print('# Báo cáo dự án Việt hóa Nintendo Switch\n')
        print('| Game | TitleID | Dung lượng mod | Dung lượng dữ liệu | QA |')
        print('|---|---|---|---|---|')
        for r in rows:
            qa = 'PASS' if r['qa_ok'] else f"FAIL ({r['errs']} lỗi)"
            print(f"| {r['name']} | `{r['tid']}` | {mb(r['mod'])} | {mb(r['src'])} | {qa} |")
        print(f"\n**Tổng thành phẩm:** {mb(tot_mod)} · **Tổng dữ liệu nguồn:** {mb(tot_src)}")
        return 0

    print('=' * 78)
    print('BÁO CÁO DỰ ÁN VIỆT HÓA NINTENDO SWITCH')
    print('=' * 78)
    for r in rows:
        print(f"\n▌ {r['name']}  ({r['tid']})")
        print(f"   mod: {mb(r['mod']):>10}   |   dữ liệu nguồn: {mb(r['src'])}")
        if r['ent']:
            n_src, n_build, n_un = r['ent'].groups()
            pct = (int(n_build) - int(n_un)) / max(int(n_build), 1) * 100
            print(f"   chuỗi: {n_build} (nguồn {n_src}) | đã dịch: {int(n_build) - int(n_un)} ({pct:.1f}%) | chưa dịch: {n_un}")
        if not a.no_qa:
            print(f"   cổng QA: {'✅ PASS' if r['qa_ok'] else '❌ FAIL ' + str(r['errs']) + ' lỗi'}"
                  + (f" | cảnh báo: {r['warns']}" if r['warns'] else ''))
    print('\n' + '=' * 78)
    print(f'TỔNG: thành phẩm {mb(tot_mod)} · dữ liệu nguồn {mb(tot_src)}')
    print('=' * 78)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
