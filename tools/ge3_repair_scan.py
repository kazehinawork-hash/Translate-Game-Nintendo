import os
import re
import struct
import sys
import zlib

BOM = b"\xff\xfe"
TEXT_HEADER = b"T\x00e\x00x\x00t\x00I\x00d"

HAN_RANGES = [
    (0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xF900, 0xFAFF),
    (0x1100, 0x11FF), (0x3130, 0x318F), (0xAC00, 0xD7FF),
    (0x3040, 0x30FF), (0x0600, 0x06FF), (0x0400, 0x04FF),
]


def parse_pkh(path):
    raw = open(path, "rb").read()
    count = struct.unpack(">I", raw[:4])[0]
    return [struct.unpack(">6I", raw[4 + i * 24:4 + i * 24 + 24]) for i in range(count)]


def read_entry(pk_path, entry):
    _, _, _, off, unc, comp = entry
    with open(pk_path, "rb") as f:
        f.seek(off)
        raw = f.read(comp if comp > 0 else unc)
    return zlib.decompress(raw) if comp > 0 else raw


def has_han(text):
    for ch in text:
        cp = ord(ch)
        for lo, hi in HAN_RANGES:
            if lo <= cp <= hi:
                return True
    return False


def main():
    orig_dir, mod_dir, out_json = sys.argv[1], sys.argv[2], sys.argv[3]
    import json
    entries = parse_pkh(os.path.join(orig_dir, "archive00.pkh"))
    mod_entries = parse_pkh(os.path.join(mod_dir, "archive00.pkh"))
    need = {}
    blank = 0
    untrans = 0
    for i, (oe, me) in enumerate(zip(entries, mod_entries)):
        odata = read_entry(os.path.join(orig_dir, "archive00.pk"), oe)
        if odata[:2] != BOM or TEXT_HEADER not in odata[:20]:
            continue
        mdata = read_entry(os.path.join(mod_dir, "archive00.pk"), me)
        otext = odata[2:].decode("utf-16-le")
        mtext = mdata[2:].decode("utf-16-le")
        o_lines, m_lines = otext.splitlines(), mtext.splitlines()
        header = [c.strip().lstrip("\ufeff") for c in o_lines[0].split("\t")]
        if "TextId" not in header or "Text" not in header:
            continue
        idi, ti = header.index("TextId"), header.index("Text")
        for ol, ml in zip(o_lines[1:], m_lines[1:]):
            if not ol.strip():
                continue
            oc, mc = ol.split("\t"), ml.split("\t")
            if len(oc) <= ti or len(mc) <= ti:
                continue
            tid, src, dst = oc[idi], oc[ti], mc[ti]
            bad = False
            if src.strip() and not dst.strip():
                bad = True
                blank += 1
            elif has_han(dst):
                bad = True
                untrans += 1
            if bad and tid.strip():
                cur = need.get(tid)
                if cur is None or (not cur.strip() and src.strip()):
                    need[tid] = src
    print("blank defects", blank, "untranslated defects", untrans,
          "unique ids to repair", len(need))
    json.dump(need, open(out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("written", out_json)


if __name__ == "__main__":
    main()
