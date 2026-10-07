"""MONOPOLY: QA/gop ban dich + soi cau truc THO cua TextAsset Oasis."""
import json
import os
import re
import struct
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game'
TID = '01002C201BC40000'
G = os.path.join(ROOT, 'games', f'{TID}_Monopoly')
T = os.path.join(G, 'translations')

# --- 1. QA + gop
uniq = json.load(open(os.path.join(T, 'uniq_en.json'), encoding='utf-8'))
vi = {}
bad = miss = cjk = nl = 0
BAD = re.compile(r'[\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff00-\uffef'
                 r'\u1100-\u11ff\u3130-\u318f\uac00-\ud7ff\u3040-\u30ff\u0600-\u06ff\u0400-\u04ff]')
for n in range(1, 6):
    p = os.path.join(T, f'vi_{n}.json')
    if not os.path.exists(p):
        print(f'  THIEU vi_{n}.json'); continue
    for k, v in json.load(open(p, encoding='utf-8')).items():
        vi.setdefault(k, v)
        if not str(v).strip():
            bad += 1
        if BAD.search(str(v)):
            cjk += 1
            if cjk <= 3:
                print(f'  KY TU LA: {k[:40]!r} -> {str(v)[:40]!r}')
        if str(k).count('\n') != str(v).count('\n'):
            nl += 1
missk = [k for k in uniq if k not in vi]
print(f'gop {len(vi):,}/{len(uniq):,} | thieu {len(missk)} | rong {bad} | ky tu la {cjk} | lech \\n {nl}')
if missk:
    for k in missk[:5]:
        print('  thieu:', repr(k[:60]))
json.dump(vi, open(os.path.join(T, 'mono_vi.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('-> translations/mono_vi.json')

# --- 2. soi TextAsset raw
import UnityPy
env = UnityPy.load(r'E:\MONO_work\data.unity3d')
for o in env.objects:
    if o.type.name != 'TextAsset':
        continue
    d = o.read()
    if getattr(d, 'm_Name', '') != 'oasis_englishgb':
        continue
    raw = o.get_raw_data()
    print(f'\n=== TextAsset oasis_englishgb: raw {len(raw):,} byte ===')
    print('  16 byte dau:', raw[:16].hex(' '))
    ln, = struct.unpack_from('<i', raw, 0)
    print(f'  int32 dau = {ln:,} | so sanh len-4 = {len(raw)-4:,}')
    print('  byte 4..12:', raw[4:12].hex(' '))
    print('  4 byte cuoi:', raw[-4:].hex(' '))
    break
