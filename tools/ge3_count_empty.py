import glob
import json
import os
import sys


def main():
    chunks_dir = sys.argv[1]
    total = 0
    empty = []
    for path in sorted(glob.glob(os.path.join(chunks_dir, "chunk_???_vi.json"))):
        data = json.load(open(path, encoding="utf-8"))
        for k, v in data.items():
            total += 1
            if not v.strip():
                empty.append((os.path.basename(path), k, repr(v)[:60]))
    print("total", total, "empty translations", len(empty))
    for e in empty[:40]:
        print(e)


if __name__ == "__main__":
    main()
