"""Translate all 271 strings of Zeus in Hades II."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "games" / "0100A00019DE0000_Hades2" / "source"))

from hades2_sjson_helper import apply_translation_to_sjson
from zeus_trans_part1 import translations_part1
from zeus_trans_part2 import translations_part2

SRC = ROOT / "games/0100A00019DE0000_Hades2/source/raw_text/en/_LootData_Zeus.en.sjson"
OUT = ROOT / "games/0100A00019DE0000_Hades2/translations/Game/Text/en/_LootData_Zeus.en.sjson"

all_translations = {}
all_translations.update(translations_part1)
all_translations.update(translations_part2)

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    source_raw = SRC.read_text(encoding="utf-8")
    entries_dict = {
        k: v if isinstance(v, dict) else {"DisplayName": v}
        for k, v in all_translations.items()
    }
    updated_raw = apply_translation_to_sjson(source_raw, entries_dict)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(updated_raw, encoding="utf-8")
    print(f"Đã dịch và lưu thành công {len(entries_dict)} chuỗi của Zeus vào: {OUT}")

if __name__ == "__main__":
    main()
