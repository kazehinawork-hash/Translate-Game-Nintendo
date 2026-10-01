"""
unity_text_tool.py — Bóc & vá text trong Unity AssetBundle (Ori and the Will of the Wisps).

Cấu trúc đã giải mã (kiểm chứng trên nhiều object):
    MonoBehaviour `TextMessageProvider` gồm:
        0x00  12 byte (PPtr + cờ)
        0x0C  int32  m_Enabled (1)
        0x10  int32  (1)
        0x14  int32  id
        0x18  8 byte
        0x20  int32  nameLen
        0x24  name (nameLen byte, kết thúc bằng "TextMessageProvider") + pad 4
        ...   int32 1 HOẶC 2 (cờ, thay đổi tuỳ loại message — CÓ THỂ KHÔNG CÓ)
        ...   int32 enLen
        ...   CHUỖI TIẾNG ANH (enLen byte) + pad 4
        ...   int32 1 (?) rồi mảng 20 ngôn ngữ khác (FR, IT, DE, ES, JA, PT, ZH-CN,
              RU, ZH-TW, CS, DA, NL, FI, HU, KO, NO, PL, ES-MX, SV, TR) — KHÔNG có tiếng Việt.

Chuỗi kiểu Unity: [int32 độ_dài][UTF-8][pad cho tròn 4 byte].

⇒ Cách Việt hóa: ghi tiếng Việt ĐÈ LÊN khe tiếng Anh (chơi ở ngôn ngữ English sẽ ra tiếng Việt).
   Patch = splice blob (bội số 4) + `ObjectReader.set_raw_data()` + `env.save(out_path=...)`.
   Đã kiểm chứng: số object trong bundle giữ nguyên.

Dùng (chạy từ gốc dự án):
    python tools/unity_text_tool.py scan  <bundle.unity3d> [--out list.json]
    python tools/unity_text_tool.py patch <bundle.unity3d> <map.json> <out_dir>
    python tools/unity_text_tool.py scan-all <thu_muc_bundle> --out all.json

map.json: {"<path_id>": "bản dịch tiếng Việt", ...}
Cần: pip install UnityPy
"""
import json
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
import UnityPy  # noqa: E402

NAME_OFF = 0x20
NAME_PTR = 0x24
NAME_TAIL = b'TextMessageProvider'


def _u32(b, i):
    return int.from_bytes(b[i:i + 4], 'little')


def _align4(n):
    return (n + 3) & ~3


def parse_message(raw):
    """Trả (name, en_prefix_off, en_len, english) nếu object là TextMessageProvider.

    Layout (đã kiểm chứng):
        [.. int32 nameLen][name .. "TextMessageProvider"][pad 4]
        [int32 1][int32 enLen][CHUỖI TIẾNG ANH][pad 4]
        [int32 1][mảng 20 ngôn ngữ khác]
    Định vị theo NỘI DUNG (đuôi tên) chứ không theo offset cố định, vì header mỗi object khác nhau.
    """
    idx = raw.find(NAME_TAIL)
    if idx < 0:
        return None
    name_end = idx + len(NAME_TAIL)
    # tìm điểm bắt đầu tên (lùi về trước, chỉ nhận ký tự in được)
    s = idx
    while s > 4:
        c = raw[s - 1]
        if 0x20 <= c < 0x7f or c in (0x5f, 0x2e, 0x2d):
            s -= 1
        else:
            break
    if s < 4:
        return None
    nlen = _u32(raw, s - 4)
    if nlen != name_end - s:
        return None
    name = raw[s:name_end].decode('utf-8', 'replace')
    pos = _align4(name_end)
    # Sau tên có thể là: [int32 cờ][int32 len][chuỗi]  HOẶC  [int32 len][chuỗi]
    # (giá trị cờ thay đổi tuỳ loại message: 1, 2, ...). Thử lần lượt.
    for delta in (4, 0):
        p = pos + delta
        if p + 4 > len(raw):
            continue
        ln = _u32(raw, p)
        if not (1 <= ln <= 4000) or p + 4 + ln > len(raw):
            continue
        try:
            text = raw[p + 4:p + 4 + ln].decode('utf-8')
        except UnicodeDecodeError:
            continue
        if not text.isprintable() or not any(ch.isalpha() for ch in text):
            continue
        return name, p, ln, text
    return None


def _blob(text):
    b = text.encode('utf-8')
    out = struct.pack('<I', len(b)) + b
    while len(out) % 4:
        out += b'\x00'
    return out


def scan_bundle(path):
    env = UnityPy.load(path)
    out = []
    for o in env.objects:
        if o.type.name != 'MonoBehaviour':
            continue
        try:
            raw = o.get_raw_data()
        except Exception:
            continue
        m = parse_message(raw)
        if m:
            name, off, ln, en = m
            out.append({'path_id': o.path_id, 'name': name, 'english': en})
    return out


def patch_bundle(path, mapping, out_dir, pack='original'):
    env = UnityPy.load(path)
    done = 0
    for o in env.objects:
        if o.type.name != 'MonoBehaviour':
            continue
        key = str(o.path_id)
        if key not in mapping:
            continue
        raw = o.get_raw_data()
        m = parse_message(raw)
        if not m:
            continue
        _name, off, ln, _en = m
        old_total = _align4(4 + ln)
        new_raw = raw[:off] + _blob(mapping[key]) + raw[off + old_total:]
        o.set_raw_data(new_raw)
        done += 1
    os.makedirs(out_dir, exist_ok=True)
    env.save(pack=pack, out_path=out_dir)
    return done


def patch_font(path, name_to_ttf, out_dir, pack='original'):
    """Thay TTF nhúng trong Font asset (Unity dynamic font) bằng font tiếng Việt.

    name_to_ttf: {'Candara': '<duong/dan/Lato-Regular.ttf>', ...}
    """
    env = UnityPy.load(path)
    done = []
    for o in env.objects:
        if o.type.name != 'Font':
            continue
        try:
            d = o.read()
        except Exception:
            continue
        nm = getattr(d, 'm_Name', '')
        if nm not in name_to_ttf:
            continue
        ttf = open(name_to_ttf[nm], 'rb').read()
        d.m_FontData = ttf
        d.save()
        done.append(nm)
    if done:
        os.makedirs(out_dir, exist_ok=True)
        env.save(pack=pack, out_path=out_dir)
    return done


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    cmd = sys.argv[1].lower()
    if cmd == 'scan':
        entries = scan_bundle(sys.argv[2])
        out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
        if out:
            json.dump(entries, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            print(f'{len(entries)} muc -> {out}')
        else:
            print(f'{len(entries)} muc')
            for e in entries[:5]:
                print('  ', e['path_id'], e['name'], '|', e['english'][:70])
    elif cmd == 'scan-all':
        src = sys.argv[2]
        all_e = []
        files = [f for f in sorted(os.listdir(src)) if f.endswith('.unity3d')]
        for i, f in enumerate(files):
            try:
                for e in scan_bundle(os.path.join(src, f)):
                    e['bundle'] = f
                    all_e.append(e)
            except Exception as ex:
                print('  loi', f, ex)
            if (i + 1) % 50 == 0:
                print(f'  {i+1}/{len(files)} ({len(all_e)} muc)', flush=True)
        out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else 'ori_text_all.json'
        json.dump(all_e, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'tong {len(all_e)} muc -> {out}')
    elif cmd == 'patch':
        mapping = json.load(open(sys.argv[3], encoding='utf-8'))
        done = patch_bundle(sys.argv[2], mapping, sys.argv[4])
        print(f'da va {done} object')
    else:
        print(__doc__)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
