"""Boc tat ca part .kit va quet tim kho text (Unravel Two)."""
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

from kit_extract import scan

LANG = [b'English', b'French', b'German', b'Spanish', b'Italian', b'Japanese',
        b'Korean', b'Russian', b'Polish', b'Portuguese', b'Chinese', b'Dutch',
        b'Fran', b'Deutsch', b'Espa', b'Italiano', b'localiz', b'Localiz']
UI = [b'New Game', b'Continue', b'Chapter', b'Trophy', b'Collectible', b'Subtitle',
      b'Language', b'Credits', b'Restart', b'Checkpoint', b'Press', b'Button']

out_dir = r'E:\UNR_work\parts'
os.makedirs(out_dir, exist_ok=True)
files = sorted(os.listdir(out_dir))
print('part san co:', files, flush=True)

summary = []
for f in files:
    p = os.path.join(out_dir, f)
    recs, resync, n = scan(p)
    good = [r for r in recs if r[2]]
    lang_hits = {}
    ui_hits = {}
    best = None
    best_ui = 0
    for off, ln, r in good:
        for k in LANG:
            if k in r:
                lang_hits[k] = lang_hits.get(k, 0) + 1
        c = 0
        for k in UI:
            if k in r:
                ui_hits[k] = ui_hits.get(k, 0) + 1
                c += 1
        if c > best_ui:
            best_ui = c
            best = (off, ln, len(r), r)
    print(f'{f}: {len(recs)} record | LZ4 {len(good)} | resync {resync} | {n:,} byte', flush=True)
    print(f'   ngon ngu gap: { {k.decode(): v for k, v in lang_hits.items()} }', flush=True)
    print(f'   nhan UI gap: { {k.decode(): v for k, v in ui_hits.items()} }', flush=True)
    if best and best_ui >= 3:
        off, ln, rl, r = best
        print(f'   >>> record @{off:#x} -> {rl:,} byte co {best_ui} nhan UI', flush=True)
        os.makedirs(r'E:\UNR_work\textrec', exist_ok=True)
        open(rf'E:\UNR_work\textrec\{f}_{off:x}.json', 'wb').write(r)
    summary.append((f, len(recs), len(good), lang_hits, ui_hits))

print('\n=== TONG KET ===', flush=True)
for f, nr, ng, lh, uh in summary:
    print(f'  {f}: {nr} record, {ng} LZ4, ngon ngu={len(lh)}, UI={len(uh)}', flush=True)
