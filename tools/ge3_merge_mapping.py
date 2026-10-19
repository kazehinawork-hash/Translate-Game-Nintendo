import glob
import json
import os
import sys


def load(pattern):
    merged = {}
    for p in sorted(glob.glob(pattern)):
        merged.update(json.load(open(p, encoding="utf-8")))
    return merged


def main():
    game = sys.argv[1]
    chunks = os.path.join(game, "translations", "chunks")
    repair = os.path.join(game, "translations", "repair_chunks")
    merged = load(os.path.join(chunks, "chunk_???_vi.json"))
    n1 = len(merged)
    merged.update(load(os.path.join(repair, "repair_??_vi.json")))
    n2 = len(merged)
    out = os.path.join(game, "translations", "vi_master.json")
    json.dump(merged, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("base", n1, "after repair", n2, "written", out)


if __name__ == "__main__":
    main()
