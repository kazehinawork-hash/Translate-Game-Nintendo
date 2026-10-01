"""
unity_text_tool.py — Bóc & vá text trong Unity AssetBundle (Ori and the Will of the Wisps).

Bối cảnh kỹ thuật (đã kiểm chứng trên Ori):
  - Engine Unity IL2CPP; text nằm trong `Data/data_*.unity3d` (bundle nén, file RỜI trong RomFS
    → LayeredFS thay được, không cần patch pak).
  - Mỗi đoạn hội thoại là 1 MonoBehaviour `TextMessageProvider`. Chuỗi lưu kiểu Unity:
        [int32 độ_dài][UTF-8 bytes][pad 0..3 cho tròn 4 byte]
  - Thứ tự ngôn ngữ: TIẾNG ANH là 1 chuỗi riêng, ngay sau đó là mảng 19 ngôn ngữ khác
    (Ý, Đức, TBN, Nhật, Bồ, Trung giản, Nga, Trung phồn, Séc, Đan, Hà, Phần, Hung, Hàn,
     Na Uy, Ba Lan, TBN-Mỹ, Thụy Điển, Thổ). KHÔNG có tiếng Việt.
  - Vì vậy: ghi tiếng Việt ĐÈ LÊN khe tiếng Anh → chơi ở ngôn ngữ English sẽ ra tiếng Việt.
  - Patch = splice byte (blob mới vẫn là bội số 4) + `ObjectReader.set_raw_data()` + `env.save()`
    → UnityPy tự cập nhật kích thước/offset. Đã kiểm chứng: object count giữ nguyên.

Cách dùng (chạy từ gốc dự án):
    python tools/unity_text_tool.py scan  <bundle.unity3d> [--out out.json]
    python tools/unity_text_tool.py patch <bundle.unity3d> <map.json> <out_dir>

map.json: {"<path_id>": "bản dịch tiếng Việt", ...}
"""
import json
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
import UnityPy  # noqa: E402

MIN_RUN = 10          # số chuỗi tối thiểu để coi là mảng đa ngôn ngữ
MAX_RUN = 40
LOOKBACK = 120        # số byte tìm ngược để bắt chuỗi tiếng Anh đứng trước mảng


def _u32(b, i):
    return int.from_bytes(b[i:i + 4], 'little')


def _read_string(raw, pos):
    """Đọc 1 chuỗi Unity tại `pos` (pos trỏ tới length prefix). Trả (giá_trị, vị_trí_sau_khi_căn)."""
    if pos + 4 > len(raw):
        return None, pos
    ln = _u32(raw, pos)
    if not (1 <= ln <= 4000) or pos + 4 + ln > len(raw):
        return None, pos
    try:
        s = raw[pos + 4:pos + 4 + ln].decode('utf-8')
    except UnicodeDecodeError:
        return None, pos
    if not s.isprintable():
        return None, pos
    end = pos + 4 + ln
    return s, (end + 3) & ~3


def _find_runs(raw, min_n=MIN_RUN):
    """Tìm mọi dãy >= min_n chuỗi Unity liên tiếp."""
    runs, i = [], 0
    while i < len(raw) - 8:
        strs, pos = [], i
        while len(strs) < MAX_RUN:
            s, nxt = _read_string(raw, pos)
            if s is None:
                break
            strs.append((pos, s))
            pos = nxt
        if len(strs) >= min_n:
            runs.append((i, strs))
            i = pos
            continue
        i += 1
    return runs


def _langish(strs):
    """Lọc bớt dãy rác: phải có ít nhất 1 chuỗi dài kèm khoảng trắng."""
    return any(len(s) > 12 and ' ' in s and not s.startswith('/') for _, s in strs)


def _preceding_string(raw, run_start):
    """Chuỗi (tiếng Anh) đứng ngay trước mảng đa ngôn ngữ, trong khoảng LOOKBACK byte."""
    best = None
    for p in range(max(0, run_start - LOOKBACK), run_start):
        s, nxt = _read_string(raw, p)
        if s is not None and nxt <= run_start:
            best = (p, s)
    return best


def scan(path):
    env = UnityPy.load(path)
    out = []
    for o in env.objects:
        if o.type.name != 'MonoBehaviour':
            continue
        try:
            raw = o.get_raw_data()
        except Exception:
            continue
        for start, strs in _find_runs(raw):
            if not _langish(strs):
                continue
            pre = _preceding_string(raw, start)
            out.append({
                'path_id': o.path_id,
                'run_offset': start,
                'english_offset': pre[0] if pre else None,
                'english': pre[1] if pre else None,
                'other_langs': [s for _, s in strs],
            })
            break
    return out


def patch(path, mapping, out_dir):
    env = UnityPy.load(path)
    done = 0
    for o in env.objects:
        if o.type.name != 'MonoBehaviour':
            continue
        key = str(o.path_id)
        if key not in mapping:
            continue
        raw = o.get_raw_data()
        runs = [r for r in _find_runs(raw) if _langish(r[1])]
        if not runs:
            continue
        start, _strs = runs[0]
        pre = _preceding_string(raw, start)
        if not pre:
            continue
        p, _old = pre
        val = mapping[key].encode('utf-8')
        blob = struct.pack('<I', len(val)) + val
        while len(blob) % 4:
            blob += b'\x00'
        new_raw = raw[:p] + blob + raw[p + 4 + len(_old.encode('utf-8')) + ((4 - (len(_old.encode('utf-8')) % 4)) % 4):]
        # chuỗi cũ chiếm (4 + len) căn lên bội 4
        old_len = 4 + len(_old.encode('utf-8'))
        old_padded = (old_len + 3) & ~3
        new_raw = raw[:p] + blob + raw[p + old_padded:]
        o.set_raw_data(new_raw)
        done += 1
    os.makedirs(out_dir, exist_ok=True)
    saved = env.save(pack='none', out_path=out_dir)
    return done, saved


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    cmd = sys.argv[1].lower()
    if cmd == 'scan':
        entries = scan(sys.argv[2])
        out = None
        if '--out' in sys.argv:
            out = sys.argv[sys.argv.index('--out') + 1]
        if out:
            json.dump(entries, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            print(f'{len(entries)} muc -> {out}')
        else:
            print(f'{len(entries)} muc')
            for e in entries[:10]:
                print('  ', e['path_id'], repr(e['english'])[:80])
    elif cmd == 'patch':
        mapping = json.load(open(sys.argv[3], encoding='utf-8'))
        done, saved = patch(sys.argv[2], mapping, sys.argv[4])
        print(f'da va {done} object; file luu: {saved}')
    else:
        print(__doc__)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
