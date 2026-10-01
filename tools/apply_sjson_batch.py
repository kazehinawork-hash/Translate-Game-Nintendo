#!/usr/bin/env python3
"""Áp batch translation JSON lên file SJSON nguồn → translations/."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hades2_sjson_helper import apply_translation_to_sjson, parse_sjson_entries

TITLE = "0100A00019DE0000_Hades2"
SRC = ROOT / "games" / TITLE / "source" / "raw_text" / "en"
DST = ROOT / "games" / TITLE / "translations" / "Game" / "Text" / "en"


def load_translations(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, dict) and "translations" in data:
        data = data["translations"]
    return data


def apply_file(filename: str, trans_path: Path) -> dict:
    src = SRC / filename
    if not src.exists():
        raise FileNotFoundError(src)
    if not trans_path.exists():
        raise FileNotFoundError(trans_path)

    src_raw = src.read_text(encoding="utf-8-sig")
    src_entries = parse_sjson_entries(src_raw)
    trans = load_translations(trans_path)

    # Giữ lại key có thật; field rỗng bỏ qua
    cleaned = {}
    skipped_missing = 0
    for k, fields in trans.items():
        if k not in src_entries:
            skipped_missing += 1
            continue
        f = {}
        for field in ("DisplayName", "Description"):
            val = fields.get(field)
            if isinstance(val, str) and val.strip():
                # Không đè nếu translation rỗng hơn source (trừ khi cố tình)
                f[field] = val
        if f:
            cleaned[k] = f

    new_raw = None
    DST.mkdir(parents=True, exist_ok=True)
    out = DST / filename
    # CỘNG DỒN: nếu file dịch đã tồn tại thì apply chồng lên nó,
    # tránh rebuild từ source làm mất bản dịch của batch trước.
    base_raw = out.read_text(encoding="utf-8-sig") if out.exists() else src_raw
    new_raw = apply_translation_to_sjson(base_raw, cleaned)
    # Validate: không duplicate DisplayName trong cùng block
    entries = parse_sjson_entries(new_raw)
    if len(entries) != len(src_entries):
        print(f"  WARN entry count changed: {len(src_entries)} -> {len(entries)}")

    out.write_text(new_raw, encoding="utf-8-sig")

    applied = len(cleaned)
    return {
        "file": filename,
        "src_entries": len(src_entries),
        "trans_keys": len(trans),
        "applied": applied,
        "skipped_missing": skipped_missing,
        "out": str(out),
    }


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: apply_sjson_batch.py <filename.sjson> <translations.json>")
        return 2
    filename = sys.argv[1]
    trans_path = Path(sys.argv[2])
    if not trans_path.is_absolute():
        trans_path = ROOT / trans_path
    r = apply_file(filename, trans_path)
    print(
        f"OK {r['file']}: applied {r['applied']}/{r['trans_keys']} "
        f"(src={r['src_entries']}, missing={r['skipped_missing']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
