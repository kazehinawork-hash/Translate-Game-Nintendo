"""Phan loai chuoi 'chua dich': (A) chi co tag/placeholder  (B) ten rieng/thuong hieu  (C) CAN DICH."""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, 'games', '_consistency')

STRIP = re.compile(r'\{[^{}]*\}|<[^>]*>|\[[^\]]*\]|%[sdfiu]|\\[nt]|\$[\w.]+|\|plural\(|\|\w+\(|[\s\d\W_]+')

BRAND = re.compile(r'^(NVIDIA|AMD|Intel|DLSS|FSR|Xbox|PlayStation|Steam|Epic|Ubisoft|Switch|Windows|DirectX|Vulkan|Dolby|THX|Ray|HDR|VRR)$', re.I)


def classify(v):
    core = STRIP.sub(' ', v).strip()
    core = re.sub(r'\s+', ' ', core)
    words = [w for w in core.split(' ') if len(w) > 1]
    if not words:
        return 'A', core
    if all(BRAND.match(w) for w in words):
        return 'B', core
    return 'C', core


for game in ('hogwarts', 'hades2', 'switchsports'):
    p = os.path.join(D, f'untranslated_{game}.json')
    if not os.path.exists(p):
        continue
    data = json.load(open(p, encoding='utf-8'))
    print(f'\n{"="*74}\n{game.upper()}\n{"="*74}')
    for name, items in data.items():
        if not items:
            continue
        buckets = {'A': [], 'B': [], 'C': []}
        for k, v in sorted(items.items()):
            b, core = classify(v)
            buckets[b].append((k, v, core))
        print(f'\n  --- {name}: {len(items)} muc')
        print(f'      A (chi tag/placeholder, KHONG can dich): {len(buckets["A"])}')
        print(f'      B (ten rieng/thuong hieu, giu nguyen)   : {len(buckets["B"])}')
        print(f'      C (CAN DICH)                            : {len(buckets["C"])}')
        if buckets['B']:
            print('      vd B: ' + ' | '.join(c for _, _, c in buckets['B'][:8]))
        print('      --- C ---')
        for k, v, c in buckets['C'][:40]:
            print(f'        {k[:44]:<44} {v[:70]!r}')
        if len(buckets['C']) > 40:
            print(f'        ... con {len(buckets["C"])-40} muc C nua')
