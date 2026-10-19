import glob
import json
import os
import sys

from fontTools.ttLib import TTFont

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
from add_glyphs_glyf import add_glyphs_glyf
from rebuild_cff_font import rebuild

VI_EXTRA = (
    "ăâđêôơưĂÂĐÊÔƠƯ"
    "áàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ"
    "ÁÀẢÃẠẮẰẲẴẶẤẦẨẪẬÉÈẺẼẸẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌỐỒỔỖỘỚỜỞỠỢÚÙỦŨỤỨỪỬỮỰÝỲỶỸỴ"
)


def used_chars(mapping):
    cps = set()
    for v in mapping.values():
        for ch in v:
            if ord(ch) > 0x7F:
                cps.add(ord(ch))
    return cps


def main():
    game = sys.argv[1]
    mapping = json.load(open(os.path.join(game, "translations", "vi_master.json"),
                             encoding="utf-8"))
    used = used_chars(mapping)
    print("distinct non-ascii chars used:", len(used))
    print("max cp", hex(max(used)))
    need = sorted(used | {ord(c) for c in VI_EXTRA})
    supply = r"C:\Windows\Fonts\ARIALUNI.TTF"
    fonts_dir = os.path.join(game, "source", "fonts")
    out_dir = os.path.join(game, "source", "fonts_patched")
    os.makedirs(out_dir, exist_ok=True)
    for p in sorted(glob.glob(os.path.join(fonts_dir, "*.otf")) + glob.glob(os.path.join(fonts_dir, "*.ttf"))):
        data = open(p, "rb").read()
        f = TTFont(p, lazy=True)
        have = set(f.getBestCmap())
        missing = [cp for cp in need if cp not in have]
        try:
            if data[:4] == b"OTTO":
                out = rebuild(data, supply, missing, verbose=True)
                kind = "CFF"
            else:
                out = add_glyphs_glyf(data, supply, missing, verbose=True)
                kind = "TTF"
        except Exception as e:
            print(os.path.basename(p), "FAILED", e)
            continue
        op = os.path.join(out_dir, os.path.basename(p))
        open(op, "wb").write(out)
        nf = TTFont(op, lazy=True)
        nc = set(nf.getBestCmap())
        still = [cp for cp in need if cp not in nc]
        print(os.path.basename(p), kind, "missing_before", len(missing),
              "still_missing", len(still), "out_size", len(out))


if __name__ == "__main__":
    main()
