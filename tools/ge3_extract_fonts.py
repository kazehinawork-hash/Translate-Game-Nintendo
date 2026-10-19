import json
import os
import struct
import sys
import zlib

VI_CHARS = ("ăâđêôơư" + "ĂÂĐÊÔƠƯ" +
            "áàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ" +
            "ÁÀẢÃẠẮẰẲẴẶẤẦẨẪẬÉÈẺẼẸẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌỐỒỔỖỘỚỜỞỠỢÚÙỦŨỤỨỪỬỮỰÝỲỶỸỴ")


def parse_pkh(path):
    raw = open(path, "rb").read()
    count = struct.unpack(">I", raw[:4])[0]
    return [struct.unpack(">6I", raw[4 + i * 24:4 + i * 24 + 24]) for i in range(count)]


def read_entry(pk, entry):
    _, _, _, off, unc, comp = entry
    with open(pk, "rb") as f:
        f.seek(off)
        raw = f.read(comp if comp > 0 else unc)
    return zlib.decompress(raw) if comp > 0 else raw


def main():
    stem = sys.argv[1]
    indices = [int(x) for x in sys.argv[2].split(",")]
    outdir = sys.argv[3]
    os.makedirs(outdir, exist_ok=True)
    entries = parse_pkh(stem + ".pkh")
    from fontTools.ttLib import TTFont
    for i in indices:
        data = read_entry(stem + ".pk", entries[i])
        ext = ".otf" if data[:4] == b"OTTO" else ".ttf"
        p = os.path.join(outdir, f"{i:06d}{ext}")
        open(p, "wb").write(data)
        try:
            f = TTFont(p, fontNumber=0, lazy=True)
            cmap = f.getBestCmap()
            miss = [c for c in VI_CHARS if ord(c) not in cmap]
            name = ""
            for rec in f["name"].names:
                if rec.nameID in (4, 1):
                    try:
                        name = rec.toUnicode()
                        break
                    except Exception:
                        pass
            print(i, ext, "glyphs", len(cmap), "vi_missing", len(miss),
                  "name", name[:60], "units", f["head"].unitsPerEm,
                  "CFF", "CFF " in f)
        except Exception as e:
            print(i, ext, "ERROR", e)


if __name__ == "__main__":
    main()
