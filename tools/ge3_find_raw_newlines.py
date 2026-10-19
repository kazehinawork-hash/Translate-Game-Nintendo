import glob
import json
import os
import sys


def main():
    chunks_dir = sys.argv[1]
    bad = []
    for path in sorted(glob.glob(os.path.join(chunks_dir, "chunk_???_vi.json"))):
        data = json.load(open(path, encoding="utf-8"))
        for k, v in data.items():
            if isinstance(v, str) and ("\n" in v or "\r" in v):
                bad.append((os.path.basename(path), k, repr(v)[:120]))
    print("values containing raw newline:", len(bad))
    for b in bad[:50]:
        print(b)


if __name__ == "__main__":
    main()
