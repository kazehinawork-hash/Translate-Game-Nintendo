"""
Thống nhất tên riêng / thuật ngữ Hades II theo danh sách games/_consistency/hades2.json.

Quy trình:
  1. Gom nhóm "cùng câu nguồn EN -> nhiều bản dịch" bằng cách đối chiếu
     games/<TID>_Hades2/source/raw_text/en/*.sjson  với  translations/Game/Text/en/*.sjson.
  2. Mỗi mục trong danh sách consistency được quyết định GIỮ NGUYÊN (khác ngữ cảnh)
     hay THỐNG NHẤT về một bản dịch chuẩn.
     - GIỮ NGUYÊN khi: các biến thể khác nhau về đại từ xưng hô (quan hệ nhân vật),
       khi là cặp "tên đầy đủ vs tên ngắn" (_Short), hoặc theo bảng ghi đè OVERRIDE.
     - THỐNG NHẤT: chọn biến thể nhiều chỗ nhất (hòa -> chuỗi dài hơn -> alphabet);
       bản dịch lỗi encoding ('?' thay ký tự tiếng Việt) luôn bị loại khỏi ứng viên.
  3. Chỉ sửa trường DisplayName, và chỉ trong khoảng giữa 2 `Id` liên tiếp của đúng
     những Id thuộc nhóm -> không gán nhầm sang entry khác.

Dùng:
    python tools/harmonize_hades2_consistency.py            # xem trước (dry-run)
    python tools/harmonize_hades2_consistency.py --apply    # ghi thật
Sau khi ghi: chạy `python tools/build_hades2_mod.py` rồi `python tools/qa_text.py --game hades2`.
"""
from __future__ import annotations

import collections
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TITLE_ID = "0100A00019DE0000"
GAME = os.path.join(ROOT, "games", f"{TITLE_ID}_Hades2")
SRC = os.path.join(GAME, "source", "raw_text", "en")
TR = os.path.join(GAME, "translations", "Game", "Text", "en")
TERMS = os.path.join(ROOT, "games", "_consistency", "hades2.json")

sys.path.insert(0, os.path.join(ROOT, "tools"))
from hades2_sjson_helper import _iter_text_blocks, parse_sjson_entries  # noqa: E402

# Ký tự tiếng Việt bị thay bằng '?' (bản dịch lỗi encoding) — luôn thay bằng bản sạch.
MOJI = re.compile(r"\?[a-zà-ỹ]|\?\?")
# Đại từ xưng hô -> khác nhau là do QUAN HỆ NHÂN VẬT, phải giữ nguyên.
ADDR = {"ngươi", "người", "mày", "mi", "cậu", "bạn", "em", "muội", "con", "cháu", "cô", "tỷ",
        "tỉ", "huynh", "ngài", "chị", "anh", "tao", "tớ", "tôi", "chàng", "nàng", "nó", "hắn"}

# Ghi đè thủ công cho các mục đã rà soát bằng tay (theo chỉ số trong hades2.json).
OVERRIDE = {
    5: "KEEP", 6: "KEEP", 7: "KEEP", 8: "KEEP",   # Adamant/Kudos/Rubbish/Plankton: tên đầy đủ vs ngắn
    13: "KEEP",                                    # Horror: tên quái vật vs tên kỹ năng (khác khái niệm)
    20: "KEEP",                                    # Orchestration: mục credits vs tên kỹ năng
    25: "KEEP",                                    # Syncing Cross-Save Data: 4 trạng thái hộp thoại khác nhau
    12: "Con Mắt Hắc Ám",                          # Evil Eye (kỷ vật Nemesis)
    19: "Đội ngũ thực hiện",                        # Credits
    30: "Chronos phải chết.",                       # Death to Chronos.
    164: "Con Mắt Đêm...",                         # khớp glossary "Eye of Night = Con Mắt Đêm"
}

FIELD = re.compile(r'(DisplayName\s*=\s*)(?:"""(.*?)"""|"((?:[^"\\]|\\.)*)")', re.S)


def read_display(dirpath: str) -> dict:
    out = {}
    for name in sorted(os.listdir(dirpath)):
        if not name.endswith(".sjson"):
            continue
        with open(os.path.join(dirpath, name), encoding="utf-8-sig") as fh:
            for eid, fields in parse_sjson_entries(fh.read()).items():
                if isinstance(fields.get("DisplayName"), str):
                    out[(name, eid)] = fields["DisplayName"].strip()
    return out


def tokens(text: str) -> set:
    return {t for t in re.findall(r"[0-9A-Za-zÀ-ỹ]+", text.lower())}


def decide(src_disp: dict, tr_disp: dict) -> list:
    groups = collections.defaultdict(list)
    for (f, i), en in src_disp.items():
        if en:
            groups[en].append((f, i))
    with open(TERMS, encoding="utf-8") as fh:
        items = json.load(fh)
    rows = []
    for n, it in enumerate(items):
        members = [(f, i, tr_disp.get((f, i))) for (f, i) in groups.get(it["en"], [])]
        members = [m for m in members if m[2] is not None]
        cnt = collections.Counter(m[2] for m in members)
        variants = [(v, c, [f"{f}::{i}" for (f, i, vv) in members if vv == v])
                    for v, c in cnt.most_common()]
        clean = [t for t in variants if not MOJI.search(t[0])]
        dirty = [v for v, c, e in variants if MOJI.search(v)]
        if len(variants) <= 1 and not dirty:
            continue                                   # đã nhất quán, không cần xử lý
        if OVERRIDE.get(n) == "KEEP":
            rows.append({"n": n, "en": it["en"], "canonical": None,
                         "why": "ghi đè: khác ngữ cảnh", "variants": variants})
            continue
        if n in OVERRIDE:
            rows.append({"n": n, "en": it["en"], "canonical": OVERRIDE[n], "why": "ghi đè",
                         "variants": variants})
            continue
        if len({frozenset(tokens(v) & ADDR) for v, c, e in clean}) > 1:
            rows.append({"n": n, "en": it["en"], "canonical": None,
                         "why": "khác đại từ xưng hô (quan hệ nhân vật)", "variants": variants})
            continue
        if any("_Short" in e for v, c, ex in variants for e in ex):
            rows.append({"n": n, "en": it["en"], "canonical": None,
                         "why": "tên đầy đủ vs tên ngắn (_Short)", "variants": variants})
            continue
        canon = sorted(clean, key=lambda t: (-t[1], -len(t[0]), t[0]))[0][0]
        rows.append({"n": n, "en": it["en"], "canonical": canon, "why": "cùng khái niệm",
                     "variants": variants})
    return rows


def apply(src_disp: dict, rows: list, dry: bool) -> tuple:
    canon = {r["en"]: r["canonical"] for r in rows if r["canonical"]}
    n_edit = n_files = 0
    for name in sorted(os.listdir(TR)):
        if not name.endswith(".sjson"):
            continue
        path = os.path.join(TR, name)
        with open(path, encoding="utf-8", newline="") as fh:
            raw = fh.read()
        bom = raw.startswith("\ufeff")
        if bom:
            raw = raw[1:]
        new_raw = raw
        for eid, full, body, start, end in reversed(list(_iter_text_blocks(raw))):
            want = canon.get(src_disp.get((name, eid), ""))
            if want is None:
                continue
            m = FIELD.search(body)
            if not m:
                continue
            if m.group(2) is not None:
                cur, rep = m.group(2), m.group(1) + '"""' + want + '"""'
            else:
                cur = m.group(3)
                rep = m.group(1) + '"' + want.replace("\\", "\\\\").replace('"', '\\"') + '"'
            if cur == want:
                continue
            prefix = len(full) - 1 - len(body)          # phần '{ Id = "..."'
            new_full = full[:prefix] + body[:m.start()] + rep + body[m.end():] + "}"
            new_raw = new_raw[:start] + new_full + new_raw[end + 1:]
            n_edit += 1
        if new_raw != raw:
            n_files += 1
            if not dry:
                with open(path, "w", encoding="utf-8", newline="") as fh:
                    fh.write(("\ufeff" if bom else "") + new_raw)
    return n_edit, n_files


def main() -> None:
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    dry = "--apply" not in sys.argv
    src_disp, tr_disp = read_display(SRC), read_display(TR)
    rows = decide(src_disp, tr_disp)
    unify = [r for r in rows if r["canonical"]]
    keep = [r for r in rows if not r["canonical"]]
    n_edit, n_files = apply(src_disp, rows, dry)
    print(f"{'DRY-RUN' if dry else 'ĐÃ GHI'}: {len(unify)} mục thống nhất | "
          f"{len(keep)} mục giữ nguyên (khác ngữ cảnh) | {n_edit} trường DisplayName trong {n_files} file")
    for r in unify[:20]:
        print(f"   #{r['n']:<3} {r['en']!r:<40} -> {r['canonical']!r}")


if __name__ == "__main__":
    main()
