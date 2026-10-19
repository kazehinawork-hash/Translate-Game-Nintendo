import json
import os
import struct
import sys
import zlib

MAGICS = {
    b"OTTO": "OTTO/CFF",
    b"\x00\x01\x00\x00": "TTF",
    b"true": "TTF-true",
    b"typ1": "TTF-typ1",
    b"FFNT": "BFFNT",
    b"CFNT": "BCFNT",
    b"FONT": "FONT",
    b"XFNT": "XFNT",
}


def parse_pkh(path):
    raw = open(path, "rb").read()
    count = struct.unpack(">I", raw[:4])[0]
    return [struct.unpack(">6I", raw[4 + i * 24:4 + i * 24 + 24]) for i in range(count)]


def main():
    stem = sys.argv[1]
    out = sys.argv[2]
    entries = parse_pkh(stem + ".pkh")
    hits = []
    with open(stem + ".pk", "rb") as f:
        for i, (h, a, b, off, unc, comp) in enumerate(entries):
            f.seek(off)
            raw = f.read(comp if comp > 0 else unc)
            try:
                data = zlib.decompress(raw) if comp > 0 else raw
            except Exception:
                continue
            tag = MAGICS.get(data[:4])
            if not tag and data[:4] == b"\x00\x01\x00\x00":
                tag = "TTF"
            if tag:
                hits.append({"i": i, "magic": tag, "unc": len(data),
                             "head": data[:16].hex()})
            if i % 5000 == 0:
                print("scan", i, "hits", len(hits), flush=True)
    json.dump(hits, open(out, "w"), indent=1)
    print("total hits", len(hits))


if __name__ == "__main__":
    main()
