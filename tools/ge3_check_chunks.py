import glob
import json
import os
import sys


def main():
    root = sys.argv[1]
    src = sorted(glob.glob(os.path.join(root, "chunk_*.json")))
    src = [p for p in src if not p.endswith("_vi.json")]
    missing = []
    bad = []
    total = 0
    done = 0
    for p in src:
        vi = p[:-5] + "_vi.json"
        if not os.path.exists(vi):
            missing.append(os.path.basename(p))
            continue
        a = json.load(open(p, encoding="utf-8"))
        b = json.load(open(vi, encoding="utf-8"))
        total += len(a)
        done += 1
        if list(a.keys()) != list(b.keys()):
            bad.append((os.path.basename(p), len(a), len(b)))
    print("chunks", len(src), "translated", done, "missing", len(missing),
          "key_mismatch", len(bad), "total_ids", total)
    print("missing:", missing)
    print("bad:", bad)


if __name__ == "__main__":
    main()
