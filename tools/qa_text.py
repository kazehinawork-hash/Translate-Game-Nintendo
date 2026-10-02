"""
qa_text.py — Cổng kiểm tra chất lượng (QA GATE) cho MỌI game trong dự án.

Đọc lại THÀNH PHẨM ĐÃ BUILD rồi so với nguồn gốc. Bắt 12 nhóm lỗi:
  1. Thiếu / thừa key                7. Mục [error:...] / [KEY]
  2. Chuỗi rỗng                      8. Thẻ <i> không đóng
  3. Ký tự lạ (CJK/Hangul/Kana/Ả Rập/Cyrillic)   9. \\n literal vs xuống dòng thật
  4. Lệch tag (<img>, <i>...)       10. Ký tự điều khiển / zero-width / BOM
  5. Lệch placeholder               11. Độ phủ font (--font)
  6. Ngoặc {} lệch                  12. SOÁT RÒ RỈ: text có trong file gốc mà CHƯA được trích (--leak)

Dùng:
    python tools/qa_text.py --game hogwarts
    python tools/qa_text.py --game ori --font tools/fonts_hades2/Lato-Regular.ttf
    python tools/qa_text.py --game hades2 --verbose
    python tools/qa_text.py --game switchsports
    python tools/qa_text.py --game ori --leak          # soát rò rỉ (chậm hơn)
"""
import argparse
import collections
import glob
import json
import os
import re
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))

TAG = re.compile(r'<[^>]{0,60}>')
# |plural(...) chỉ so PHẦN ĐÁNH DẤU (nội dung bên trong là bản dịch, được phép khác nguồn)
PH = re.compile(r'\{[^{}]{0,24}\}|%[sdf]|\[[A-Za-z_][A-Za-z0-9_]{2,}\]|\|plural\(')
# Một số game KHÔNG dùng cú pháp placeholder [...]:
#  - Switch Sports: '\x0e...' là mã điều khiển; '[None]' chỉ là NHÃN (dịch '[Không có]' là ĐÚNG)
#  - Hades II: dùng {$...} / {!Icons...} / {#Format}, không dùng [...]
NO_BRACKET_PH = {'Switch Sports (MSBT)', 'Hades II (SJSON)'}
PH_NO_BRACKET = re.compile(r'\{[^{}]{0,24}\}|%[sdf]|\|plural\(')
FOREIGN = re.compile(
    r'[\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff00-\uffef'
    r'\u1100-\u11ff\u3130-\u318f\uac00-\ud7ff\u3040-\u30ff'
    r'\u0600-\u06ff\ufb50-\ufdff\ufe70-\ufeff\u0400-\u04ff]')
BADCHAR = re.compile(r'[\u00a0\u200b\u200e\u200f\ufeff]')          # luôn là lỗi
# Mã điều khiển / glyph icon game — KHÔNG tính \t \n \r (xuống dòng so riêng ở XUONG_DONG_LECH)
CTRL = re.compile(r'[\u0000-\u0008\u000b\u000c\u000e-\u001f\ue000-\uf8ff]')
# Mức độ: lỗi này làm FAIL cổng QA. Các loại khác chỉ là CẢNH BÁO (không chặn bàn giao).
# CONTROL_CODE_LECH: khác mã điều khiển so với nguồn. Đã kiểm chứng thực tế ở Switch Sports:
# toàn bộ khác biệt là NGẮT DÒNG/TAG (0x0a, 0x0e…) chứ KHÔNG phải icon -> cần xem, không chặn.
WARN_KINDS = {'XUONG_DONG_LECH', 'RONG', 'THUA_KEY', 'RONG_NGUON_CUNG_RONG', 'CONTROL_CODE_LECH'}
# Các key ĐÃ VÁ CÓ CHỦ ĐÍCH: lệch placeholder so với nguồn là ĐÚNG (nguồn bị lỗi)
KNOWN_FIXED = {'Data_RefreshesIn', 'FGC_Collect_AstronomyTower',
               'FGC_Demiguise_AstronomyTower', 'ZSI_01'}


def check(name, src, built, font=None, verbose=False):
    errs = []
    ph = PH_NO_BRACKET if name in NO_BRACKET_PH else PH

    def add(kind, *detail):
        errs.append((kind, detail))

    built_files = {FILE_OF(k) for k in built}
    not_built = sorted({FILE_OF(k) for k in src if FILE_OF(k) not in built_files})
    if not_built:
        print(f'    (ghi chú: {len(not_built)} file nguồn không được build lại — bỏ qua: {not_built[:6]})')
    for k in set(src) - set(built):
        if FILE_OF(k) in built_files:
            add('THIEU_KEY', k)
    for k in list(set(built) - set(src))[:10]:
        add('THUA_KEY', k)

    untranslated = []
    for k, v in built.items():
        s = src.get(k)
        if not v.strip():
            # chi coi la LOI neu nguon co noi dung (nguon rong san thi bo qua)
            add('RONG' if (s is None or s.strip()) else 'RONG_NGUON_CUNG_RONG', k)
        # ky tu la: chi bao khi LA MOI so voi nguon
        new_foreign = [c for c in set(FOREIGN.findall(v)) if s is None or c not in s]
        if new_foreign:
            add('KY_TU_LA', k, new_foreign[:4], v[:60])
        new_bad = [c for c in set(BADCHAR.findall(v)) if c is None or s is None or c not in s]
        if new_bad:
            add('KY_TU_DIEU_KHIEN', k, [hex(ord(c)) for c in new_bad][:4])
        if s is not None and collections.Counter(CTRL.findall(s)) != collections.Counter(CTRL.findall(v)):
            add('CONTROL_CODE_LECH', k, len(CTRL.findall(s)), len(CTRL.findall(v)))
        if '[error:' in v:
            add('ERROR_TAG', k, v[:70])
        ph_only = re.fullmatch(r'\s*(\[[A-Za-z0-9_]+\]\s*)+', v)
        if ph_only and not re.fullmatch(r'\s*(\[[A-Za-z0-9_]+\]\s*)+', s or ''):
            add('KEY_CHUA_DICH', k, v[:70])
        # Ngoac: chi bao khi DO LECH khac nguon (nguon co the da lech san)
        if s is None:
            if v.count('{') != v.count('}'):
                add('NGOAC_LECH', k, v[:60])
        elif (v.count('{') - v.count('}')) != (s.count('{') - s.count('}')):
            add('NGOAC_LECH', k, s.count('{') - s.count('}'), v.count('{') - v.count('}'), v[:60])
        if v.count('<i>') != v.count('</i>'):
            add('THE_I_LECH', k, v[:60])
        if s is not None:
            if collections.Counter(TAG.findall(s)) != collections.Counter(TAG.findall(v)):
                add('TAG_LECH', k, collections.Counter(TAG.findall(s)), collections.Counter(TAG.findall(v)))
            if (collections.Counter(ph.findall(s)) != collections.Counter(ph.findall(v))
                    and k not in KNOWN_FIXED):
                add('PLACEHOLDER_LECH', k, collections.Counter(ph.findall(s)), collections.Counter(ph.findall(v)))
            if ('\\n' in s) != ('\\n' in v):
                add('BACKSLASH_N_LECH', k, s[:50], v[:50])
            if s.count('\n') != v.count('\n'):
                add('XUONG_DONG_LECH', k, s.count('\n'), v.count('\n'), v[:60])
            if v == s and len(v) >= 8 and len(v.split()) >= 2:
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
        for k in untranslated[:10]:
            print(f'      [chưa dịch] {k[:44]:44} {built[k][:70]!r}')
    kinds = collections.Counter(e[0] for e in errs)
    n_err = sum(n for kk, n in kinds.items() if kk not in WARN_KINDS)
    n_warn = sum(n for kk, n in kinds.items() if kk in WARN_KINDS)
    for kind, n in kinds.most_common():
        print(f'    [{"CẢNH BÁO" if kind in WARN_KINDS else "LỖI    "}] {kind}: {n}')
    if verbose:
        for e in errs[:20]:
            print('      ', e)
    return n_err, n_warn


# ============================ ADAPTERS ============================

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
    return [('Hogwarts MAIN', main_src,
             unpack_avafdict(open(os.path.join(SW, 'MAIN-enUS.bin'), 'rb').read())),
            ('Hogwarts SUB', sub_src,
             unpack_avafdict(open(os.path.join(SW, 'SUB-enUS.bin'), 'rb').read()))]


def _scan_unity(dirpath, keys=None):
    from unity_text_tool import parse_message
    import UnityPy
    out = {}
    for f in sorted(os.listdir(dirpath)):
        if not f.endswith('.unity3d'):
            continue
        try:
            env = UnityPy.load(os.path.join(dirpath, f))
        except Exception:
            continue
        for o in env.objects:
            if o.type.name != 'MonoBehaviour':
                continue
            k = f'{f}:{o.path_id}'
            if keys is not None and k not in keys:
                continue
            m = parse_message(o.get_raw_data())
            if m:
                out[k] = m[3]
    return out


def load_ori():
    G = os.path.join(ROOT, 'games', '01008DD013200000_OriAndTheWillOfTheWisps')
    OUT = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01008DD013200000', 'romfs', 'Data')
    ent = json.load(open(os.path.join(G, 'source', 'ori_text_all.json'), encoding='utf-8'))
    src = {f"{e['bundle']}:{e['path_id']}": e['english'] for e in ent}
    return [('Ori (Unity)', src, _scan_unity(OUT, set(src)))]


SJSON_ID = re.compile(r'\bId\s*=\s*"([^"]+)"')
SJSON_DN = re.compile(r'DisplayName\s*=\s*(?:"""(.*?)"""|"([^"]*)")', re.S)
FILE_OF = lambda k: k.split('::', 1)[0]


def _read_sjson_dir(dirpath):
    """Đọc SJSON. Quan trọng: chỉ tìm DisplayName TRONG KHOẢNG giữa 2 `Id` liên tiếp,
    nếu không sẽ gán nhầm DisplayName của entry sau cho entry trước."""
    out = {}
    for f in sorted(glob.glob(os.path.join(dirpath, '*.sjson'))):
        try:
            text = open(f, encoding='utf-8').read()
        except Exception:
            continue
        base = os.path.basename(f)
        ids = [(m.start(), m.group(1)) for m in SJSON_ID.finditer(text)]
        for i, (pos, name) in enumerate(ids):
            end = ids[i + 1][0] if i + 1 < len(ids) else len(text)
            m = SJSON_DN.search(text, pos, end)
            if not m:
                continue                      # entry ke thua, khong co DisplayName -> bo qua
            out[f'{base}::{name}'] = m.group(1) if m.group(1) is not None else (m.group(2) or '')
    return out


def load_obf():
    """Ori and the Blind Forest: Definitive Edition (Unity IL2CPP, BitmapFont)."""
    G = os.path.join(ROOT, 'games', '010061D00DB74000_OriAndTheBlindForest')
    OUT = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '010061D00DB74000', 'romfs', 'Data')
    ent = json.load(open(os.path.join(G, 'source', 'obf_text_all.json'), encoding='utf-8'))
    # _scan_unity() đặt khoá dạng "<tên_file>:<path_id>" -> nguồn phải khớp định dạng đó
    src = {f'data.unity3d:{e["path_id"]}': e['english'] for e in ent}
    return [('Ori Blind Forest (Unity)', src, _scan_unity(OUT, set(src)))]


def load_hades2():
    G = os.path.join(ROOT, 'games', '0100A00019DE0000_Hades2')
    OUT = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '0100A00019DE0000', 'romfs', 'Game', 'Text', 'en')
    src = _read_sjson_dir(os.path.join(G, 'source', 'raw_text', 'en'))
    built = _read_sjson_dir(OUT)
    return [('Hades II (SJSON)', src, built)]


def load_switchsports():
    from extract_msbt import parse_msbt_bytes
    import zstandard
    import oead
    G = os.path.join(ROOT, 'games', '0100D2F00D5C0000_SwitchSports')
    src_dir = os.path.join(G, 'source', 'raw_text_extracted', 'USen')
    src = {}
    for f in sorted(glob.glob(os.path.join(src_dir, '*.msbt.json'))):
        for k, v in json.load(open(f, encoding='utf-8')).items():
            src[f'{os.path.basename(f)[:-5]}::{k}'] = v

    sarc_path = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '0100D2F00D5C0000',
                             'romfs', 'Mals', 'USen.Product.150.sarc.zs')
    built = {}
    if os.path.exists(sarc_path):
        data = zstandard.ZstdDecompressor().decompress(open(sarc_path, 'rb').read())
        for fe in oead.Sarc(data).get_files():
            if not fe.name.endswith('.msbt'):
                continue
            for k, v in parse_msbt_bytes(bytes(fe.data)).items():
                built[f'{fe.name.replace("/", "__")}::{k}'] = v
    return [('Switch Sports (MSBT)', src, built)]


ADAPTERS = {'hogwarts': load_hogwarts, 'ori': load_ori, 'obf': load_obf,
            'hades2': load_hades2, 'switchsports': load_switchsports}


# ============================ SOÁT RÒ RỈ ============================
def leak_scan():
    """Quét bundle Unity tìm chuỗi giống CÂU nhưng KHÔNG nằm trong tập đã trích."""
    print('\n=== SOÁT RÒ RỈ (Ori) ===')
    import UnityPy
    G = os.path.join(ROOT, 'games', '01008DD013200000_OriAndTheWillOfTheWisps')
    ent = json.load(open(os.path.join(G, 'source', 'ori_text_all.json'), encoding='utf-8'))
    known = {e['english'] for e in ent}
    srcdir = os.environ.get('ORI_BUNDLES', '')
    if not os.path.isdir(srcdir):
        srcdir = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '01008DD013200000', 'romfs', 'Data')
        print('  (không có bundle gốc -> chỉ quét các bundle TRONG MOD)')
    CAND = re.compile(rb'[\x20-\x7e\xc0-\xff][\x20-\x7e\xc0-\xff\s]{29,300}')
    found = collections.Counter()
    samp = {}
    for i, f in enumerate(sorted(os.listdir(srcdir))):
        if not f.endswith('.unity3d'):
            continue
        try:
            env = UnityPy.load(os.path.join(srcdir, f))
        except Exception:
            continue
        seen = set()
        for o in env.objects:
            try:
                raw = o.get_raw_data()
            except Exception:
                continue
            for m in CAND.finditer(raw):
                try:
                    t = m.group(0).decode('utf-8').strip()
                except UnicodeDecodeError:
                    continue
                if '_' in t or t in known or t in seen or t.count(' ') < 4:
                    continue
                if re.search(r'[{};=<>\\|@^&*]|Variant|shader|Shader|Texture|HAS_|US_', t):
                    continue
                if not re.search(r'[a-z]{2,}', t) or sum(c.isalpha() or c == ' ' for c in t) / len(t) < 0.8:
                    continue
                seen.add(t)
                found[f] += 1
                samp.setdefault(f, t[:90])
    print(f'  bundle có câu nghi CHƯA TRÍCH: {len(found)} | tổng chuỗi: {sum(found.values())}')
    for f, n in found.most_common(10):
        print(f'    {f}: {n}  vd: {samp[f]!r}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--game', required=True, choices=sorted(ADAPTERS))
    ap.add_argument('--font', default=None)
    ap.add_argument('--verbose', action='store_true')
    ap.add_argument('--leak', action='store_true', help='soát rò rỉ text chưa được trích (chỉ Ori)')
    a = ap.parse_args()

    total = warns = 0
    for name, src, built in ADAPTERS[a.game]():
        e, w = check(name, src, built, font=a.font, verbose=a.verbose)
        total += e
        warns += w
    if a.leak and a.game == 'ori':
        leak_scan()

    print('\n' + '=' * 62)
    print('KẾT QUẢ:', 'PASS — mọi thứ êm ru' if total == 0 else f'FAIL — còn {total} LỖI, XEM CHI TIẾT Ở TRÊN')
    if warns:
        print(f'         (kèm {warns} cảnh báo — không chặn bàn giao, nên xem qua)')
    print('=' * 62)
    return 1 if total else 0


if __name__ == '__main__':
    raise SystemExit(main())
