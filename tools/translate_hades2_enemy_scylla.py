"""Apply all 461 translated strings of Scylla to _EnemyData_Scylla.en.sjson."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "working"))

from hades2_sjson_helper import apply_translation_to_sjson
from scylla_trans_part1 import translations_part1
from scylla_trans_part2 import translations_part2

SRC = ROOT / "working/0100A00019DE0000_Hades2/raw_text/en/_EnemyData_Scylla.en.sjson"
TARGET = ROOT / "translations/0100A00019DE0000_Hades2/Game/Text/en/_EnemyData_Scylla.en.sjson"

all_translations = {}
all_translations.update(translations_part1)
all_translations.update(translations_part2)

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    
    if TARGET.exists():
        current_text = TARGET.read_text(encoding="utf-8")
    else:
        current_text = SRC.read_text(encoding="utf-8-sig")
        
    entries_dict = {
        k: v if isinstance(v, dict) else {"DisplayName": v}
        for k, v in all_translations.items()
    }
    
    updated = apply_translation_to_sjson(current_text, entries_dict)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(updated, encoding="utf-8")
    print(f"Đã cập nhật thành công {len(entries_dict)} chuỗi cho Scylla vào: {TARGET}")

if __name__ == "__main__":
    main()
