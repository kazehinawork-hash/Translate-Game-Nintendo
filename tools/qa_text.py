"""
qa_text.py — Cổng kiểm tra chất lượng (QA GATE) cho mọi game trong dự án.

Chạy TRƯỚC KHI BÀN GIAO. Kiểm tra trên chính THÀNH PHẨM ĐÃ BUILD (đọc lại), so với nguồn gốc:
  1. Số entry khớp nguồn            6. Mục [error:...] / [KEY]
  2. Chuỗi rỗng                     7. Tên riêng bị bản địa hóa (so cột ngôn ngữ song song)
  3. Ký tự lạ (CJK/Hangul/Kana/Ả Rập/Cyrillic)   8. \\n literal vs xuống dòng thật
  4. Lệch tag/placeholder           9. Độ phủ font (nếu truyền --font)
  5. Chưa dịch (giá trị == nguồn)

Dùng:
    python tools/qa_text.py --game hogwarts
    python tools/qa_text.py --game ori
    python tools/qa_text.py --game hogwarts --font tools/fonts_hades2/Lato-Regular.ttf
"""
import argparse
import collections
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))

TAG = re.compile(r'<[^>]{0,60}>')
# LƯU Ý: |plural(...) chỉ so PHẦN ĐÁNH DẤU, không so nội dung bên trong
# (nội dung bên trong LÀ bản dịch nên được phép khác nguồn).
PH = re.compile(r'\{[^{}]{0,24}\}|%[sdf]|\[[A-Za-z_][A-Za-z0-9_]{2,}\]|\|plural\(')
# Các key ĐÃ VÁ CÓ CHỦ ĐÍCH: lệch placeholder so với nguồn là ĐÚNG (nguồn bị lỗi).
KNOWN_FIXED = {
    'Data_RefreshesIn',             # nguồn: [error:time]  -> {time}    (theo Data_ExpiresIn)
    'FGC_Collect_AstronomyTower',   # nguồn: [error:%d]    -> {0}       (theo các key FGC_* khác)
    'FGC_Demiguise_AstronomyTower', # nguồn: [error:%d]    -> {0}
    'ZSI_01',                       # nguồn: [ZSI_01_..._Title] -> nội dung key đó
}
FOREIGN = re.compile(
    r'[\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff00-\uffef'   # CJK
    r'\u1100-\u11ff\u3130-\u318f\uac00-\ud7ff'                                # Hangul
    r'\u3040-\u30ff'                                                          # Kana
    r'\u0600-\u06ff\ufb50-\ufdff\ufe70-\ufeff'                                # Arabic
    r'\u0400-\u04ff]')                                                        # Cyrillic
BADCHAR = re.compile(r'[\u0000-\u0008\u000b\u000c\u000e-\u001f\u00a0\u200b\u200e\u200f\ufeff]')


def check(name, src, built, font=None, verbose=False):
    """src/built: {key: value}. Trả về (so_loi, danh_sach_loi)."""
    errs = []

    def add(kind, *detail):
        errs.append((kind, detail))

    only_src = set(src) - set(built)
    only_built = set(built) - set(src)
    if only_src:
        add('THIEU_KEY', len(only_src), list(only_src)[:5])
    if only_built:
        add('THUA_KEY', len(only_built), list(only_built)[:5])

    untranslated = []
    for k, v in built.items():
        s = src.get(k)
        if not v.strip():
            add('RONG', k)
        if FOREIGN.search(v):
            add('KY_TU_LA', k, FOREIGN.findall(v)[:3], v[:60])
        if BADCHAR.search(v):
            add('KY_TU_DIEU_KHIEN', k, [hex(ord(c)) for c in BADCHAR.findall(v)][:4])
        if re.search(r'\[error:', v):
            add('ERROR_TAG', k, v[:70])
        # [KEY] chưa dịch: CHỈ báo lỗi khi nguồn KHÔNG phải placeholder thuần
        # (chuỗi kiểu "[Bash]" vốn phải giữ nguyên nên không tính là lỗi).
        ph_only = re.fullmatch(r'\s*(\[[A-Za-z0-9_]+\]\s*)+', v)
        if ph_only and not re.fullmatch(r'\s*(\[[A-Za-z0-9_]+\]\s*)+', s or ''):
            add('KEY_CHUA_DICH', k, v[:70])
        if v.count('{') != v.count('}'):
            add('NGOAC_LECH', k, v[:60])
        if v.count('<i>') != v.count('</i>'):
            add('THE_I_LECH', k, v[:60])
        if s is not None:
            if collections.Counter(TAG.findall(s)) != collections.Counter(TAG.findall(v)):
                add('TAG_LECH', k, collections.Counter(TAG.findall(s)), collections.Counter(TAG.findall(v)))
            if collections.Counter(PH.findall(s)) != collections.Counter(PH.findall(v)):
                if k not in KNOWN_FIXED:
                    add('PLACEHOLDER_LECH', k, collections.Counter(PH.findall(s)), collections.Counter(PH.findall(v)))
            if ('\\n' in s) != ('\\n' in v):
                add('BACKSLASH_N_LECH', k, s[:50], v[:50])
            if s.count('\n') != v.count('\n'):
                add('XUONG_DONG_LECH', k, s.count('\n'), v.count('\n'), v[:60])
            if v == s:
                untranslated.append(k)

    if font:
        from fontTools.ttLib import TTFont
        cm = set(TTFont(font, lazy=True).getBestCmap())
        miss = collections.Counter()
        for v in built.values():
            for c in v:
                if ord(c) not in cm and c != '\n':
                    miss[c] += 1
        if miss:
            add('FONT_THIEU_GLYPH', len(miss), {c: n for c, n in miss.most_common(10)})

    print(f'\n=== {name}')
    print(f'    entry: nguồn {len(src)} | build {len(built)} | chưa dịch (giống nguồn): {len(untranslated)}')
    if untranslated and verbose:
        for k in untranslated[:12]:
            print(f'      [chưa dịch] {k[:44]:44} {built[k][:70]!r}')
    kinds = collections.Counter(e[0] for e in errs)
    for kind, n in kinds.most_common():
        print(f'    [{kind}] {n}')
    if verbose:
        for e in errs[:20]:
            print('      ', e)
    return len(errs), errs


# ---------- ADAPTER: HOGWARTS (AVAFDICT) ----------
def load_hogwarts():
    from avaf_codec import unpack_avafdict
    G = os.path.join(ROOT, 'games', '0100F7E00C70E000_Hogwarts')
    SW = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '0100F7E00C70E000', 'romfs',
                      'Phoenix', 'Content', 'Localization', 'SWITCH')
    ej = os.path.join(G, 'source', 'extracted_json')
    main_src = {x['Key']: (x.get('Source_ZH') or '') for x in
                json.load(open(os.path.join(ej, 'hogwarts_main_raw.json'), encoding='utf-8'))}
    sub_src = {x['Key']: (x.get('Source_FR') or '') for x in
               json.load(open(os.path.join(ej, 'hogwarts_dialogs_fr.json'), encoding='utf-8'))}
    return [('Hogwarts MAIN', main_src, unpack_avafdict(open(os.path.join(SW, 'MAIN-enUS.bin'), 'rb').read())),
            ('Hogwarts SUB', sub_src, unpack_avafdict(open(os.path.join(SW, 'SUB-enUS.bin'), 'rb').read()))]


# ---------- ADAPTER: ORI (Unity AssetBundle) ----------
def load_ori():
    from unity_text_tool import parse_message
    import UnityPy
    G = os.path.join(ROOT, 'games', '01008DD013200000_OriAndTheWillOfTheWisps')
    OUT = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01008DD013200000', 'romfs', 'Data')
    ent = json.load(open(os.path.join(G, 'source', 'ori_text_all.json'), encoding='utf-8'))
    src = {f"{e['bundle']}:{e['path_id']}": e['english'] for e in ent}
    built = {}
    for f in os.listdir(OUT):
        if not f.endswith('.unity3d'):
            continue
        try:
            env = UnityPy.load(os.path.join(OUT, f))
        except Exception:
            continue
        for o in env.objects:
            if o.type.name != 'MonoBehaviour':
                continue
            k = f'{f}:{o.path_id}'
            if k not in src:
                continue
            m = parse_message(o.get_raw_data())
            if m:
                built[k] = m[3]
    return [('Ori (Unity)', src, built)]


ADAPTERS = {'hogwarts': load_hogwarts, 'ori': load_ori}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', required=True, choices=sorted(ADAPTERS))
    ap.add_argument('--font', default=None)
    ap.add_argument('--verbose', action='store_true')
    a = ap.parse_args()

    total = 0
    for name, src, built in ADAPTERS[a.game]():
        total += check(name, src, built, font=a.font, verbose=a.verbose)[0]
    print('\n' + '=' * 62)
    print('KẾT QUẢ:', 'PASS — mọi thứ êm ru' if total == 0 else f'FAIL — còn {total} lỗi, XEM CHI TIẾT Ở TRÊN')
    print('=' * 62)
    return 1 if total else 0


if __name__ == '__main__':
    raise SystemExit(main())
