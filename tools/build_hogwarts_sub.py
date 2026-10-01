"""
build_hogwarts_sub.py — Đóng gói từ điển hội thoại (SUB) tiếng Việt cho Hogwarts Legacy.

Ghép bản dịch trong `games/0100F7E00C70E000_Hogwarts/translations/sub_trans/sub_*.json`
với kho gốc tiếng Pháp (`source/raw_text/sub_dump/SUB-koKR.bin`) rồi pack ra `SUB-*.bin`
cho 5 slot ngôn ngữ trong thư mục LayeredFS.

Cách dùng (chạy từ gốc dự án):
    python tools/build_hogwarts_sub.py
"""
import os
import sys
import glob
import json
import struct

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from avaf_codec import pack_avafdict  # noqa: E402

W = os.path.join(ROOT, 'games', '0100F7E00C70E000_Hogwarts', 'source')
S = os.path.join(W, 'split_tasks')
FR_BIN = os.path.join(W, 'raw_text', 'sub_dump', 'SUB-koKR.bin')
MOD = os.path.join(ROOT, 'output', 'atmosphere', 'contents', '0100F7E00C70E000',
                   'romfs', 'Phoenix', 'Content', 'Localization', 'SWITCH')
TARGETS = ['enUS', 'frFR', 'deDE', 'zhCN', 'zhTW']


def parse_avaf(path):
    data = open(path, 'rb').read()
    ec, hl, o1, o2, o3 = struct.unpack('<QQQQQ', data[0x20:0x48])
    out, t = {}, 0x48
    for i in range(ec):
        ko, ku, kl = struct.unpack('<III', data[t + i * 24:t + i * 24 + 12])
        vo, vu, vl = struct.unpack('<III', data[t + i * 24 + 12:t + i * 24 + 24])
        out[data[o2 + ko:o2 + ko + kl].decode('utf-8', 'replace')] = \
            data[o2 + vo:o2 + vo + vl].decode('utf-8', 'replace')
    return out


def main():
    uniq = json.load(open(os.path.join(W, 'extracted_json', 'dialogs_fr_unique.json'), encoding='utf-8'))
    U, key2fr = uniq['unique'], uniq['key2fr']
    id2vi = {}
    for fp in sorted(glob.glob(os.path.join(S, 'sub_trans', 'sub_*.json'))):
        for it in json.load(open(fp, encoding='utf-8')):
            id2vi[it['Id']] = it['VI']

    fr2vi = {fr: (id2vi.get(i) or fr) for i, fr in enumerate(U)}
    fr_dict = parse_avaf(FR_BIN)
    final = {k: fr2vi.get(v, v) for k, v in fr_dict.items()}
    print(f'SUB entries: {len(final)}')
    packed = pack_avafdict(final)

    os.makedirs(MOD, exist_ok=True)
    for lang in TARGETS:
        open(os.path.join(MOD, f'SUB-{lang}.bin'), 'wb').write(packed)
    print(f'Da ghi {len(TARGETS)} file SUB-*.bin ({len(packed)} bytes)')


if __name__ == '__main__':
    main()
