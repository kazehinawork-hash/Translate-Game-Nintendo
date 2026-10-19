import os
import re
import struct
import sys
import unicodedata
import zlib

BOM = b"\xff\xfe"
TEXT_HEADER = b"T\x00e\x00x\x00t\x00I\x00d"

CJK_RANGES = [
    (0x3000, 0x303F), (0x3400, 0x4DBF), (0x4E00, 0x9FFF),
    (0xF900, 0xFAFF), (0xFF00, 0xFFEF),
    (0x1100, 0x11FF), (0x3130, 0x318F), (0xAC00, 0xD7FF),
    (0x3040, 0x30FF), (0x0600, 0x06FF), (0x0400, 0x04FF),
]

TAG_RE = re.compile(r"<[^>]*>|\{[^}]*\}|%[sd]|\[\[[^\]]*\]\]")


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


def cjk_count(text):
    n = 0
    for ch in text:
        cp = ord(ch)
        for lo, hi in CJK_RANGES:
            if lo <= cp <= hi:
                n += 1
                break
    return n


def tags(text):
    return sorted(TAG_RE.findall(text))


def main():
    orig_dir, mod_dir = sys.argv[1], sys.argv[2]
    entries = parse_pkh(os.path.join(orig_dir, "archive00.pkh"))
    mod_entries = parse_pkh(os.path.join(mod_dir, "archive00.pkh"))
    errors = []
    empties = 0
    tag_mismatch = 0
    cjk_new = 0
    tables = 0
    rows = 0
    for i, (oe, me) in enumerate(zip(entries, mod_entries)):
        odata = read_entry(os.path.join(orig_dir, "archive00.pk"), oe)
        if odata[:2] != BOM or TEXT_HEADER not in odata[:20]:
            continue
        mdata = read_entry(os.path.join(mod_dir, "archive00.pk"), me)
        if mdata[:2] != BOM:
            errors.append(f"entry {i}: no BOM in mod")
            continue
        try:
            otext = odata[2:].decode("utf-16-le")
            mtext = mdata[2:].decode("utf-16-le")
        except UnicodeDecodeError as e:
            errors.append(f"entry {i}: decode error {e}")
            continue
        tables += 1
        o_lines = otext.splitlines()
        m_lines = mtext.splitlines()
        if len(o_lines) != len(m_lines):
            errors.append(f"entry {i}: line count {len(o_lines)} -> {len(m_lines)}")
        header = [c.strip().lstrip("\ufeff") for c in o_lines[0].split("\t")]
        if "TextId" not in header or "Text" not in header:
            continue
        idi, ti = header.index("TextId"), header.index("Text")
        for ol, ml in zip(o_lines[1:], m_lines[1:]):
            if not ol.strip():
                continue
            rows += 1
            oc = ol.split("\t")
            mc = ml.split("\t")
            if len(oc) != len(mc):
                errors.append(f"entry {i}: col count row {oc[:1]}")
                continue
            if oc[idi] != mc[idi]:
                errors.append(f"entry {i}: id mismatch {oc[idi]} vs {mc[idi]}")
            src, dst = oc[ti], mc[ti]
            if src.strip() and not dst.strip():
                empties += 1
                errors.append(f"entry {i}: emptied {oc[idi]}")
            if tags(src) != tags(dst):
                tag_mismatch += 1
                if len(errors) < 50:
                    errors.append(f"entry {i}: tag mismatch {oc[idi]} {tags(src)} -> {tags(dst)}")
            new_cjk = cjk_count(dst) - cjk_count(src)
            if new_cjk > 0:
                cjk_new += 1
                if len(errors) < 50:
                    errors.append(f"entry {i}: new CJK {oc[idi]} {dst[:40]!r}")
    print("tables", tables, "rows", rows)
    print("emptied", empties, "tag_mismatch", tag_mismatch, "new_cjk", cjk_new,
          "errors", len(errors))
    for e in errors[:60]:
        print(" ", e)


if __name__ == "__main__":
    main()
