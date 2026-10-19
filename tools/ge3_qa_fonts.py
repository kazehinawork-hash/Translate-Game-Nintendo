import io
import os
import struct
import sys
import zlib

from fontTools.ttLib import TTFont


def parse_pkh(path):
    raw = open(path, "rb").read()
    count = struct.unpack(">I", raw[:4])[0]
    return [struct.unpack(">6I", raw[4 + i * 24:4 + i * 24 + 24]) for i in range(count)]


def main():
    mod = sys.argv[1]
    mapping_path = sys.argv[2]
    import json
    mapping = json.load(open(mapping_path, encoding="utf-8"))
    need = set()
    for v in mapping.values():
        for ch in v:
            if ord(ch) > 0x7F:
                need.add(ord(ch))
    entries = parse_pkh(os.path.join(mod, "archive00.pkh"))
    indices = [1979, 2478, 3384, 5000, 5869, 6600, 17048, 17574, 18486,
               30187, 31492, 31998, 32916, 40351]
    for i in indices:
        _, _, _, off, unc, comp = entries[i]
        with open(os.path.join(mod, "archive00.pk"), "rb") as f:
            f.seek(off)
            raw = f.read(comp if comp > 0 else unc)
        data = zlib.decompress(raw) if comp > 0 else raw
        f = TTFont(io.BytesIO(data), lazy=True)
        cmap = set(f.getBestCmap())
        miss = [cp for cp in need if cp not in cmap]
        print(i, "size", len(data), "glyphs", f["maxp"].numGlyphs,
              "missing_needed", len(miss), "sample", [hex(c) for c in miss[:5]])


if __name__ == "__main__":
    main()
