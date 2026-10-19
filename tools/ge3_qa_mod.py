import os
import struct
import sys
import zlib

BOM = b"\xff\xfe"


def parse_pkh(path):
    raw = open(path, "rb").read()
    count = struct.unpack(">I", raw[:4])[0]
    entries = []
    off = 4
    for _ in range(count):
        entries.append(struct.unpack(">6I", raw[off:off + 24]))
        off += 24
    return entries


def read_entry(pk_path, entry):
    _, _, _, off, unc, comp = entry
    with open(pk_path, "rb") as f:
        f.seek(off)
        raw = f.read(comp if comp > 0 else unc)
    return zlib.decompress(raw) if comp > 0 else raw


def main():
    orig_dir = sys.argv[1]
    mod_dir = sys.argv[2]
    for stem in ("archive00", "archive01"):
        op = os.path.join(orig_dir, stem)
        mp = os.path.join(mod_dir, stem)
        if not os.path.exists(mp + ".pk"):
            print(stem, "SKIP (no mod file)")
            continue
        oe = parse_pkh(op + ".pkh")
        me = parse_pkh(mp + ".pkh")
        assert len(oe) == len(me), (stem, len(oe), len(me))
        size_mod = os.path.getsize(mp + ".pk")
        max_end = max((e[3] + (e[5] if e[5] else e[4])) for e in me)
        text_tables = 0
        translated_rows = 0
        rows = 0
        corrupt = 0
        for i, e in enumerate(me):
            data = read_entry(mp + ".pk", e)
            if data[:2] != BOM:
                continue
            if b"T\x00e\x00x\x00t\x00I\x00d" not in data[:20]:
                continue
            text_tables += 1
            try:
                txt = data[2:].decode("utf-16-le")
            except UnicodeDecodeError:
                corrupt += 1
                continue
            lines = txt.splitlines()
            for ln in lines[1:]:
                rows += 1
        print(stem, "entries", len(me), "pk_size", size_mod,
              "max_end", max_end, "text_tables", text_tables,
              "rows", rows, "corrupt_text", corrupt)


if __name__ == "__main__":
    main()
