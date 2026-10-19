import os
import re
import struct
import sys
import zlib
from collections import Counter

BOM = b"\xff\xfe"
TEXT_HEADER = b"T\x00e\x00x\x00t\x00I\x00d"

HAN_ONLY = [
    (0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xF900, 0xFAFF),
    (0x3040, 0x30FF), (0x1100, 0x11FF), (0x3130, 0x318F),
    (0xAC00, 0xD7FF), (0x0600, 0x06FF), (0x0400, 0x04FF),
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


def han_only(text):
    n = 0
    for ch in text:
        cp = ord(ch)
        for lo, hi in HAN_ONLY:
            if lo <= cp <= hi:
                n += 1
                break
    return n


def split_like_builder(text):
    nl = "\r\n" if "\r\n" in text else "\n"
    return text.split(nl)


def main():
    orig_dir, mod_dir = sys.argv[1], sys.argv[2]
    entries = parse_pkh(os.path.join(orig_dir, "archive00.pkh"))
    mod_entries = parse_pkh(os.path.join(mod_dir, "archive00.pkh"))
    missing_tags = Counter()
    extra_tags = Counter()
    tag_rows = 0
    han_rows = 0
    han_total = 0
    line_bad = []
    id_bad = 0
    rows = 0
    for i, (oe, me) in enumerate(zip(entries, mod_entries)):
        odata = read_entry(os.path.join(orig_dir, "archive00.pk"), oe)
        if odata[:2] != BOM or TEXT_HEADER not in odata[:20]:
            continue
        mdata = read_entry(os.path.join(mod_dir, "archive00.pk"), me)
        otext = odata[2:].decode("utf-16-le")
        mtext = mdata[2:].decode("utf-16-le")
        ol = split_like_builder(otext)
        ml = split_like_builder(mtext)
        if len(ol) != len(ml):
            line_bad.append((i, len(ol), len(ml)))
            continue
        header = [c.strip().lstrip("\ufeff") for c in ol[0].split("\t")]
        if "TextId" not in header or "Text" not in header:
            continue
        idi, ti = header.index("TextId"), header.index("Text")
        for a, b in zip(ol[1:], ml[1:]):
            if not a.strip():
                continue
            rows += 1
            ac, bc = a.split("\t"), b.split("\t")
            if len(ac) <= ti or len(bc) <= ti:
                continue
            if ac[idi] != bc[idi]:
                id_bad += 1
            ot, nt = ac[ti], bc[ti]
            o_t, n_t = Counter(TAG_RE.findall(ot)), Counter(TAG_RE.findall(nt))
            if o_t != n_t:
                tag_rows += 1
                for k in (o_t - n_t):
                    missing_tags[k] += (o_t - n_t)[k]
                for k in (n_t - o_t):
                    extra_tags[k] += (n_t - o_t)[k]
            h = han_only(nt)
            if h:
                han_rows += 1
                han_total += h
    print("rows", rows, "line_bad", len(line_bad), line_bad[:10], "id_bad", id_bad)
    print("tag_rows", tag_rows)
    print("missing tags top:", missing_tags.most_common(15))
    print("extra tags top:", extra_tags.most_common(15))
    print("han_rows", han_rows, "han_total", han_total)


if __name__ == "__main__":
    main()
