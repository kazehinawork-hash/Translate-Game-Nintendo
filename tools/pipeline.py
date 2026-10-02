"""
pipeline.py — Chạy TRỌN quy trình build cho một game, dừng ngay nếu có bước lỗi.

Mục đích: chống lại lỗi nặng nhất của dự án (build thiếu/sai bước rồi tưởng là xong).
Mỗi game là một DANH SÁCH BƯỚC có thứ tự; bước nào trả mã lỗi khác 0 thì DỪNG NGAY,
không chạy tiếp, và không chạy cổng QA (vì thành phẩm đã sai).

Dùng:
    python tools/pipeline.py hogwarts
    python tools/pipeline.py ori
    python tools/pipeline.py hades2
    python tools/pipeline.py switchsports
    python tools/pipeline.py all              # chạy lần lượt cả 4 game
    python tools/pipeline.py hogwarts --only qa      # chỉ chạy 1 bước (theo tên)
    python tools/pipeline.py hogwarts --list         # xem các bước
"""
import argparse
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable

# (tên bước, lệnh) — chạy tuần tự theo đúng thứ tự này
PIPELINES = {
    'hogwarts': [
        ('build MAIN (UI/menu/HUD)', [PY, 'tools/build_hogwarts_mod.py']),
        ('build SUB (hội thoại)', [PY, 'tools/build_hogwarts_sub.py']),
        ('vá lỗi hiển thị MAIN', [PY, 'tools/fix_hogwarts_main_errors.py']),
        ('sửa tên bị bản địa hóa', [PY, 'tools/fix_hogwarts_fr_names.py']),
        ('build lại MAIN sau khi sửa', [PY, 'tools/build_hogwarts_mod.py']),
        ('đóng patch pak', [PY, 'tools/build_patch_pak.py']),
        ('font tiếng Việt', [PY, 'tools/check_font_coverage.py',
                            'tools/fonts_hades2/Lato-Regular.ttf',
                            'output/atmosphere/contents/0100F7E00C70E000/romfs/Phoenix/Content/Localization/SWITCH/MAIN-enUS.bin',
                            'output/atmosphere/contents/0100F7E00C70E000/romfs/Phoenix/Content/Localization/SWITCH/SUB-enUS.bin']),
        ('CỔNG QA', [PY, 'tools/qa_text.py', '--game', 'hogwarts',
                     '--font', 'tools/fonts_hades2/Lato-Regular.ttf']),
        ('kiểm tra glossary + nhất quán', [PY, 'tools/check_glossary.py', '--game', 'hogwarts']),
    ],
    'ori': [
        ('build bundle text', [PY, 'tools/build_ori_mod.py']),
        ('vá font (thay + hợp nhất)', [PY, 'tools/patch_font_ori.py']),
        ('CỔNG QA', [PY, 'tools/qa_text.py', '--game', 'ori']),
        ('kiểm tra glossary + nhất quán', [PY, 'tools/check_glossary.py', '--game', 'ori']),
    ],
    'hades2': [
        ('sửa lỗi QA (ngoặc/chữ lạ)', [PY, 'tools/fix_hades2_qa_bugs.py']),
        ('build mod', [PY, 'tools/build_hades2_mod.py']),
        ('font XNB', [PY, 'tools/patch_hades2_xnb_font.py']),
        ('CỔNG QA', [PY, 'tools/qa_text.py', '--game', 'hades2']),
        ('kiểm tra glossary + nhất quán', [PY, 'tools/check_glossary.py', '--game', 'hades2']),
    ],
    'switchsports': [
        ('font BFARC (CHỈ font Latin)', [PY, 'tools/build_custom_font.py']),
        ('build MSBT/SARC', [PY, 'tools/build_mod.py']),
        ('CỔNG QA', [PY, 'tools/qa_text.py', '--game', 'switchsports']),
        ('kiểm tra glossary + nhất quán', [PY, 'tools/check_glossary.py', '--game', 'switchsports']),
    ],
}


def run(name, cmd, dry=False):
    print(f'\n──── [{name}] {" ".join(cmd)}')
    if dry:
        return 0
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        print(f'\n❌ DỪNG: bước "{name}" lỗi (mã {r.returncode}). KHÔNG chạy tiếp, KHÔNG bàn giao.')
    return r.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('game', help='hogwarts | ori | hades2 | switchsports | all')
    ap.add_argument('--only', default=None, help='chỉ chạy bước có tên chứa chuỗi này')
    ap.add_argument('--list', action='store_true', help='chỉ liệt kê các bước')
    ap.add_argument('--dry', action='store_true', help='in lệnh, không chạy')
    a = ap.parse_args()

    games = list(PIPELINES) if a.game == 'all' else [a.game]
    if a.game not in PIPELINES and a.game != 'all':
        print('game không hợp lệ. Chọn:', ', '.join(PIPELINES))
        return 2

    failed = []
    for g in games:
        steps = PIPELINES[g]
        print(f'\n{"=" * 62}\n### PIPELINE: {g}  ({len(steps)} bước)\n{"=" * 62}')
        for name, cmd in steps:
            if a.list:
                print(f'  - {name}')
                continue
            if a.only and a.only.lower() not in name.lower():
                continue
            if run(f'{g} · {name}', cmd, dry=a.dry) != 0:
                failed.append(f'{g} · {name}')
                break
        if a.list:
            continue

    if a.list:
        return 0
    print('\n' + '=' * 62)
    if failed:
        print('KẾT QUẢ: ❌ THẤT BẠI ở:', ', '.join(failed))
    else:
        print('KẾT QUẢ: ✅ TẤT CẢ BƯỚC + CỔNG QA ĐÃ PASS — sẵn sàng chép vào thẻ nhớ.')
    print('=' * 62)
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
