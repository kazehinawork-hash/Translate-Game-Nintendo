"""Align unambiguous existing Hades II term usages with glossary/hades2.csv."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from hades2_sjson_helper import parse_sjson_entries  # noqa: E402

SOURCE = ROOT / "working/0100A00019DE0000_Hades2/raw_text/en"
TRANSLATIONS = ROOT / "translations/0100A00019DE0000_Hades2/Game/Text/en"

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPLACEMENTS = [
    ("Ân Huệ Song Tinh", "Ân Huệ Kép"),
    ("Song Tinh", "Ân Huệ Kép"),
    ("Đầu Lộn", "Đầu Lâu Bạc"),
    ("Quả Cầu Sức Mạnh Cực Đại", "Siêu Lựu Tăng Cường"),
    ("Quả Cầu Sức Mạnh Đại Lực", "Đại Lựu Tăng Cường"),
    ("Quả Cầu Sức Mạnh", "Lựu Tăng Cường"),
    ("Đại Khắc Kích", "Tấn Công Omega"),
    ("Đại Đặc Kỹ", "Đặc Kỹ Omega"),
    ("Đại Vòng Phép", "Vòng Phép Omega"),
    ("CỎ ASPHODEL", "ASPHODEL"),
    ("Cỏ Asphodel", "Asphodel"),
    ("NÂNG PHẩm", "NÂNG PHẨM"),
]


def align_infusion(source_text: str, translated_text: str) -> str:
    if not re.search(r"\binfusion\b|\binfused\b", source_text, re.I):
        return translated_text
    translated_text = translated_text.replace("Hòa Tan Nguyên Tố", "Truyền Nguyên Tố")
    translated_text = translated_text.replace("Siêu Hòa Tan", "Siêu Truyền Nguyên Tố")
    translated_text = translated_text.replace("{#ElementalFormat}Hòa Tan{#Prev}", "{#ElementalFormat}Truyền Nguyên Tố{#Prev}")
    translated_text = translated_text.replace("Sinh Lực Tối Đa Hòa Tan:", "Sinh lực tối đa nhờ truyền nguyên tố:")
    translated_text = translated_text.replace("Cơ Hội Né Hòa Tan:", "Tỉ lệ né nhờ truyền nguyên tố:")
    return translated_text


changed_files = 0
changed_fields = 0
for target_path in sorted(TRANSLATIONS.glob("*.sjson")):
    source_path = SOURCE / target_path.name
    if not source_path.exists():
        continue
    source_entries = parse_sjson_entries(source_path.read_text(encoding="utf-8-sig"))
    target_entries = parse_sjson_entries(target_path.read_text(encoding="utf-8-sig"))
    raw = target_path.read_text(encoding="utf-8-sig")
    file_changed = False
    # These terms are unique, fixed glossary equivalents and safe to replace as raw text.
    for old, new in REPLACEMENTS:
        if old in raw:
            raw = raw.replace(old, new)
            file_changed = True

    # Infusion has grammatical forms; replace only where source confirms this mechanic.
    for entry_id, fields in target_entries.items():
        original = source_entries.get(entry_id, {})
        for field in ("DisplayName", "Description"):
            source_text = original.get(field)
            translated_text = fields.get(field)
            if not isinstance(source_text, str) or not isinstance(translated_text, str):
                continue
            revised = align_infusion(source_text, translated_text)
            if revised == translated_text:
                continue
            # Translation strings in this project are plain SJSON field contents;
            # replace the exact field value while retaining its quote style.
            block = re.search(
                rf'(\{{\s*Id\s*=\s*"{re.escape(entry_id)}".*?\n\s*\}})', raw, re.S
            )
            if not block:
                continue
            body = block.group(1)
            value_re = re.compile(
                rf'({field}\s*=\s*)(?:"""(.*?)"""|"((?:[^"\\]|\\.)*)")', re.S
            )
            match = value_re.search(body)
            if not match or match.group(2) is not None:
                # Triple-quoted source fields retain physical line layout; only handle
                # them if the replacement is length neutral around the changed token.
                if not match:
                    continue
                content = match.group(2)
                if content is None:
                    continue
                revised_content = align_infusion(source_text, content)
                if revised_content == content:
                    continue
                replacement = match.group(1) + '"""' + revised_content + '"""'
            else:
                replacement = match.group(1) + '"' + revised + '"'
            new_body = body[:match.start()] + replacement + body[match.end():]
            raw = raw[:block.start(1)] + new_body + raw[block.end(1):]
            file_changed = True
            changed_fields += 1

    if file_changed:
        target_path.write_text(raw, encoding="utf-8")
        changed_files += 1

print(f"Đã đồng bộ thuật ngữ trong {changed_fields} trường và {changed_files} file.")
