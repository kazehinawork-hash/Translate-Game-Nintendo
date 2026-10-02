"""
fix_hogwarts_main_errors.py — Vá các mục MAIN bị lỗi hiển thị `[error:...]` / `[KEY]`.

Các mục này CÓ SẴN trong nguồn gốc (tiếng Trung cũng lỗi y hệt) nhưng vá được
vì key tham chiếu bị gõ sai/thiếu — suy ra giá trị đúng từ các key anh em:

  Category_Hair              [error:Menu_Hair]          -> 'Kiểu Tóc'  (Menu_Hairstyle)
  Category_Outfit            [error:Menu_Outfits]       -> 'Trang Phục' (Menu_Outfit)
  Category_Quests            [error:Menu_ActiveQuests]  -> 'Nhiệm Vụ Đang Thực Hiện' (MENU_ACTIVEQUEST)
  Data_RefreshesIn           '... [error:time]'         -> '{time}'   (Data_ExpiresIn dung {time})
  FGC_Collect_AstronomyTower '... [error:%d] ...'       -> '{0}'      (cac key FGC_* khac dung {0})
  FGC_Demiguise_AstronomyTower                          -> '{0}'
  Hamlet_Halkirk_CO_BB       [error:Hamelt_Halkirk]     -> 'Bainburgh' (FT_OL_HamletHalkirk_CO_BB)
  ZSI_01                     [ZSI_01_01_DADASide_Title] -> lay noi dung key do

Chạy: python tools/fix_hogwarts_main_errors.py   (rồi build lại MAIN + patch pak)
"""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TR = os.path.join(ROOT, 'games', '0100F7E00C70E000_Hogwarts', 'translations')

FIXES = {
    'Category_Hair': 'Kiểu Tóc',
    'Category_Outfit': 'Trang Phục',
    'Category_Quests': 'Nhiệm Vụ Đang Thực Hiện',
    'Data_RefreshesIn': 'Làm mới sau {time}',
    'FGC_Collect_AstronomyTower': 'Tìm {0} mẩu Kiến Thức',
    'FGC_Demiguise_AstronomyTower': 'Tìm {0} tượng Khỉ Tàng Hình Demiguise',
    'Hamlet_Halkirk_CO_BB': 'Bainburgh',
    'ZSI_01': 'Bài tập của Giáo sư Hecat 1',
}


def main():
    files = sorted(glob.glob(os.path.join(TR, 'translated_*.json')))
    done = set()
    for f in files:
        data = json.load(open(f, encoding='utf-8'))
        dirty = False
        for it in data:
            k = it.get('Key')
            if k in FIXES:
                it['Vietnamese'] = FIXES[k]
                done.add(k)
                dirty = True
        if dirty:
            json.dump(data, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            print(f'  sua {os.path.basename(f)}')
    left = {k: v for k, v in FIXES.items() if k not in done}
    if left:
        out = os.path.join(TR, 'translated_fixes_error.json')
        json.dump([{'Key': k, 'Vietnamese': v} for k, v in left.items()],
                  open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'  them file moi cho {len(left)} key: {os.path.basename(out)}')
    print(f'da va {len(done)}/{len(FIXES)} key')


if __name__ == '__main__':
    main()
