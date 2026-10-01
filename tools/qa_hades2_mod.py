"""
QA tổng mod Hades II: đảm bảo mọi thứ hoạt động êm ru.
1. Mọi file SJSON trong translations/ parse OK, không duplicate field trong block.
2. Multiset tag {...} của mỗi DisplayName/Description dịch khớp 100% với source.
3. translations/ và output/romfs/ đồng bộ (mod mới nhất).
4. Font XNB đã patch tồn tại đầy đủ.
5. Báo cáo tiến độ DN dịch.
Chạy từ root: python tools/qa_hades2_mod.py
"""
import re
import struct
import sys
from collections import Counter
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from hades2_sjson_helper import parse_sjson_entries, _iter_text_blocks  # noqa: E402
from patch_hades2_xnb_font import VIETNAMESE_ALL  # noqa: E402

SRC = ROOT / 'working/0100A00019DE0000_Hades2/raw_text/en'
TR = ROOT / 'translations/0100A00019DE0000_Hades2/Game/Text/en'
OUT = ROOT / 'output/atmosphere/contents/0100A00019DE0000/romfs'
FONT_OUT = OUT / 'Fonts/bin'
TAG_RE = re.compile(r'\{[^{}]*\}')
# Formatting/control tokens that must remain byte-for-byte equivalent to source.
FORMAT_RE = re.compile(r'\{[^{}]*\}|<[^<>]*>|%\d*(?:\$)?[sdif]|(?:\\+n|\\+t)')
UI_FILES = {'ScreenText.en.sjson', 'ShellText.en.sjson'}
length_flags = []
unchanged_prose = Counter()
legacy_terms = {
    'Đầu Lộn', 'Song Tinh', 'Quả Cầu Sức Mạnh', 'Đại Khắc Kích',
    'Đại Đặc Kỹ', 'Đại Vòng Phép', 'Cỏ Asphodel', 'Hòa Tan Nguyên Tố',
    'Siêu Hòa Tan', 'NÂNG PHẩm',
}
legacy_hits = []

errors = []
warnings = []


def read_7bit(data: bytes, offset: int) -> tuple[int, int]:
    value = shift = 0
    while True:
        if offset >= len(data) or shift > 28:
            raise ValueError('invalid 7-bit integer')
        byte = data[offset]
        offset += 1
        value |= (byte & 0x7F) << shift
        if byte < 0x80:
            return value, offset
        shift += 7


def check_xnb(path: Path) -> list[str]:
    """Check patched XNB structure and Vietnamese glyph coverage."""
    problems = []
    data = path.read_bytes()
    rel = path.relative_to(FONT_OUT)
    if len(data) < 30 or data[:3] != b'XNB' or data[4] != 6:
        return [f'{rel}: invalid XNB header/version']
    declared_size = struct.unpack_from('<I', data, 6)[0]
    if declared_size != len(data):
        problems.append(f'{rel}: declared size {declared_size} != {len(data)}')
    _fmt, _width, _height, _mips, pixel_len = struct.unpack_from('<IIIII', data, 10)
    offset = 30 + pixel_len
    if pixel_len <= 0 or offset > len(data):
        return problems + [f'{rel}: invalid/truncated atlas']
    try:
        glyph_count, offset = read_7bit(data, offset)
        offset += glyph_count * 16
        crop_count, offset = read_7bit(data, offset)
        offset += crop_count * 16
        char_count, offset = read_7bit(data, offset)
        chars = []
        for _ in range(char_count):
            if offset >= len(data):
                raise ValueError('truncated character table')
            first = data[offset]
            char_len = 1 if first < 0x80 else 2 if first & 0xE0 == 0xC0 else 3 if first & 0xF0 == 0xE0 else 4
            chars.append(data[offset:offset + char_len].decode('utf-8'))
            offset += char_len
        offset += 12  # line spacing, spacing, font size
        kern_count, offset = read_7bit(data, offset)
        offset += kern_count * 12
        if max(glyph_count, crop_count, char_count, kern_count) != min(glyph_count, crop_count, char_count, kern_count):
            problems.append(f'{rel}: glyph/crop/character/kerning counts differ')
        if len(chars) != len(set(chars)):
            problems.append(f'{rel}: duplicate characters')
        missing = sorted(set(VIETNAMESE_ALL) - set(chars))
        if missing:
            problems.append(f'{rel}: missing Vietnamese glyphs: ' + ''.join(missing))
        if offset > len(data):
            problems.append(f'{rel}: truncated font data')
    except (IndexError, UnicodeDecodeError, ValueError, struct.error) as exc:
        problems.append(f'{rel}: malformed glyph tables ({exc})')
    return problems


def tags(s: str) -> Counter:
    return Counter(TAG_RE.findall(s or ''))


def visible_text(s: str) -> str:
    return FORMAT_RE.sub('', s or '').replace('\\n', ' ').replace('\\t', ' ').strip()


def main() -> int:
    tr_files = sorted(TR.glob('*.sjson'))
    if not tr_files:
        print('FAIL: khong co file dich nao')
        return 1

    total_src = 0
    total_vi = 0
    # Đếm tổng source 1 lần
    src_cache = {}
    for f in sorted(SRC.glob('*.sjson')):
        se = parse_sjson_entries(f.read_text(encoding='utf-8-sig'))
        src_cache[f.name] = se
        total_src += sum(1 for v in se.values() if (v.get('DisplayName') or '').strip())

    for f in tr_files:
        raw = f.read_text(encoding='utf-8-sig')
        # 1. parse + duplicate field
        try:
            te = parse_sjson_entries(raw)
        except Exception as e:  # noqa: BLE001
            errors.append(f'{f.name}: parse FAIL {e}')
            continue
        for _eid, _full, body, _s, _e in _iter_text_blocks(raw):
            for field in ('DisplayName', 'Description'):
                n = len(re.findall(rf'{field}\s*=', body))
                if n > 1:
                    errors.append(f'{f.name}: block {_eid} co {n} {field}')
        # 2. tag check vs source
        se = src_cache.get(f.name, {})
        for k, v in te.items():
            s = se.get(k, {})
            if (v.get('DisplayName') or '') != (s.get('DisplayName') or ''):
                total_vi += 1
            for field in ('DisplayName', 'Description'):
                if tags(v.get(field)) != tags(s.get(field)):
                    # Chỉ báo khi key tồn tại ở source
                    if k in se:
                        errors.append(f'{f.name}:{k} lech tag {field}')
                if k in se and Counter(FORMAT_RE.findall(v.get(field) or '')) != Counter(FORMAT_RE.findall(s.get(field) or '')):
                    errors.append(f'{f.name}:{k} lech control/placeholder {field}')
                # Flag possible UI overflow; actual fit depends on layout and font metrics.
                if f.name in UI_FILES and field == 'DisplayName':
                    source_text = visible_text(s.get(field) or '')
                    translated_text = visible_text(v.get(field) or '')
                    if len(source_text) >= 5 and len(translated_text) >= 16 and len(translated_text) >= 1.5 * len(source_text):
                        length_flags.append((len(translated_text) / len(source_text), f'{f.name}:{k}', len(source_text), len(translated_text), translated_text))
                source_text = s.get(field) or ''
                translated_text = v.get(field) or ''
                if (re.search(r'\bclear(?:s|ed|ing)?\b', source_text, re.I)
                        and re.search(r'bount|trial', source_text, re.I)
                        and re.search(r'thu\s+dọn', translated_text, re.I)):
                    errors.append(f'{f.name}:{k} dùng sai “Clear” trong ngữ cảnh thử thách')
                if source_text and translated_text == source_text:
                    prose = FORMAT_RE.sub(' ', source_text).replace('\\n', ' ').replace('\\t', ' ')
                    words = re.findall(r'[A-Za-z]{3,}', prose)
                    if len(words) >= 3 and sum(map(len, words)) >= 18:
                        unchanged_prose[f.name] += 1
        # 3. đồng bộ output/
        of = OUT / 'Game/Text/en' / f.name
        if not of.exists():
            warnings.append(f'{f.name}: chua co trong output/romfs (chua build?)')
        elif of.read_bytes() != (TR / f.name).read_bytes():
            warnings.append(f'{f.name}: output/romfs LECH translations/ (can build lai)')

    # 4. font
    font_files = list(FONT_OUT.rglob('*.xnb')) if FONT_OUT.exists() else []
    for font in font_files:
        errors.extend(check_xnb(font))
    for f in tr_files:
        content = f.read_text(encoding='utf-8-sig')
        for term in legacy_terms:
            if term in content:
                legacy_hits.append(f'{f.name}: còn thuật ngữ cũ “{term}”')
    errors.extend(legacy_hits)
    print(f'--- QA Hades II ---')
    print(f'File dịch: {len(tr_files)}/180 | DN: {total_vi}/{total_src} ({total_vi * 100 / max(total_src, 1):.1f}%)')
    print(f'Font XNB output: {len(font_files)}')
    unchanged_total = sum(unchanged_prose.values())
    if unchanged_total:
        print(f'Potential untranslated English prose (heuristic): {unchanged_total} fields in {len(unchanged_prose)} files')
        for filename, count in unchanged_prose.most_common(12):
            print(f'  [U] {filename}: {count}')
    if length_flags:
        print(f'UI length flags (heuristic only; inspect in game): {len(length_flags)}')
        for ratio, key, source_len, translated_len, text in sorted(length_flags, reverse=True)[:20]:
            print(f'  [L] {key}: {source_len}->{translated_len} ({ratio:.1f}x) {text[:100]}')
    if errors:
        print(f'ERRORS ({len(errors)}):')
        for e in errors[:30]:
            print('  [E]', e)
    if warnings:
        print(f'WARNINGS ({len(warnings)}):')
        for w in warnings[:20]:
            print('  [W]', w)
    if not errors and not warnings:
        print('OK - moi thu em ru.')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
