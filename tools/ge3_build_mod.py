import glob
import json
import os
import re
import struct
import sys
import time
import zlib

BOM = b"\xff\xfe"
HEADER_PREFIX = b"T\x00e\x00x\x00t\x00I\x00d"
TAG_RE = re.compile(r"<[^>]*>|\{[^}]*\}|%[sd]|\[\[[^\]]*\]\]")


def _fix_tags(src, dst):
    if not TAG_RE.search(src) and not TAG_RE.search(dst):
        return dst
    from collections import Counter
    st = Counter(TAG_RE.findall(src))
    dt = Counter(TAG_RE.findall(dst))
    # remove extra non-<br> tags
    for tag, cnt in list(dt.items()):
        if tag == "<br>":
            continue
        extra = cnt - st.get(tag, 0)
        for _ in range(max(extra, 0)):
            dst = dst.replace(tag, "", 1)
    # reconcile <br> count
    src_br = st.get("<br>", 0)
    dst_br = dst.count("<br>")
    if dst_br > src_br:
        for _ in range(dst_br - src_br):
            i = dst.find("<br>")
            dst = dst[:i] + " " + dst[i + 4:]
    elif dst_br < src_br:
        need = src_br - dst_br
        words = dst.split(" ")
        if len(words) > 1 and need < len(words):
            step = max(1, len(words) // (need + 1))
            pos = [min(len(words) - 1, step * (k + 1)) for k in range(need)]
            out = []
            for idx, w in enumerate(words):
                out.append(w)
                if idx in pos:
                    out.append("<br>")
            dst = " ".join(out)
    # append missing closing tags to avoid color bleed
    if st.get("</>", 0) > dst.count("</>"):
        dst += "</>" * (st["</>"] - dst.count("</>"))
    return dst


def load_mapping(chunks_dir):
    game_dir = os.path.dirname(os.path.dirname(chunks_dir))
    master = os.path.join(game_dir, "translations", "vi_master.json")
    if os.path.exists(master):
        return json.load(open(master, encoding="utf-8"))
    mapping = {}
    for path in sorted(glob.glob(os.path.join(chunks_dir, "chunk_???_vi.json"))):
        data = json.load(open(path, encoding="utf-8"))
        mapping.update(data)
    return mapping


def parse_pkh(path):
    raw = open(path, "rb").read()
    count = struct.unpack(">I", raw[:4])[0]
    entries = []
    off = 4
    for _ in range(count):
        entries.append(struct.unpack(">6I", raw[off:off + 24]))
        off += 24
    return entries


def is_text_table(data):
    return data[:2] == BOM and HEADER_PREFIX in data[:20]


def translate_table(data, mapping):
    text = data[2:].decode("utf-16-le")
    newline = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(newline)
    if not lines:
        return None, 0
    header = [c.strip().lstrip("\ufeff") for c in lines[0].split("\t")]
    if "TextId" not in header or "Text" not in header:
        return None, 0
    id_col = header.index("TextId")
    text_col = header.index("Text")
    changed = 0
    out_lines = [lines[0]]
    for line in lines[1:]:
        if not line.strip():
            out_lines.append(line)
            continue
        cols = line.split("\t")
        if len(cols) <= text_col:
            out_lines.append(line)
            continue
        tid = cols[id_col]
        if tid in mapping:
            new_val = _fix_tags(cols[text_col], mapping[tid])
            if cols[text_col] != new_val:
                cols[text_col] = new_val
                changed += 1
        out_lines.append("\t".join(cols))
    if changed == 0:
        return None, 0
    new_text = newline.join(out_lines)
    return (BOM + new_text.encode("utf-16-le")), changed


def build_archive(stem, mapping, out_dir, font_dir, verbose=True):
    pkh_path = stem + ".pkh"
    pk_path = stem + ".pk"
    entries = parse_pkh(pkh_path)
    if verbose:
        print(f"[{os.path.basename(stem)}] entries={len(entries)}")
    t0 = time.time()
    replacements = {}
    changed_rows = 0
    text_tables = 0
    for i, (h, z1, z2, off, unc, comp) in enumerate(entries):
        with open(pk_path, "rb") as f:
            f.seek(off)
            raw = f.read(comp if comp > 0 else unc)
        data = zlib.decompress(raw) if comp > 0 else raw
        if not is_text_table(data):
            continue
        text_tables += 1
        new_data, changed = translate_table(data, mapping)
        if new_data is None:
            continue
        compressed = zlib.compress(new_data, 9)
        if len(compressed) >= len(new_data):
            payload = new_data
            new_comp = 0
        else:
            payload = compressed
            new_comp = len(compressed)
        replacements[i] = (payload, len(new_data), new_comp)
        changed_rows += changed
        if text_tables % 500 == 0 and verbose:
            print(f"  scanned {i+1}/{len(entries)} text_tables={text_tables} "
                  f"changed_rows={changed_rows} t={time.time()-t0:.0f}s")
    if verbose:
        print(f"[{os.path.basename(stem)}] text tables={text_tables} "
              f"changed rows={changed_rows} replaced entries={len(replacements)}")
    # Font replacements (patched fonts live next to the game source data)
    font_files = {
        1979: "001979.otf", 2478: "002478.otf", 3384: "003384.otf",
        5000: "005000.otf", 5869: "005869.otf", 6600: "006600.ttf",
        17048: "017048.otf", 17574: "017574.otf", 18486: "018486.otf",
        30187: "030187.ttf", 31492: "031492.otf", 31998: "031998.ttf",
        32916: "032916.otf", 40351: "040351.otf",
    }
    font_count = 0
    for idx, name in font_files.items():
        p = os.path.join(font_dir, name)
        if not os.path.exists(p):
            continue
        data = open(p, "rb").read()
        compressed = zlib.compress(data, 9)
        if len(compressed) >= len(data):
            payload, new_comp = data, 0
        else:
            payload, new_comp = compressed, len(compressed)
        replacements[idx] = (payload, len(data), new_comp)
        font_count += 1
    if verbose and font_count:
        print(f"[{os.path.basename(stem)}] patched fonts={font_count}")
    # Rebuild pk
    out_pk = os.path.join(out_dir, os.path.basename(stem) + ".pk")
    new_entries = []
    with open(pk_path, "rb") as src, open(out_pk, "wb") as dst:
        cursor = 0
        for i, (h, z1, z2, off, unc, comp) in enumerate(entries):
            if i in replacements:
                payload, new_unc, new_comp = replacements[i]
                dst.write(payload)
                new_off = cursor
                cursor += len(payload)
                new_entries.append((h, z1, z2, new_off, new_unc, new_comp))
            else:
                src.seek(off)
                payload = src.read(comp if comp > 0 else unc)
                dst.write(payload)
                new_off = cursor
                cursor += len(payload)
                new_entries.append((h, z1, z2, new_off, unc, comp))
    # Write pkh
    out_pkh = os.path.join(out_dir, os.path.basename(stem) + ".pkh")
    with open(out_pkh, "wb") as f:
        f.write(struct.pack(">I", len(new_entries)))
        for e in new_entries:
            f.write(struct.pack(">6I", *e))
    if verbose:
        print(f"[{os.path.basename(stem)}] wrote pk and pkh "
              f"in {time.time()-t0:.0f}s")
    return changed_rows


def main():
    game_dir = sys.argv[1]
    chunks_dir = os.path.join(game_dir, "translations", "chunks")
    romfs = sys.argv[2]
    out_root = os.path.join(sys.argv[3], "01001C700873E000", "romfs",
                            "resource", "target", "nx", "pack", "mount", "retail")
    os.makedirs(out_root, exist_ok=True)
    mapping = load_mapping(chunks_dir)
    print("mapping entries:", len(mapping))
    font_dir = os.path.join(game_dir, "source", "fonts_patched")
    for stem_name in ("archive00",):
        stem = os.path.join(romfs, "resource", "target", "nx", "pack", "mount",
                            "retail", stem_name)
        build_archive(stem, mapping, out_root, font_dir)


if __name__ == "__main__":
    main()
