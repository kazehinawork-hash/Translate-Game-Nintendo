"""Gop ban dich Unravel Two thanh 1 bang duy nhat, uu tien ban dich tu TIENG ANH."""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
G = r'E:\OneDrive\3.家 Jiā Home\99. 其他 Qítā Other\96.Translate Game\games\0100E5D00CC0C000_UnravelTwo'
T = os.path.join(G, 'translations')
CJK = re.compile(r'[\u3040-\u30ff\u4e00-\u9fff\uac00-\ud7ff]')


def is_english(s):
    return not CJK.search(s)


merged = {}
stats = {'en': 0, 'nonen': 0, 'overwrite': 0}
for f in sorted(os.listdir(T)):
    if not f.startswith('todo_'):
        continue
    vf = 'vi_' + f[5:]
    if not os.path.exists(os.path.join(T, vf)):
        continue
    src = json.load(open(os.path.join(T, f), encoding='utf-8'))
    dst = {x['key']: x['vi'] for x in json.load(open(os.path.join(T, vf), encoding='utf-8'))}
    for x in src:
        k = x['key']
        v = dst.get(k, '')
        if not v:
            continue
        eng = is_english(x['en'])
        if k not in merged:
            merged[k] = {'vi': v, 'en': x['en'], 'from_en': eng}
            stats['en' if eng else 'nonen'] += 1
        elif eng and not merged[k]['from_en']:
            merged[k] = {'vi': v, 'en': x['en'], 'from_en': True}
            stats['overwrite'] += 1

# giu nguyen 5 muc NOLOCA/EULA (khong dich)
huge = json.load(open(os.path.join(T, 'huge.json'), encoding='utf-8'))
for x in huge:
    merged.setdefault(x['key'], {'vi': x['en'], 'en': x['en'], 'from_en': True, 'keep': True})

out = [{'key': k, 'vi': d['vi'], 'en': d['en'], 'keep': d.get('keep', False)}
       for k, d in sorted(merged.items())]
p = os.path.join(T, 'vi_all.json')
json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'gop xong: {len(out)} key -> {p}')
print(f'  dich tu tieng Anh: {stats["en"]} | tu ngon ngu khac: {stats["nonen"]} | ghi de bang ban tieng Anh: {stats["overwrite"]}')
print(f'  giu nguyen (NOLOCA/EULA): {sum(1 for x in out if x["keep"])}')
