"""
Công cụ xử lý, bóc tách và đóng gói file SJSON cho Hades II (Nintendo Switch).
Bảo toàn nguyên vẹn format, comment, indentation và các control tag ({#...}, {!...}, {CN}...).
"""
import re


TQ = '"' * 3


def _find_block_end(s: str, start: int) -> int:
    """
    start = index của '{' mở block. Trả về index của '}' đóng block tương ứng,
    xét string escapes, ngoặc lồng nhau (tag {CN} trong "..."), và triple-quote.
    """
    depth = 0
    i = start
    n = len(s)
    in_str = False
    in_triple = False
    while i < n:
        ch = s[i]
        if in_triple:
            if s.startswith(TQ, i):
                in_triple = False
                i += 3
                continue
            if ch == '\\':
                i += 2
                continue
            i += 1
            continue
        if in_str:
            if ch == '\\':
                i += 2
                continue
            if ch == '"':
                in_str = False
        else:
            if s.startswith(TQ, i):
                in_triple = True
                i += 3
                continue
            if ch == '"':
                in_str = True
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return -1


def _iter_text_blocks(sjson_content: str):
    """
    Duyệt từng block object trong mảng Texts.
    Yield (entry_id, full_block, body, start, end)
    - body = phần sau field Id đến trước '}' đóng.
    """
    for m in re.finditer(r'\{\s*Id\s*=\s*"([^"]+)"', sjson_content):
        entry_id = m.group(1)
        brace_start = m.start()
        brace_end = _find_block_end(sjson_content, brace_start)
        if brace_end < 0:
            continue
        full_block = sjson_content[brace_start:brace_end + 1]
        id_field = re.match(r'\{\s*Id\s*=\s*"[^"]+"', full_block)
        body_start = id_field.end()
        body = full_block[body_start:-1]
        yield entry_id, full_block, body, brace_start, brace_end


def parse_sjson_entries(sjson_content: str) -> dict:
    """
    Trích xuất { Id: { DisplayName?, Description?, Speaker?, ... } } từ nội dung SJSON.
    """
    entries = {}
    triple_re = re.compile(
        rf'(DisplayName|Description)\s*=\s*{TQ}(.*?){TQ}', re.S
    )
    single_re = re.compile(
        r'(DisplayName|Description|Speaker|Style|Sound)\s*=\s*"((?:[^"\\]|\\.)*)"'
    )
    for entry_id, _full, body, _s, _e in _iter_text_blocks(sjson_content):
        data = {'Id': entry_id}
        for fm in triple_re.finditer(body):
            data[fm.group(1)] = fm.group(2)
        for fm in single_re.finditer(body):
            if fm.group(1) not in data:
                data[fm.group(1)] = fm.group(2)
        entries[entry_id] = data
    return entries


def _escape_val(val: str) -> str:
    return (
        val.replace('\\', '\\\\')
        .replace('"', '\\"')
        .replace('\n', '\\n')
        .replace('\r', '\\r')
        .replace('\t', '\\t')
    )


def apply_translation_to_sjson(original_sjson: str, translations: dict) -> str:
    """
    Thay DisplayName / Description trong original_sjson theo translations.
    Giữ nguyên comment, indentation, tag điều khiển. Không sinh duplicate key.
    """
    if not translations:
        return original_sjson

    blocks = list(_iter_text_blocks(original_sjson))
    for entry_id, full_block, body, start, end in reversed(blocks):
        if entry_id not in translations:
            continue
        trans = translations[entry_id]
        new_body = body
        changed = False

        for field in ('DisplayName', 'Description'):
            if field not in trans or trans[field] is None:
                continue
            val_raw = trans[field]
            triple_re = re.compile(rf'{field}\s*=\s*{TQ}(.*?){TQ}', re.S)
            tm = triple_re.search(new_body)
            if tm:
                new_body = (
                    new_body[:tm.start()]
                    + f'{field} = {TQ}{val_raw}{TQ}'
                    + new_body[tm.end():]
                )
                changed = True
                continue
            val = _escape_val(val_raw)
            field_re = re.compile(rf'{field}\s*=\s*"((?:[^"\\]|\\.)*)"')
            fm = field_re.search(new_body)
            if fm:
                new_body = (
                    new_body[:fm.start()]
                    + f'{field} = "{val}"'
                    + new_body[fm.end():]
                )
                changed = True
            else:
                insert = f'\n      {field} = "{val}"'
                stripped = new_body.rstrip()
                trail = new_body[len(stripped):]
                new_body = (stripped + insert + trail) if trail else (new_body + insert)
                changed = True

        if changed:
            m_id = re.match(r'(\{\s*Id\s*=\s*"[^"]+")', full_block)
            prefix = m_id.group(1)
            new_full = prefix + new_body + '}'
            original_sjson = (
                original_sjson[:start] + new_full + original_sjson[end + 1:]
            )

    return original_sjson
